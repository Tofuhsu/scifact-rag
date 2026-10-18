import hashlib
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scifact_rag  # noqa: E402,F401  (sets OpenMP env before faiss loads)
from scifact_rag.index import FaissIndex  # noqa: E402
from scifact_rag.service import Retriever  # noqa: E402

DIM = 64


class HashEncoder:
    """Deterministic bag-of-words encoder: no model download, fast, normalized float32."""

    def encode(self, texts):
        out = np.zeros((len(texts), DIM), dtype=np.float32)
        for row, text in enumerate(texts):
            for token in text.lower().split():
                out[row, int(hashlib.md5(token.encode()).hexdigest(), 16) % DIM] += 1.0
        out[:, -1] += 1e-3  # keep every vector nonzero
        return out / np.linalg.norm(out, axis=1, keepdims=True)


DOCS = {
    "101": ("Vitamin D", "vitamin d supplementation reduces fracture risk in elderly adults"),
    "102": ("Statins", "statin therapy lowers ldl cholesterol and cardiovascular events"),
    "103": ("Malaria", "artemisinin resistance in plasmodium falciparum malaria parasites"),
    "104": ("Sleep", "short sleep duration is associated with obesity in children"),
    "105": ("Aspirin", "low dose aspirin and colorectal cancer prevention"),
}


@pytest.fixture
def retriever():
    ids = sorted(DOCS)
    enc = HashEncoder()
    index = FaissIndex(enc.encode([f"{DOCS[d][0]}\n{DOCS[d][1]}" for d in ids]), ids)
    return Retriever(enc, index, {d: DOCS[d][0] for d in ids})
