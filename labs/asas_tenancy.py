"""A minute-by-minute replay of one working hour on Asas, for Lab 3.3.

Nine teams share the Ministry-hosted model (a fixed number of requests a minute) and pay for hosted
models per token. Three incidents can be switched on: a leaked key, a noisy neighbour and a runaway
agent. A tenancy model decides who is served. Deterministic: same numbers on every run.
"""

from __future__ import annotations

from dataclasses import dataclass, field

TEAMS = ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09"]
MINUTES = 60
OWN_CAPACITY = 120                       # requests a minute the Ministry-hosted model serves
BASE_OWN = {"T01": 10, "T02": 4, "T03": 6, "T04": 2, "T05": 8, "T06": 12, "T07": 10, "T08": 14, "T09": 6}
BASE_PAID = {"T01": 20, "T02": 8, "T03": 6, "T04": 0, "T05": 15, "T06": 0, "T07": 0, "T08": 0, "T09": 6}
SAR_PER_PAID_REQUEST = 0.03

INCIDENTS = {
    "noisy_neighbour": {"team": "T08", "from": 10, "to": 25, "own_extra": 300, "paid_extra": 0, "cost_mult": 1},
    "leaked_key": {"team": "T05", "from": 30, "to": 45, "own_extra": 0, "paid_extra": 400, "cost_mult": 1},
    "runaway_agent": {"team": "T03", "from": 20, "to": 60, "own_extra": 0, "paid_extra": 90, "cost_mult": 6},
}


@dataclass
class Tenancy:
    """How Asas shares itself. The defaults are the pilot's: one shared key, nothing per team."""
    per_team_keys: bool = False
    own_share_cap: float | None = None         # most of the own model one team may take in a minute
    budget_per_key_sar: float | None = None    # per key, for the hour
    shared_budget_sar: float = 60.0            # the hour's budget when all teams share one key
    revoke_on_spike: bool = False              # revoke a key whose paid rate exceeds 5 times its baseline
    allocate: object = None                    # function(demand, capacity, cap) -> served per team


def proportional(demand: dict, capacity: int, cap=None) -> dict:
    total = sum(demand.values())
    if total <= capacity:
        return dict(demand)
    return {t: demand[t] * capacity / total for t in demand}


def run(tenancy: Tenancy, incident: str | None) -> dict:
    inc = INCIDENTS.get(incident) if incident else None
    served_own = {t: 0.0 for t in TEAMS}
    asked_own = {t: 0.0 for t in TEAMS}
    served_paid = {t: 0.0 for t in TEAMS}
    asked_paid = {t: 0.0 for t in TEAMS}
    spend = {t: 0.0 for t in TEAMS}
    revoked_at = None
    total_spend = 0.0
    for m in range(MINUTES):
        own = dict(BASE_OWN)
        paid = dict(BASE_PAID)
        mult = {t: 1 for t in TEAMS}
        if inc and inc["from"] <= m < inc["to"]:
            own[inc["team"]] += inc["own_extra"]
            paid[inc["team"]] += inc["paid_extra"]
            mult[inc["team"]] = inc["cost_mult"]
        alloc = tenancy.allocate or proportional
        got = alloc(own, OWN_CAPACITY, tenancy.own_share_cap) if tenancy.per_team_keys else proportional(own, OWN_CAPACITY)
        for t in TEAMS:
            asked_own[t] += own[t]
            served_own[t] += got[t]
            asked_paid[t] += paid[t]
            ok = paid[t]
            if tenancy.per_team_keys:
                if tenancy.revoke_on_spike and paid[t] > 5 * max(BASE_PAID[t], 1) and revoked_at is None:
                    revoked_at = m
                if revoked_at is not None and inc and t == inc["team"] and revoked_at <= m < revoked_at + 5:
                    ok = 0  # revoked; the team gets a new key five minutes later
                elif revoked_at is not None and inc and t == inc["team"] and m >= revoked_at + 5:
                    ok = BASE_PAID[t]  # new key: the leaked one stays dead
                if tenancy.budget_per_key_sar is not None:
                    room = max(0.0, tenancy.budget_per_key_sar - spend[t])
                    ok = min(ok, room / (SAR_PER_PAID_REQUEST * mult[t]))
            else:
                room = max(0.0, tenancy.shared_budget_sar - total_spend)
                ok = min(ok, room / (SAR_PER_PAID_REQUEST * mult[t]))
            cost = ok * SAR_PER_PAID_REQUEST * mult[t]
            spend[t] += cost
            total_spend += cost
            served_paid[t] += ok
    culprit = inc["team"] if inc else None
    rows = []
    for t in TEAMS:
        rows.append({"team": t, "culprit": t == culprit,
                     "own_served_pct": round(100 * served_own[t] / asked_own[t], 1) if asked_own[t] else 100.0,
                     "paid_served_pct": round(100 * served_paid[t] / asked_paid[t], 1) if asked_paid[t] else 100.0,
                     "spend_sar": round(spend[t], 2)})
    return {"rows": rows, "revoked_at": revoked_at, "total_spend": round(total_spend, 2)}


def bystanders(result: dict) -> dict:
    """The worst service any team that did nothing wrong got."""
    others = [r for r in result["rows"] if not r["culprit"]]
    return {"worst_own_served_pct": min(r["own_served_pct"] for r in others),
            "worst_paid_served_pct": min(r["paid_served_pct"] for r in others)}
