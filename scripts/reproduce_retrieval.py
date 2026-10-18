"""Build FAISS indexes and recompute test nDCG@10 / Recall@10 for each model.

Compares against the values reported by the original fine-tuning experiment
(official-test-*/summary.json). No training or tuning happens here.

    .venv/bin/python scripts/reproduce_retrieval.py
"""
from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scifact_rag.data import load_corpus, load_test  # noqa: E402
from scifact_rag.index import FaissIndex  # noqa: E402
from scifact_rag.metrics import evaluate  # noqa: E402
from scifact_rag.models import Encoder, artifacts_dir, model_labels  # noqa: E402

# Full-precision values from the original experiment's official-test-*/summary.json.
REFERENCE = {
    "original": {"nDCG@10": 0.6450816521455776, "Recall@10": 0.7833333333333333},
    "C-seed13": {"nDCG@10": 0.67873377945951, "Recall@10": 0.8198888888888889},
    "C-seed42": {"nDCG@10": 0.6800859565516719, "Recall@10": 0.8148888888888889},
    "C-seed2026": {"nDCG@10": 0.6766480677972116, "Recall@10": 0.8115555555555556},
}
ORIGINAL_RUN_DIR = {"original": "official-test-A-original"} | {
    f"C-seed{s}": f"official-test-C-seed{s}" for s in (13, 42, 2026)}
TOLERANCE = 1e-3  # absolute; see README for why this is not exact equality


def compare_rankings(label, run):
    """Fraction of test queries whose top-10 doc IDs match the original run exactly (if available)."""
    path = artifacts_dir() / ORIGINAL_RUN_DIR[label] / "top10.json"
    if not path.exists():
        return None
    original = {qid: [hit["document_id"] for hit in hits] for qid, hits in json.loads(path.read_text()).items()}
    same_order = sum(original[q] == run[q] for q in run)
    same_set = sum(set(original[q]) == set(run[q]) for q in run)
    return {"queries": len(run), "identical_top10_order": same_order, "identical_top10_set": same_set}


def exact_numpy_top10(doc_emb, doc_ids, query_emb):
    """Reference ranking: full float32 dot products, ties broken by ascending doc_id."""
    keys = np.asarray(doc_ids)
    out = []
    for q in query_emb:
        scores = doc_emb @ q
        out.append([doc_ids[i] for i in np.lexsort((keys, -scores))[:10]])
    return out


def mean_std(values):
    return {"mean": statistics.fmean(values), "population_std": statistics.pstdev(values),
            "sample_std": statistics.stdev(values), "n_seeds": len(values)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index-dir", type=Path, default=ROOT / "indexes")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "retrieval_reproduction.json")
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    corpus = load_corpus()
    texts = corpus.texts()
    query_ids, claims, qrels = load_test()

    rows = {}
    for label in model_labels():
        encoder = Encoder(label, device=args.device)
        start = time.perf_counter()
        doc_emb = encoder.encode(texts)
        encoder.synchronize()
        corpus_seconds = time.perf_counter() - start
        index = FaissIndex(doc_emb, corpus.doc_ids)
        index.save(args.index_dir / label)

        query_emb = encoder.encode(claims)
        hits = index.search(query_emb, k=10)
        run = {qid: [did for did, _ in h] for qid, h in zip(query_ids, hits)}
        exact = exact_numpy_top10(doc_emb, corpus.doc_ids, query_emb)
        faiss_matches_exact = sum(run[q] == e for q, e in zip(query_ids, exact))
        metrics = evaluate(qrels, run, k=10)
        ref = REFERENCE[label]
        rows[label] = {
            "nDCG@10": metrics["nDCG@10"], "Recall@10": metrics["Recall@10"], "queries": metrics["queries"],
            "reference": ref,
            "abs_diff": {m: abs(metrics[m] - ref[m]) for m in ref},
            "within_tolerance": all(abs(metrics[m] - ref[m]) <= TOLERANCE for m in ref),
            "faiss_top10_identical_to_exact_numpy": f"{faiss_matches_exact}/{len(query_ids)}",
            "ranking_vs_original_run": compare_rankings(label, run),
            "corpus_encoding_seconds": corpus_seconds, "device": encoder.device,
        }
        print(f"{label:10s} nDCG@10={metrics['nDCG@10']:.4f} (ref {ref['nDCG@10']:.4f})  "
              f"Recall@10={metrics['Recall@10']:.4f} (ref {ref['Recall@10']:.4f})", flush=True)

    c_labels = [label for label in rows if label.startswith("C-")]
    summary = {
        "scope": "BEIR SciFact official test, 300 claims, 339 qrels, corpus 5183 docs; FAISS IndexFlatIP on "
                 "L2-normalized float32 embeddings; no training or tuning",
        "tolerance_abs": TOLERANCE,
        "models": rows,
        "C_aggregate": {m: mean_std([rows[label][m] for label in c_labels]) for m in ("nDCG@10", "Recall@10")},
        "C_reference_aggregate": {m: mean_std([REFERENCE[label][m] for label in c_labels])
                                  for m in ("nDCG@10", "Recall@10")},
        "all_within_tolerance": all(r["within_tolerance"] for r in rows.values()),
        "faiss_matches_exact_everywhere": all(
            r["faiss_top10_identical_to_exact_numpy"] == f"{r['queries']}/{r['queries']}" for r in rows.values()),
        "environment": {"python": platform.python_version(), "machine": platform.machine(),
                        "platform": platform.platform()},
    }
    import faiss
    import sentence_transformers
    import torch
    import transformers
    summary["environment"].update(torch=torch.__version__, transformers=transformers.__version__,
                                  sentence_transformers=sentence_transformers.__version__,
                                  faiss=faiss.__version__)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    agg = summary["C_aggregate"]
    print(f"C mean: nDCG@10={agg['nDCG@10']['mean']:.4f} ± {agg['nDCG@10']['population_std']:.4f}  "
          f"Recall@10={agg['Recall@10']['mean']:.4f} ± {agg['Recall@10']['population_std']:.4f} (population std)")
    ok = summary["all_within_tolerance"] and summary["faiss_matches_exact_everywhere"]
    print(f"within tolerance: {summary['all_within_tolerance']}; "
          f"FAISS == exact NumPy on every query: {summary['faiss_matches_exact_everywhere']}")
    print("REPRODUCED" if ok else "MISMATCH — investigate before continuing")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
