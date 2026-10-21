"""Choose the reranker candidate depth on VALIDATION claims (never the official test set).

Reports validation nDCG@10 / Recall@10 for each retriever with and without the
cross-encoder reranker at several candidate depths.

    .venv/bin/python scripts/dev_rerank.py
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scifact_rag.data import load_corpus, load_validation  # noqa: E402
from scifact_rag.index import FaissIndex  # noqa: E402
from scifact_rag.metrics import evaluate  # noqa: E402
from scifact_rag.models import Encoder, model_labels  # noqa: E402
from scifact_rag.rerank import RERANKER_MODEL, CrossEncoderScorer, RerankingRetriever  # noqa: E402
from scifact_rag.service import Retriever  # noqa: E402


def run(retriever, query_ids, claims, qrels):
    start = time.perf_counter()
    result = {q: [h.doc_id for h in retriever.search(c, k=10)[0]] for q, c in zip(query_ids, claims)}
    seconds = time.perf_counter() - start
    m = evaluate(qrels, result, k=10)
    return {"nDCG@10": m["nDCG@10"], "Recall@10": m["Recall@10"], "queries": m["queries"],
            "wall_seconds_all_queries": seconds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", default="20,50,100")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "dev" / "rerank_validation.json")
    args = parser.parse_args()

    corpus = load_corpus()
    titles = dict(zip(corpus.doc_ids, corpus.titles))
    abstracts = dict(zip(corpus.doc_ids, corpus.abstracts))
    query_ids, claims, qrels = load_validation()
    scorer = CrossEncoderScorer()
    depths = [int(x) for x in args.candidates.split(",")]

    report = {"split": "validation (development only)", "queries": len(query_ids), "reranker": RERANKER_MODEL,
              "note": "The fine-tuned models' learning rate was chosen on this split, so C rows are optimistic.",
              "rows": {}}
    for label in model_labels():
        base = Retriever(Encoder(label), FaissIndex.load(ROOT / "indexes" / label), titles)
        report["rows"][label] = run(base, query_ids, claims, qrels)
        for n in depths:
            rr = RerankingRetriever(base, scorer, abstracts, candidates=n)
            report["rows"][f"{label}+rerank@{n}"] = run(rr, query_ids, claims, qrels)
        for name, row in report["rows"].items():
            if name.startswith(label):
                print(f"{name:24s} nDCG@10={row['nDCG@10']:.4f} Recall@10={row['Recall@10']:.4f} "
                      f"({row['wall_seconds_all_queries']:.1f} s)", flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
