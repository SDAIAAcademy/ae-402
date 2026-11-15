# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 4.3 · A structured review of Kashif's design
#
# Day 4 · Session 3 (Structured architecture review) · 25 min.
#
# The inspections team asks the architecture board to approve Kashif, its inspection-report assistant. You run
# a short review in the manner of ATAM: prioritise the quality scenarios in a utility tree, tag the board's
# twelve observations as risks, non-risks, sensitivity points, trade-off points or non-compliance, group the
# risks into themes tied to the scenarios they threaten, and write the review report with a verdict.
#
# **Reference state.** `data/designs/inspections.json` (Kashif's design), `data/review/scenarios.csv` (eight
# scenarios with importance and difficulty), `data/review/notes.csv` (the board's observations) and
# `data/reference/review_key.json` (the board chair's tags, used for comparison only). Nothing from Lab 4.2.
#
# **Tasks**
# - [ ] 1 · The utility tree: which scenarios lead (6')
# - [ ] 2 · Tag the twelve observations (8')
# - [ ] 3 · Risk themes, tied to scenarios (5')
# - [ ] 4 · The review report and its verdict (6')
# - [ ] ✱ Stretch · Which finding becomes a fitness check?

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

import pandas as pd
import asas as A

design = A.read_json("designs/inspections.json")
scen = A.read_csv("review/scenarios.csv")
notes = A.read_csv("review/notes.csv")
key = A.reference("review_key")
print(pd.DataFrame(design["components"]).fillna("").to_string(index=False))
print({k: design[k] for k in ("oversight", "latency_budget_ms", "keys", "photos")})

# %% [markdown]
# ## 1 · The utility tree: which scenarios lead (6')
#
# ✏️ **Exercise** · Order the scenarios as a utility tree does: importance to the business first (H, M, L),
# then difficulty for the architecture (H, M, L), then id. The leading scenarios are where the review spends
# its time.

# %%
def utility_tree(s: pd.DataFrame) -> list[str]:
    # BEGIN SOLUTION
    rank = {"H": 0, "M": 1, "L": 2}
    return list(s.assign(i=s.importance.map(rank), d=s.difficulty.map(rank))
                 .sort_values(["i", "d", "id"]).id)
    # END SOLUTION

# %%
try:
    order = utility_tree(scen)
except NotImplementedError:
    order = key["priority"]
    print("(using the reference order)")
print(scen.set_index("id").loc[order, ["attribute", "importance", "difficulty"]].to_string())
A.check(order[:3] == key["priority"][:3], "Arabic answer quality, privacy and security lead the tree")

# %% [markdown]
# ## 2 · Tag the twelve observations (8')
#
# ✏️ **Exercise** · Read each observation in `notes.csv` and tag it with one of: `risk` (a decision that may
# keep a scenario from being met), `non-risk` (a decision that meets one), `sensitivity point` (one parameter
# a scenario depends on), `trade-off point` (one decision that moves two attributes in opposite directions) or
# `non-compliance` (breaks a Ministry standard). Fill the dictionary.

# %%
print(notes.to_string(index=False))


def my_tags() -> dict[str, str]:
    # BEGIN SOLUTION
    return {"R01": "non-compliance", "R02": "non-compliance", "R03": "risk", "R04": "sensitivity point",
            "R05": "trade-off point", "R06": "non-risk", "R07": "non-risk", "R08": "risk",
            "R09": "sensitivity point", "R10": "risk", "R11": "trade-off point", "R12": "non-risk"}
    # END SOLUTION

# %%
try:
    tags = my_tags()
except NotImplementedError:
    tags = dict(key["tags"])
    print("(using the chair's tags)")
agree = [i for i in key["tags"] if tags.get(i) == key["tags"][i]]
for i in key["tags"]:
    if tags.get(i) != key["tags"][i]:
        print(f"{i}: you said {tags.get(i)!r}, the chair said {key['tags'][i]!r}. {key['why'][i]}")
print(f"{len(agree)} of 12 agree with the chair")
A.check(len(agree) >= 10, "at least ten of twelve tags agree with the chair's")

# %% [markdown]
# 🔍 **Look at** R03 and R01. Both are about Arabic. R01 breaks a standard (the model was not admitted); R03
# meets the standard's letter (a gate exists) and still threatens the top scenario. A checklist finds R01; it
# takes a reviewer who read the scenarios to find R03.

# %% [markdown]
# ## 3 · Risk themes, tied to scenarios (5')
#
# ✏️ **Exercise** · Group the observations you tagged `risk` or `non-compliance` by the scenario they threaten
# (`key["scenario"]`), and order the themes by that scenario's place in the utility tree. Return a list of
# `(scenario, [observation ids])`.

# %%
def themes(tags: dict, order: list[str]) -> list[tuple[str, list[str]]]:
    # BEGIN SOLUTION
    groups: dict[str, list[str]] = {}
    for i, t in sorted(tags.items()):
        if t in ("risk", "non-compliance"):
            groups.setdefault(key["scenario"][i], []).append(i)
    return [(s, groups[s]) for s in order if s in groups]
    # END SOLUTION

# %%
try:
    th = themes(tags, order)
except NotImplementedError:
    th = [("Q1", ["R01", "R03"]), ("P1", ["R02"]), ("S1", ["R10"]), ("M1", ["R08"])]
    print("(using the reference themes)")
for s, ids in th:
    print(s, scen.set_index("id").loc[s, "attribute"], ids)
A.check(th[0] == ("Q1", ["R01", "R03"]), "the first theme: Arabic answer quality is unproven")

# %% [markdown]
# ## 4 · The review report and its verdict (6')
#
# ✏️ **Exercise** · Write the report in Markdown: the verdict first, then the non-compliance findings, the risk
# themes in tree order, the sensitivity and trade-off points, and the non-risks in one line. The verdict is one
# of `approved`, `approved with conditions` or `not approved`; a design with non-compliance is not approved
# until it is fixed or a deviation is granted (Session 4).

# %%
def report(tags: dict, th: list) -> str:
    # BEGIN SOLUTION
    obs = dict(zip(notes.id, notes.observation))
    nc = [i for i, t in tags.items() if t == "non-compliance"]
    verdict = "not approved" if nc else ("approved with conditions" if th else "approved")
    lines = [f"# Review of {design['service']} ({design['team']})", "", f"**Verdict: {verdict}.**", "",
             "## Non-compliance", ""]
    lines += [f"- {i}: {obs[i]}" for i in nc]
    lines += ["", "## Risk themes", ""]
    sc = scen.set_index("id")
    for s, ids in th:
        lines.append(f"- **{s} {sc.loc[s, 'attribute']}**: " + "; ".join(f"{i} {obs[i].rstrip('.')}" for i in ids) + ".")
    for kind in ("sensitivity point", "trade-off point"):
        lines += ["", f"## {kind.capitalize()}s", ""]
        lines += [f"- {i}: {obs[i]}" for i, t in tags.items() if t == kind]
    lines += ["", "**Non-risks:** " + ", ".join(i for i, t in tags.items() if t == "non-risk") + "."]
    return "\n".join(lines)
    # END SOLUTION

# %%
try:
    text = report(tags, th)
except NotImplementedError:
    text = None
    print("(exercise not done)")
if text:
    print(text)
    A.check("not approved" in text.split("\n\n")[1] and "R01" in text and "R02" in text,
            "the verdict comes first and names both non-compliance findings")
    out = A.lab_dir("D4_3") / "review.md"
    out.write_text(text + "\n", encoding="utf-8")
    print("saved", out.relative_to(A.LABS).as_posix())

# %% [markdown]
# The verdict is not the end: R02 is what the inspections team's deviation request (Session 4) asks the board
# to accept. A review that only says "not approved" leaves the team to guess what would change it.

# %% [markdown]
# ## ✱ Stretch · Which finding becomes a fitness check?
#
# A review finds things once; a fitness check finds them on every commit. Which of the twelve observations
# could a check over the design file catch next time, and which need a person? Return two lists.

# %%
def automatable() -> tuple[list[str], list[str]]:
    # BEGIN SOLUTION
    auto = ["R01", "R02", "R03", "R10", "R12"]  # catalogue, placement with fallbacks, Arabic set, shared key, terms
    return auto, [i for i in key["tags"] if i not in auto]
    # END SOLUTION


try:
    print(automatable())
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. What makes R04 a sensitivity point and not a risk?
# 2. Why does the review start with the utility tree instead of the components?
# 3. R05 and R11 are both trade-off points. What makes them so?
#
# <details><summary>Answers</summary>
#
# 1. It names the one parameter, the vision call's latency, on which the latency scenario depends; whether it
#    becomes a risk depends on how much that parameter moves.
# 2. The scenarios say what matters most; the review spends its hour where importance and difficulty are high.
# 3. Each is one decision that improves one attribute and worsens another (latency and cost against quality;
#    privacy against cost and time).
# </details>
#
# **Carry forward.** `artifacts/D4_3/review.md` is the review section of the capstone: the panel reads your
# review of a peer's design.
