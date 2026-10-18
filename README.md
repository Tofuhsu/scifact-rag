# SciFact RAG: retrieval service and end-to-end evaluation

> **Status: draft, week 1 of 4.** The retrieval service and the retrieval
> reproduction are done. Generation, citation, faithfulness, latency and cost
> results do not exist yet; the tables below mark them as pending.

This project turns an earlier controlled fine-tuning experiment
(MiniLM, hard vs random negatives on BEIR SciFact, 3 seeds; personal fork of
sentence-transformers) into a small retrieval-augmented generation service,
and measures what that experiment did not: online latency, cost, and answer
quality with citations.

## Research question

On the 300-claim BEIR SciFact test set, does the hard-negative fine-tuned
MiniLM retriever, compared with the original `all-MiniLM-L6-v2`, change
**end-to-end** answer quality (citation correctness, faithfulness), and at
what per-query latency and cost? Does adding a cross-encoder reranker change
that trade-off?

Secondary: does the offline retrieval gain (nDCG@10 0.6451 → 0.6785) carry
through to the citations an LLM actually produces?

## What will be measured

| Setting | nDCG@10 / Recall@10 | Citation correctness | Faithfulness | p50 / p95 latency | Cost per query |
| --- | --- | --- | --- | --- | --- |
| Original MiniLM | **done (below)** | pending | pending | pending | pending |
| Fine-tuned C (3 seeds) | **done (below)** | pending | pending | pending | pending |
| Fine-tuned C + reranker | pending | pending | pending | pending | pending |

Definitions (fixed before any generation results are seen):

- **nDCG@10, Recall@10**: binary relevance, same definitions and test split as
  the original experiment (unweighted mean over 300 claims; 339 qrel rows;
  corpus 5,183 abstracts; ties broken by ascending doc ID).
- **Citation correctness**: of the doc IDs cited in an answer, the fraction
  that are in SciFact's labelled relevant documents for that claim. Reported
  with its denominator (number of citations, number of answers).
- **Faithfulness**: whether each answer's content is supported by the
  abstracts it cites. LLM-as-judge, calibrated by manually labelling about 30
  answers; the judge–human agreement rate is reported next to the score.
- **Latency**: per-stage wall-clock time (embedding, FAISS search, rerank,
  generation) over the 300 test claims; p50 and p95 by nearest rank. Hardware,
  warm vs cold start, and batch size are recorded with every number.
- **Cost**: local Ollama is recorded as $0 marginal API cost (hardware and
  electricity not included). Any API model is costed from token counts.

### Test-set protocol

The retrieval numbers below re-evaluate models that were frozen before the
test set was first opened in the original experiment; nothing is trained or
tuned here. For weeks 2–3, prompt design, the abstain behaviour and the
reranker choice will be developed on non-test claims (the original
experiment's validation split), and the full matrix will be run on the test
set once, after those choices are frozen.

## Week 1 result: retrieval reproduction

Command (all four models, about 1 minute on the machine below):

```bash
SCIFACT_HF_CACHE=<hf cache with the pinned dataset/model> .venv/bin/python scripts/reproduce_retrieval.py
```

Output: `results/retrieval_reproduction.json`. Conditions: BEIR SciFact
official test, 300 claims / 339 qrels / 5,183 documents, dataset revision
`b3b5335`, qrels revision `2938d17`, both checked by SHA-256; FAISS
`IndexFlatIP` (exact search) on L2-normalized float32 embeddings; encoding on
Apple M4 Pro, MPS, float32, batch 32, max 256 tokens; Python 3.11.6,
torch 2.14.1, transformers 5.20.1, sentence-transformers 6.1.0 (PyPI release,
not the fork), faiss-cpu 1.15.1.

| Model | nDCG@10 | Recall@10 | Original experiment | Abs. difference |
| --- | --- | --- | --- | --- |
| Original MiniLM | 0.6451 | 0.7833 | 0.6451 / 0.7833 | 0 / 0 |
| C, seed 13 | 0.6787 | 0.8199 | 0.6787 / 0.8199 | 0 / 0 |
| C, seed 42 | 0.6801 | 0.8149 | 0.6801 / 0.8149 | 0 / 0 |
| C, seed 2026 | 0.6766 | 0.8116 | 0.6766 / 0.8116 | 0 / 0 |
| **C, mean ± std (3 seeds)** | **0.6785 ± 0.0014** | **0.8154 ± 0.0034** | 0.6785 ± 0.0014 / 0.8154 ± 0.0034 | — |

- Differences are computed at full float precision and are exactly 0.0 for
  every model and metric.
- For all 4 models, the top-10 doc IDs are identical, in the same order, to
  the original experiment's saved run on 300 of 300 claims.
- FAISS top-10 equals an exact NumPy ranking (full dot products, doc-ID tie
  break) on 300 of 300 claims for every model.
- The "±" in the original report matches the **population** standard
  deviation over the 3 seeds (ddof = 0). The sample standard deviation would
  be 0.0017 (nDCG@10) and 0.0042 (Recall@10). Both are in the JSON output.

## Search API

```bash
.venv/bin/uvicorn scifact_rag.api:build_default_app --factory --port 8000
curl -s -X POST localhost:8000/search -H 'content-type: application/json' \
  -d '{"query": "Statins reduce cardiovascular events.", "k": 5, "model": "C-seed42"}'
```

`POST /search` takes `query` (1–2000 chars), `k` (1–100, default 10) and an
optional `model` (`original`, `C-seed13`, `C-seed42`, `C-seed2026`; the
server loads `SCIFACT_MODELS`, default `original,C-seed42`). It returns ranked
`{rank, doc_id, score, title}` hits and `timings` (`embed_ms`, `search_ms`,
`total_ms`). `GET /health` lists loaded models. Indexes are built by the
reproduction script into `indexes/` (not committed).

Timings in responses are single-request wall-clock values, not benchmark
results. Latency is measured in week 3.

## Setup and tests

```bash
python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

32 unit tests (API validation and responses, FAISS ranking and tie-breaking,
index save/load, metric known-answer fixtures, data parsing). They use a
small hash-based fake encoder, so they need no model download. Environment
variables: `SCIFACT_HF_CACHE` (Hugging Face cache dir), `SCIFACT_ARTIFACTS`
(fine-tuned models; default `~/scientific-retrieval/scientific-retrieval-artifacts`),
`SCIFACT_INDEX_DIR`, `SCIFACT_MODELS`.

## Plan

- Week 1 (done): repo, README draft, FAISS indexes, retrieval reproduction, `/search` + tests.
- Week 2: local LLM through Ollama; prompt that answers only from retrieved abstracts and cites doc IDs; `/ask` endpoint; tests for citation parsing and "not found" answers.
- Week 3: evaluation harness for the full matrix; cross-encoder reranker ablation; latency and cost.
- Week 4: Docker image with authentication or rate limiting; final README with results, limits and non-claims; GitHub Actions CI.

## Limits (so far)

- SciFact is a small benchmark (5,183 abstracts, 300 test claims). Results do
  not represent real-world use.
- The fine-tuned models come from the earlier experiment and are loaded from
  a local artifacts folder; they are not published, so others cannot rerun the
  fine-tuned rows without them.
- Measured on one machine (Apple M4 Pro, MPS). Bit-identical results are not
  claimed on other hardware.
- torch and faiss-cpu each ship their own OpenMP runtime on macOS arm64. The
  package sets `KMP_DUPLICATE_LIB_OK=TRUE` and `OMP_NUM_THREADS=1` to load
  both; this is an unsupported workaround, which is why the reproduction
  script checks every FAISS result against exact NumPy search.
- FAISS ties are broken by doc ID within the top k + 16 candidates; ties
  extending beyond that window would not be fully resolved. None affected the
  test run (300/300 identical to exact search).

## Not claimed

Production use, real users, results better than the SciFact paper, or a
"fact-checking system". SciFact's original task is claim verification; this
project does retrieval plus cited generation only.

## AI assistance

Code and this README were written with an AI coding assistant (Claude Code)
under the author's direction and review. Retrieval numbers were produced by
running the committed script, not copied from the original report.
