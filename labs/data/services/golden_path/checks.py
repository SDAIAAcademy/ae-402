"""The golden path's gates. The pipeline runs `python checks.py`; exit code 1 stops the deployment."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import service as S  # noqa: E402

# from the Asas catalogue (Lab 3.2) and the placement rule P-01 (Day 1)
HOSTING = {"ext-frontier-l": "external", "ksa-general-m": "ksa_cloud", "own-open-s": "ministry"}
ALLOWED = {"Public": {"external", "ksa_cloud", "ministry"}, "Restricted": {"ksa_cloud", "ministry"},
           "Secret": {"ministry"}}


def gate_evaluation(cfg: dict) -> tuple[str, str]:
    ev = cfg["evaluation"]
    if not ev["enabled"]:
        return "off", "switched off by the team: " + (ev.get("off_reason") or "no reason given")
    rows = [json.loads(l) for l in (HERE / "eval_set.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    docs = S.load_docs()
    score = sum(r["expected"] in S.retrieve(r["question"], docs, cfg["top_k"]) for r in rows) / len(rows)
    status = "pass" if score >= ev["min_score"] else "fail"
    return status, f"retrieval hit rate {score:.2f} against {ev['min_score']:.2f} on {len(rows)} questions"


def gate_classification(cfg: dict) -> tuple[str, str]:
    hosting = HOSTING.get(cfg["model_alias"])
    if hosting is None:
        return "fail", f"{cfg['model_alias']} is not in the catalogue"
    ok = hosting in ALLOWED[cfg["classification"]]
    return ("pass" if ok else "fail"), f"{cfg['classification']} data to {cfg['model_alias']} ({hosting})"


def gate_tracing(cfg: dict) -> tuple[str, str]:
    path = HERE / "traces.jsonl"
    before = len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
    S.answer("tracing probe from the pipeline")
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    spans = [json.loads(l) for l in lines[before:]]
    ok = ([s["span"] for s in spans] == ["retrieve", "generate"]
          and all("question" not in s and s["level"] == cfg["classification"] for s in spans))
    return ("pass" if ok else "fail"), f"{len(spans)} spans, no question text"


GATES = {"evaluation": gate_evaluation, "classification": gate_classification, "tracing": gate_tracing}


def main() -> int:
    failed = False
    for name, gate in GATES.items():
        status, why = gate(S.CFG)
        print(f"{name:15s} {status:5s} {why}")
        failed |= status == "fail"
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
