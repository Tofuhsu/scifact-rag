"""FastAPI app: POST /search (retrieval) and POST /ask (cited generation).

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
MAX_ASK_K = 20
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


class AskRequest(BaseModel):
    query: str = Field(min_length=1, max_length=MAX_QUERY_CHARS)
    k: int = Field(default=5, ge=1, le=MAX_ASK_K)
    model: str | None = None


class Citation(BaseModel):
    doc_id: str
    title: str


class AskTimings(BaseModel):
    embed_ms: float
    search_ms: float
    generate_ms: float
    total_ms: float


class Usage(BaseModel):
    llm: str
    prompt_tokens: int | None
    completion_tokens: int | None


class AskResponse(BaseModel):
    model: str
    answer: str
    abstained: bool
    citations: list[Citation]
    invalid_citations: list[str]
    uncited: bool
    retrieved: list[SearchHit]
    timings: AskTimings
    usage: Usage
    prompt_version: str


def create_app(retrievers, default_model, llm=None, abstracts=None):
    """retrievers: {model_label: Retriever}. llm (with .chat(messages)) and abstracts
    ({doc_id: abstract}) enable POST /ask; without them /ask returns 503."""
    if default_model not in retrievers:
        raise ValueError("default_model must be one of the retrievers")
    app = FastAPI(title="SciFact RAG", version="0.2.0")

    def pick(label, query):
        label = label or default_model
        if label not in retrievers:
            raise HTTPException(status_code=400, detail=f"Unknown model '{label}'; available: {sorted(retrievers)}")
        if not query.strip():
            raise HTTPException(status_code=422, detail="Query must contain non-whitespace text")
        return label, retrievers[label]

    @app.get("/health")
    def health():
        return {"status": "ok", "models": sorted(retrievers), "default_model": default_model}

    @app.post("/search", response_model=SearchResponse)
    def search(request: SearchRequest):
        label, retriever = pick(request.model, request.query)
        k = min(request.k, len(retriever.index))
        start = time.perf_counter()
        hits, timings = retriever.search(request.query, k=k)
        total_ms = 1000 * (time.perf_counter() - start)
        return SearchResponse(model=label, results=[SearchHit(**vars(h)) for h in hits],
                              timings=Timings(total_ms=total_ms, **timings))

    @app.post("/ask", response_model=AskResponse)
    def ask(request: AskRequest):
        if llm is None or abstracts is None:
            raise HTTPException(status_code=503, detail="Generation is not configured on this server")
        from .generation import PROMPT_VERSION, Answerer

        label, retriever = pick(request.model, request.query)
        k = min(request.k, len(retriever.index))
        start = time.perf_counter()
        try:
            out = Answerer(retriever, llm, abstracts).ask(request.query, k=k)
        except Exception as exc:  # LLM server down, timeout, malformed reply
            raise HTTPException(status_code=502, detail=f"LLM call failed: {type(exc).__name__}") from exc
        total_ms = 1000 * (time.perf_counter() - start)
        parsed, hits = out["parsed"], out["hits"]
        titles = {h.doc_id: h.title for h in hits}
        return AskResponse(
            model=label, answer=parsed.text, abstained=parsed.abstained,
            citations=[Citation(doc_id=d, title=titles[d]) for d in parsed.citations],
            invalid_citations=parsed.invalid_citations, uncited=parsed.uncited,
            retrieved=[SearchHit(**vars(h)) for h in hits],
            timings=AskTimings(total_ms=total_ms, **out["timings"]),
            usage=Usage(llm=out["llm"].model, prompt_tokens=out["llm"].prompt_tokens,
                        completion_tokens=out["llm"].completion_tokens),
            prompt_version=PROMPT_VERSION)

    return app


def build_default_app():
    """Load prebuilt indexes. SCIFACT_MODELS (comma list) picks models; the first is the default."""
    from .data import load_corpus
    from .generation import OllamaClient
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
    llm = OllamaClient(model=os.environ.get("SCIFACT_LLM", "qwen3:14b"),
                       base_url=os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434"))
    abstracts = dict(zip(corpus.doc_ids, corpus.abstracts))
    return create_app(retrievers, labels[0], llm=llm, abstracts=abstracts)
