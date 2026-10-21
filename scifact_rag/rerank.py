"""Cross-encoder reranking on top of the bi-encoder + FAISS retriever."""
from __future__ import annotations

import time

from .data import document_text, query_text
from .service import Hit

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANKER_REVISION = "233902d25c440f23af6f7d6e94d2946bac0bee0a"


class CrossEncoderScorer:
    def __init__(self, model=RERANKER_MODEL, revision=RERANKER_REVISION, device=None):
        from sentence_transformers import CrossEncoder

        from .models import default_device

        self.device = device or default_device()
        self.model = CrossEncoder(model, revision=revision, device=self.device, max_length=512)

    def score(self, query, documents, batch_size=32):
        pairs = [(query, d) for d in documents]
        return [float(s) for s in self.model.predict(pairs, batch_size=batch_size, show_progress_bar=False)]


class RerankingRetriever:
    """Same .search(query, k) interface as Retriever; reranks the first `candidates` hits."""

    def __init__(self, retriever, scorer, abstracts, candidates=50):
        if candidates < 1:
            raise ValueError("candidates must be positive")
        self.retriever = retriever
        self.scorer = scorer
        self.abstracts = abstracts
        self.candidates = candidates
        self.index = retriever.index
        self.titles = retriever.titles

    def search(self, query, k=10):
        text = query_text(query)
        n = max(k, min(self.candidates, len(self.index)))
        hits, timings = self.retriever.search(text, k=n)
        start = time.perf_counter()
        docs = [document_text(h.title, self.abstracts[h.doc_id]) for h in hits]
        scores = self.scorer.score(text, docs)
        # Stable order: cross-encoder score desc, then first-stage rank.
        order = sorted(range(len(hits)), key=lambda i: (-scores[i], i))[:k]
        reranked = [Hit(rank, hits[i].doc_id, scores[i], hits[i].title) for rank, i in enumerate(order, 1)]
        timings = dict(timings, rerank_ms=1000 * (time.perf_counter() - start))
        return reranked, timings
