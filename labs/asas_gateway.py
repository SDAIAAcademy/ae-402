"""The Asas gateway: a small, in-process AI gateway for the AE-402 labs.

It does what a gateway product does (LiteLLM and agentgateway are examples), in about 150 lines a
participant can read: one door for every model call, with keys per team, rate limits and budgets,
model aliases from the catalogue, fallback, tool mediation and an audit log that keeps no prompt
text. Policies are plain functions run before routing; the supplied gateway has none that looks at
classification. Lab 3.2 adds it.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

import asas as A

NATIONAL_ID = re.compile(r"\b[12]\d{9}\b")      # the ten-digit identity number format
SECRET_MARK = re.compile(r"\[SECRET\]|tender \d+", re.I)


def detect_level(text: str) -> str:
    """A deliberately simple content check: what the text shows, not what it is labelled."""
    if SECRET_MARK.search(text):
        return "Secret"
    if NATIONAL_ID.search(text):
        return "Restricted"
    return "Public"


@dataclass
class Response:
    status: int
    reason: str = ""
    model: str = ""
    text: str = ""
    cost_sar: float = 0.0


@dataclass
class Gateway:
    catalogue: dict                     # alias -> {"model", "hosting", "fallbacks": [...], ...}
    keys: dict                          # key id -> {"team", "max_level", "rpm", "budget_sar", "tools"}
    models: dict                        # model id -> object with .complete(messages) and .hosting
    price_card: dict = field(default_factory=dict)   # model id -> {"in": SAR/M, "out": SAR/M}
    policies: list = field(default_factory=list)     # functions ctx -> None or (status, reason)
    audit: list = field(default_factory=list)
    spent: dict = field(default_factory=dict)
    minute_calls: dict = field(default_factory=dict)
    minute: int = 0

    def _log(self, key, team, alias, model, level, status, reason, tin=0, tout=0, cost=0.0, text=""):
        self.audit.append({"seq": len(self.audit) + 1, "minute": self.minute, "key": key, "team": team,
                           "alias": alias, "model": model, "level": level, "status": status, "reason": reason,
                           "in_tokens": tin, "out_tokens": tout, "cost_sar": round(cost, 6),
                           "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]})

    def handle(self, key: str, request: dict) -> Response:
        """request: {"model": alias, "messages": [...], "classification": level or None, "tools": [...]}"""
        text = " ".join(m.get("content", "") for m in request.get("messages", []))
        alias = request.get("model", "")
        k = self.keys.get(key)
        if k is None:
            self._log(key, "", alias, "", "", 401, "unknown key", text=text)
            return Response(401, "unknown key")
        team = k["team"]
        entry = self.catalogue.get(alias)
        if entry is None:
            self._log(key, team, alias, "", "", 404, "model not in the catalogue", text=text)
            return Response(404, "model not in the catalogue")
        calls = self.minute_calls.get((key, self.minute), 0)
        if calls >= k.get("rpm", 10**9):
            self._log(key, team, alias, "", "", 429, "rate limit", text=text)
            return Response(429, "rate limit")
        if self.spent.get(key, 0.0) >= k.get("budget_sar", float("inf")):
            self._log(key, team, alias, "", "", 402, "budget exhausted", text=text)
            return Response(402, "budget exhausted")
        self.minute_calls[(key, self.minute)] = calls + 1

        ctx = {"key": key, "key_info": k, "team": team, "alias": alias, "entry": entry, "request": request,
               "text": text, "level": request.get("classification")}
        for policy in self.policies:
            verdict = policy(ctx)
            if verdict:
                status, reason = verdict
                self._log(key, team, alias, entry["model"], ctx.get("level") or "", status, reason, text=text)
                return Response(status, reason)

        allowed_tools = set(k.get("tools", []))
        request = {**request, "tools": [t for t in request.get("tools", []) if t in allowed_tools]}

        for model_id in [entry["model"], *entry.get("fallbacks", [])]:
            if model_id != entry["model"]:
                fb = {**ctx, "entry": {**entry, "model": model_id, "hosting": self.models[model_id].hosting}}
                if any(p(fb) for p in self.policies):
                    continue  # a fallback must pass the same policies as the first choice
            try:
                out = self.models[model_id].complete(request["messages"])
            except ConnectionError:
                continue
            price = self.price_card.get(model_id, {"in": 0.0, "out": 0.0})
            cost = (out["in_tokens"] * price["in"] + out["out_tokens"] * price["out"]) / 1e6
            self.spent[key] = self.spent.get(key, 0.0) + cost
            self._log(key, team, alias, model_id, ctx.get("level") or "", 200, "ok", out["in_tokens"],
                      out["out_tokens"], cost, text)
            return Response(200, "ok", model_id, out["text"], cost)
        self._log(key, team, alias, entry["model"], ctx.get("level") or "", 503, "no model available", text=text)
        return Response(503, "no model available")


def default_models(fail_every_own: int = 0) -> dict:
    """Stand-ins for the catalogue's models (no download, no key)."""
    return {
        "ext-frontier-l": A.StandInModel("ext-frontier-l", "external", 1200),
        "ksa-general-m": A.StandInModel("ksa-general-m", "ksa_cloud", 1400),
        "own-open-s": A.StandInModel("own-open-s", "ministry", 1700, fail_every_own),
        "own-embed-m": A.StandInModel("own-embed-m", "ministry", 60),
    }


def default_keys(teams) -> dict:
    """One key per team from teams.csv rows, with the team's highest level and modest limits."""
    out = {}
    for t in teams:
        out[f"k-{t['team'].lower()}-a"] = {"team": t["team"], "max_level": t["max_level"], "rpm": 60,
                                           "budget_sar": 50.0, "tools": ["permits_status"]}
    return out
