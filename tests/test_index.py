import numpy as np
import pytest

from scifact_rag.index import FaissIndex


def normalized(rng, n, dim=16):
    x = rng.standard_normal((n, dim)).astype(np.float32)
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def test_matches_exact_numpy_ranking():
    rng = np.random.default_rng(0)
    docs, queries = normalized(rng, 500), normalized(rng, 20)
    ids = [f"d{i:04d}" for i in range(500)]
    index = FaissIndex(docs, ids)
    for q, hits in zip(queries, index.search(queries, k=10)):
        expected = [ids[i] for i in np.argsort(-(docs @ q), kind="stable")[:10]]
        assert [d for d, _ in hits] == expected


def test_exact_ties_break_by_ascending_doc_id():
    v = np.array([[1.0, 0.0]], dtype=np.float32)
    docs = np.repeat(v, 4, axis=0)
    index = FaissIndex(docs, ["c", "a", "d", "b"])
    assert [d for d, _ in index.search(v[0], k=3)[0]] == ["a", "b", "c"]


def test_save_and_load_round_trip(tmp_path):
    rng = np.random.default_rng(1)
    docs = normalized(rng, 50)
    ids = [str(i) for i in range(50)]
    index = FaissIndex(docs, ids)
    index.save(tmp_path / "idx")
    loaded = FaissIndex.load(tmp_path / "idx")
    assert loaded.doc_ids == ids
    assert loaded.search(docs[:3], k=5) == index.search(docs[:3], k=5)


def test_rejects_unnormalized_embeddings():
    with pytest.raises(ValueError, match="normalized"):
        FaissIndex(np.full((2, 4), 2.0, dtype=np.float32), ["a", "b"])


def test_rejects_duplicate_ids_and_bad_k():
    docs = np.eye(3, dtype=np.float32)
    with pytest.raises(ValueError, match="Duplicate"):
        FaissIndex(docs, ["a", "a", "b"])
    index = FaissIndex(docs, ["a", "b", "c"])
    with pytest.raises(ValueError):
        index.search(docs[0], k=4)
    with pytest.raises(ValueError):
        index.search(np.ones(5, dtype=np.float32), k=1)
