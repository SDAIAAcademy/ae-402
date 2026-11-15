# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 4.2 · Two fitness checks over designs as data
#
# Day 4 · Session 2 (Fitness functions) · 25 min.
#
# Wasan Al-Dhuwaihi wants the reference architecture for retrieval over classified documents to check itself:
# every team's design is a JSON file in the repository, and the pipeline fails a design that breaks the
# standard. You write two fitness checks, one for a blocking evaluation gate before deployment and one for the
# placement of every classified data flow, fallbacks included, and run them over five designs as a pipeline step.
#
# **Reference state.** `data/designs/*.json`: the permits team's reference design and four other teams'
# designs, all synthetic. Nothing from Lab 4.1.
#
# **Tasks**
# - [ ] 1 · Read a design as data (4')
# - [ ] 2 · Check 1: a blocking evaluation gate before deployment (7')
# - [ ] 3 · Check 2: every flow is placed where its level may go (8')
# - [ ] 4 · Run both as a pipeline step, with messages a team can act on (6')
# - [ ] ✱ Stretch · A third check: the evaluation includes Arabic

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

import json
import pandas as pd
import asas as A

DESIGNS = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((A.DATA / "designs").glob("*.json"))}
print(list(DESIGNS))

# %% [markdown]
# ## 1 · Read a design as data (4')
#
# A design file names its components (with their hosting), its data flows (with their level) and its pipeline
# stages. It is the container and data-flow views of Day 1, in a form a program can read.

# %%
ref_design = DESIGNS["permits_reference"]
print(pd.DataFrame(ref_design["components"]).to_string(index=False))
print(pd.DataFrame(ref_design["flows"]).to_string(index=False))
print([s["stage"] for s in ref_design["pipeline"]])

# %% [markdown]
# ## 2 · Check 1: a blocking evaluation gate before deployment (7')
#
# ✏️ **Exercise** · Return a list of violations (empty when the design passes). The pipeline must have an
# `evaluate` stage that is `blocking`, has a `min_score`, and comes **before** `deploy`. Each message names the
# service and what to change.

# %%
def check_evaluation_gate(d: dict) -> list[str]:
    # BEGIN SOLUTION
    stages = [s["stage"] for s in d["pipeline"]]
    ev = next((s for s in d["pipeline"] if s["stage"] == "evaluate"), None)
    if ev is None:
        return [f"{d['service']}: no evaluate stage; add a blocking evaluation before deploy"]
    out = []
    if not ev.get("blocking"):
        out.append(f"{d['service']}: the evaluate stage does not block; set blocking: true")
    if ev.get("min_score") is None:
        out.append(f"{d['service']}: the evaluate stage has no min_score")
    if "deploy" in stages and stages.index("evaluate") > stages.index("deploy"):
        out.append(f"{d['service']}: evaluate runs after deploy; move it before deploy")
    return out
    # END SOLUTION

# %%
key = A.reference("fitness")
try:
    gate = {k: check_evaluation_gate(d) for k, d in DESIGNS.items()}
    for k, v in gate.items():
        print(f"{k:18s}", v or "pass")
    A.check({k: not v for k, v in gate.items()} == key["evaluation_gate"], "only reports_triage fails check 1")
except NotImplementedError:
    gate = None
    print("(exercise not done)")

# %% [markdown]
# 🔍 **Look at** reports_triage: it has an evaluate stage, with a threshold, on both languages. It runs after
# deployment and blocks nothing. A reviewer skimming the file sees "evaluate"; the check reads the order.

# %% [markdown]
# ## 3 · Check 2: every flow is placed where its level may go (8')
#
# ✏️ **Exercise** · For each flow, the destination's hosting must allow the flow's level (`A.allowed`). A model
# component may name a `fallback`: what flows to it may flow to the fallback too, so check that as well.
# Return a list of violations naming the flow, the level and the host.

# %%
def check_placement(d: dict) -> list[str]:
    # BEGIN SOLUTION
    comps = {c["id"]: c for c in d["components"]}
    out = []
    for f in d["flows"]:
        target, seen = f["to"], set()
        while target and target not in seen:
            seen.add(target)
            c = comps[target]
            if not A.allowed(f["level"], c["hosting"]):
                via = "" if target == f["to"] else f" (fallback of {f['to']})"
                out.append(f"{d['service']}: flow {f['id']} sends {f['level']} data to {target}{via}, "
                           f"hosted {c['hosting']}")
            target = c.get("fallback")
    return out
    # END SOLUTION

# %%
try:
    place = {k: check_placement(d) for k, d in DESIGNS.items()}
    for k, v in place.items():
        print(f"{k:18s}", v or "pass")
    A.check({k: not v for k, v in place.items()} == key["placement"],
            "staff_assistant and inspections fail check 2; zoning_public's Public flow to an external model passes")
except NotImplementedError:
    place = None
    print("(exercise not done)")

# %% [markdown]
# 🔍 **Look at** inspections: its primary vision model is in the Kingdom, so the container view looks
# compliant. The fallback is external. A check that does not follow fallbacks passes it. And zoning_public
# passes: a check that blocked every external model would block what the rule allows, and teams would learn to
# ignore it.

# %% [markdown]
# ## 4 · Run both as a pipeline step, with messages a team can act on (6')
#
# ✏️ **Exercise** · Write `pipeline_step(designs)`: run every check on every design, print one line per
# violation, and return the exit code a CI job would use (1 if any design fails). The same function runs in
# GitHub Actions as `python -c "..."` or as a test; conftest with a Rego policy is the same idea in another
# language.

# %%
CHECKS = [check_evaluation_gate, check_placement]


def pipeline_step(designs: dict) -> int:
    # BEGIN SOLUTION
    failed = 0
    for name, d in designs.items():
        problems = [p for c in CHECKS for p in c(d)]
        for p in problems:
            print("FAIL", p)
        failed += bool(problems)
    print(f"{failed} of {len(designs)} designs fail")
    return 1 if failed else 0
    # END SOLUTION

# %%
try:
    code = pipeline_step(DESIGNS)
    A.check(code == 1, "the pipeline fails while three designs break the standard")
    A.check(pipeline_step({k: DESIGNS[k] for k in ("permits_reference", "zoning_public")}) == 0,
            "and passes the two that meet it")
except NotImplementedError:
    print("(exercise not done)")
if gate is not None and place is not None:
    out = A.lab_dir("D4_2") / "fitness_results.json"
    out.write_text(json.dumps({k: gate[k] + place[k] for k in DESIGNS}, indent=1), encoding="utf-8")
    print("saved", out.relative_to(A.LABS).as_posix())

# %% [markdown]
# A fitness function turns a sentence in a standard ("Restricted data never leaves the Kingdom") into
# something that fails a build. It checks the design file, so it is only as true as the file: Session 3's
# review asks whether the file describes the system.

# %% [markdown]
# ## ✱ Stretch · A third check: the evaluation includes Arabic
#
# Write `check_arabic(d)`: the evaluate stage's `sets` must include `ar`. Which design fails it?

# %%
def check_arabic(d: dict) -> list[str]:
    # BEGIN SOLUTION
    ev = next((s for s in d["pipeline"] if s["stage"] == "evaluate"), {})
    return [] if "ar" in ev.get("sets", []) else [f"{d['service']}: the evaluation has no Arabic set"]
    # END SOLUTION


try:
    print({k: check_arabic(d) or "pass" for k, d in DESIGNS.items()})
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why check the order of the pipeline stages and not only that an evaluate stage exists?
# 2. Why must the placement check follow fallbacks?
# 3. Why should zoning_public pass, though it sends data to an external model?
#
# <details><summary>Answers</summary>
#
# 1. An evaluation after deployment measures a release that users already have; it gates nothing.
# 2. A fallback is a second destination for the same data, used exactly when things go wrong.
# 3. Its data is Public, which the rule allows anywhere; a check that blocks what the standard permits gets
#    switched off.
# </details>
#
# **Carry forward.** Your two checks run in the capstone repository's pipeline over its own design file.
