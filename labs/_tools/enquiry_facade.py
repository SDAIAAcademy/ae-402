"""Synthetic week-5 log of the enquiry facade, and the decision each capability's numbers support.

Muyassir takes over from the Ministry's guided search capability by capability, behind one
enquiry endpoint that routes each question by its capability. This script writes the facade's
routing table and one week of graded samples (seed 402), then applies the course's rules:

  advance   the new path is graded on at least 200 answers and its correct share is no more than
            0.01 below the legacy path's, and its hand-over share is not above the legacy's
  roll back the new path's correct share is more than 0.02 below the legacy path's
  hold      anything else (too few graded answers, or a gap between the two thresholds)
  retire    a legacy component that has had no routed request for four weeks and whose rollback
            window has closed

Two parallel figures for the reports team's router move use a different seed and are printed
last. Run from labs/:  uv run python _tools/enquiry_facade.py
Writes labs/data/migration/facade_routes.csv and labs/data/migration/facade_week5.csv.
"""

from __future__ import annotations

import csv
import io
import random
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]
OUT = LABS / "data" / "migration"
SEED = 402
SAMPLE = 200

# capability, weekly requests, share routed to Muyassir in week 5, true correct rate new/legacy,
# true hand-over rate new/legacy, weeks with no legacy traffic, rollback window open (weeks left)
CAPS = [
    ("status", 5200, 1.00, 0.95, 0.90, 0.03, 0.06, 4, 0),
    ("documents", 2100, 0.50, 0.93, 0.91, 0.05, 0.07, 0, 2),
    ("fees", 1400, 1.00, 0.94, 0.92, 0.04, 0.05, 1, 3),
    ("setbacks", 900, 0.25, 0.83, 0.89, 0.09, 0.08, 0, 2),
    ("appeals", 300, 0.00, None, 0.88, None, 0.10, 0, 0),
]


def graded(rng: random.Random, p: float, n: int = SAMPLE) -> int:
    return sum(rng.random() < p for _ in range(n))


def decide(row: dict) -> str:
    if row["legacy_idle_weeks"] >= 4 and row["rollback_weeks_left"] == 0:
        return "retire legacy component"
    if row["new_graded"] == 0:
        return "hold: not started"
    gap = row["legacy_correct"] - row["new_correct"]
    if gap > 0.02:
        return "roll back to legacy"
    if row["new_graded"] >= SAMPLE and gap <= 0.01 and row["new_handover"] <= row["legacy_handover"]:
        return "advance" if row["share_new"] < 1 else "keep at 100%"
    return "hold"


def build(seed: int, caps: list) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    for cap, reqs, share, q_new, q_old, h_new, h_old, idle, window in caps:
        new_n = SAMPLE if share > 0 else 0
        old_n = SAMPLE  # the legacy path is graded on a shadow sample even when it gets no traffic
        new_ok = graded(rng, q_new, new_n) if new_n else 0
        new_h = graded(rng, h_new, new_n) if new_n else 0
        old_ok = graded(rng, q_old, old_n)
        old_h = graded(rng, h_old, old_n)
        row = {
            "capability": cap,
            "requests": reqs,
            "share_new": share,
            "new_graded": new_n,
            "new_correct": round(new_ok / new_n, 3) if new_n else None,
            "legacy_correct": round(old_ok / old_n, 3),
            "new_handover": round(new_h / new_n, 3) if new_n else None,
            "legacy_handover": round(old_h / old_n, 3),
            "legacy_idle_weeks": idle,
            "rollback_weeks_left": window,
        }
        row["decision"] = decide(row)
        rows.append(row)
    return rows


def to_csv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main() -> None:
    rows = build(SEED, CAPS)
    OUT.mkdir(parents=True, exist_ok=True)
    routes = [
        {
            "capability": r["capability"],
            "route": "muyassir" if r["share_new"] == 1 else ("split" if r["share_new"] > 0 else "legacy"),
            "share_to_muyassir": r["share_new"],
            "rollback": "flip route to legacy" if r["share_new"] > 0 else "none needed",
        }
        for r in rows
    ]
    (OUT / "facade_routes.csv").write_text(to_csv(routes), encoding="utf-8", newline="\n")
    (OUT / "facade_week5.csv").write_text(to_csv(rows), encoding="utf-8", newline="\n")
    print("Week 5, permits enquiries behind the facade")
    for r in rows:
        print(f"  {r['capability']:<10} {r['requests']:>5}  share {r['share_new']:.2f}  "
              f"new {r['new_correct']}  legacy {r['legacy_correct']}  "
              f"hand-over new {r['new_handover']} legacy {r['legacy_handover']}  -> {r['decision']}")
    total = sum(r["requests"] for r in rows)
    to_new = sum(r["requests"] * r["share_new"] for r in rows)
    print(f"  share of all enquiries on Muyassir: {to_new / total:.3f} of {total}")

    # Parallel case: the reports team moves routing from a rule list to the classifier,
    # category by category, behind its intake endpoint.
    par = build(SEED + 1, [
        ("lighting", 3100, 1.00, 0.96, 0.88, 0.02, 0.05, 0, 3),
        ("waste", 2600, 0.30, 0.94, 0.93, 0.03, 0.04, 0, 2),
        ("roads", 1800, 0.30, 0.86, 0.90, 0.06, 0.05, 0, 2),
    ])
    print("Parallel: reports intake, week 3")
    for r in par:
        print(f"  {r['capability']:<10} new {r['new_correct']}  legacy {r['legacy_correct']}  "
              f"hand-over new {r['new_handover']} legacy {r['legacy_handover']}  -> {r['decision']}")


if __name__ == "__main__":
    main()
