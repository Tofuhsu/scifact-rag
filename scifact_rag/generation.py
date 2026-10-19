"""Grounded answer generation with inline [doc_id] citations.

The LLM sees only the retrieved abstracts. It must cite every claim with the
bracketed doc IDs of those abstracts, or answer with the NOT_FOUND sentinel
when the abstracts do not address the question.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

NOT_FOUND = "NOT_FOUND"
PROMPT_VERSION = "v1"
MAX_ABSTRACT_CHARS = 2000

SYSTEM_PROMPT = f"""You answer questions about biomedical research using ONLY the abstracts provided. Each abstract starts with its ID in square brackets.

Rules:
1. Use only information stated in the abstracts. Do not use outside knowledge.
2. After every sentence that states a finding, cite the supporting abstract IDs in square brackets, e.g. [12345] or [12345, 67890]. Cite only IDs that appear in the provided abstracts.
3. If the abstracts do not contain information that answers the question or bears on the claim, reply with exactly {NOT_FOUND} and nothing else.
4. If the abstracts partly address it, answer only the supported part and say what is not covered.
5. Be concise: at most 4 sentences. Do not say whether the claim is true overall unless an abstract directly states it."""

_CITATION_GROUP = re.compile(r"\[\s*([^\[\]]+?)\s*\]")
_DOC_ID = re.compile(r"^\d+$")
_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


def build_messages(question, passages):
    """passages: list of (doc_id, title, abstract) in retrieval order."""
    blocks = []
    for doc_id, title, abstract in passages:
        body = abstract.strip()
        if len(body) > MAX_ABSTRACT_CHARS:
            body = body[:MAX_ABSTRACT_CHARS].rstrip() + " ..."
        blocks.append(f"[{doc_id}] {title.strip()}\n{body}")
    context = "\n\n".join(blocks) if blocks else "(no abstracts retrieved)"
    user = f"Abstracts:\n\n{context}\n\nQuestion or claim: {question.strip()}"
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}]


@dataclass(frozen=True)
class ParsedAnswer:
    text: str
    abstained: bool
    citations: list[str]          # valid cited doc IDs, first-mention order, no duplicates
    invalid_citations: list[str]  # cited IDs that were not in the provided abstracts
    uncited: bool                 # non-abstaining answer with no valid citation


def parse_answer(raw, allowed_ids):
    """Extract citations from an LLM answer. Unknown IDs are reported, never silently dropped."""
    text = _THINK.sub("", raw or "").strip()
    if text.strip(" .\"'`*") == NOT_FOUND or not text:
        return ParsedAnswer(NOT_FOUND, True, [], [], False)
    allowed = set(allowed_ids)
    valid, invalid = [], []
    for group in _CITATION_GROUP.findall(text):
        parts = [p.strip() for p in re.split(r"[,;]", group)]
        if not all(_DOC_ID.match(p) for p in parts if p):
            continue  # bracketed text that is not a citation, e.g. "[see Methods]"
        for doc_id in filter(None, parts):
            bucket = valid if doc_id in allowed else invalid
            if doc_id not in bucket:
                bucket.append(doc_id)
    return ParsedAnswer(text, False, valid, invalid, not valid)


@dataclass
class LLMResult:
    content: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    model: str = ""
    extra: dict = field(default_factory=dict)


class OllamaClient:
    """Minimal client for a local Ollama server (/api/chat, non-streaming)."""

    def __init__(self, model="qwen3:14b", base_url="http://127.0.0.1:11434", timeout=300.0, seed=0):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.seed = seed

    def chat(self, messages):
        import httpx

        payload = {"model": self.model, "messages": messages, "stream": False, "think": False,
                   "options": {"temperature": 0, "seed": self.seed, "num_ctx": 8192}}
        response = httpx.post(f"{self.base_url}/api/chat", json=payload, timeout=self.timeout)
        response.raise_for_status()
        body = response.json()
        return LLMResult(content=body["message"]["content"], prompt_tokens=body.get("prompt_eval_count"),
                         completion_tokens=body.get("eval_count"), model=body.get("model", self.model),
                         extra={"load_duration_ms": body.get("load_duration", 0) / 1e6})


class Answerer:
    """retrieve top-k -> prompt -> LLM -> parsed answer with citations and per-stage timings."""

    def __init__(self, retriever, llm, abstracts):
        self.retriever = retriever
        self.llm = llm
        self.abstracts = abstracts  # {doc_id: abstract}

    def ask(self, question, k=5):
        hits, timings = self.retriever.search(question, k=k)
        passages = [(h.doc_id, h.title, self.abstracts.get(h.doc_id, "")) for h in hits]
        messages = build_messages(question, passages)
        start = time.perf_counter()
        result = self.llm.chat(messages)
        timings = dict(timings, generate_ms=1000 * (time.perf_counter() - start))
        parsed = parse_answer(result.content, [h.doc_id for h in hits])
        return {"parsed": parsed, "hits": hits, "timings": timings, "llm": result}
