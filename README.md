# SciFact RAG: retrieval service and end-to-end evaluation

> **Status: complete (4 weeks).** The frozen test run (6 settings × 300 claims) and
> the blinded human faithfulness sample are in
> [Test results](#test-results-frozen-protocol); the API runs in Docker with
> API-key auth and rate limiting ([Docker](#docker)), and CI runs the unit tests
> and builds the image on every push.

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
| Original MiniLM | done | done | done (human, sample) | done | $0 API |
| Fine-tuned C (3 seeds) | done | done | done (seed 42, human, sample) | done | $0 API |
| Original and C42 + reranker | done | done | done (C42+R, human, sample) | done | $0 API |

All are reported in [Test results](#test-results-frozen-protocol). Faithfulness
ended up human-labelled, not LLM-judged (the judge failed calibration, below).

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
SCIFACT_API_KEYS=dev-key .venv/bin/uvicorn scifact_rag.api:build_default_app --factory --port 8000
curl -s -X POST localhost:8000/search -H 'content-type: application/json' -H 'X-API-Key: dev-key' \
  -d '{"query": "Statins reduce cardiovascular events.", "k": 5, "model": "C-seed42"}'
```

**Auth and rate limits.** `/search` and `/ask` need an `X-API-Key` header
(401 otherwise); `/health` is open for health checks. Keys come from
`SCIFACT_API_KEYS` (comma-separated) or a file named by `SCIFACT_API_KEYS_FILE`;
the server refuses to start with no keys unless `SCIFACT_AUTH=off` (local
development only). Each key gets a token bucket per endpoint:
`SCIFACT_SEARCH_RATE_LIMIT` (default `60/minute`) and `SCIFACT_ASK_RATE_LIMIT`
(default `10/minute`, since one answer takes 11–15 s of local GPU time). Over
the limit the server returns 429 with `Retry-After`. Keys are compared as
SHA-256 digests in constant time and are never logged.

`POST /search` takes `query` (1–2000 chars), `k` (1–100, default 10) and an
optional `model` (`original`, `C-seed13`, `C-seed42`, `C-seed2026`; the
server loads `SCIFACT_MODELS`, default `original,C-seed42`). It returns ranked
`{rank, doc_id, score, title}` hits and `timings` (`embed_ms`, `search_ms`,
`total_ms`). `GET /health` lists loaded models. Indexes are built by the
reproduction script into `indexes/` (not committed).

### `POST /ask`

```bash
curl -s -X POST localhost:8000/ask -H 'content-type: application/json' \
  -d '{"query": "Statins reduce cardiovascular events.", "k": 5, "model": "C-seed42"}' \
  -H 'X-API-Key: dev-key'
```

Retrieves the top `k` abstracts (1–20, default 5), sends only those to a local
LLM through Ollama (default `qwen3:14b`, Q4_K_M; temperature 0, seed 0,
thinking off; `SCIFACT_LLM` and `OLLAMA_URL` override), and returns:

- `answer`, with inline `[doc_id]` citations after each finding;
- `citations`: valid cited doc IDs (those among the retrieved abstracts) with titles;
- `invalid_citations`: cited IDs that were *not* retrieved — reported, never silently dropped;
- `abstained`: true when the model answers with the `NOT_FOUND` sentinel;
- `uncited`: true for a non-abstaining answer with no valid citation;
- `retrieved`, per-stage `timings` (`embed_ms`, `search_ms`, `generate_ms`,
  `total_ms`), token `usage`, and `prompt_version`.

The prompt (`scifact_rag/generation.py`, version `v1`) tells the model to use
only the given abstracts, cite every finding, answer `NOT_FOUND` when the
abstracts do not address the question, and not judge a claim true overall
unless an abstract states it. LLM errors return 502; a server without an LLM
returns 503 for `/ask`.

Timings in responses are single-request wall-clock values, not benchmark
results. Latency is measured in week 3.

## Week 2 development check (validation claims, not results)

`scripts/dev_ask.py --sample 30` ran prompt `v1` with `qwen3:14b` on 30
validation claims (seeded sample of the original experiment's 160-claim
validation split; official test claims are not used) for two retrievers, k = 5,
plus 5 out-of-domain questions. Output: `results/dev/ask_validation_v1.json`.

| Retriever | Claims with a relevant doc in top 5 | Abstained | Abstained although a relevant doc was retrieved | Answers with invalid citations | Uncited answers | Cited docs in qrels | Out-of-domain abstained |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Original MiniLM | 22/30 | 9/30 | 4/9 | 0/21 | 0/21 | 17/34 | 5/5 |
| C, seed 42 | 21/30 | 10/30 | 4/10 | 0/20 | 0/20 | 16/28 | 5/5 |

How to read this:

- It checks that the pipeline behaves as designed: every non-abstaining answer
  cited at least one retrieved abstract, no answer cited an ID outside the
  retrieved set, and all out-of-domain questions got `NOT_FOUND`.
- It is **not** a retriever comparison. 30 claims is small, the validation
  split was used to choose the fine-tuning learning rate, and one seed (42) is
  shown.
- "Cited docs in qrels" understates correctness when SciFact's labels are
  incomplete (an unlabelled abstract can still support the answer). That is why
  faithfulness is judged separately in week 3.
- Main issue found for week 3: the model abstained on 4 claims in each run
  where a labelled relevant abstract was in the top 5 (over-abstention).
  Prompt changes will be made and checked on validation claims only.
- Generation time with a warm model, sequential single requests, one run on
  Apple M4 Pro (48 GB): p50 8.6 s / p95 14.6 s (original) and 10.2 s / 16.2 s
  (C seed 42), nearest rank over 30 requests. Mean prompt ≈ 1,750 tokens,
  completion ≈ 66 tokens. Local Ollama has $0 marginal API cost (hardware and
  electricity not counted). These are not the week-3 latency benchmark.

## Week 3 progress (validation claims only)

**Prompt v2.** Reviewing the week-2 "abstained although a relevant doc was
retrieved" cases showed that 3 of the 4 C-seed-42 cases were reasonable: the
labelled abstracts do not state anything about the claim (SciFact labels
documents, and the BEIR abstract text can be short). One case (query 323) was
a real miss: the abstract's result runs against the claim and the model said
NOT_FOUND. Prompt v2 asks for contradicting or partial evidence to be reported
with citations, and raises the per-abstract limit from 2,000 to 4,000
characters (truncates 17 of 5,183 abstracts instead of 535). The parser now
also treats an explanation followed by `[NOT_FOUND]` with no citations as an
abstention.

Same 30 validation claims, k = 5, `qwen3:14b` (counts re-parsed with the current parser):

| Prompt | Retriever | Abstained | Abstained although a relevant doc was retrieved | Cited docs in qrels | Answers with invalid citations |
| --- | --- | --- | --- | --- | --- |
| v1 | Original | 9/30 | 4/9 | 17/34 | 0/21 |
| v2 | Original | 6/30 | 3/6 | 20/34 | 0/24 |
| v1 | C, seed 42 | 10/30 | 4/10 | 16/28 | 0/20 |
| v2 | C, seed 42 | 6/30 | 1/6 | 20/33 | 0/24 |

Fewer abstentions could also mean more unsupported answers; the faithfulness
judge (below) checks that before v2 is frozen.

**Reranker depth.** `scripts/dev_rerank.py`: cross-encoder
`cross-encoder/ms-marco-MiniLM-L-6-v2` (revision `233902d`) reranking the
bi-encoder's top N, 160 validation claims, Apple M4 Pro MPS. Output:
`results/dev/rerank_validation.json`.

| Retriever | No rerank nDCG@10 / R@10 | Rerank top 20 | Rerank top 50 | Rerank top 100 |
| --- | --- | --- | --- | --- |
| Original | 0.6134 / 0.7516 | 0.6498 / 0.7672 | 0.6533 / 0.7891 | 0.6680 / 0.7995 |
| C, seed 13 | 0.6150 / 0.7536 | 0.6586 / 0.7672 | 0.6664 / 0.7797 | 0.6672 / 0.7891 |
| C, seed 42 | 0.6158 / 0.7599 | 0.6551 / 0.7703 | 0.6643 / 0.7797 | 0.6678 / 0.7891 |
| C, seed 2026 | 0.6146 / 0.7536 | 0.6640 / 0.7766 | 0.6665 / 0.7797 | 0.6678 / 0.7891 |

Wall time for all 160 claims (embedding + search + rerank, warm, sequential):
about 2 s without reranking, 13–14 s at top 20, 27 s at top 50, 47 s at top 100.

- On validation, the fine-tuned models are only +0.001 to +0.002 nDCG@10 over
  the original without reranking, much less than the +0.033 on test. The
  validation split was used to choose the fine-tuning learning rate, and 160
  claims is a small sample, so neither number is a clean estimate on its own.
- Reranking adds +0.04 to +0.05 nDCG@10 on validation for every retriever. With
  reranking, the original and C models are within 0.002 of each other at top 100.
- Proposed frozen depth for the test run: **top 50**. For the C models, top 100
  adds at most 0.0035 nDCG@10 for about 1.7× the rerank time; the original
  model gains more from top 100 (+0.0147), which will be stated with the result.

**Judge calibration (failed so far).** `scifact_rag/judge.py`, `JUDGE_RUBRIC.md`.
The author labelled 30 validation items (20 answers, 10 abstentions;
`calibration/labels_v2.csv`, committed before the judge was run on them).
Judge: `gemma3:12b` through local Ollama (a different family from the
generator `qwen3:14b`).

| Judge prompt | Faithfulness agreement | Cohen's kappa | Abstention agreement | Cohen's kappa |
| --- | --- | --- | --- | --- |
| j1 | 12/20 | −0.07 | 9/10 | 0.00 |
| j2 (revised after seeing j1 errors, same 30 items) | 11/20 | −0.29 | 9/10 | 0.00 |

- Faithfulness agreement is no better than chance. Where the judge was
  stricter than the human (4 items), it marked uncited framing or summary
  sentences ("The evidence contradicts the claim.") as NOT_SUPPORTED. Where it
  was more lenient (4 items), it missed overreach and reversed direction of
  effect (an abstract showing that knocking out Gpr124 causes BBB disruption was
  accepted as support for "Gpr124 increases BBB breakdown").
- j2 targeted both patterns and did worse even on the items it was written
  after, so the limit appears to be the judge model, not the prompt.
- The abstention judge said "justified" for all 10 items. 9/10 agreement
  reflects that 9 of the 10 human labels were also "justified"; kappa is 0.
- Result: no faithfulness numbers from this judge will be reported. A
  different judge (or human-only labelling) has to pass calibration first, on
  items it was not tuned on. With 20 and 10 items, these agreement figures are
  themselves imprecise.

**Plan for the test run.** Faithfulness will be labelled by a human on a
blinded, paired sample (30 test claims × 3 settings, plus 10 repeated items
for self-consistency); automatic metrics and latency cover all 300 claims for
six settings. The full plan is in [`PROTOCOL.md`](PROTOCOL.md), which is
frozen before the test set is used.

## Test results (frozen protocol)

Run once under [`PROTOCOL.md`](PROTOCOL.md) (SHA-256 `a960127e…`, frozen
before any test generation), 2026-10-27 15:11–21:48 UTC, from commit
`c05190e`. Output: `results/test/*.json`, one
file per setting with every answer. Deviations (two stopped runs with no saved
output, and one short CPU-only overlap) are in [`DEVIATIONS.md`](DEVIATIONS.md).

Conditions: BEIR SciFact test, 300 claims; generator `qwen3:14b` (Ollama,
Q4_K_M), temperature 0, seed 0, thinking off, prompt `v2`, k = 5 abstracts per
answer; reranker `ms-marco-MiniLM-L-6-v2` over the bi-encoder top 50;
Apple M4 Pro 48 GB; sequential single requests, warm model (one discarded
warm-up per setting).

### Retrieval and answers (all 300 claims)

| Setting | nDCG@10 | Recall@10 | Claims with a relevant doc in top 5 | Abstained | Abstained with a relevant doc in top 5 | Cited docs in qrels | Answers with invalid citations | Uncited answers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A: original | 0.6451 | 0.7833 | 226/300 | 54/300 | 20/54 | 207/410 (50.5%) | 0/246 | 3/246 |
| C, seed 13 | 0.6787 | 0.8199 | 228/300 | 49/300 | 20/49 | 210/434 (48.4%) | 0/251 | 2/251 |
| C, seed 42 | 0.6801 | 0.8149 | 229/300 | 50/300 | 21/50 | 210/423 (49.6%) | 0/250 | 2/250 |
| C, seed 2026 | 0.6766 | 0.8116 | 228/300 | 49/300 | 20/49 | 209/410 (51.0%) | 0/251 | 3/251 |
| A + rerank | 0.6936 | 0.8222 | 228/300 | 46/300 | 19/46 | 212/425 (49.9%) | 0/254 | 3/254 |
| C42 + rerank | 0.6946 | 0.8222 | 227/300 | 46/300 | 18/46 | 210/425 (49.4%) | 0/254 | 2/254 |

"Cited docs in qrels" is a lower bound on citation correctness: SciFact labels
are incomplete, so a cited abstract outside the qrels can still support the
answer (see the human sample below).

### Latency and cost (all 300 claims, ms, nearest-rank p50 / p95)

| Setting | Embed | Search | Rerank | Generate | Total | Mean prompt / completion tokens |
| --- | --- | --- | --- | --- | --- | --- |
| A | 33 / 44 | 0 / 0 | — | 11,172 / 17,661 | 11,208 / 17,694 | 1,960 / 87 |
| C13 | 31 / 40 | 0 / 0 | — | 12,389 / 19,868 | 12,434 / 19,901 | 1,963 / 90 |
| C42 | 29 / 39 | 0 / 0 | — | 12,334 / 19,919 | 12,376 / 19,949 | 1,950 / 88 |
| C2026 | 29 / 39 | 0 / 0 | — | 12,370 / 19,581 | 12,401 / 19,613 | 1,944 / 89 |
| A + rerank | 31 / 41 | 0 / 0 | 218 / 257 | 14,085 / 21,021 | 14,339 / 21,277 | 2,121 / 92 |
| C42 + rerank | 42 / 75 | 0 / 0 | 240 / 308 | 14,300 / 21,883 | 14,580 / 22,180 | 2,118 / 93 |

Search is FAISS exact search over 5,183 vectors (under 0.5 ms, shown as 0).
Cost: $0 marginal API cost for every setting (all models local); hardware and
electricity are not counted. Leaving out the two C42 + rerank rows that
overlapped outside CPU work (D3) changes its total p50 to 14,515 ms; p95 is
unchanged.

### Human faithfulness (blinded sample)

30 test claims (`random.Random(2026)`), the same claims for A, C42 and
C42 + rerank, shuffled with the setting hidden; 10 items repeated for a
consistency check (100 items). One annotator, the author. Labels were committed
(`8608814`) before the key was opened and scored. Output:
`results/test/human_faithfulness.json`.

| Setting | Faithful answers (Wilson 95%) | Justified abstentions |
| --- | --- | --- |
| A: original | 19/24 = 79% (60–91%) | 6/6 |
| C, seed 42 | 21/25 = 84% (65–94%) | 5/5 |
| C42 + rerank | 19/24 = 79% (60–91%) | 6/6 |

- Paired, "good outcome" = faithful answer or justified abstention, 30 claims:
  C42 vs A, 3 claims good only with C42 and 2 only with A; C42 + rerank vs C42,
  1 only with rerank and 2 only without. Descriptive only; no test of
  significance is meaningful at this size, and the intervals overlap widely.
- Self-agreement on the 10 repeated items: 10/10.

### What this shows

- **The retrieval gain does not carry through to answers in this setup.** The
  fine-tuned models raise nDCG@10 by about +0.03 and the reranker by about
  +0.05 over the original, but the number of claims with a labelled relevant
  abstract in the top 5 moves only from 226 to 227–229 of 300, cited-in-qrels
  stays at 48–51% for every setting, and abstentions fall only from 54 to 46.
  With k = 5 the LLM sees most of the useful abstracts either way; better
  ordering inside or just past the top 5 matters for nDCG@10 but little for
  the answer.
- Faithfulness on the sample is 79–84% for all three settings, with no
  difference that 24–25 answers per setting could detect. Every abstention in
  the sample (17/17) was judged justified, so the abstentions with a "relevant"
  doc in the top 5 are, in the sample, cases where the labelled abstract does
  not state anything about the claim.
- **Cost of the reranker:** about +0.25 s of reranking plus +2 to +3 s of
  generation at p50, because reranked top-5 abstracts are longer on average
  (about +160 prompt tokens). Generation dominates latency in every setting
  (over 99% of p50).
- The C models' generation p50 is about 1.2 s higher than A's at nearly the
  same token counts. Settings ran one after another over 6.5 hours on one
  machine, so this may be drift (for example thermal) rather than an effect of
  the retriever; it is not interpreted.

## Docker

```bash
mkdir -p secrets && python3 -c "import secrets; print(secrets.token_urlsafe(32))" > secrets/api_keys
docker compose up --build        # http://127.0.0.1:8000
curl -s -X POST localhost:8000/search -H 'content-type: application/json' \
  -H "X-API-Key: $(head -1 secrets/api_keys)" -d '{"query": "Statins reduce cardiovascular events."}'
```

- CPU-only image (`python:3.11.6-slim`, CPU torch wheel, about 2.2 GB), non-root
  user, read-only root filesystem, one uvicorn worker, health check on `/health`.
- Nothing large is baked in. `compose.yaml` mounts `indexes/` (built by
  `scripts/reproduce_retrieval.py`), the Hugging Face cache and the fine-tuned
  model folder read-only (`SCIFACT_HF_CACHE_HOST`, `SCIFACT_ARTIFACTS_HOST`
  override the host paths). Keys are a Docker secret (`secrets/`, gitignored).
  The port is bound to 127.0.0.1 only.
- `/ask` calls Ollama on the host (`host.docker.internal:11434`); the container
  has no GPU access, so generation stays on the host's Ollama.
- Check (2026-10-29, Apple M4 Pro, Docker Desktop 29.2.0 arm64): querying the
  container (CPU query embeddings) returned top-5 doc IDs identical to the
  frozen test run (MPS query embeddings) on 300/300 test claims for both the
  original and C-seed-42 models. Requests without a key got 401, searches past the 60th
  within a minute got 429 with `Retry-After`, `/ask` returned a cited answer through host
  Ollama, and the image exits with an error when no key is configured.

## Continuous integration

`.github/workflows/ci.yml` runs on every push to `main` and every pull request:
the unit tests on Python 3.11 with `requirements-test.txt` (no torch; the tests
use fake encoders and LLMs), and a Docker build that also checks the container
refuses to start without API keys. CI does not run models, Ollama or the
evaluation; those need local data and a GPU.

## Setup and tests

```bash
python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

112 unit tests (API key auth and rate limiting, API validation and responses for `/search` and `/ask`, the
judge and its agreement statistics, reranking,
citation parsing, the NOT_FOUND abstain path, LLM failure handling, FAISS
ranking and tie-breaking, index save/load, metric known-answer fixtures, data
parsing). They use a hash-based fake encoder and a scripted fake LLM, so they
need no model download and no Ollama server. Environment
variables: `SCIFACT_HF_CACHE` (Hugging Face cache dir), `SCIFACT_ARTIFACTS`
(fine-tuned models; default `~/scientific-retrieval/scientific-retrieval-artifacts`),
`SCIFACT_INDEX_DIR`, `SCIFACT_MODELS`.

## Plan

- Week 1 (done): repo, README draft, FAISS indexes, retrieval reproduction, `/search` + tests.
- Week 2 (done): local LLM through Ollama; prompt that answers only from retrieved abstracts and cites doc IDs; `/ask` endpoint; tests for citation parsing and "not found" answers; development check on validation claims (below).
- Week 3 (done): evaluation harness, reranker depth on validation, judge calibration (failed), frozen protocol, test run, blinded human faithfulness sample.
- Week 4 (done): Docker image with API-key auth and per-key rate limiting; GitHub Actions CI; final README.

## Limits

- Rate limits are kept in memory per process: they reset on restart and do
  not add up across replicas. A shared store (e.g. Redis) would be needed to
  run more than one worker. There is no TLS; put the API behind a reverse
  proxy that terminates TLS before exposing it beyond localhost.

- Faithfulness is from one annotator (the author, who built the system), on
  30 claims × 3 settings. Blinding hid the setting, not the fact that the
  author wrote the prompt. The intervals are wide.
- All settings use one generator (`qwen3:14b`), one prompt and k = 5. A
  smaller k, or a weaker generator, could make retrieval quality matter more.
- Latency is sequential single requests on one laptop with settings run one
  after another; it says nothing about throughput under concurrent load.

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

## Data and licence

Code in this repository is under the [MIT License](LICENSE). The data is not:
claims and abstracts come from SciFact (Wadden et al., 2020, "Fact or Fiction:
Verifying Scientific Claims"), loaded from the BEIR copy on Hugging Face
(`BeIR/scifact`, whose dataset card lists CC BY-SA 4.0); the original SciFact
release by AllenAI is under CC BY-NC 2.0. Abstract text quoted in
`results/test/`, `results/dev/`, `calibration/` and `human_eval/` stays under
the dataset's licence. Model weights are not included: the base model is
`sentence-transformers/all-MiniLM-L6-v2` (Apache 2.0), and the fine-tuned
models are not published.

## AI assistance

Code and this README were written with an AI coding assistant (Claude Code)
under the author's direction and review. Retrieval numbers were produced by
running the committed script, not copied from the original report.
