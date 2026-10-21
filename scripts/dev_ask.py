"""Development check of /ask behaviour on VALIDATION claims (never the official test set).

Runs the grounded generator on a seeded sample of validation claims for each
retriever, plus a few out-of-domain questions that should be answered with
NOT_FOUND. Reports citation format health, a provisional citation-correctness
signal and abstain behaviour. These are development numbers for prompt design,
not the week-3 evaluation results.

    .venv/bin/python scripts/dev_ask.py --sample 30
"""
from __future__ import annotations

import argparse
import json
import platform
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scifact_rag.data import load_corpus, load_validation  # noqa: E402
from scifact_rag.generation import PROMPT_VERSION, Answerer, OllamaClient  # noqa: E402
from scifact_rag.index import FaissIndex  # noqa: E402
from scifact_rag.models import Encoder  # noqa: E402
from scifact_rag.service import Retriever  # noqa: E402

# Questions the SciFact abstracts should not answer; the expected output is NOT_FOUND.
OUT_OF_DOMAIN = [
    "What is the capital of France?",
    "Who won the 2018 FIFA World Cup?",
    "How do I reverse a linked list in Python?",
    "What is the boiling point of ethanol at sea level?",
    "Which planet has the most moons?",
]


def nearest_rank(values, p):
    ordered = sorted(values)
    return ordered[max(0, -(-len(ordered) * p // 100) - 1)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=int, default=30)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--models", default="original,C-seed42")
    parser.add_argument("--llm", default="qwen3:14b")
    parser.add_argument("--prompt-version", default=PROMPT_VERSION)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    corpus = load_corpus()
    titles = dict(zip(corpus.doc_ids, corpus.titles))
    abstracts = dict(zip(corpus.doc_ids, corpus.abstracts))
    query_ids, claims, qrels = load_validation()
    picked = sorted(random.Random(args.seed).sample(range(len(query_ids)), args.sample))
    llm = OllamaClient(model=args.llm)
    llm.chat([{"role": "user", "content": "Reply with OK."}])  # load the model; excluded from timings

    report = {"split": "validation (development only)", "sample": args.sample, "sample_seed": args.seed,
              "k": args.k, "llm": args.llm, "prompt_version": args.prompt_version, "models": {},
              "machine": f"{platform.machine()} {platform.platform()}"}
    for label in [m.strip() for m in args.models.split(",")]:
        answerer = Answerer(Retriever(Encoder(label), FaissIndex.load(ROOT / "indexes" / label), titles),
                            llm, abstracts, args.prompt_version)
        rows = []
        for i in picked:
            out = answerer.ask(claims[i], k=args.k)
            p = out["parsed"]
            rows.append({"query_id": query_ids[i], "claim": claims[i], "answer": p.text, "abstained": p.abstained,
                         "citations": p.citations, "invalid_citations": p.invalid_citations, "uncited": p.uncited,
                         "retrieved": [h.doc_id for h in out["hits"]], "relevant": sorted(qrels[query_ids[i]]),
                         "timings": out["timings"], "prompt_tokens": out["llm"].prompt_tokens,
                         "completion_tokens": out["llm"].completion_tokens})
        ood = []
        for q in OUT_OF_DOMAIN:
            out = answerer.ask(q, k=args.k)
            ood.append({"question": q, "answer": out["parsed"].text, "abstained": out["parsed"].abstained})

        answered = [r for r in rows if not r["abstained"]]
        cited = [(r["query_id"], d) for r in answered for d in r["citations"]]
        correct = sum(d in qrels[q] for q, d in cited)
        relevant_retrieved = sum(bool(set(r["retrieved"]) & set(r["relevant"])) for r in rows)
        gen = [r["timings"]["generate_ms"] for r in rows]
        report["models"][label] = {
            "claims": len(rows),
            "abstained": f"{len(rows) - len(answered)}/{len(rows)}",
            "claims_with_a_relevant_doc_in_top_k": f"{relevant_retrieved}/{len(rows)}",
            "answers_with_invalid_citations": f"{sum(bool(r['invalid_citations']) for r in answered)}/{len(answered)}",
            "uncited_answers": f"{sum(r['uncited'] for r in answered)}/{len(answered)}",
            "cited_doc_in_qrels": f"{correct}/{len(cited)}",
            "cited_doc_in_qrels_fraction": correct / len(cited) if cited else None,
            "out_of_domain_abstained": f"{sum(o['abstained'] for o in ood)}/{len(ood)}",
            "generate_ms": {"p50": nearest_rank(gen, 50), "p95": nearest_rank(gen, 95),
                            "mean": statistics.fmean(gen), "samples": len(gen),
                            "note": "warm model, sequential single requests, one run; not the week-3 benchmark"},
            "rows": rows, "out_of_domain": ood,
        }
        s = report["models"][label]
        print(f"{label}: abstained {s['abstained']}, cited-in-qrels {s['cited_doc_in_qrels']}, "
              f"invalid {s['answers_with_invalid_citations']}, uncited {s['uncited_answers']}, "
              f"OOD abstained {s['out_of_domain_abstained']}, generate p50 {s['generate_ms']['p50']:.0f} ms",
              flush=True)

    output = args.output or ROOT / "results" / "dev" / f"ask_validation_{args.prompt_version}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    report["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
