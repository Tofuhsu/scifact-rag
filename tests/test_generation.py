import pytest

from scifact_rag.generation import (MAX_ABSTRACT_CHARS, NOT_FOUND, SYSTEM_PROMPT, Answerer, LLMResult,
                                    build_messages, parse_answer)

ALLOWED = ["101", "102", "103"]


@pytest.mark.parametrize("raw, expected", [
    ("Statins lower LDL [102].", ["102"]),
    ("A [101, 102]. B [103].", ["101", "102", "103"]),
    ("A [101][102]. Again [101].", ["101", "102"]),
    ("A [ 103 ;101 ].", ["103", "101"]),
])
def test_parse_valid_citations_in_first_mention_order(raw, expected):
    parsed = parse_answer(raw, ALLOWED)
    assert parsed.citations == expected
    assert parsed.invalid_citations == [] and not parsed.abstained and not parsed.uncited


def test_unknown_ids_are_reported_not_dropped():
    parsed = parse_answer("A [101, 999]. B [888].", ALLOWED)
    assert parsed.citations == ["101"]
    assert parsed.invalid_citations == ["999", "888"]


def test_non_numeric_brackets_are_not_citations():
    parsed = parse_answer("As shown [see Methods] and [n=30], effects held [102].", ALLOWED)
    assert parsed.citations == ["102"] and parsed.invalid_citations == []


def test_answer_without_citations_is_flagged_uncited():
    parsed = parse_answer("Statins lower LDL.", ALLOWED)
    assert parsed.uncited and parsed.citations == [] and not parsed.abstained


@pytest.mark.parametrize("raw", [NOT_FOUND, f" {NOT_FOUND}. ", f"`{NOT_FOUND}`", "", None,
                                 f"<think>hmm</think>\n{NOT_FOUND}"])
def test_not_found_sentinel_means_abstain(raw):
    parsed = parse_answer(raw, ALLOWED)
    assert parsed.abstained and parsed.text == NOT_FOUND
    assert parsed.citations == [] and not parsed.uncited


def test_sentinel_inside_a_longer_answer_is_not_an_abstention():
    parsed = parse_answer(f"Partly covered [101]. {NOT_FOUND} for dosage.", ALLOWED)
    assert not parsed.abstained and parsed.citations == ["101"]


def test_think_block_is_stripped():
    parsed = parse_answer("<think>maybe [999]</think>Answer [101].", ALLOWED)
    assert parsed.text == "Answer [101]." and parsed.invalid_citations == []


def test_build_messages_labels_abstracts_by_id_and_truncates():
    long = "x" * (MAX_ABSTRACT_CHARS + 50)
    messages = build_messages("  Does X cause Y? ", [("101", "Title A", "Body A"), ("102", "Title B", long)])
    assert messages[0] == {"role": "system", "content": SYSTEM_PROMPT}
    user = messages[1]["content"]
    assert "[101] Title A\nBody A" in user and "[102] Title B" in user
    assert "x" * (MAX_ABSTRACT_CHARS + 1) not in user and user.endswith("Question or claim: Does X cause Y?")
    assert NOT_FOUND in SYSTEM_PROMPT


class FakeLLM:
    def __init__(self, reply):
        self.reply, self.messages = reply, None

    def chat(self, messages):
        self.messages = messages
        return LLMResult(self.reply, prompt_tokens=42, completion_tokens=7, model="fake")


def test_answerer_passes_only_retrieved_abstracts(retriever):
    from tests.conftest import DOCS

    llm = FakeLLM("Statin therapy lowers LDL [102].")
    out = Answerer(retriever, llm, {d: DOCS[d][1] for d in DOCS}).ask("statin cholesterol", k=2)
    retrieved = [h.doc_id for h in out["hits"]]
    assert len(retrieved) == 2 and retrieved[0] == "102"
    user = llm.messages[1]["content"]
    assert all(f"[{d}]" in user for d in retrieved)
    assert all(f"[{d}]" not in user for d in set(DOCS) - set(retrieved))
    assert out["parsed"].citations == ["102"]
    assert set(out["timings"]) == {"embed_ms", "search_ms", "generate_ms"}
