"""Claude API client for the judge, with a cumulative cost ledger and a hard budget cap.

Every call's token usage and cost are appended to a JSONL ledger. Before each
call, the ledger total plus the call's worst-case cost (estimated input tokens
plus max_tokens of output) must stay within the budget, or the call is refused.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from .generation import LLMResult

# USD per million tokens, Anthropic first-party API (from the claude-api skill's model table, cached 2026-10-06).
# Claude Haiku 5.5 prices apply to prompts up to 100K tokens; this client refuses longer prompts.
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.00, 10.00)}
MAX_PROMPT_TOKENS = 100_000
CHARS_PER_TOKEN_LOW = 2.5  # pessimistic, for the pre-call worst-case estimate only


class BudgetExceeded(RuntimeError):
    pass


def strict_schema(schema):
    """Structured outputs need additionalProperties: false on objects; array length limits are checked locally."""
    if isinstance(schema, dict):
        out = {k: strict_schema(v) for k, v in schema.items() if k not in ("minItems", "maxItems")}
        if out.get("type") == "object":
            out["additionalProperties"] = False
        return out
    if isinstance(schema, list):
        return [strict_schema(x) for x in schema]
    return schema


class ClaudeClient:
    def __init__(self, model="claude-haiku-5-5", budget_usd=5.0, ledger_path="results/api_cost_ledger.jsonl",
                 effort="high", max_tokens=16000, client=None, label=""):
        if model not in PRICES:
            raise ValueError(f"No price configured for {model}")
        self.model = model
        self.budget_usd = budget_usd
        self.ledger_path = Path(ledger_path)
        self.effort = effort
        self.max_tokens = max_tokens
        self.label = label
        if client is None:
            import anthropic

            client = anthropic.Anthropic()
        self.client = client

    def spent_usd(self):
        if not self.ledger_path.exists():
            return 0.0
        with self.ledger_path.open(encoding="utf-8") as f:
            return sum(json.loads(line)["cost_usd"] for line in f if line.strip())

    def cost(self, input_tokens, output_tokens):
        p_in, p_out = PRICES[self.model]
        return (input_tokens * p_in + output_tokens * p_out) / 1e6

    def chat(self, messages, schema=None):
        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        turns = [m for m in messages if m["role"] != "system"]
        est_in = sum(len(m["content"]) for m in messages) / CHARS_PER_TOKEN_LOW
        if est_in > MAX_PROMPT_TOKENS:
            raise ValueError("Prompt too long for the configured price tier")
        spent = self.spent_usd()
        worst = self.cost(est_in, self.max_tokens)
        if spent + worst > self.budget_usd:
            raise BudgetExceeded(f"Spent ${spent:.4f}; next call could cost up to ${worst:.4f}; "
                                 f"budget ${self.budget_usd:.2f}")

        kwargs = {"model": self.model, "max_tokens": self.max_tokens, "messages": turns,
                  "thinking": {"type": "adaptive"}, "output_config": {"effort": self.effort}}
        if system:
            kwargs["system"] = system
        if schema is not None:
            kwargs["output_config"]["format"] = {"type": "json_schema", "schema": strict_schema(schema)}
        start = time.perf_counter()
        response = self.client.messages.create(**kwargs)
        seconds = time.perf_counter() - start

        usage = response.usage
        cost = self.cost(usage.input_tokens, usage.output_tokens)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "label": self.label,
                                "model": self.model, "effort": self.effort, "input_tokens": usage.input_tokens,
                                "output_tokens": usage.output_tokens, "cost_usd": cost,
                                "stop_reason": response.stop_reason, "seconds": seconds}) + "\n")
        if response.stop_reason in ("refusal", "max_tokens"):
            raise RuntimeError(f"Claude stopped with {response.stop_reason}")
        text = next(b.text for b in response.content if b.type == "text")
        return LLMResult(content=text, prompt_tokens=usage.input_tokens, completion_tokens=usage.output_tokens,
                         model=self.model, extra={"cost_usd": cost, "seconds": seconds})
