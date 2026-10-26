"""Run the frozen test protocol (PROTOCOL.md) once: six settings x 300 test claims.

Refuses to run unless --protocol-sha matches PROTOCOL.md exactly and the
working tree is clean, and refuses to overwrite results/test/.

    .venv/bin/python scripts/run_test_matrix.py --protocol-sha $(shasum -a 256 PROTOCOL.md | cut -d' ' -f1)
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scifact_rag.data import load_corpus, load_test, sha256_file  # noqa: E402
from scifact_rag.generation import PROMPT_VERSION, Answerer, OllamaClient  # noqa: E402
from scifact_rag.index import FaissIndex  # noqa: E402
from scifact_rag.metrics import evaluate  # noqa: E402
from scifact_rag.models import Encoder  # noqa: E402
from scifact_rag.rerank import CrossEncoderScorer, RerankingRetriever  # noqa: E402
from scifact_rag.service import Retriever  # noqa: E402

SETTINGS = {  # id -> (retriever label, rerank?)
    "A": ("original", False), "C13": ("C-seed13", False), "C42": ("C-seed42", False),
    "C2026": ("C-seed2026", False), "A+R": ("original", True), "C42+R": ("C-seed42", True),
}
K, RERANK_CANDIDATES, LLM = 5, 50, "qwen3:14b"


def nearest_rank(values, p):
    ordered = sorted(values)
    return ordered[max(0, -(-len(ordered) * p // 100) - 1)]


def summarize(rows, qrels):
    answered = [r for r in rows if not r["abstained"]]
    cited = [(r["query_id"], d) for r in answered for d in r["citations"]]
    stages = sorted({s for r in rows for s in r["timings"]})
    return {
        "claims": len(rows),
        "abstained": {"count": len(rows) - len(answered), "of": len(rows)},
        "citation_in_qrels": {"count": sum(d in qrels[q] for q, d in cited), "of": len(cited)},
        "answers_with_invalid_citations": {"count": sum(bool(r["invalid_citations"]) for r in answered),
                                           "of": len(answered)},
        "uncited_answers": {"count": sum(r["uncited"] for r in answered), "of": len(answered)},
        "latency_ms": {s: {"p50": nearest_rank([r["timings"][s] for r in rows], 50),
                           "p95": nearest_rank([r["timings"][s] for r in rows], 95)} for s in stages},
        "tokens_mean": {"prompt": sum(r["prompt_tokens"] for r in rows) / len(rows),
                        "completion": sum(r["completion_tokens"] for r in rows) / len(rows)},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol-sha", required=True)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "results" / "test")
    parser.add_argument("--settings", default=",".join(SETTINGS), help="for resuming after a crash only")
    args = parser.parse_args()

    actual = sha256_file(ROOT / "PROTOCOL.md")
    if args.protocol_sha != actual:
        raise SystemExit(f"PROTOCOL.md sha256 is {actual}, not the approved {args.protocol_sha}")
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
    if dirty.strip():
        raise SystemExit("Working tree is not clean; commit first so the run maps to one commit")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    corpus = load_corpus()
    titles = dict(zip(corpus.doc_ids, corpus.titles))
    abstracts = dict(zip(corpus.doc_ids, corpus.abstracts))
    query_ids, claims, qrels = load_test()
    llm = OllamaClient(model=LLM)
    scorer = None
    encoders = {}

    for setting in [s.strip() for s in args.settings.split(",")]:
        path = args.out_dir / f"{setting}.json"
        if path.exists():
            raise SystemExit(f"{path} exists; the test run is not repeated")
        label, rerank = SETTINGS[setting]
        encoders.setdefault(label, Encoder(label))
        retriever = Retriever(encoders[label], FaissIndex.load(ROOT / "indexes" / label), titles)
        if rerank:
            scorer = scorer or CrossEncoderScorer()
            retriever = RerankingRetriever(retriever, scorer, abstracts, candidates=RERANK_CANDIDATES)

        # Retrieval metrics at k=10 for this retriever, before generation.
        run10 = {q: [h.doc_id for h in retriever.search(c, k=10)[0]] for q, c in zip(query_ids, claims)}
        retrieval = evaluate(qrels, run10, k=10)

        answerer = Answerer(retriever, llm, abstracts, PROMPT_VERSION)
        answerer.ask(claims[0], k=K)  # warm-up, discarded
        rows = []
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for q, c in zip(query_ids, claims):
            t0 = time.perf_counter()
            out = answerer.ask(c, k=K)
            total_ms = 1000 * (time.perf_counter() - t0)
            p = out["parsed"]
            rows.append({"query_id": q, "claim": c, "answer": p.text, "abstained": p.abstained,
                         "citations": p.citations, "invalid_citations": p.invalid_citations, "uncited": p.uncited,
                         "retrieved": [h.doc_id for h in out["hits"]], "relevant": sorted(qrels[q]),
                         "timings": dict(out["timings"], total_ms=total_ms),
                         "prompt_tokens": out["llm"].prompt_tokens, "completion_tokens": out["llm"].completion_tokens})
        report = {"setting": setting, "retriever": label, "rerank_top": RERANK_CANDIDATES if rerank else None,
                  "k": K, "llm": LLM, "prompt_version": PROMPT_VERSION, "protocol_sha256": actual,
                  "commit": commit, "started_utc": started,
                  "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "machine": f"{platform.machine()} {platform.platform()}",
                  "retrieval": {"nDCG@10": retrieval["nDCG@10"], "Recall@10": retrieval["Recall@10"],
                                "queries": retrieval["queries"]},
                  "summary": summarize(rows, qrels), "rows": rows}
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        s = report["summary"]
        print(f"{setting:6s} nDCG@10={retrieval['nDCG@10']:.4f} abstained {s['abstained']['count']}/300 "
              f"cited-in-qrels {s['citation_in_qrels']['count']}/{s['citation_in_qrels']['of']} "
              f"total p50 {s['latency_ms']['total_ms']['p50']:.0f} ms", flush=True)


if __name__ == "__main__":
    main()
