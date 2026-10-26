"""Compare the LLM judge with the human labels in calibration/labels_<version>.csv.

Run only after every item has a human label.

    .venv/bin/python scripts/judge_calibration.py --answers results/dev/ask_validation_v2.json \
        --labels calibration/labels_v2.csv --judge-llm gemma3:12b
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scifact_rag.data import load_corpus  # noqa: E402
from scifact_rag.generation import OllamaClient, parse_answer  # noqa: E402
from scifact_rag.judge import JUDGE_VERSION, Judge, agreement  # noqa: E402

YES, NO = {"yes", "y", "true", "1"}, {"no", "n", "false", "0"}


def human_bool(value, item_id):
    v = value.strip().lower()
    if v in YES:
        return True
    if v in NO:
        return False
    raise SystemExit(f"{item_id}: human_label must be yes/no, got {value!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--judge-llm", default="gemma3:12b")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    report = json.loads(args.answers.read_text(encoding="utf-8"))
    rows = {(model, r["query_id"]): r for model, b in report["models"].items() for r in b["rows"]}
    with args.labels.open(newline="", encoding="utf-8-sig") as f:
        text = f.read()
    # Spreadsheet apps may re-save the file tab-separated; accept either.
    dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=",\t")
    labels = list(csv.DictReader(text.splitlines(), dialect=dialect))
    missing = [lab["item_id"] for lab in labels if not (lab.get("human_label") or "").strip()]
    if missing:
        raise SystemExit(f"{len(missing)}/{len(labels)} items have no human_label: {', '.join(missing)}")
    corpus = load_corpus()
    passages = {d: (d, t, a) for d, t, a in zip(corpus.doc_ids, corpus.titles, corpus.abstracts)}
    judge = Judge(OllamaClient(model=args.judge_llm))

    items, pairs = [], {"faithfulness": [], "abstention": []}
    for lab in labels:
        human = human_bool(lab["human_label"], lab["item_id"])
        r = rows[(lab["retriever"], lab["query_id"])]
        if lab["kind"] == "faithfulness":
            cited = parse_answer(r["answer"], r["retrieved"]).citations
            out = judge.faithfulness(r["claim"], r["answer"], [passages[d] for d in cited])
            judged = out["faithful"]
        else:
            out = judge.abstention(r["claim"], [passages[d] for d in r["retrieved"]])
            judged = out["justified"]
        pairs[lab["kind"]].append((human, judged))
        items.append({**lab, "human": human, "judge": judged, "judge_detail": out})
        print(f"{lab['item_id']} {lab['kind']:12s} human={human!s:5s} judge={judged!s:5s}", flush=True)

    summary = {"judge_llm": args.judge_llm, "judge_version": JUDGE_VERSION, "split": "validation",
               "faithfulness": agreement(pairs["faithfulness"]) if pairs["faithfulness"] else None,
               "abstention": agreement(pairs["abstention"]) if pairs["abstention"] else None,
               "items": items}
    output = args.output or args.labels.with_name(f"agreement_{args.labels.stem}_{JUDGE_VERSION}.json")
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for kind in ("faithfulness", "abstention"):
        a = summary[kind]
        if a:
            kappa = "n/a" if a["cohen_kappa"] is None else f"{a['cohen_kappa']:.2f}"
            print(f"{kind}: agree {a['agree']}/{a['pairs']}, kappa {kappa}")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
