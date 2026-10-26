import pytest

from scifact_rag.human_eval import build_items, score, wilson

QIDS = [str(i) for i in range(100)]
SETTINGS = ("A", "C42", "C42+R")


def fake_results(abstain=()):
    return {s: {q: {"abstained": (s, q) in abstain} for q in QIDS} for s in SETTINGS}


def test_wilson_known_values():
    lo, hi = wilson(15, 20)
    assert lo == pytest.approx(0.5313, abs=1e-3) and hi == pytest.approx(0.8881, abs=1e-3)
    assert wilson(0, 0) is None
    assert wilson(0, 10)[0] == pytest.approx(0.0, abs=1e-12) and wilson(10, 10)[1] == pytest.approx(1.0, abs=1e-12)


def test_build_items_is_paired_blinded_and_deterministic():
    items = build_items(fake_results(), QIDS)
    assert items == build_items(fake_results(), QIDS)
    originals = [it for it in items if it["duplicate_of"] is None]
    assert len(originals) == 90 and len(items) == 100
    claims = {it["query_id"] for it in originals}
    assert len(claims) == 30
    for q in claims:  # every sampled claim appears once per setting
        assert sorted(it["setting"] for it in originals if it["query_id"] == q) == sorted(SETTINGS)
    assert [it["sheet_id"] for it in items] == [f"H{i:03d}" for i in range(1, 101)]
    assert all("A" not in it["sheet_id"] and "C" not in it["sheet_id"] for it in items)
    first_half = {it["sheet_id"] for it in items[:45]}
    assert not any(it["duplicate_of"] is not None and it["sheet_id"] in first_half for it in items)


def test_kind_follows_abstention():
    items = build_items(fake_results(abstain={("A", q) for q in QIDS}), QIDS)
    assert all(it["kind"] == ("abstention" if it["setting"] == "A" else "faithfulness") for it in items)


def test_score_counts_wilson_pairs_and_self_agreement():
    items = build_items(fake_results(), QIDS)
    labels = {}
    for it in items:
        labels[it["sheet_id"]] = it["setting"] != "A"  # A always "no", others "yes"
    dup = next(it for it in items if it["duplicate_of"] is not None)
    labels[dup["sheet_id"]] = not labels[dup["sheet_id"]]  # one inconsistent duplicate
    out = score(items, labels)
    assert out["per_setting"]["A"]["faithful"] == {"count": 0, "of": 30, "wilson95": wilson(0, 30)}
    assert out["per_setting"]["C42"]["faithful"]["count"] == 30
    assert out["paired"]["C42 vs A"]["only_C42_good"] == 30 and out["paired"]["C42 vs A"]["only_A_good"] == 0
    assert out["paired"]["C42+R vs C42"]["only_C42+R_good"] == 0
    assert out["self_agreement"] == {"same": 9, "of": 10}


def test_score_rejects_missing_labels():
    items = build_items(fake_results(), QIDS)
    with pytest.raises(ValueError):
        score(items, {})
