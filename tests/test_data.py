import hashlib

import pytest

from scifact_rag.data import document_text, query_text, read_qrels_tsv, sha256_file


def test_text_policy_matches_original_experiment():
    assert document_text("  Title ", " Abstract body. ") == "Title\nAbstract body."
    assert document_text("", "Abstract only") == "Abstract only"
    assert query_text("  claim text \n") == "claim text"
    with pytest.raises(ValueError):
        query_text("   ")
    with pytest.raises(ValueError):
        document_text("Title", "  ")


def test_read_qrels_tsv(tmp_path):
    p = tmp_path / "q.tsv"
    p.write_text("query-id\tcorpus-id\tscore\n1\t10\t1\n1\t11\t1\n3\t12\t1\n")
    assert read_qrels_tsv(p) == {"1": {"10": 1, "11": 1}, "3": {"12": 1}}


@pytest.mark.parametrize("body", ["1\t10\t2\n", "1\t10\t1\n1\t10\t1\n"])
def test_read_qrels_rejects_graded_or_duplicate_rows(tmp_path, body):
    p = tmp_path / "q.tsv"
    p.write_text("query-id\tcorpus-id\tscore\n" + body)
    with pytest.raises(ValueError):
        read_qrels_tsv(p)


def test_sha256_file(tmp_path):
    p = tmp_path / "f"
    p.write_bytes(b"abc")
    assert sha256_file(p) == hashlib.sha256(b"abc").hexdigest()
