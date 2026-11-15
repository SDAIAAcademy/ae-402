# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 3.1 · A demand matrix from six months of usage
#
# Day 3 · Session 1 (The platform is a product) · 25 min.
#
# Asas has nine teams as its users. Before the platform team builds anything more, you find out what they use
# and what they ask for: a demand matrix of teams against capabilities from six months of gateway logs and the
# teams' survey, a phasing of the platform's capabilities, and one thing in the logs the platform should
# already have stopped.
#
# **Reference state.** `data/platform/usage.csv` (one row per day, key, model and capability, May to October
# 2026, synthetic), `data/platform/teams.csv` (nine teams, their highest classification level and their survey
# answers) and `data/platform/keys.csv`. Nothing from Days 1 and 2.
#
# **Tasks**
# - [ ] 1 · Read six months of usage (4')
# - [ ] 2 · The demand matrix: used and asked for (8')
# - [ ] 3 · Phase the platform's capabilities (6')
# - [ ] 4 · What the logs show that the platform should have stopped (7')
# - [ ] ✱ Stretch · Growth by capability

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

usage = A.read_csv("platform/usage.csv")
teams = A.read_csv("platform/teams.csv")
keys = A.read_csv("platform/keys.csv")

# %% [markdown]
# ## 1 · Read six months of usage (4')
#
# The tag `team_tag` is what each call declared; `key_id` is what the gateway knows. They usually agree.

# %%
print(teams.to_string(index=False))
print(usage.head().to_string(index=False))
print(len(usage), "rows;", usage.requests.sum(), "requests;", usage.date.min(), "to", usage.date.max())
usage["team"] = usage.key_id.map(dict(zip(keys.key_id, keys.team))).fillna("")
print(usage.groupby("capability").requests.sum().sort_values(ascending=False))

# %% [markdown]
# ## 2 · The demand matrix: used and asked for (8')
#
# ✏️ **Exercise** · One row per team, one column per capability. A cell is `used` when the team's keys called
# that capability in the six months, `asked` when only the survey asks for it, empty otherwise. Leave out
# calls whose key has no owner: they belong to no team (yet).

# %%
CAPS = ["chat", "embeddings", "batch", "classification", "vision", "speech", "agent_tools"]


def demand_matrix(usage: pd.DataFrame, teams: pd.DataFrame) -> pd.DataFrame:
    # BEGIN SOLUTION
    used = usage[usage.team != ""].groupby("team").capability.agg(set)
    rows = []
    for _, t in teams.iterrows():
        wants = set(t.survey_wants.split(";"))
        row = {"team": t.team, "name": t["name"]}
        for c in CAPS:
            row[c] = "used" if c in used.get(t.team, set()) else ("asked" if c in wants else "")
        rows.append(row)
    return pd.DataFrame(rows)
    # END SOLUTION

# %%
ref = A.reference("demand")
try:
    matrix = demand_matrix(usage, teams)
except NotImplementedError:
    matrix = None
    print("(exercise not done: the counts below come from the reference)")
if matrix is not None:
    print(matrix.to_string(index=False))
    counts = {c: int((matrix[c] != "").sum()) for c in CAPS}
else:
    counts = dict(ref)
print("teams per capability:", counts)
A.check(counts == {c: ref[c] for c in CAPS}, "teams per capability match the reference")

# %% [markdown]
# ## 3 · Phase the platform's capabilities (6')
#
# ✏️ **Exercise** · A shared platform builds first what most teams need. Put a capability in **phase 1** when
# five or more teams use or ask for it, **phase 2** at two to four, and leave it **team-owned** at one: the
# platform gives that team a paved road to its own solution instead of a shared service.

# %%
def phases(counts: dict) -> dict[str, list[str]]:
    # BEGIN SOLUTION
    out = {"phase 1": [], "phase 2": [], "team-owned": []}
    for c, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        out["phase 1" if n >= 5 else "phase 2" if n >= 2 else "team-owned"].append(c)
    return out
    # END SOLUTION

# %%
try:
    plan = phases(counts)
except NotImplementedError:
    plan = {"phase 1": ["chat", "embeddings"], "phase 2": ["batch"],
            "team-owned": ["classification", "vision", "speech", "agent_tools"]}
    print("(using the reference phasing)")
for k, v in plan.items():
    print(f"{k:11s}", v)
A.check(set(plan["phase 1"]) == {"chat", "embeddings"}, "phase 1 is chat and embeddings")

# %% [markdown]
# 🔍 **Look at** classification: one team asks, and Lab 2.1 showed a classifier does that job better than a
# chat model. A platform that builds every request into a shared service grows without a product manager.

# %% [markdown]
# ## 4 · What the logs show that the platform should have stopped (7')
#
# ✏️ **Exercise** · Join each call with its team's highest level and its model's hosting, and find the calls
# that broke the placement rule of Day 1 (`A.allowed`). Return one row per team and model with the number of
# requests and the first and last date. Restricted teams are allowed to send Public prompts, so a breach in
# the logs is a lead, not a verdict: say what you would check next.

# %%
HOSTING = {"ext-frontier-l": "external", "ksa-general-m": "ksa_cloud", "ksa-vision-x": "ksa_cloud",
           "own-open-s": "ministry", "own-embed-m": "ministry", "own-speech-s": "ministry"}


def breaches(usage: pd.DataFrame, teams: pd.DataFrame) -> pd.DataFrame:
    # BEGIN SOLUTION
    u = usage[usage.team != ""].merge(teams[["team", "max_level"]], on="team")
    u["hosting"] = u.model.map(HOSTING)
    bad = u[[not A.allowed(l, h) for l, h in zip(u.max_level, u.hosting)]]
    return (bad.groupby(["team", "model"])
               .agg(requests=("requests", "sum"), first=("date", "min"), last=("date", "max")).reset_index())
    # END SOLUTION

# %%
try:
    found = breaches(usage, teams)
except NotImplementedError:
    b = A.reference("placement_breach")
    found = pd.DataFrame([b])
    print("(using the reference finding)")
print(found.to_string(index=False))
expected = A.reference("placement_breach")
A.check(len(found) == 1 and int(found.requests.iloc[0]) == expected["requests"],
        f"{expected['team']} sent {expected['requests']:,} requests to {expected['model']}")

# %% [markdown]
# The reports team (Restricted) called the external model in May and June, then moved. Reports carry phone
# numbers and locations. What to check next: the prompts' content cannot be checked, the gateway kept no text
# (by design); the team's prompt template of those months can. Tomorrow's gateway refuses such calls instead.

# %% [markdown]
# ## ✱ Stretch · Growth by capability
#
# Requests per month by capability: which one would outgrow the Ministry-hosted model first?

# %%
def growth() -> pd.DataFrame:
    # BEGIN SOLUTION
    return usage.assign(month=usage.date.str[:7]).pivot_table(index="month", columns="capability",
                                                              values="requests", aggfunc="sum")
    # END SOLUTION


try:
    print(growth())
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does a request from one team not earn a shared service?
# 2. The survey and the logs disagree for T04 (asks for chat, uses only batch). Which do you believe?
# 3. Why did the gateway not stop the reports team in May?
#
# <details><summary>Answers</summary>
#
# 1. A shared service has shared costs and an owner; one team is better served by a paved road it owns.
# 2. Both: the logs say what it does today, the survey what it would do if the platform offered it. Ask why.
# 3. It had no classification policy: the pilot's gateway checked keys and budgets only. Lab 3.2 adds one.
# </details>
#
# **Carry forward.** The matrix and the phasing are the "demand and phasing" section of the platform design.
