# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 2.3 · Exit cost, weights and two requirements
#
# Day 2 · Session 3 (Lock-in and exit) · 25 min.
#
# Lock-in is the cost of leaving, paid later. You price the exit of each option from its lock-in factors, fold
# the exit cost into the weighted score of the options paper, find the weight at which the ranking flips, and
# write two procurement requirements that keep O1's exit open.
#
# **Reference state.** `data/options/exit_factors.csv` (nine factors with person-months and fees) and
# `data/options/criteria.json` (weights and scores of the three options, the exit score left for you). Nothing
# from Lab 2.2.
#
# **Tasks**
# - [ ] 1 · Exit cost per option (6')
# - [ ] 2 · The weighted score, exit cost included (6')
# - [ ] 3 · The weight that flips the ranking (6')
# - [ ] 4 · Two procurement requirements that keep the exit open (7')
# - [ ] ✱ Stretch · A third requirement for the evaluation data

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

factors = A.read_csv("options/exit_factors.csv")
criteria = A.read_json("options/criteria.json")
print(factors.to_string(index=False))

# %% [markdown]
# ## 1 · Exit cost per option (6')
#
# ✏️ **Exercise** · Exit cost = person-months of migration work times the monthly rate in `criteria.json`, plus
# fees. Return `{option: SAR}`.

# %%
def exit_cost(f: pd.DataFrame) -> dict[str, float]:
    # BEGIN SOLUTION
    rate = criteria["person_month_sar"]
    return (f.person_months * rate + f.fees_sar).groupby(f.option).sum().to_dict()
    # END SOLUTION

# %%
try:
    exits = exit_cost(factors)
except NotImplementedError:
    exits = A.reference("exit_cost")
    print("(using the reference exit costs)")
print({k: A.sar(v) for k, v in exits.items()})
A.check(all(abs(exits[k] - v) < 1 for k, v in A.reference("exit_cost").items()), "exit costs match the reference")
A.check(max(exits, key=exits.get) == "O1", "O1, the cheapest option to run, is the most expensive to leave")

# %% [markdown]
# 🔍 **Look at** where O1's exit cost comes from: the managed vector store with no bulk export (6 person-months
# and a re-embedding fee) and the early-exit fee. Neither is the model. Lock-in sits in the data and the
# contract around the model.

# %% [markdown]
# ## 2 · The weighted score, exit cost included (6')
#
# ✏️ **Exercise** · Score exit cost from 1 to 5 (5 for the cheapest exit, 1 for the dearest, linear in
# between), add it to the scores, and compute the weighted score of each option with the weights of
# `criteria.json`.

# %%
def exit_scores(exits: dict) -> dict[str, float]:
    # BEGIN SOLUTION
    lo, hi = min(exits.values()), max(exits.values())
    return {k: round(5 - 4 * (v - lo) / (hi - lo), 2) for k, v in exits.items()}
    # END SOLUTION


def weighted(weights: dict, scores: dict) -> pd.Series:
    return pd.Series({o: sum(weights[c] * s[c] for c in weights) for o, s in scores.items()}).round(3)

# %%
try:
    xs = exit_scores(exits)
except NotImplementedError:
    xs = {"O1": 1.0, "O2": 5.0, "O3": 4.4}
    print("(using the reference exit scores)")
scores = {o: {**s, "exit_cost": xs[o]} for o, s in criteria["scores"].items()}
base_score = weighted(criteria["weights"], scores)
print(pd.DataFrame(scores).T.assign(weighted=base_score).to_string())
A.check(base_score.idxmax() == "O1", "with exit cost at weight 0.10, O1 ranks first")

# %% [markdown]
# ## 3 · The weight that flips the ranking (6')
#
# A weighted score is only as good as its weights, and weights are opinions. ✏️ **Exercise** · Raise the weight
# of `exit_cost` from 0 to 0.6 in steps of 0.01, scaling the other weights so all still add up to 1, and return
# the first weight at which O1 is no longer first, with the new leader.

# %%
def flip_weight() -> tuple[float, str] | None:
    others = {c: w for c, w in criteria["weights"].items() if c != "exit_cost"}
    total = sum(others.values())
    # BEGIN SOLUTION
    for k in range(0, 61):
        w = k / 100
        weights = {c: v / total * (1 - w) for c, v in others.items()} | {"exit_cost": w}
        s = weighted(weights, scores)
        if s.idxmax() != "O1":
            return w, s.idxmax()
    return None
    # END SOLUTION

# %%
try:
    flip = flip_weight()
except NotImplementedError:
    flip = None
    print("(exercise not done)")
print("ranking flips at exit-cost weight:", flip)
if flip:
    A.check(flip[1] == "O2" and 0.10 < flip[0] < 0.6, "O2 overtakes O1 when exit cost weighs enough")

# %% [markdown]
# 🔍 **Look at** the flip weight. If the room would argue for a weight above it, the ranking is not robust and
# the decision record must say so. The pitfall is not having weights: it is reporting one ranking as if the
# weights were facts.

# %% [markdown]
# ## 4 · Two procurement requirements that keep the exit open (7')
#
# ✏️ **Exercise** · Write two requirements for O1's contract that cut its exit cost. Each must use "shall",
# name something a reviewer can verify (a format, a number of days, a standard interface) and address one of
# O1's factors. `lint_requirement` checks the form; the content is yours.

# %%
VERIFIABLE = re.compile(r"\d|JSON|CSV|Parquet|OpenAI-compatible|open format|standard", re.I)


def lint_requirement(r: str) -> list[str]:
    problems = []
    if " shall " not in f" {r} ":
        problems.append("no 'shall'")
    if not VERIFIABLE.search(r):
        problems.append("nothing a reviewer can verify (a number, a format, a standard interface)")
    if re.search(r"\b(best effort|as appropriate|reasonable|where possible)\b", r, re.I):
        problems.append("an escape phrase")
    return problems


def requirements() -> list[str]:
    # BEGIN SOLUTION
    return [
        "The provider shall export all indexed documents, their embeddings and metadata in an open format "
        "(JSON Lines or Parquet) within 10 working days of a request, at no extra charge.",
        "The service shall expose an OpenAI-compatible chat interface, and the Ministry shall be able to end "
        "the contract with 90 days' notice and no fee after the first 12 months.",
    ]
    # END SOLUTION

# %%
try:
    reqs = requirements()
except NotImplementedError:
    reqs = ["The provider shall export all indexed documents in JSON Lines within 10 working days of a request."]
    print("(using a reference requirement)")
for r in reqs:
    print("-", r, "->", lint_requirement(r) or "verifiable")
A.check(all(not lint_requirement(r) for r in reqs), "every requirement passes the lint")
print("lint of a weak one:", lint_requirement("The provider will make data available where possible."))

# %% [markdown]
# ## ✱ Stretch · The evaluation data
#
# O1 keeps the evaluation set and results in the provider's console (1.5 person-months to rebuild). Write the
# requirement that removes that factor.

# %%
def third_requirement() -> str:
    # BEGIN SOLUTION
    return ("Evaluation sets and every evaluation result shall be stored in the Ministry's repository in "
            "JSON Lines, and the provider's console shall not be their only copy.")
    # END SOLUTION


try:
    r3 = third_requirement()
    print(r3, "->", lint_requirement(r3) or "verifiable")
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. O1 costs least to run and most to leave. Does that rule it out?
# 2. Why scale the other weights when you raise one?
# 3. Which of O1's factors does an OpenAI-compatible interface not touch?
#
# <details><summary>Answers</summary>
#
# 1. No. It means the exit must be bought down in the contract, and the record names the exit cost.
# 2. So the weights still add up to 1 and only the balance between criteria changes.
# 3. The vector store with no bulk export: the interface moves the calls, not the data.
# </details>
#
# **Carry forward.** The exit costs, the flip weight and the requirements are the lock-in section of the options paper.
