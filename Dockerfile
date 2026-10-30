# SciFact RAG API (CPU). Models, the Hugging Face cache and FAISS indexes are
# mounted at run time, not baked in: the fine-tuned models are not published.
FROM python:3.11.6-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements.txt .
# CPU-only torch wheel first (the default PyPI wheel on x86-64 pulls in CUDA);
# requirements.txt then sees torch==2.14.1 as already satisfied.
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch==2.14.1 \
    && pip install -r requirements.txt

COPY scifact_rag ./scifact_rag
COPY data ./data

RUN useradd --create-home --uid 10001 app
USER app

ENV SCIFACT_HF_CACHE=/models/hf-cache \
    SCIFACT_ARTIFACTS=/models/artifacts \
    SCIFACT_INDEX_DIR=/indexes \
    HF_HUB_OFFLINE=1 \
    TOKENIZERS_PARALLELISM=false \
    OLLAMA_URL=http://host.docker.internal:11434

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)"

# One worker: rate-limit state is per process.
CMD ["uvicorn", "scifact_rag.api:build_default_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
