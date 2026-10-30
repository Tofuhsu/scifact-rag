import pytest
from fastapi.testclient import TestClient

from scifact_rag import api
from scifact_rag.api import create_app
from scifact_rag.security import KeyChecker, RateLimiter, load_api_keys, parse_api_keys, parse_rate_limit

QUERY = {"query": "statin therapy cholesterol", "k": 3}


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def secured(retriever, clock):
    app = create_app({"original": retriever}, "original", api_keys=["alpha-key", "beta-key"],
                     search_limit=(2, 60.0), clock=clock)
    return TestClient(app)


def test_parse_api_keys_ignores_blanks():
    assert parse_api_keys(" a, b ,\n c\n\n") == ["a", "b", "c"]


def test_load_api_keys_from_env_and_file(tmp_path):
    secret = tmp_path / "keys"
    secret.write_text("file-key\n", encoding="utf-8")
    assert load_api_keys({"SCIFACT_API_KEYS": "env-key", "SCIFACT_API_KEYS_FILE": str(secret)}) == [
        "env-key", "file-key"]
    assert load_api_keys({}) == []


@pytest.mark.parametrize("value,expected", [("60/minute", (60, 60.0)), ("5/s", (5, 1.0)), ("100/hour", (100, 3600.0)),
                                            ("off", None), ("", None)])
def test_parse_rate_limit(value, expected):
    assert parse_rate_limit(value) == expected


@pytest.mark.parametrize("value", ["60", "0/minute", "x/minute", "10/day"])
def test_parse_rate_limit_rejects_bad_values(value):
    with pytest.raises(ValueError):
        parse_rate_limit(value)


def test_key_checker():
    checker = KeyChecker(["alpha-key"])
    assert checker.client_id("alpha-key").startswith("key:")
    assert checker.client_id("alpha-keyx") is None
    assert checker.client_id("") is None
    assert checker.client_id(None) is None
    with pytest.raises(ValueError):
        KeyChecker([])


def test_token_bucket_refills_continuously(clock):
    limiter = RateLimiter(2, 10.0, clock=clock)  # one token every 5 s
    assert limiter.acquire("c") == 0.0
    assert limiter.acquire("c") == 0.0
    assert limiter.acquire("c") == pytest.approx(5.0)
    clock.now += 2.5
    assert limiter.acquire("c") == pytest.approx(2.5)
    clock.now += 2.5
    assert limiter.acquire("c") == 0.0
    assert limiter.acquire("other") == 0.0  # clients are independent


def test_token_bucket_caps_tracked_clients(clock):
    limiter = RateLimiter(1, 60.0, clock=clock, max_clients=3)
    for c in "abcd":
        limiter.acquire(c)
    assert len(limiter._buckets) <= 3


def test_health_needs_no_key(secured):
    assert secured.get("/health").status_code == 200


@pytest.mark.parametrize("headers", [{}, {"X-API-Key": "wrong"}, {"X-API-Key": ""}])
def test_search_rejects_missing_or_wrong_key(secured, headers):
    r = secured.post("/search", json=QUERY, headers=headers)
    assert r.status_code == 401
    assert r.headers["www-authenticate"] == "ApiKey"


def test_ask_requires_key_before_anything_else(secured):
    # No LLM is configured, but an unauthenticated caller must get 401, not 503.
    assert secured.post("/ask", json=QUERY).status_code == 401


def test_search_with_valid_key(secured):
    r = secured.post("/search", json=QUERY, headers={"X-API-Key": "beta-key"})
    assert r.status_code == 200
    assert r.json()["results"][0]["doc_id"] == "102"


def test_rate_limit_per_key_with_retry_after(secured, clock):
    alpha, beta = {"X-API-Key": "alpha-key"}, {"X-API-Key": "beta-key"}
    assert [secured.post("/search", json=QUERY, headers=alpha).status_code for _ in range(2)] == [200, 200]
    r = secured.post("/search", json=QUERY, headers=alpha)
    assert r.status_code == 429
    assert r.headers["retry-after"] == "30"
    assert secured.post("/search", json=QUERY, headers=beta).status_code == 200  # separate bucket
    clock.now += 30
    assert secured.post("/search", json=QUERY, headers=alpha).status_code == 200


def test_rejected_requests_do_not_use_tokens(secured):
    for _ in range(5):
        secured.post("/search", json=QUERY, headers={"X-API-Key": "wrong"})
    assert secured.post("/search", json=QUERY, headers={"X-API-Key": "alpha-key"}).status_code == 200


def test_rate_limit_by_ip_without_auth(retriever, clock):
    client = TestClient(create_app({"original": retriever}, "original", search_limit=(1, 60.0), clock=clock))
    assert client.post("/search", json=QUERY).status_code == 200
    assert client.post("/search", json=QUERY).status_code == 429


def test_search_and_ask_have_separate_limits(retriever, clock):
    client = TestClient(create_app({"original": retriever}, "original", api_keys=["k"], search_limit=(1, 60.0),
                                   ask_limit=(1, 60.0), clock=clock))
    h = {"X-API-Key": "k"}
    assert client.post("/search", json=QUERY, headers=h).status_code == 200
    assert client.post("/ask", json=QUERY, headers=h).status_code == 503  # passes the guard; no LLM here
    assert client.post("/ask", json=QUERY, headers=h).status_code == 429


def test_default_app_refuses_to_start_without_keys(monkeypatch):
    for name in ("SCIFACT_API_KEYS", "SCIFACT_API_KEYS_FILE", "SCIFACT_AUTH"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(RuntimeError, match="No API keys"):
        api.build_default_app()
