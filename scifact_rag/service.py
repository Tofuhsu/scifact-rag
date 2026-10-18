"""Retriever: query text -> embedding -> FAISS top-k, with per-stage timings."""
from __future__ import annotations

import time
from dataclasses import dataclass

from .data import query_text


@dataclass(frozen=True)
class Hit:
    rank: int
    doc_id: str
    score: float
    title: str


class Retriever:
    def __init__(self, encoder, index, titles):
        """encoder: has .encode(list[str]) -> (n, dim) float32 normalized, optional .synchronize().
        index: FaissIndex. titles: {doc_id: title}."""
        self.encoder = encoder
        self.index = index
        self.titles = titles

    def search(self, query, k=10):
        text = query_text(query)
        sync = getattr(self.encoder, "synchronize", lambda: None)
        start = time.perf_counter()
        embedding = self.encoder.encode([text])
        sync()
        embedded = time.perf_counter()
        (hits,) = self.index.search(embedding, k=k)
        searched = time.perf_counter()
        results = [Hit(rank, did, score, self.titles.get(did, "")) for rank, (did, score) in enumerate(hits, 1)]
        timings = {"embed_ms": 1000 * (embedded - start), "search_ms": 1000 * (searched - embedded)}
        return results, timings
