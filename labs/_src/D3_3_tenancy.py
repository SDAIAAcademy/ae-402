# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 3.3 · Three incidents, two tenancy models
#
# Day 3 · Session 3 (Tenancy and shared capacity) · 25 min.
#
# In the pilot, all nine teams shared one gateway key, one budget and the Ministry-hosted model's capacity. You
# replay one working hour three times, with a leaked key, a noisy neighbour and a runaway agent, first under
# the pilot's shared model, then under a tenancy model you design: a key per team, a cap on each team's share of
# the Ministry-hosted model, a budget per key and revocation of a key that spikes. The measure is what happens
# to the teams that did nothing wrong.
#
# **Reference state.** `asas_tenancy.py`: a deterministic minute-by-minute replay of nine teams' demand, with
# the three incidents. No data from earlier labs.
#
# **Tasks**
# - [ ] 1 · Replay the three incidents on the shared model (5')
# - [ ] 2 · A capped share of the Ministry-hosted model (7')
# - [ ] 3 · Your tenancy model: keys, budgets, revocation (6')
# - [ ] 4 · The incident table: who was harmed (7')
# - [ ] ✱ Stretch · The cap that costs the culprit least

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
import asas_tenancy as T

INCIDENTS = list(T.INCIDENTS)
print("own-model capacity:", T.OWN_CAPACITY, "requests a minute; incidents:")
for k, v in T.INCIDENTS.items():
    print(f"  {k:16s}", v)

# %% [markdown]
# ## 1 · Replay the three incidents on the shared model (5')
#
# The pilot's model: `T.Tenancy()` with its defaults. Run each incident and look at the worst service any
# bystander got.

# %%
shared = T.Tenancy(shared_budget_sar=150.0)
quiet = T.run(shared, None)
print("a quiet hour costs", quiet["total_spend"], "SAR; bystanders:", T.bystanders(quiet))
for inc in INCIDENTS:
    print(f"{inc:16s}", T.bystanders(T.run(shared, inc)))

# %% [markdown]
# 🔍 **Look at** the leaked key and the runaway agent: neither touches the Ministry-hosted model, and both cut
# every team off paid models, because one shared budget runs out for everyone. With one shared key, the only
# way to stop the leak is to revoke the key all nine teams use.

# %% [markdown]
# ## 2 · A capped share of the Ministry-hosted model (7')
#
# ✏️ **Exercise** · Write `capped(demand, capacity, cap)`: no team gets more than `cap` times the capacity in a
# minute; capacity a team does not use goes to the others, still under the cap (fill the smallest demands
# first). Return the served requests per team.

# %%
def capped(demand: dict, capacity: int, cap: float | None) -> dict:
    # BEGIN SOLUTION
    limit = capacity * cap if cap else capacity
    served = {t: 0.0 for t in demand}
    left = capacity
    pending = sorted(demand, key=lambda t: demand[t])
    while pending and left > 1e-9:
        fair = left / len(pending)
        t = pending[0]
        want = min(demand[t], limit) - served[t]
        if want <= fair:
            served[t] += want
            left -= want
            pending.pop(0)
        else:
            for u in pending:
                served[u] += fair
            left = 0
    return served
    # END SOLUTION

# %%
demand = {"T01": 10, "T08": 314, "T06": 12, "T04": 2}
try:
    got = capped(demand, 120, 0.3)
except NotImplementedError:
    got = {"T01": 10, "T08": 36, "T06": 12, "T04": 2}
    print("(using the reference allocation)")
print({k: round(v, 1) for k, v in got.items()})
A.check(abs(got["T08"] - 36) < 1e-6 and got["T01"] == 10, "the noisy team is held to 30%; the others get all they ask")

# %% [markdown]
# ## 3 · Your tenancy model: keys, budgets, revocation (6')
#
# ✏️ **Exercise** · Return a `T.Tenancy` with a key per team, your allocation function and cap, a budget per key
# for the hour, and revocation of a key whose paid rate exceeds five times its normal rate. A quiet hour costs
# each team at most about SAR 36 (`quiet["rows"]`): set the budget so no team is stopped in a quiet hour.

# %%
def my_tenancy() -> T.Tenancy:
    # BEGIN SOLUTION
    return T.Tenancy(per_team_keys=True, allocate=capped, own_share_cap=0.3, budget_per_key_sar=60.0,
                     revoke_on_spike=True)
    # END SOLUTION

# %%
try:
    mine = my_tenancy()
except NotImplementedError:
    mine = T.Tenancy(per_team_keys=True, allocate=T.proportional, own_share_cap=None, budget_per_key_sar=60.0,
                     revoke_on_spike=True)
    print("(using a reference tenancy without a cap)")
q = T.run(mine, None)
A.check(T.bystanders(q)["worst_paid_served_pct"] == 100.0, "nobody is stopped in a quiet hour")

# %% [markdown]
# ## 4 · The incident table: who was harmed (7')
#
# ✏️ **Exercise** · One row per incident and tenancy model, with the worst own-model and paid service of any
# bystander, the culprit's spend, and when the leaked key was revoked.

# %%
def incident_table(models: dict) -> pd.DataFrame:
    # BEGIN SOLUTION
    rows = []
    for inc in INCIDENTS:
        for name, ten in models.items():
            r = T.run(ten, inc)
            culprit = next(x for x in r["rows"] if x["culprit"])
            rows.append({"incident": inc, "tenancy": name, **T.bystanders(r),
                         "culprit_spend_sar": culprit["spend_sar"], "revoked_at_minute": r["revoked_at"]})
    return pd.DataFrame(rows)
    # END SOLUTION

# %%
try:
    table = incident_table({"shared": shared, "per team": mine})
except NotImplementedError:
    table = pd.DataFrame([{"incident": i, "tenancy": n, **T.bystanders(T.run(t, i))}
                          for i in INCIDENTS for n, t in {"shared": shared, "per team": mine}.items()])
print(table.to_string(index=False))
per_team = table[table.tenancy == "per team"]
A.check((per_team.worst_paid_served_pct == 100.0).all(), "under the per-team model no bystander loses a paid request")
A.check(table[(table.tenancy == "shared") & (table.incident == "runaway_agent")].worst_paid_served_pct.iloc[0] < 60,
        "under the shared model the runaway agent cuts the other teams off")
out = A.lab_dir("D3_3") / "incidents.csv"
table.to_csv(out, index=False)
print("saved", out.relative_to(A.LABS).as_posix())

# %% [markdown]
# 🔍 **Look at** the noisy neighbour under your model: bystanders keep their own-model service only if the cap
# is there. Budgets and revocation do nothing for capacity; a cap does nothing for spend. Each incident needs its
# own control, and the tenancy model is the set of them. Kill switches per agent version are AE-305's subject;
# here the point is that one team's incident stays that team's incident.

# %% [markdown]
# ## ✱ Stretch · The cap that costs the culprit least
#
# Try caps of 0.2, 0.3, 0.4 and 0.5 on the noisy neighbour. Which is the largest cap at which no bystander
# loses own-model service?

# %%
def best_cap() -> float | None:
    # BEGIN SOLUTION
    ok = [c for c in (0.2, 0.3, 0.4, 0.5)
          if T.bystanders(T.run(T.Tenancy(per_team_keys=True, allocate=capped, own_share_cap=c,
                                          budget_per_key_sar=60.0), "noisy_neighbour"))["worst_own_served_pct"] == 100.0]
    return max(ok) if ok else None
    # END SOLUTION


try:
    print("largest safe cap:", best_cap())
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does a shared key turn a leak at one team into an outage for nine?
# 2. Which control limits a noisy neighbour, and which a runaway agent?
# 3. What does revocation cost the team whose key leaked, and why is that acceptable?
#
# <details><summary>Answers</summary>
#
# 1. The only way to stop the leak is to revoke the key everybody uses, and until then the shared budget burns.
# 2. A cap on the share of shared capacity; a budget per key.
# 3. Five minutes without paid models until its new key; it is that team's incident, contained to that team.
# </details>
#
# **Carry forward.** `artifacts/D3_3/incidents.csv` is the tenancy section's evidence in the platform design.
