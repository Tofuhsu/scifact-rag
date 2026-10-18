"""Exact inner-product FAISS index over L2-normalized embeddings (= cosine)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

# Extra candidates fetched beyond k so exact score ties at the cutoff can be
# broken by ascending doc_id, matching the original experiment's ranking rule.
TIE_WINDOW = 16


class FaissIndex:
    def __init__(self, embeddings, doc_ids):
        import faiss

        embeddings = np.ascontiguousarray(embeddings, dtype=np.float32)
        if embeddings.ndim != 2 or embeddings.shape[0] != len(doc_ids):
            raise ValueError("Embeddings must be (len(doc_ids), dim)")
        if len(set(doc_ids)) != len(doc_ids):
            raise ValueError("Duplicate document IDs")
        norms = np.linalg.norm(embeddings, axis=1)
        if not np.allclose(norms, 1.0, rtol=0, atol=5e-4):
            raise ValueError("Cosine search requires L2-normalized embeddings")
        self.doc_ids = list(doc_ids)
        self.dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embeddings)

    def __len__(self):
        return len(self.doc_ids)

    def search(self, queries, k=10):
        """queries: (n, dim) or (dim,). Returns one [(doc_id, score), ...] list per query."""
        queries = np.ascontiguousarray(np.atleast_2d(queries), dtype=np.float32)
        if queries.shape[1] != self.dim:
            raise ValueError("Query dimension differs from the index")
        if not 1 <= k <= len(self.doc_ids):
            raise ValueError("k must be between 1 and the corpus size")
        fetch = min(len(self.doc_ids), k + TIE_WINDOW)
        scores, rows = self.index.search(queries, fetch)
        results = []
        for score_row, id_row in zip(scores, rows):
            hits = sorted(((self.doc_ids[i], float(s)) for i, s in zip(id_row, score_row) if i >= 0),
                          key=lambda hit: (-hit[1], hit[0]))
            results.append(hits[:k])
        return results

    def save(self, directory):
        import faiss

        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(directory / "index.faiss"))
        (directory / "doc_ids.json").write_text(json.dumps(self.doc_ids), encoding="utf-8")

    @classmethod
    def load(cls, directory):
        import faiss

        directory = Path(directory)
        obj = cls.__new__(cls)
        obj.index = faiss.read_index(str(directory / "index.faiss"))
        obj.doc_ids = json.loads((directory / "doc_ids.json").read_text(encoding="utf-8"))
        obj.dim = obj.index.d
        if obj.index.ntotal != len(obj.doc_ids):
            raise ValueError("Saved index and doc_ids differ in size")
        return obj
