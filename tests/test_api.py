import pytest
from fastapi.testclient import TestClient

from scifact_rag.api import MAX_K, create_app


@pytest.fixture
def client(retriever):
    return TestClient(create_app({"original": retriever, "C-seed42": retriever}, "original"))


def test_health_lists_models(client):
    body = client.get("/health").json()
    assert body == {"status": "ok", "models": ["C-seed42", "original"], "default_model": "original"}


def test_search_returns_ranked_hits_with_titles(client):
    r = client.post("/search", json={"query": "statin therapy cholesterol", "k": 3})
    assert r.status_code == 200
    body = r.json()
    assert body["model"] == "original"
    assert [h["rank"] for h in body["results"]] == [1, 2, 3]
    assert body["results"][0]["doc_id"] == "102"
    assert body["results"][0]["title"] == "Statins"
    scores = [h["score"] for h in body["results"]]
    assert scores == sorted(scores, reverse=True)


def test_search_default_k_is_clamped_to_corpus_size(client):
    body = client.post("/search", json={"query": "malaria"}).json()
    assert len(body["results"]) == 5
    assert len({h["doc_id"] for h in body["results"]}) == 5


def test_search_reports_nonnegative_timings(client):
    t = client.post("/search", json={"query": "sleep obesity"}).json()["timings"]
    assert t["embed_ms"] >= 0 and t["search_ms"] >= 0
    assert t["total_ms"] >= t["embed_ms"] + t["search_ms"] - 1e-6


def test_search_can_select_model(client):
    assert client.post("/search", json={"query": "aspirin", "model": "C-seed42"}).json()["model"] == "C-seed42"


def test_unknown_model_is_400(client):
    r = client.post("/search", json={"query": "aspirin", "model": "B-seed42"})
    assert r.status_code == 400
    assert "Unknown model" in r.json()["detail"]


@pytest.mark.parametrize("payload", [
    {"query": ""},
    {"query": "   "},
    {"query": "x", "k": 0},
    {"query": "x", "k": MAX_K + 1},
    {"query": "x" * 2001},
    {"k": 3},
])
def test_invalid_requests_are_422(client, payload):
    assert client.post("/search", json=payload).status_code == 422


def test_create_app_rejects_unknown_default(retriever):
    with pytest.raises(ValueError):
        create_app({"original": retriever}, "C-seed42")
