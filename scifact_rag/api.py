"""FastAPI app exposing POST /search over one or more embedding models.

Run against the indexes built by scripts/reproduce_retrieval.py:

    .venv/bin/uvicorn scifact_rag.api:build_default_app --factory --port 8000
"""
from __future__ import annotations

import os
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MAX_K = 100
MAX_QUERY_CHARS = 2000


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=MAX_QUERY_CHARS)
    k: int = Field(default=10, ge=1, le=MAX_K)
    model: str | None = None


class SearchHit(BaseModel):
    rank: int
    doc_id: str
    score: float
    title: str


class Timings(BaseModel):
    embed_ms: float
    search_ms: float
    total_ms: float


class SearchResponse(BaseModel):
    model: str
    results: list[SearchHit]
    timings: Timings


def create_app(retrievers, default_model):
    """retrievers: {model_label: Retriever}."""
    if default_model not in retrievers:
        raise ValueError("default_model must be one of the retrievers")
    app = FastAPI(title="SciFact RAG", version="0.1.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "models": sorted(retrievers), "default_model": default_model}

    @app.post("/search", response_model=SearchResponse)
    def search(request: SearchRequest):
        label = request.model or default_model
        if label not in retrievers:
            raise HTTPException(status_code=400, detail=f"Unknown model '{label}'; available: {sorted(retrievers)}")
        if not request.query.strip():
            raise HTTPException(status_code=422, detail="Query must contain non-whitespace text")
        retriever = retrievers[label]
        k = min(request.k, len(retriever.index))
        start = time.perf_counter()
        hits, timings = retriever.search(request.query, k=k)
        total_ms = 1000 * (time.perf_counter() - start)
        return SearchResponse(model=label, results=[SearchHit(**vars(h)) for h in hits],
                              timings=Timings(total_ms=total_ms, **timings))

    return app


def build_default_app():
    """Load prebuilt indexes. SCIFACT_MODELS (comma list) picks models; the first is the default."""
    from .data import load_corpus
    from .index import FaissIndex
    from .models import Encoder
    from .service import Retriever

    index_dir = Path(os.environ.get("SCIFACT_INDEX_DIR", Path(__file__).resolve().parents[1] / "indexes"))
    labels = [s.strip() for s in os.environ.get("SCIFACT_MODELS", "original,C-seed42").split(",") if s.strip()]
    corpus = load_corpus()
    titles = dict(zip(corpus.doc_ids, corpus.titles))
    retrievers = {}
    for label in labels:
        index = FaissIndex.load(index_dir / label)
        if index.doc_ids != corpus.doc_ids:
            raise ValueError(f"Index {label} was built over a different corpus")
        retrievers[label] = Retriever(Encoder(label), index, titles)
    return create_app(retrievers, labels[0])
