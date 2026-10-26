import json
from types import SimpleNamespace

import pytest

from scifact_rag.claude_client import BudgetExceeded, ClaudeClient, strict_schema
from scifact_rag.judge import ABSTENTION_SCHEMA, faithfulness_schema


class FakeMessages:
    def __init__(self, text='{"labels": ["SUPPORTED"]}', stop="end_turn", usage=(1000, 2000)):
        self.text, self.stop, self.usage, self.kwargs = text, stop, usage, None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=self.text)],
            stop_reason=self.stop, usage=SimpleNamespace(input_tokens=self.usage[0], output_tokens=self.usage[1]))


def make(tmp_path, budget=5.0, **fake):
    messages = FakeMessages(**fake)
    client = ClaudeClient(budget_usd=budget, ledger_path=tmp_path / "ledger.jsonl",
                          client=SimpleNamespace(messages=messages), label="test")
    return client, messages


MSGS = [{"role": "system", "content": "rules"}, {"role": "user", "content": "question"}]


def test_request_shape_and_ledger(tmp_path):
    client, fake = make(tmp_path)
    out = client.chat(MSGS, schema=faithfulness_schema(1))
    assert out.content == '{"labels": ["SUPPORTED"]}'
    kw = fake.kwargs
    assert kw["model"] == "claude-haiku-5-5" and kw["system"] == "rules"
    assert kw["messages"] == [{"role": "user", "content": "question"}]
    assert kw["thinking"] == {"type": "adaptive"} and kw["output_config"]["effort"] == "high"
    fmt = kw["output_config"]["format"]
    assert fmt["type"] == "json_schema" and fmt["schema"]["additionalProperties"] is False
    assert "temperature" not in kw
    # 1000 in * $0.10/M + 2000 out * $0.50/M
    assert out.extra["cost_usd"] == pytest.approx(0.0011)
    row = json.loads((tmp_path / "ledger.jsonl").read_text())
    assert row["cost_usd"] == pytest.approx(0.0011) and row["label"] == "test"
    assert client.spent_usd() == pytest.approx(0.0011)


def test_budget_includes_previous_runs_and_refuses_before_calling(tmp_path):
    (tmp_path / "ledger.jsonl").write_text(json.dumps({"cost_usd": 4.995}) + "\n")
    client, fake = make(tmp_path)
    with pytest.raises(BudgetExceeded):
        client.chat(MSGS)
    assert fake.kwargs is None


@pytest.mark.parametrize("stop", ["refusal", "max_tokens"])
def test_bad_stop_reasons_raise_but_are_still_billed(tmp_path, stop):
    client, _ = make(tmp_path, stop=stop)
    with pytest.raises(RuntimeError, match=stop):
        client.chat(MSGS)
    assert client.spent_usd() > 0


def test_strict_schema_adds_additional_properties_and_drops_length_limits():
    s = strict_schema(faithfulness_schema(3))
    assert s["additionalProperties"] is False and "minItems" not in s["properties"]["labels"]
    assert strict_schema(ABSTENTION_SCHEMA)["additionalProperties"] is False


def test_unknown_model_rejected(tmp_path):
    with pytest.raises(ValueError):
        ClaudeClient(model="claude-opus-5-5", ledger_path=tmp_path / "l", client=object())
