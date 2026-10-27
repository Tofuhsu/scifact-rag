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

## D2 — 2026-10-25: restarted test run killed when the Claude desktop app exited

- **What happened.** The restarted run (D1) began at about 20:31:50 PDT on
  2026-10-25. It stopped at 20:56:57 PDT, about 25 minutes in, during
  setting A. macOS power logs show the `caffeinate` wrapper's assertion ending
  ("ClientDied") in the same second the Claude desktop app released its own
  assertions, i.e. the app exited. The run was a child process of a Claude Code
  session inside that app, so it was terminated with it. There was no sleep, no
  crash report and no memory-pressure kill; the Mac's next reboot was at
  11:47 PDT on 2026-10-26.
- **Partial output.** None. Results are written only when a setting finishes,
  and setting A had not finished. `results/test/` stayed empty, and the
  session's temporary console output file no longer exists.
- **What was done.** The run is now started in its own process session
  (`os.setsid`) under `nohup` and `caffeinate -i`, with a log file under
  `logs/`, so it no longer depends on the app staying open. PROTOCOL.md is
  unchanged (same SHA-256), and the run starts again from the beginning.
- **Effect.** As in D1: nothing from the stopped run was saved or seen, and no
  choice depends on it.

## D3 — 2026-10-27: short CPU-only test suites during setting C42+R

- **What happened.** The completed run (all six settings, 15:11:53–21:47:48
  UTC on 2026-10-27) overlapped once with outside work. Another local project
  ran two CPU-only unit-test suites (tiny models, no GPU/MPS), about 20 s in
  total, at about 20:56:10–20:56:40 UTC, during setting C42+R. That project
  reported it; nothing else was reported during the run, and its later test
  suite (about 21:49 UTC) started after the run had exited.
- **Rows affected.** Using the per-row `started_utc` and `total_ms`, two
  C42+R rows overlap the window: claim 1379 (started 20:56:08.264Z, total
  26.6 s, 240 completion tokens) and claim 1382 (started 20:56:34.864Z,
  total 17.4 s, 157 completion tokens). No row of any other setting overlaps.
- **What was done.** Nothing was rerun or removed; the reported numbers use
  all 300 rows as the protocol specifies. As a sensitivity check, excluding
  the two rows changes C42+R total latency p50 from 14,580 ms to 14,515 ms
  and leaves p95 at 22,180 ms. Claim 1379's longer time is consistent with
  its longer answer (median completion in C42+R: 97.5 tokens).
- **Effect.** Answers, citations and retrieval metrics do not depend on
  machine load (deterministic retrieval; generator at temperature 0, seed 0).
  The latency effect is at most 65 ms at p50 and none at p95.
