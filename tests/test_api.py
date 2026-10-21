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


from scifact_rag.generation import LLMResult, NOT_FOUND  # noqa: E402


class ScriptedLLM:
    def __init__(self, reply=None, error=None):
        self.reply, self.error = reply, error

    def chat(self, messages):
        if self.error:
            raise self.error
        return LLMResult(self.reply, prompt_tokens=100, completion_tokens=12, model="fake-llm")


def ask_client(retriever, llm):
    from tests.conftest import DOCS

    app = create_app({"original": retriever}, "original", llm=llm, abstracts={d: DOCS[d][1] for d in DOCS})
    return TestClient(app)


def test_ask_returns_answer_citations_timings_and_usage(retriever):
    c = ask_client(retriever, ScriptedLLM("Statins lower LDL [102]. Unrelated id [555]."))
    body = c.post("/ask", json={"query": "statin cholesterol", "k": 3}).json()
    assert body["answer"].startswith("Statins lower LDL")
    assert body["citations"] == [{"doc_id": "102", "title": "Statins"}]
    assert body["invalid_citations"] == ["555"]
    assert body["abstained"] is False and body["uncited"] is False
    assert len(body["retrieved"]) == 3
    assert set(body["timings"]) == {"embed_ms", "search_ms", "generate_ms", "total_ms"}
    assert body["usage"] == {"llm": "fake-llm", "prompt_tokens": 100, "completion_tokens": 12}
    assert body["prompt_version"] == "v2"


def test_ask_not_found_is_an_abstention(retriever):
    body = ask_client(retriever, ScriptedLLM(NOT_FOUND)).post("/ask", json={"query": "capital of France"}).json()
    assert body["abstained"] is True and body["citations"] == [] and body["answer"] == NOT_FOUND


def test_ask_llm_failure_is_502(retriever):
    r = ask_client(retriever, ScriptedLLM(error=ConnectionError("down"))).post("/ask", json={"query": "aspirin"})
    assert r.status_code == 502 and "ConnectionError" in r.json()["detail"]


def test_ask_without_llm_is_503(client):
    assert client.post("/ask", json={"query": "aspirin"}).status_code == 503


@pytest.mark.parametrize("payload", [{"query": " "}, {"query": "x", "k": 21}, {"query": "x", "k": 0}])
def test_ask_invalid_requests_are_422(retriever, payload):
    assert ask_client(retriever, ScriptedLLM("x [101].")).post("/ask", json=payload).status_code == 422


def test_ask_unknown_model_is_400(retriever):
    r = ask_client(retriever, ScriptedLLM("x")).post("/ask", json={"query": "x", "model": "nope"})
    assert r.status_code == 400
