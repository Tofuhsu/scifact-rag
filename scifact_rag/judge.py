"""LLM-as-judge for faithfulness and abstention, with a rubric shared with human labels.

Faithfulness: the answer is split into sentences; for each, the judge sees only
the abstracts that the answer cites and labels it SUPPORTED, PARTIAL or
NOT_SUPPORTED. An answer is faithful when every sentence is SUPPORTED.

Abstention: for a NOT_FOUND answer, the judge sees all retrieved abstracts and
says whether any of them reports something about the specific entities and
relationship in the claim. The abstention is justified when none does.

Human calibration labels use exactly these definitions (see JUDGE_RUBRIC.md).
"""
from __future__ import annotations

import json
import re

JUDGE_VERSION = "j1"
LABELS = ("SUPPORTED", "PARTIAL", "NOT_SUPPORTED")

_SENTENCE_END = re.compile(r"(?<=[.!?])(?:\s*\[[^\[\]]*\])*\s+(?=[A-Z0-9(])")
_TRAILING_CITES = re.compile(r"^((?:\s*\[[^\[\]]*\])+)")


def split_sentences(text):
    """Split on sentence ends, keeping citation brackets that follow a period with their sentence."""
    text = text.strip()
    if not text:
        return []
    sentences, start = [], 0
    for match in _SENTENCE_END.finditer(text):
        sentences.append(text[start:match.start()].strip())
        start = match.start()
    sentences.append(text[start:].strip())
    out = []
    for s in sentences:
        cites = _TRAILING_CITES.match(s)
        if cites and out:  # "...finding. [123] Next" -> move "[123]" back to the previous sentence
            out[-1] = f"{out[-1]} {cites.group(1).strip()}"
            s = s[cites.end():].strip()
        if s:
            out.append(s)
    return out


def _abstract_block(passages):
    return "\n\n".join(f"[{d}] {t.strip()}\n{a.strip()}" for d, t, a in passages) or "(none)"


FAITHFULNESS_SYSTEM = """You check whether sentences of an answer are supported by the abstracts they cite.
For each numbered sentence, use ONLY the abstracts shown. Labels:
- SUPPORTED: everything the sentence states is stated in, or directly follows from, the abstracts.
- PARTIAL: part of the sentence is supported, but it adds or overstates something the abstracts do not state.
- NOT_SUPPORTED: the abstracts do not state it, or contradict it.
A sentence that only says what the abstracts do NOT cover is SUPPORTED if that is accurate.
Return one label per sentence, in order."""


def faithfulness_messages(claim, sentences, cited_passages):
    numbered = "\n".join(f"{i}. {s}" for i, s in enumerate(sentences, 1))
    user = (f"Abstracts cited by the answer:\n\n{_abstract_block(cited_passages)}\n\n"
            f"Question or claim: {claim}\n\nAnswer sentences:\n{numbered}")
    return [{"role": "system", "content": FAITHFULNESS_SYSTEM}, {"role": "user", "content": user}]


def faithfulness_schema(n):
    return {"type": "object", "required": ["labels"], "properties": {
        "labels": {"type": "array", "minItems": n, "maxItems": n, "items": {"type": "string", "enum": list(LABELS)}}}}


ABSTENTION_SYSTEM = """You check whether a set of abstracts contains any information about a specific claim.
Answer true if at least one abstract reports a finding about the specific entities and relationship in the claim,
whether it supports or contradicts the claim, even partly. Answer false if the abstracts are only on related topics
without reporting anything about that relationship. Use ONLY the abstracts shown. List the IDs of abstracts that do."""

ABSTENTION_SCHEMA = {"type": "object", "required": ["has_relevant_information", "doc_ids"], "properties": {
    "has_relevant_information": {"type": "boolean"}, "doc_ids": {"type": "array", "items": {"type": "string"}}}}


def abstention_messages(claim, passages):
    user = f"Abstracts:\n\n{_abstract_block(passages)}\n\nClaim: {claim}"
    return [{"role": "system", "content": ABSTENTION_SYSTEM}, {"role": "user", "content": user}]


class Judge:
    """llm: has .chat(messages, schema=...) returning an object with .content (JSON text)."""

    def __init__(self, llm):
        self.llm = llm

    def faithfulness(self, claim, answer, cited_passages):
        sentences = split_sentences(answer)
        if not sentences:
            raise ValueError("Cannot judge an empty answer")
        reply = self.llm.chat(faithfulness_messages(claim, sentences, cited_passages),
                              schema=faithfulness_schema(len(sentences)))
        labels = json.loads(reply.content)["labels"]
        if len(labels) != len(sentences) or any(label not in LABELS for label in labels):
            raise ValueError(f"Judge returned {labels!r} for {len(sentences)} sentences")
        return {"sentences": sentences, "labels": labels, "faithful": all(x == "SUPPORTED" for x in labels)}

    def abstention(self, claim, passages):
        reply = self.llm.chat(abstention_messages(claim, passages), schema=ABSTENTION_SCHEMA)
        body = json.loads(reply.content)
        has_info = body["has_relevant_information"]
        if not isinstance(has_info, bool):
            raise ValueError("Judge returned a non-boolean decision")
        known = {d for d, _, _ in passages}
        return {"has_relevant_information": has_info, "justified": not has_info,
                "doc_ids": [d for d in body.get("doc_ids", []) if d in known]}


def agreement(pairs):
    """pairs: list of (human_bool, judge_bool). Returns raw agreement and Cohen's kappa."""
    n = len(pairs)
    if n == 0:
        raise ValueError("No pairs")
    agree = sum(h == j for h, j in pairs) / n
    p_h = sum(h for h, _ in pairs) / n
    p_j = sum(j for _, j in pairs) / n
    expected = p_h * p_j + (1 - p_h) * (1 - p_j)
    kappa = None if expected == 1 else (agree - expected) / (1 - expected)
    return {"pairs": n, "agree": sum(h == j for h, j in pairs), "agreement": agree, "cohen_kappa": kappa}
