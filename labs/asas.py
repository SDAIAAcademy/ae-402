"""Shared helpers for the AE-402 labs (Ministry of Municipal Services, the Asas platform).

Everything here runs on a laptop processor with the Python standard library and pandas.
No model is downloaded and no key is needed: model calls go to scripted stand-ins
(`StandInModel`), unless ASAS_UPSTREAM_URL points the gateway at a hosted model.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import sys
from pathlib import Path

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
REF = DATA / "reference"
ARTIFACTS = LABS / "artifacts"

QUICK = os.environ.get("ASAS_QUICK", "0") == "1"


def pick(full, quick):
    """The small value in quick mode (ASAS_QUICK=1), the full one otherwise."""
    return quick if QUICK else full


def reference(name: str):
    """A reference result written by prepare_data.py: the safety net when an exercise is not done."""
    return json.loads((REF / f"{name}.json").read_text(encoding="utf-8"))


def check(cond: bool, msg: str) -> None:
    """Print a self-check. A failed check stops the cell, so a wrong result never passes silently."""
    print(("✅ " if cond else "❌ ") + msg)
    if not cond:
        raise AssertionError(msg)


def lab_dir(name: str, reset: bool = False) -> Path:
    """A folder under labs/artifacts/ for one lab's outputs. Delete artifacts/ when you are done."""
    path = ARTIFACTS / name
    if reset and path.exists():
        def writable(func, p, _exc):
            os.chmod(p, stat.S_IWRITE)
            func(p)
        if sys.version_info >= (3, 12):
            shutil.rmtree(path, onexc=writable)
        else:  # pragma: no cover
            shutil.rmtree(path, onerror=writable)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_text(rel: str) -> str:
    return (DATA / rel).read_text(encoding="utf-8")


def read_json(rel: str):
    return json.loads(read_text(rel))


def read_csv(rel: str):
    import pandas as pd
    return pd.read_csv(DATA / rel, keep_default_na=False, na_values=[""])


# --------------------------------------------------------------------------------------
# Classification and placement: the Ministry's rule for the case
# --------------------------------------------------------------------------------------

LEVELS = ["Public", "Restricted", "Secret", "Top Secret"]

# Where data of each level may be processed, by the Ministry's placement rule (Asas policy P-01).
# This is the case's own rule, stricter than the minimum the national texts require.
HOSTING_ALLOWED = {
    "Public": {"ministry", "ksa_cloud", "external"},
    "Restricted": {"ministry", "ksa_cloud"},
    "Secret": {"ministry"},
    "Top Secret": set(),
}
HOSTINGS = ["ministry", "ksa_cloud", "external"]


def rank(level: str) -> int:
    return LEVELS.index(level)


def highest(levels) -> str:
    """The highest of several levels: a dataset that combines levels takes the highest one."""
    levels = [l for l in levels if l]
    return max(levels, key=rank) if levels else "Public"


def allowed(level: str, hosting: str) -> bool:
    return hosting in HOSTING_ALLOWED[level]


# --------------------------------------------------------------------------------------
# Stand-in models: deterministic, free, offline
# --------------------------------------------------------------------------------------

def tokens(text: str) -> int:
    """A rough token count (about four characters a token), the same on every machine."""
    return max(1, round(len(text) / 4))


class StandInModel:
    """A scripted stand-in for a hosted or Ministry-hosted model.

    It answers with a fixed, labelled text and counts tokens, so gateways, quotas, costs and
    audit logs can be exercised without a key. It is not a language model.
    """

    def __init__(self, name: str, hosting: str, latency_ms: int = 900, fail_every: int = 0):
        self.name, self.hosting, self.latency_ms, self.fail_every = name, hosting, latency_ms, fail_every
        self.calls = 0

    def complete(self, messages: list[dict]) -> dict:
        self.calls += 1
        if self.fail_every and self.calls % self.fail_every == 0:
            raise ConnectionError(f"{self.name} is busy (stand-in failure {self.calls})")
        prompt = " ".join(m.get("content", "") for m in messages)
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8]
        text = f"[{self.name} stand-in answer {digest}]"
        return {"model": self.name, "text": text, "in_tokens": tokens(prompt), "out_tokens": 60,
                "latency_ms": self.latency_ms}


def upstream_from_env():
    """An OpenAI-compatible hosted model, when ASAS_UPSTREAM_URL, _KEY and _MODEL are set.

    Optional: the labs never need it. Use a free model (for example one whose id ends in
    ':free' on OpenRouter). Returns None when the variables are not set.
    """
    url, key, model = (os.environ.get(f"ASAS_UPSTREAM_{k}") for k in ("URL", "KEY", "MODEL"))
    if not (url and key and model):
        return None

    class Hosted:
        name, hosting, latency_ms = model, "external", 0

        def complete(self, messages):
            import urllib.error
            import urllib.request
            body = json.dumps({"model": model, "messages": messages}).encode("utf-8")
            req = urllib.request.Request(url.rstrip("/") + "/chat/completions", data=body, headers={
                "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    out = json.loads(r.read().decode("utf-8"))
            except (urllib.error.URLError, TimeoutError, ValueError) as e:
                # The gateway treats ConnectionError as "this model failed": it tries the fallback, or answers 503.
                raise ConnectionError(f"{model} did not answer: {e}") from e
            usage = out.get("usage", {})
            return {"model": model, "text": out["choices"][0]["message"]["content"],
                    "in_tokens": usage.get("prompt_tokens", 0), "out_tokens": usage.get("completion_tokens", 0),
                    "latency_ms": 0}

    return Hosted()


def md_table(df) -> str:
    """A DataFrame as a Markdown table, without extra dependencies."""
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def sar(x: float) -> str:
    return f"SAR {x:,.0f}"
