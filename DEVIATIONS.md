# Deviations from PROTOCOL.md

Each entry records something that happened during the frozen test run that
the protocol did not anticipate, what was done, and its effect.

## D1 — 2026-10-25: first test run stopped because of GPU contention

- **What happened.** About 26 minutes into setting A (no setting finished, no
  test output written to disk or read by anyone), another local project
  started GPU jobs on the same Mac (Qwen2.5-1.5B rollouts and LoRA updates on
  MPS, up to about 50 GB of driver memory and about 10 GB of swap), overlapping
  this run for about 35 minutes in total according to that project's report.
  The protocol requires latency to be measured with nothing else heavy
  running.
- **What was done.** The run was stopped. Because per-request rows had no
  timestamps, the affected requests could not be isolated. `run_test_matrix.py`
  now records a UTC start time on every row. The run was then restarted from
  the beginning with the same frozen PROTOCOL.md (SHA-256 unchanged), after the
  other jobs had finished and memory pressure was back to normal.
- **Effect.** The discarded partial run produced no saved answers or metrics,
  and no choice depends on it. The generator is deterministic in intent
  (temperature 0, seed 0), so the restart should regenerate the same answers;
  bit-identical GPU output is not claimed.
