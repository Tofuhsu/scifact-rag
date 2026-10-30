"""API-key authentication and per-client rate limiting for the HTTP service.

Both are in-process: keys come from the environment, and rate-limit state lives
in memory, so limits apply per server process (one uvicorn worker in the image).
"""
from __future__ import annotations

import hashlib
import hmac
import math
import os
import threading
import time
from pathlib import Path


def parse_api_keys(value):
    """Comma- or newline-separated keys; blanks ignored."""
    return [k.strip() for k in value.replace("\n", ",").split(",") if k.strip()]


def load_api_keys(environ=os.environ):
    """Keys from SCIFACT_API_KEYS, or from the file named by SCIFACT_API_KEYS_FILE (e.g. a Docker secret)."""
    keys = parse_api_keys(environ.get("SCIFACT_API_KEYS", ""))
    path = environ.get("SCIFACT_API_KEYS_FILE")
    if path:
        keys += parse_api_keys(Path(path).read_text(encoding="utf-8"))
    return keys


def parse_rate_limit(value):
    """'60/minute' -> (60, 60.0). Units: second, minute, hour. Empty or 'off' -> None."""
    value = (value or "").strip().lower()
    if value in ("", "off", "none"):
        return None
    count, _, unit = value.partition("/")
    seconds = {"second": 1.0, "s": 1.0, "minute": 60.0, "m": 60.0, "hour": 3600.0, "h": 3600.0}.get(unit.strip())
    if seconds is None or not count.strip().isdigit() or int(count) < 1:
        raise ValueError(f"Rate limit must look like '60/minute', got {value!r}")
    return int(count), seconds


class KeyChecker:
    """Constant-time comparison against stored key digests; returns a short client id for a valid key."""

    def __init__(self, keys):
        if not keys:
            raise ValueError("At least one API key is required")
        self._digests = {hashlib.sha256(k.encode()).hexdigest() for k in keys}

    def client_id(self, key):
        if not key:
            return None
        digest = hashlib.sha256(key.encode()).hexdigest()
        ok = False
        for stored in self._digests:  # compare against every key so timing does not reveal which matched
            ok |= hmac.compare_digest(digest, stored)
        return f"key:{digest[:12]}" if ok else None


class RateLimiter:
    """Token bucket per client: `requests` per `per_seconds`, refilled continuously, burst = `requests`."""

    def __init__(self, requests, per_seconds, clock=time.monotonic, max_clients=10_000):
        self.capacity = float(requests)
        self.rate = requests / per_seconds
        self.clock = clock
        self.max_clients = max_clients
        self._buckets = {}
        self._lock = threading.Lock()

    def acquire(self, client):
        """Returns 0.0 if the request is allowed, else seconds until one token is available."""
        now = self.clock()
        with self._lock:
            tokens, last = self._buckets.get(client, (self.capacity, now))
            tokens = min(self.capacity, tokens + (now - last) * self.rate)
            if tokens >= 1.0:
                self._store(client, tokens - 1.0, now)
                return 0.0
            self._store(client, tokens, now)
            return (1.0 - tokens) / self.rate

    def _store(self, client, tokens, now):
        if client not in self._buckets and len(self._buckets) >= self.max_clients:
            # Drop full buckets first; they carry no state worth keeping.
            for c, (t, last) in list(self._buckets.items()):
                if t + (now - last) * self.rate >= self.capacity:
                    del self._buckets[c]
            if len(self._buckets) >= self.max_clients:
                self._buckets.pop(next(iter(self._buckets)))
        self._buckets[client] = (tokens, now)


def retry_after_header(seconds):
    return str(max(1, math.ceil(seconds)))
