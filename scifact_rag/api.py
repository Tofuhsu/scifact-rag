"""FastAPI app: POST /search (retrieval) and POST /ask (cited generation).

Run against the indexes built by scripts/reproduce_retrieval.py:

    SCIFACT_API_KEYS=<key> .venv/bin/uvicorn scifact_rag.api:build_default_app --factory --port 8000

/search and /ask require an `X-API-Key` header and are rate limited per key;
/health is open (for container health checks).
"""
from __future__ import annotations

import os
import time
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from .security import KeyChecker, RateLimiter, load_api_keys, parse_rate_limit, retry_after_header

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


def create_app(retrievers, default_model, llm=None, abstracts=None, api_keys=None, search_limit=None,
               ask_limit=None, clock=time.monotonic):
    """retrievers: {model_label: Retriever}. llm (with .chat(messages)) and abstracts
    ({doc_id: abstract}) enable POST /ask; without them /ask returns 503.

    api_keys: list of accepted X-API-Key values (None = no auth). search_limit / ask_limit:
    (requests, per_seconds) per client, where a client is its API key, or its IP without auth."""
    if default_model not in retrievers:
        raise ValueError("default_model must be one of the retrievers")
    app = FastAPI(title="SciFact RAG", version="0.3.0")
    checker = KeyChecker(api_keys) if api_keys is not None else None
    limiters = {name: RateLimiter(*limit, clock=clock) if limit else None
                for name, limit in (("search", search_limit), ("ask", ask_limit))}

    def guard(name):
        def dependency(request: Request, x_api_key: str | None = Header(default=None)):
            if checker is not None:
                client = checker.client_id(x_api_key)
                if client is None:
                    raise HTTPException(status_code=401, detail="Missing or invalid X-API-Key",
                                        headers={"WWW-Authenticate": "ApiKey"})
            else:
                client = f"ip:{request.client.host if request.client else 'unknown'}"
            limiter = limiters[name]
            if limiter is not None:
                wait = limiter.acquire(client)
                if wait > 0:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded",
                                        headers={"Retry-After": retry_after_header(wait)})
        return Depends(dependency)

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
    def search(request: SearchRequest, _=guard("search")):
        label, retriever = pick(request.model, request.query)
        k = min(request.k, len(retriever.index))
        start = time.perf_counter()
        hits, timings = retriever.search(request.query, k=k)
        total_ms = 1000 * (time.perf_counter() - start)
        return SearchResponse(model=label, results=[SearchHit(**vars(h)) for h in hits],
                              timings=Timings(total_ms=total_ms, **timings))

    @app.post("/ask", response_model=AskResponse)
    def ask(request: AskRequest, _=guard("ask")):
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
    """Load prebuilt indexes. SCIFACT_MODELS (comma list) picks models; the first is the default.

    Refuses to start without API keys (SCIFACT_API_KEYS or SCIFACT_API_KEYS_FILE) unless
    SCIFACT_AUTH=off. Rate limits: SCIFACT_SEARCH_RATE_LIMIT (default 60/minute) and
    SCIFACT_ASK_RATE_LIMIT (default 10/minute) per key; 'off' disables.
    """
    api_keys = load_api_keys()
    if os.environ.get("SCIFACT_AUTH", "on").lower() == "off":
        api_keys = None
    elif not api_keys:
        raise RuntimeError("No API keys configured: set SCIFACT_API_KEYS or SCIFACT_API_KEYS_FILE "
                           "(or SCIFACT_AUTH=off for local development only)")
    search_limit = parse_rate_limit(os.environ.get("SCIFACT_SEARCH_RATE_LIMIT", "60/minute"))
    ask_limit = parse_rate_limit(os.environ.get("SCIFACT_ASK_RATE_LIMIT", "10/minute"))
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
    return create_app(retrievers, labels[0], llm=llm, abstracts=abstracts, api_keys=api_keys,
                      search_limit=search_limit, ask_limit=ask_limit)
