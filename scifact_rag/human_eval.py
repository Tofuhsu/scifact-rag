"""Blinded human faithfulness evaluation on a paired test sample (PROTOCOL.md)."""
from __future__ import annotations

import math
import random

SAMPLE_SEED = 2026
SAMPLE_CLAIMS = 30
HUMAN_SETTINGS = ("A", "C42", "C42+R")
DUPLICATES = 10


def wilson(k, n, z=1.959964):
    """Wilson score 95% interval for k successes out of n."""
    if n == 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def build_items(results, query_ids, seed=SAMPLE_SEED, n_claims=SAMPLE_CLAIMS, settings=HUMAN_SETTINGS,
                duplicates=DUPLICATES):
    """results: {setting: {query_id: row}}. Returns shuffled items; ids carry no setting information.

    Each item: {item_id, setting, query_id, kind, duplicate_of}. Duplicates are placed in the
    second half of the sheet so they are not next to their originals.
    """
    rng = random.Random(seed)
    claims = sorted(rng.sample(sorted(query_ids), n_claims))
    base = [{"setting": s, "query_id": q,
             "kind": "abstention" if results[s][q]["abstained"] else "faithfulness", "duplicate_of": None}
            for q in claims for s in settings]
    rng.shuffle(base)
    for i, item in enumerate(base, 1):
        item["item_id"] = f"T{i:03d}"
    dups = []
    for original in rng.sample(base, duplicates):
        dups.append(dict(original, duplicate_of=original["item_id"]))
    half = len(base) // 2
    tail = base[half:] + dups
    rng.shuffle(tail)
    items = base[:half] + tail
    for i, item in enumerate(items, 1):  # renumber so sheet order and ids agree
        item["sheet_id"] = f"H{i:03d}"
    return items


def score(items, labels):
    """items: from build_items (with sheet_id); labels: {sheet_id: bool}."""
    missing = [it["sheet_id"] for it in items if it["sheet_id"] not in labels]
    if missing:
        raise ValueError(f"{len(missing)} items unlabelled: {missing[:5]}")
    originals = [it for it in items if it["duplicate_of"] is None]
    by_item_id = {it["item_id"]: labels[it["sheet_id"]] for it in originals}
    out = {"per_setting": {}, "paired": {}, "self_agreement": None}
    for s in sorted({it["setting"] for it in originals}):
        f = [by_item_id[it["item_id"]] for it in originals if it["setting"] == s and it["kind"] == "faithfulness"]
        a = [by_item_id[it["item_id"]] for it in originals if it["setting"] == s and it["kind"] == "abstention"]
        out["per_setting"][s] = {
            "faithful": {"count": sum(f), "of": len(f), "wilson95": wilson(sum(f), len(f))},
            "justified_abstentions": {"count": sum(a), "of": len(a)},
        }
    # Good outcome = faithful answer or justified abstention (the human label is "yes" in both cases).
    good = {(it["setting"], it["query_id"]): by_item_id[it["item_id"]] for it in originals}
    claims = sorted({it["query_id"] for it in originals})
    for a, b in (("A", "C42"), ("C42", "C42+R")):
        if all((s, q) in good for s in (a, b) for q in claims):
            out["paired"][f"{b} vs {a}"] = {
                "claims": len(claims),
                f"only_{b}_good": sum(good[(b, q)] and not good[(a, q)] for q in claims),
                f"only_{a}_good": sum(good[(a, q)] and not good[(b, q)] for q in claims),
                "note": "good = faithful answer or justified abstention; descriptive only"}
    dups = [it for it in items if it["duplicate_of"] is not None]
    if dups:
        orig_sheet = {it["item_id"]: it["sheet_id"] for it in originals}
        same = sum(labels[d["sheet_id"]] == labels[orig_sheet[d["duplicate_of"]]] for d in dups)
        out["self_agreement"] = {"same": same, "of": len(dups)}
    return out
