import pytest

from scifact_rag.rerank import RerankingRetriever
from tests.conftest import DOCS


class KeywordScorer:
    """Scores a document by how many times it contains the word 'aspirin'."""

    def __init__(self):
        self.calls = []

    def score(self, query, documents):
        self.calls.append(len(documents))
        return [float(d.lower().count("aspirin")) for d in documents]


def make(retriever, candidates=5):
    return RerankingRetriever(retriever, KeywordScorer(), {d: DOCS[d][1] for d in DOCS}, candidates=candidates)


def test_reranker_reorders_candidates_and_reports_rerank_time(retriever):
    rr = make(retriever)
    hits, timings = rr.search("statin cholesterol", k=2)
    assert hits[0].doc_id == "105" and hits[0].rank == 1 and hits[0].title == "Aspirin"
    assert [h.rank for h in hits] == [1, 2]
    assert set(timings) == {"embed_ms", "search_ms", "rerank_ms"}
    assert rr.scorer.calls == [5]


def test_ties_keep_first_stage_order(retriever):
    first, _ = retriever.search("statin cholesterol", k=5)
    hits, _ = make(retriever).search("statin cholesterol", k=5)
    rest = [h.doc_id for h in hits[1:]]
    assert rest == [h.doc_id for h in first if h.doc_id != "105"]


def test_candidates_never_below_k(retriever):
    rr = make(retriever, candidates=2)
    hits, _ = rr.search("malaria", k=4)
    assert len(hits) == 4 and rr.scorer.calls == [4]


def test_invalid_candidates(retriever):
    with pytest.raises(ValueError):
        make(retriever, candidates=0)
