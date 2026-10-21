"""Build the human calibration sheet for the LLM judge from VALIDATION answers.

Writes calibration/sheet_<version>.md (what to read) and
calibration/labels_<version>.csv (what to fill in). Label each item with the
rules in JUDGE_RUBRIC.md BEFORE running scripts/judge_calibration.py.

    .venv/bin/python scripts/make_calibration_sheet.py --answers results/dev/ask_validation_v2.json
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scifact_rag.data import load_corpus  # noqa: E402
from scifact_rag.generation import parse_answer  # noqa: E402
from scifact_rag.judge import split_sentences  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--answered", type=int, default=20)
    parser.add_argument("--abstained", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "calibration")
    args = parser.parse_args()

    report = json.loads(args.answers.read_text(encoding="utf-8"))
    if not report["split"].startswith("validation"):
        raise SystemExit("Calibration items must come from validation answers")
    corpus = load_corpus()
    titles = dict(zip(corpus.doc_ids, corpus.titles))
    abstracts = dict(zip(corpus.doc_ids, corpus.abstracts))

    answered, abstained = [], []
    for model, block in report["models"].items():
        for row in block["rows"]:
            parsed = parse_answer(row["answer"], row["retrieved"])  # current parser rules
            item = dict(row, model=model, parsed_citations=parsed.citations)
            (abstained if parsed.abstained else answered).append(item)
    rng = random.Random(args.seed)
    picked = ([("faithfulness", r) for r in rng.sample(answered, min(args.answered, len(answered)))]
              + [("abstention", r) for r in rng.sample(abstained, min(args.abstained, len(abstained)))])
    rng.shuffle(picked)

    version = report["prompt_version"]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    lines = [f"# Judge calibration sheet ({version}, validation claims)", "",
             "Label every item in `labels_" + version + ".csv` using JUDGE_RUBRIC.md. "
             "Use only the abstracts shown here, not your own knowledge.", ""]
    rows = []
    for n, (kind, r) in enumerate(picked, 1):
        item_id = f"{version}-{n:02d}"
        lines += [f"## {item_id} — {kind}", "", f"**Claim:** {r['claim']}", ""]
        if kind == "faithfulness":
            lines += ["**Answer sentences:**", ""]
            lines += [f"{i}. {s}" for i, s in enumerate(split_sentences(r["answer"]), 1)]
            lines += ["", "**Cited abstracts:**", ""]
            shown = r["parsed_citations"]
            question = "faithful? (yes = every sentence SUPPORTED)"
        else:
            lines += [f"**Answer:** {r['answer']}", "", "**All retrieved abstracts:**", ""]
            shown = r["retrieved"]
            question = "justified? (yes = no abstract reports anything about the claim)"
        for d in shown:
            lines += [f"> **[{d}] {titles[d]}**", ">", f"> {abstracts[d].strip()}", ""]
        lines += [f"*Question: {question}*", ""]
        rows.append({"item_id": item_id, "kind": kind, "query_id": r["query_id"], "retriever": r["model"],
                     "human_label": "", "sentence_labels": "", "notes": ""})
    (args.out_dir / f"sheet_{version}.md").write_text("\n".join(lines), encoding="utf-8")
    path = args.out_dir / f"labels_{version}.csv"
    if path.exists():
        raise SystemExit(f"{path} exists; refusing to overwrite labels")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} items ({sum(k == 'faithfulness' for k, _ in picked)} answers, "
          f"{sum(k == 'abstention' for k, _ in picked)} abstentions) -> {args.out_dir}")


if __name__ == "__main__":
    main()
