# Test-set protocol (frozen before the test run)

Status: **draft — becomes frozen when the author approves it and it is
committed.** `scripts/run_test_matrix.py` refuses to run unless it is given
this file's SHA-256, so the test run is tied to the exact text below. Any change
after the run is reported as a deviation, never silently applied.

## What is fixed

All choices were made on validation claims only (README, "Week 3 progress").

| Item | Value |
| --- | --- |
| Test data | BEIR SciFact official test: 300 claims, 339 qrels, corpus 5,183 abstracts (revisions and SHA-256 in `scifact_rag/data.py`) |
| Generator | `qwen3:14b` (Ollama, Q4_K_M), temperature 0, seed 0, thinking off, `num_ctx` 8192 |
| Prompt | `v2` (`scifact_rag/generation.py`), abstracts truncated at 4,000 characters |
| Retrieved abstracts per answer | k = 5 |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` @ `233902d`, reranking the bi-encoder top 50 |
| Parser | `parse_answer` as of the protocol commit (NOT_FOUND sentinel, explained `[NOT_FOUND]` with no citations = abstention) |

## Settings (all 300 test claims each)

| ID | Retriever | Reranker |
| --- | --- | --- |
| A | Original MiniLM | no |
| C13 | C, seed 13 | no |
| C42 | C, seed 42 | no |
| C2026 | C, seed 2026 | no |
| A+R | Original MiniLM | top 50 |
| C42+R | C, seed 42 | top 50 |

## Automatic metrics (every setting, every claim)

- Retrieval: nDCG@10 and Recall@10 of the retriever (with reranker where used).
- Abstention rate: abstained / 300.
- Citation correctness: cited doc IDs that are in the claim's qrels / all valid
  cited doc IDs, over non-abstaining answers. A lower bound, because SciFact's
  labels are incomplete.
- Invalid citations: answers citing an ID that was not retrieved / answers.
- Latency per stage (embed, search, rerank, generate, total): p50 and p95 by
  nearest rank over 300 sequential requests, model warm (one discarded warm-up
  call per setting), Apple M4 Pro 48 GB, nothing else heavy running.
- Cost: $0 marginal API cost (local models); hardware and electricity not counted.

## Human faithfulness (sample)

- No LLM judge is used: `gemma3:12b` failed calibration (README), and the
  Claude API judge could not be run.
- Sample: 30 test claims drawn with `random.Random(2026)` from the 300, the
  same claims for settings **A**, **C42** and **C42+R** (paired), giving 90
  answers.
- Blinding: items are shuffled across settings, and the sheet does not show the
  setting. The setting key is written to a separate file that the annotator
  does not open until labelling is finished.
- Consistency check: 10 of the 90 items are repeated later in the sheet under
  new item IDs (100 items in total). Self-agreement on these is reported.
- Rubric: `JUDGE_RUBRIC.md`. Answers: faithful = every sentence SUPPORTED by
  the abstracts it cites. Abstentions: justified = no retrieved abstract
  reports anything about the claim.
- Reported per setting: faithful answers / labelled answers with a Wilson 95%
  interval; justified abstentions / abstentions. Paired comparisons (C42 vs A,
  C42+R vs C42) are reported as counts of claims where only one setting had a
  good outcome (a faithful answer or a justified abstention). With 30 claims
  these are descriptive, not significance tests.
- One annotator (the author), who also built the system. This is a stated
  limitation.

## Order of operations

1. Author approves this file; it is committed (`git log` shows the time).
2. `run_test_matrix.py --protocol-sha <sha>` runs all six settings once and
   writes `results/test/`. It refuses to overwrite existing results.
3. `make_human_sheet.py` builds the blinded sheet from those results.
4. The author labels the sheet; the labels file is committed before scoring.
5. `score_human_labels.py` reports the numbers above.
