"""Score the human faithfulness labels (PROTOCOL.md). Commit labels.csv before running this.

    .venv/bin/python scripts/score_human_labels.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scifact_rag.human_eval import score  # noqa: E402

YES, NO = {"yes", "y"}, {"no", "n"}


def main():
    folder = ROOT / "human_eval"
    items = json.loads((folder / "KEY_do_not_open_until_labelled.json").read_text(encoding="utf-8"))
    text = (folder / "labels.csv").read_text(encoding="utf-8-sig").splitlines()
    dialect = csv.Sniffer().sniff(text[0], delimiters=",\t")
    labels = {}
    for row in csv.DictReader(text, dialect=dialect):
        v = row["human_label"].strip().lower()
        if v not in YES | NO:
            raise SystemExit(f"{row['sheet_id']}: human_label must be yes/no, got {row['human_label']!r}")
        labels[row["sheet_id"]] = v in YES
    result = score(items, labels)
    (ROOT / "results" / "test" / "human_faithfulness.json").write_text(json.dumps(result, indent=2) + "\n",
                                                                      encoding="utf-8")
    for s, r in result["per_setting"].items():
        f, a = r["faithful"], r["justified_abstentions"]
        ci = f"[{f['wilson95'][0]:.2f}, {f['wilson95'][1]:.2f}]" if f["wilson95"] else "n/a"
        print(f"{s:6s} faithful {f['count']}/{f['of']} (95% {ci}); justified abstentions {a['count']}/{a['of']}")
    for k, v in result["paired"].items():
        print(k, {x: y for x, y in v.items() if x != "note"})
    print("self-agreement", result["self_agreement"])


if __name__ == "__main__":
    main()
