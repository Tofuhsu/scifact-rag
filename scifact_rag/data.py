"""BEIR SciFact loading at pinned Hugging Face revisions, with checksum checks.

Text formatting follows the original fine-tuning experiment's text policy:
documents are ``title.strip() + "\\n" + abstract.strip()`` (title omitted when
empty) and queries are ``text.strip()``.
"""
from __future__ import annotations

import csv
import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

SCIFACT_REPO = "BeIR/scifact"
SCIFACT_REVISION = "b3b5335604bf5ee3c4447671af975ea25143d4f5"
QRELS_REPO = "BeIR/scifact-qrels"
QRELS_REVISION = "2938d17dc3b09882fdb8c12bbbe2e2dc0e75a029"

SHA256 = {
    "corpus/corpus-00000-of-00001.parquet": "243324b35f03d82bd6d98a5f575966876e86cad7ce16e5333a35b1b793dc4f45",
    "queries/queries-00000-of-00001.parquet": "1c37956c5dc8b810b60302323c24d1a9e79e26411ba8f5ad9d0888642e2a9034",
    "test.tsv": "0864bb985e0ca2367ba217977e72004d549054b2b06666ed9d4825ac7c21284c",
}
CORPUS_SIZE = 5183
TEST_QUERIES = 300
TEST_QREL_ROWS = 339


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def query_text(text):
    require(isinstance(text, str) and bool(text.strip()), "Query text must be a nonempty string")
    return text.strip()


def document_text(title, abstract):
    require(isinstance(title, str), "Document title must be a string")
    require(isinstance(abstract, str) and bool(abstract.strip()), "Abstract must be a nonempty string")
    return f"{title.strip()}\n{abstract.strip()}" if title.strip() else abstract.strip()


@dataclass(frozen=True)
class Corpus:
    doc_ids: list[str]
    titles: list[str]
    abstracts: list[str]

    def texts(self):
        return [document_text(t, a) for t, a in zip(self.titles, self.abstracts)]


def hf_cache_dir():
    """SCIFACT_HF_CACHE overrides the default Hugging Face cache location."""
    value = os.environ.get("SCIFACT_HF_CACHE")
    return Path(value).expanduser() if value else None


def _fetch(repo_id, revision, filename):
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(repo_id, filename, repo_type="dataset", revision=revision,
                           cache_dir=hf_cache_dir())
    require(sha256_file(path) == SHA256[filename], f"Checksum differs for {repo_id}/{filename}")
    return Path(path)


def load_corpus():
    import pyarrow.parquet as pq

    path = _fetch(SCIFACT_REPO, SCIFACT_REVISION, "corpus/corpus-00000-of-00001.parquet")
    rows = sorted(pq.read_table(path, columns=["_id", "title", "text"]).to_pylist(), key=lambda r: r["_id"])
    doc_ids = [r["_id"] for r in rows]
    require(len(doc_ids) == len(set(doc_ids)) == CORPUS_SIZE, "Corpus count or IDs differ")
    return Corpus(doc_ids, [r["title"] for r in rows], [r["text"] for r in rows])


def read_qrels_tsv(path):
    """Parse a BEIR qrels TSV (query-id, corpus-id, score) into {qid: {doc_id: 1}}."""
    qrels = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        require(header == ["query-id", "corpus-id", "score"], f"Unexpected qrels header {header}")
        for qid, did, score in reader:
            require(score == "1", "Only binary relevance labels are supported")
            require(did not in qrels.get(qid, {}), f"Duplicate qrel {qid}/{did}")
            qrels.setdefault(qid, {})[did] = 1
    return qrels


def load_test():
    """Return (query_ids, claims, qrels) for the 300-claim official test split."""
    import pyarrow.parquet as pq

    qrels = read_qrels_tsv(_fetch(QRELS_REPO, QRELS_REVISION, "test.tsv"))
    query_ids = sorted(qrels)
    require(len(query_ids) == TEST_QUERIES, "Test query count differs")
    require(sum(map(len, qrels.values())) == TEST_QREL_ROWS, "Test qrel row count differs")
    path = _fetch(SCIFACT_REPO, SCIFACT_REVISION, "queries/queries-00000-of-00001.parquet")
    rows = sorted(pq.read_table(path, columns=["_id", "text"], filters=[("_id", "in", query_ids)]).to_pylist(),
                  key=lambda r: r["_id"])
    require([r["_id"] for r in rows] == query_ids, "Query texts do not match the test qrels")
    return query_ids, [query_text(r["text"]) for r in rows], qrels
