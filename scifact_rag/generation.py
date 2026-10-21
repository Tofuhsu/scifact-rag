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
MAX_ABSTRACT_CHARS = {"v1": 2000, "v2": 4000}
PROMPT_VERSION = "v2"

_HEADER = ("You answer questions about biomedical research using ONLY the abstracts provided. "
           "Each abstract starts with its ID in square brackets.")
_CITE = ("After every sentence that states a finding, cite the supporting abstract IDs in square brackets, "
         "e.g. [12345] or [12345, 67890]. Cite only IDs that appear in the provided abstracts.")

SYSTEM_PROMPTS = {
    # v1: week 2. Kept so results/dev/ask_validation_v1.json stays reproducible.
    "v1": f"""{_HEADER}

Rules:
1. Use only information stated in the abstracts. Do not use outside knowledge.
2. {_CITE}
3. If the abstracts do not contain information that answers the question or bears on the claim, reply with exactly {NOT_FOUND} and nothing else.
4. If the abstracts partly address it, answer only the supported part and say what is not covered.
5. Be concise: at most 4 sentences. Do not say whether the claim is true overall unless an abstract directly states it.""",
    # v2: week 3. Evidence that contradicts the claim, or bears on it only partly, must be reported
    # with citations instead of NOT_FOUND (validation query 323 abstained on contradicting evidence).
    "v2": f"""{_HEADER}

Rules:
1. Use only information stated in the abstracts. Do not use outside knowledge.
2. {_CITE}
3. Report evidence whether it supports or contradicts the claim. If an abstract reports a result that runs against the claim, say so and cite it.
4. If the abstracts address the topic only partly, state what they do report, with citations, and say what is not covered.
5. Reply with exactly {NOT_FOUND} and nothing else only when no abstract reports anything about the specific entities and relationship in the question or claim.
6. Be concise: at most 4 sentences. Do not say whether the claim is true overall unless an abstract directly states it.""",
}
SYSTEM_PROMPT = SYSTEM_PROMPTS[PROMPT_VERSION]

_CITATION_GROUP = re.compile(r"\[\s*([^\[\]]+?)\s*\]")
_DOC_ID = re.compile(r"^\d+$")
_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


def build_messages(question, passages, version=PROMPT_VERSION):
    """passages: list of (doc_id, title, abstract) in retrieval order."""
    limit = MAX_ABSTRACT_CHARS[version]
    blocks = []
    for doc_id, title, abstract in passages:
        body = abstract.strip()
        if len(body) > limit:
            body = body[:limit].rstrip() + " ..."
        blocks.append(f"[{doc_id}] {title.strip()}\n{body}")
    context = "\n\n".join(blocks) if blocks else "(no abstracts retrieved)"
    user = f"Abstracts:\n\n{context}\n\nQuestion or claim: {question.strip()}"
    return [{"role": "system", "content": SYSTEM_PROMPTS[version]}, {"role": "user", "content": user}]


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
    if not valid and not invalid and NOT_FOUND in text:
        # e.g. "The abstracts do not mention X. [NOT_FOUND]": an explanation plus the sentinel.
        return ParsedAnswer(text, True, [], [], False)
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

    def chat(self, messages, schema=None):
        """schema: optional JSON schema; Ollama then constrains the reply to valid JSON."""
        import httpx

        payload = {"model": self.model, "messages": messages, "stream": False, "think": False,
                   "options": {"temperature": 0, "seed": self.seed, "num_ctx": 8192}}
        if schema is not None:
            payload["format"] = schema
        response = httpx.post(f"{self.base_url}/api/chat", json=payload, timeout=self.timeout)
        response.raise_for_status()
        body = response.json()
        return LLMResult(content=body["message"]["content"], prompt_tokens=body.get("prompt_eval_count"),
                         completion_tokens=body.get("eval_count"), model=body.get("model", self.model),
                         extra={"load_duration_ms": body.get("load_duration", 0) / 1e6})


class Answerer:
    """retrieve top-k -> prompt -> LLM -> parsed answer with citations and per-stage timings."""

    def __init__(self, retriever, llm, abstracts, prompt_version=PROMPT_VERSION):
        self.retriever = retriever
        self.llm = llm
        self.abstracts = abstracts  # {doc_id: abstract}
        self.prompt_version = prompt_version

    def ask(self, question, k=5):
        hits, timings = self.retriever.search(question, k=k)
        passages = [(h.doc_id, h.title, self.abstracts.get(h.doc_id, "")) for h in hits]
        messages = build_messages(question, passages, self.prompt_version)
        start = time.perf_counter()
        result = self.llm.chat(messages)
        timings = dict(timings, generate_ms=1000 * (time.perf_counter() - start))
        parsed = parse_answer(result.content, [h.doc_id for h in hits])
        return {"parsed": parsed, "hits": hits, "timings": timings, "llm": result}
