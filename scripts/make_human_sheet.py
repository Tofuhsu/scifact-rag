"""Build the blinded human faithfulness sheet from the test run (PROTOCOL.md).

Writes human_eval/sheet.md, human_eval/labels.csv (to fill in) and
human_eval/KEY_do_not_open_until_labelled.json (setting of each item).

    .venv/bin/python scripts/make_human_sheet.py
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
from scifact_rag.human_eval import HUMAN_SETTINGS, build_items  # noqa: E402
from scifact_rag.judge import split_sentences  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results" / "test")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "human_eval")
    args = parser.parse_args()
    if args.out_dir.exists():
        raise SystemExit(f"{args.out_dir} exists; the sample is drawn once")

    results = {}
    for s in HUMAN_SETTINGS:
        report = json.loads((args.results_dir / f"{s}.json").read_text(encoding="utf-8"))
        results[s] = {r["query_id"]: r for r in report["rows"]}
    query_ids = sorted(results[HUMAN_SETTINGS[0]])
    items = build_items(results, query_ids)

    corpus = load_corpus()
    titles = dict(zip(corpus.doc_ids, corpus.titles))
    abstracts = dict(zip(corpus.doc_ids, corpus.abstracts))
    lines = ["# Human faithfulness sheet (test sample, blinded)", "",
             "Label each item in `labels.csv` (yes/no) using JUDGE_RUBRIC.md. Use only the abstracts shown. "
             "Do not open the KEY file until every item is labelled.", ""]
    for it in items:
        r = results[it["setting"]][it["query_id"]]
        lines += [f"## {it['sheet_id']} — {it['kind']}", "", f"**Claim:** {r['claim']}", ""]
        if it["kind"] == "faithfulness":
            lines += ["**Answer sentences:**", ""] + [f"{i}. {s}" for i, s in enumerate(split_sentences(r["answer"]), 1)]
            lines += ["", "**Cited abstracts:**", ""]
            shown, question = r["citations"], "faithful? (yes = every sentence SUPPORTED)"
        else:
            lines += [f"**Answer:** {r['answer']}", "", "**All retrieved abstracts:**", ""]
            shown, question = r["retrieved"], "justified? (yes = no abstract reports anything about the claim)"
        for d in shown:
            lines += [f"> **[{d}] {titles[d]}**", ">", f"> {abstracts[d].strip()}", ""]
        lines += [f"*Question: {question}*", ""]

    args.out_dir.mkdir(parents=True)
    (args.out_dir / "sheet.md").write_text("\n".join(lines), encoding="utf-8")
    with (args.out_dir / "labels.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sheet_id", "kind", "human_label", "notes"])
        w.writerows([it["sheet_id"], it["kind"], "", ""] for it in items)
    (args.out_dir / "KEY_do_not_open_until_labelled.json").write_text(json.dumps(items, indent=1) + "\n",
                                                                     encoding="utf-8")
    print(f"{len(items)} items -> {args.out_dir}")


if __name__ == "__main__":
    main()
