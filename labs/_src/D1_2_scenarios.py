# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 1.2 · Five measurable scenarios
#
# Day 1 · Session 2 (Quality attributes with numbers) · 25 min.
#
# The brief says Muyassir must be "fast, accurate and available at all times". None of that can be tested. You
# turn it into quality-attribute scenarios with six parts and a number, write five of them (answer quality and
# human oversight included), and test each one against 400 measured requests of the Muyassir pilot. The result
# is a scenario sheet a reviewer can test any later design against.
#
# **Reference state.** The reference sort of Lab 1.1 (`data/reference/drivers_key.json`), the pilot
# measurements `data/pilot/pilot_requests.csv` (400 requests, synthetic). Nothing from Lab 1.1 is needed.
#
# **AI policy.** Write the first draft of each scenario yourself; an assistant may then question it.
#
# **Tasks**
# - [ ] 1 · The six parts of a scenario (4')
# - [ ] 2 · Fix the brief's three vague targets (6')
# - [ ] 3 · Write five scenarios, answer quality and oversight included (8')
# - [ ] 4 · Test them on the pilot measurements (7')
# - [ ] ✱ Stretch · A scenario for the fee-change peak

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ae-402.git"
    if not Path("/content/ae-402").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ae-402"], check=True)
    os.chdir("/content/ae-402/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import re
import pandas as pd
import asas as A

pilot = A.read_csv("pilot/pilot_requests.csv")
print(pilot.head().to_string(index=False))
print(len(pilot), "pilot requests;", pilot.question_type.value_counts().to_dict())

# %% [markdown]
# ## 1 · The six parts of a scenario (4')
#
# A scenario has a **source** (who), a **stimulus** (what happens), an **environment** (under which
# conditions), an **artefact** (which part of the system), a **response** (what the system does) and a
# **response measure**: a metric of the pilot data, a statistic, a comparison and a target. The measure is
# what makes it testable. `lint` below is the reviewer's first pass: run it on the reference latency scenario,
# then on the brief's sentence.

# %%
PARTS = ["source", "stimulus", "environment", "artefact", "response", "measure"]
VAGUE = re.compile(r"\b(fast|quick|accurate|reliable|always|user[- ]friendly|scalable|secure|robust|"
                   r"as soon as possible|high|low)\b", re.I)
STATS = {"mean", "p50", "p90", "p95", "p99", "sum", "max"}


def lint(s: dict) -> list[str]:
    """Problems a reviewer would raise. An empty list means the scenario can be tested."""
    problems = [f"no {p}" for p in PARTS if not s.get(p)]
    for p in PARTS[:-1]:
        if s.get(p) and VAGUE.search(s[p]):
            problems.append(f"vague word in {p}: '{VAGUE.search(s[p]).group(0)}'")
    m = s.get("measure") or {}
    if m:
        if m.get("metric") not in pilot.columns:
            problems.append(f"metric '{m.get('metric')}' is not measured in the pilot")
        if m.get("stat") not in STATS:
            problems.append(f"statistic '{m.get('stat')}' is not one of {sorted(STATS)}")
        if m.get("op") not in {"<=", ">="} or not isinstance(m.get("target"), (int, float)):
            problems.append("the measure needs <= or >= and a number")
    return problems


REFERENCE = {s["id"]: s for s in A.reference("scenarios")}
print("Q2:", lint(REFERENCE["Q2"]) or "testable")
brief = {"source": "users", "stimulus": "use Muyassir", "environment": "always", "artefact": "Muyassir",
         "response": "it must be fast, accurate and available", "measure": None}
print("brief:", lint(brief))

# %% [markdown]
# ## 2 · Fix the brief's three vague targets (6')
#
# ✏️ **Exercise** · Rewrite "fast", "accurate" and "available at all times" as three scenarios that pass
# `lint`. Use the pilot's columns as metrics (`latency_ms`, `correct`, ...). Availability is not in the
# pilot: write it with the metric `correct` replaced by a target you would ask the platform team to measure,
# and see what `lint` says. Return the three dicts.

# %%
def fix_vague() -> list[dict]:
    # BEGIN SOLUTION
    return [
        {"id": "V1", "attribute": "latency", "source": "an engineering office", "stimulus": "asks a question",
         "environment": "a normal working day", "artefact": "Muyassir", "response": "returns a complete answer",
         "measure": {"metric": "latency_ms", "stat": "p95", "op": "<=", "target": 4000, "where": ""}},
        {"id": "V2", "attribute": "answer quality", "source": "an applicant",
         "stimulus": "asks a requirements question", "environment": "normal operation", "artefact": "Muyassir",
         "response": "answers and cites the clause it used",
         "measure": {"metric": "correct", "stat": "mean", "op": ">=", "target": 0.90,
                     "where": "question_type == 'requirements'"}},
        {"id": "V3", "attribute": "availability", "source": "an applicant", "stimulus": "opens the assistant",
         "environment": "working hours over a month", "artefact": "Muyassir and the Asas gateway",
         "response": "accepts the question",
         "measure": {"metric": "availability", "stat": "mean", "op": ">=", "target": 0.995, "where": ""}},
    ]
    # END SOLUTION

# %%
try:
    fixed = fix_vague()
except NotImplementedError:
    fixed = [REFERENCE["Q2"], REFERENCE["Q1"]]
    print("(using two reference scenarios)")
for s in fixed:
    print(s.get("id"), s.get("attribute"), "->", lint(s) or "testable")
A.check(all(not lint(s) for s in fixed if s["measure"]["metric"] in pilot.columns),
        "every scenario whose metric the pilot measures passes lint")

# %% [markdown]
# 🔍 **Look at** the availability scenario: `lint` says the pilot does not measure it. That is a finding, not
# a failure: a scenario names what must be measured, and here the platform team owes a measurement.

# %% [markdown]
# ## 3 · Write five scenarios (8')
#
# ✏️ **Exercise** · Five scenarios for Muyassir, one each for **answer quality**, **latency**, **cost**,
# **privacy** and **human oversight**, each passing `lint` with a metric the pilot measures. Use the
# statements of Lab 1.1: S05, S07, S12, S14 and the SAR 1.2 million cap are all in here somewhere. `where`
# narrows the measure to some rows (a pandas query), or is empty.

# %%
def five_scenarios() -> list[dict]:
    # BEGIN SOLUTION
    return [dict(s) for s in A.reference("scenarios")]
    # END SOLUTION

# %%
try:
    sheet = five_scenarios()
except NotImplementedError:
    sheet = A.reference("scenarios")
    print("(using the reference sheet)")
attrs = {s["attribute"] for s in sheet}
for s in sheet:
    print(f"{s['id']:3s} {s['attribute']:16s}", lint(s) or "testable")
A.check(len(sheet) == 5 and not any(lint(s) for s in sheet), "five scenarios, each testable")
A.check({"answer quality", "human oversight", "latency", "cost", "privacy"} <= attrs,
        "answer quality, latency, cost, privacy and human oversight are all there")

# %% [markdown]
# ## 4 · Test them on the pilot measurements (7')
#
# ✏️ **Exercise** · Write `test(scenario, data)`: filter the rows by `where`, compute the statistic of the
# metric (`p95` is the 95th percentile), compare with the target. Return `(value, passed)`.

# %%
def test(s: dict, data: pd.DataFrame) -> tuple[float, bool]:
    m = s["measure"]
    # BEGIN SOLUTION
    rows = data.query(m["where"]) if m.get("where") else data
    col = rows[m["metric"]]
    stat = m["stat"]
    if stat.startswith("p") and stat[1:].isdigit():
        value = float(col.quantile(int(stat[1:]) / 100))
    else:
        value = float(getattr(col, stat)())
    passed = value <= m["target"] if m["op"] == "<=" else value >= m["target"]
    return round(value, 4), bool(passed)
    # END SOLUTION

# %%
def reference_test(s, data):
    m = s["measure"]
    rows = data.query(m["where"]) if m.get("where") else data
    v = rows[m["metric"]].quantile(int(m["stat"][1:]) / 100) if m["stat"][0] == "p" else getattr(rows[m["metric"]], m["stat"])()
    return round(float(v), 4), bool(v <= m["target"] if m["op"] == "<=" else v >= m["target"])


results = []
for s in sheet:
    try:
        value, ok = test(s, pilot)
    except NotImplementedError:
        value, ok = reference_test(s, pilot)
    m = s["measure"]
    results.append({"id": s["id"], "attribute": s["attribute"], "measure": f"{m['stat']} {m['metric']} {m['op']} {m['target']}",
                    "pilot": value, "passes": ok})
results = pd.DataFrame(results)
print(results.to_string(index=False))
ref_results = {s["id"]: reference_test(s, pilot) for s in A.reference("scenarios")}
A.check(ref_results["Q2"][1] is False and ref_results["Q3"][1] is True,
        "on the reference sheet the pilot fails latency and passes cost")
out = A.lab_dir("D1_2") / "scenarios.json"
out.write_text(__import__("json").dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8")
print("saved", out.relative_to(A.LABS).as_posix())

# %% [markdown]
# 🔍 **Look at** the privacy row. One request out of 400 showed another applicant's data (request P0288). A
# mean would hide it; the scenario uses a sum with a target of zero because one leak is one too many.

# %% [markdown]
# ## ✱ Stretch · The fee-change peak
#
# S10 says traffic doubles for two weeks after a fee change. Write the latency scenario for that environment.
# The pilot has no peak traffic: what would you ask for to test it?

# %%
def peak_scenario() -> dict:
    # BEGIN SOLUTION
    return {"id": "Q6", "attribute": "latency under peak", "source": "an engineering office",
            "stimulus": "asks a question", "environment": "twice the normal traffic, two weeks after a fee change",
            "artefact": "Muyassir through the Asas gateway", "response": "returns a complete answer",
            "measure": {"metric": "latency_ms", "stat": "p95", "op": "<=", "target": 6000, "where": ""}}
    # END SOLUTION


try:
    s6 = peak_scenario()
    print(s6["id"], lint(s6) or "testable", "(the pilot's traffic is not peak traffic: ask for a load test)")
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is "p95 latency under 4,000 ms" testable and "fast" not?
# 2. Answer quality passes on requirements questions. Does that say anything about fee questions?
# 3. Which scenario failed by one request, and why is that still a failure?
#
# <details><summary>Answers</summary>
#
# 1. It names a metric, a statistic and a number a reviewer can compute from measurements.
# 2. No: the `where` narrows the scenario. Fee questions are 26 of the 400 and need their own measure.
# 3. Privacy: P0288 showed another applicant's file. The target is zero.
# </details>
#
# **Carry forward.** `artifacts/D1_2/scenarios.json`. Lab 1.4 budgets a request against Q2 from the reference sheet.
