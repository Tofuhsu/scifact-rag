import json

import pytest

from scifact_rag.generation import LLMResult
from scifact_rag.judge import Judge, agreement, faithfulness_schema, split_sentences


@pytest.mark.parametrize("text, expected", [
    ("A rose [1]. B fell [2, 3].", ["A rose [1].", "B fell [2, 3]."]),
    ("A rose. [1] B fell. [2]", ["A rose. [1]", "B fell. [2]"]),
    ("Only one sentence [5]", ["Only one sentence [5]"]),
    ("Levels rose 2.5-fold [7]. 30 mice died [8]!", ["Levels rose 2.5-fold [7].", "30 mice died [8]!"]),
    ("", []),
])
def test_split_sentences_keeps_citations_with_their_sentence(text, expected):
    assert split_sentences(text) == expected


class JsonLLM:
    def __init__(self, body):
        self.body, self.calls = body, []

    def chat(self, messages, schema=None):
        self.calls.append((messages, schema))
        return LLMResult(json.dumps(self.body))


def test_faithfulness_requires_every_sentence_supported():
    llm = JsonLLM({"labels": ["SUPPORTED", "PARTIAL"]})
    out = Judge(llm).faithfulness("claim", "A [1]. B [1].", [("1", "T", "abs")])
    assert out["labels"] == ["SUPPORTED", "PARTIAL"] and out["faithful"] is False
    messages, schema = llm.calls[0]
    assert schema == faithfulness_schema(2)
    assert "[1] T\nabs" in messages[1]["content"] and "1. A [1]." in messages[1]["content"]


def test_faithfulness_all_supported_is_faithful():
    out = Judge(JsonLLM({"labels": ["SUPPORTED"]})).faithfulness("c", "A [1].", [("1", "T", "a")])
    assert out["faithful"] is True


@pytest.mark.parametrize("labels", [["SUPPORTED"], ["SUPPORTED", "MAYBE"]])
def test_faithfulness_rejects_malformed_judge_output(labels):
    with pytest.raises(ValueError):
        Judge(JsonLLM({"labels": labels})).faithfulness("c", "A [1]. B [1].", [("1", "T", "a")])


def test_abstention_justified_only_when_no_relevant_information():
    passages = [("1", "T", "a"), ("2", "U", "b")]
    out = Judge(JsonLLM({"has_relevant_information": True, "doc_ids": ["2", "99"]})).abstention("c", passages)
    assert out == {"has_relevant_information": True, "justified": False, "doc_ids": ["2"]}
    out = Judge(JsonLLM({"has_relevant_information": False, "doc_ids": []})).abstention("c", passages)
    assert out["justified"] is True


def test_agreement_and_kappa():
    pairs = [(True, True), (True, True), (False, False), (False, True)]
    out = agreement(pairs)
    assert out["agree"] == 3 and out["agreement"] == 0.75
    # p_h = 0.5, p_j = 0.75 -> expected 0.5; kappa = (0.75 - 0.5) / 0.5
    assert out["cohen_kappa"] == pytest.approx(0.5)
    assert agreement([(True, True)])["cohen_kappa"] is None
