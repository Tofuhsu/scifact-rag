"""Embedding model registry: the original MiniLM and the hard-negative (C) fine-tunes."""
from __future__ import annotations

import os
from pathlib import Path

BASE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BASE_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
SEEDS = (13, 42, 2026)
MAX_SEQ_LENGTH = 256
# PyTorch weights and config only; skips the ONNX/OpenVINO exports in the repo.
BASE_FILES = ["*.json", "model.safetensors", "vocab.txt", "README.md", "1_Pooling/*"]


def artifacts_dir():
    return Path(os.environ.get("SCIFACT_ARTIFACTS",
                               "~/scientific-retrieval/scientific-retrieval-artifacts")).expanduser()


def model_labels():
    return ["original"] + [f"C-seed{s}" for s in SEEDS]


def resolve_model(label):
    """Return a local path for a model label (downloading the base model if needed)."""
    if label == "original":
        from huggingface_hub import snapshot_download

        from .data import hf_cache_dir

        return Path(snapshot_download(BASE_MODEL, revision=BASE_REVISION, cache_dir=hf_cache_dir(),
                                      allow_patterns=BASE_FILES))
    if label.startswith("C-seed") and int(label.removeprefix("C-seed")) in SEEDS:
        path = artifacts_dir() / f"final-{label}" / "model"
        if not (path / "model.safetensors").exists():
            raise FileNotFoundError(f"Fine-tuned model not found: {path}")
        return path
    raise ValueError(f"Unknown model label: {label}")


def default_device():
    import torch

    return "mps" if torch.backends.mps.is_available() else "cpu"


class Encoder:
    """Thin wrapper so the API and tests depend on .encode(texts) only."""

    def __init__(self, label, device=None):
        import torch
        from sentence_transformers import SentenceTransformer

        self.label = label
        self.device = device or default_device()
        self.model = SentenceTransformer(str(resolve_model(label)), device=self.device, local_files_only=True,
                                         trust_remote_code=False, similarity_fn_name="cosine",
                                         model_kwargs={"attn_implementation": "eager"})
        self.model.float().eval()
        if self.model.max_seq_length != MAX_SEQ_LENGTH:
            raise ValueError("Model max sequence length differs from the original experiment")
        self._torch = torch

    def encode(self, texts, batch_size=32):
        return self.model.encode(list(texts), batch_size=batch_size, device=self.device, show_progress_bar=False,
                                 precision="float32", convert_to_numpy=True, normalize_embeddings=True)

    def synchronize(self):
        if self.device == "mps":
            self._torch.mps.synchronize()
