import math

import pytest

from scifact_rag.metrics import evaluate, ndcg_at_k, recall_at_k

DOCS = [f"d{i:02d}" for i in range(1, 13)]
L3 = 1 / math.log2(3)


# Known-answer fixtures from the original experiment's METRICS.md (12 docs, k=10).
@pytest.mark.parametrize("positive_ranks, ndcg, recall", [
    ([1], 1.0, 1.0),
    ([2], L3, 1.0),
    ([1, 3], (1 + 1 / math.log2(4)) / (1 + L3), 1.0),
    ([1, 12], 1 / (1 + L3), 0.5),
    ([11, 12], 0.0, 0.0),
    ([10], 1 / math.log2(11), 1.0),
    (list(range(1, 13)), 1.0, 10 / 12),
])
def test_known_answers(positive_ranks, ndcg, recall):
    relevant = {DOCS[r - 1]: 1 for r in positive_ranks}
    assert ndcg_at_k(DOCS, relevant, 10) == pytest.approx(ndcg, abs=1e-12)
    assert recall_at_k(DOCS, relevant, 10) == pytest.approx(recall, abs=1e-12)


def test_evaluate_is_unweighted_mean_and_keeps_empty_runs():
    qrels = {"q1": {"d01": 1}, "q2": {"d05": 1}}
    result = evaluate(qrels, {"q1": DOCS, "q2": []}, k=10)
    assert result["queries"] == 2
    assert result["nDCG@10"] == pytest.approx(0.5)
    assert result["Recall@10"] == pytest.approx(0.5)


def test_evaluate_rejects_mismatched_queries_and_empty_qrels():
    with pytest.raises(ValueError):
        evaluate({"q1": {"d01": 1}}, {"q2": DOCS})
    with pytest.raises(ValueError):
        ndcg_at_k(DOCS, {}, 10)
