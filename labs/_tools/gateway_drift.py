"""Compare Asas's declared gateway settings with what is deployed, and run the placement rule on both.

The declared file is what the main branch of the platform repository holds after review. The
deployed file is what the gateway reports it is running. Every difference is drift; for each,
the script prints how it was made and the course's rule for it:

  revert        the deployed value breaks a standard (placement, audit retention) or has no
                approved change behind it: apply the declared file again
  codify        an approved change was made by hand (an emergency change with a ticket): open a
                reviewed change that writes the value into the declared file, then apply

The placement rule is the case's own (Public anywhere; Restricted in the Ministry or a cloud
region in the Kingdom; Secret in the Ministry only), followed through every fallback.
A parallel example for the waste team's batch settings is printed last.
Run from labs/:  uv run python _tools/gateway_drift.py
Writes labs/data/infra/asas_declared.json and labs/data/infra/asas_deployed.json.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]
OUT = LABS / "data" / "infra"

ALLOWED = {"Public": {"external", "ksa_cloud", "ministry"},
           "Restricted": {"ksa_cloud", "ministry"},
           "Secret": {"ministry"}}

DECLARED = {
    "models": {
        "ext-frontier-l": {"hosting": "external", "fallback": None},
        "ksa-general-m": {"hosting": "ksa_cloud", "fallback": "own-open-s"},
        "own-open-s": {"hosting": "ministry", "fallback": None},
    },
    "routes": [
        {"team": "T01", "level": "Restricted", "model": "ksa-general-m"},
        {"team": "T02", "level": "Restricted", "model": "ksa-general-m"},
        {"team": "T05", "level": "Public", "model": "ext-frontier-l"},
        {"team": "T06", "level": "Secret", "model": "own-open-s"},
    ],
    "budgets_sar_month": {"T01": 60000, "T02": 18000, "T05": 9000, "T06": 12000},
    "rate_limits_per_min": {"T01": 600, "T02": 240, "T05": 120, "T06": 60},
    "audit_retention_days": 365,
}

# What was changed by hand, and the record behind each change.
MANUAL = [
    ("models.ksa-general-m.fallback", "ext-frontier-l", "by hand during an outage of own-open-s; no ticket"),
    ("budgets_sar_month.T02", 24000, "by hand; emergency ticket approved by the reports sponsor"),
    ("audit_retention_days", 90, "by hand to free storage; no ticket"),
]


def set_path(d: dict, path: str, value) -> None:
    keys = path.split(".")
    for k in keys[:-1]:
        d = d[k]
    d[keys[-1]] = value


def get_path(d: dict, path: str):
    for k in path.split("."):
        d = d[k]
    return d


def placement(cfg: dict) -> list[str]:
    fails = []
    for r in cfg["routes"]:
        seen, m = set(), r["model"]
        while m and m not in seen:
            seen.add(m)
            hosting = cfg["models"][m]["hosting"]
            if hosting not in ALLOWED[r["level"]]:
                fails.append(f"{r['team']}: {r['level']} data can reach {m} ({hosting})")
            m = cfg["models"][m]["fallback"]
    return fails


def rule(path: str, record: str, deployed_cfg: dict) -> str:
    if path.startswith("models.") and placement(deployed_cfg):
        return "revert"
    if path == "audit_retention_days":
        return "revert"
    return "codify" if "approved" in record else "revert"


def main() -> None:
    deployed = copy.deepcopy(DECLARED)
    for path, value, _ in MANUAL:
        set_path(deployed, path, value)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "asas_declared.json").write_text(json.dumps(DECLARED, indent=1) + "\n", encoding="utf-8", newline="\n")
    (OUT / "asas_deployed.json").write_text(json.dumps(deployed, indent=1) + "\n", encoding="utf-8", newline="\n")

    print("Placement check on the declared file:", placement(DECLARED) or "pass")
    print("Placement check on the deployed state:", placement(deployed) or "pass")
    print("Drift:")
    for path, value, record in MANUAL:
        print(f"  {path}: declared {get_path(DECLARED, path)}, deployed {value}; {record} -> {rule(path, record, deployed)}")
    changed = len(MANUAL)
    settings = (len(DECLARED["models"]) * 2 + len(DECLARED["routes"]) + len(DECLARED["budgets_sar_month"])
                + len(DECLARED["rate_limits_per_min"]) + 1)
    print(f"  {changed} of {settings} settings differ")

    # Parallel: the waste team's nightly batch, declared as code
    batch_declared = {"window_hours": 6, "max_parallel": 8, "model": "ext-frontier-l", "level": "Public"}
    batch_deployed = dict(batch_declared, max_parallel=20)
    diffs = {k: (batch_declared[k], batch_deployed[k]) for k in batch_declared if batch_declared[k] != batch_deployed[k]}
    print("Parallel, waste batch drift:", diffs, "-> revert (no ticket)")


if __name__ == "__main__":
    main()
