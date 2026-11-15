# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 1.3 · Classified flows and placement
#
# Day 1 · Session 3 (Regulation as a design constraint) · 25 min.
#
# Classification is an input to the architecture, not a form filled after it. You complete the Ministry's
# data inventory, give each of Muyassir's fourteen data flows the level of the most sensitive item it
# carries, derive where each flow may be processed under the Ministry's placement rule, and find the flows
# that break it.
#
# **Reference state.** `data/case/data_inventory.csv` (24 items, three without a level) and
# `data/case/muyassir_flows.csv` (14 flows). Nothing from earlier labs.
#
# **The Ministry's placement rule (Asas policy P-01, part of the case).** Public data may be processed by the
# Ministry, by a cloud region in the Kingdom or by an external service. Restricted data: the Ministry or a
# cloud region in the Kingdom. Secret data: the Ministry only. The rule is the Ministry's own; it is stricter
# than the minimum the national texts set, by the Ministry's choice.
#
# **Tasks**
# - [ ] 1 · Fill the three blank levels (5')
# - [ ] 2 · The level of each flow (6')
# - [ ] 3 · Where each flow may go (6')
# - [ ] 4 · The violations and what each breaks (8')
# - [ ] ✱ Stretch · Redesign the violating flows

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

inventory = A.read_csv("case/data_inventory.csv")
flows = A.read_csv("case/muyassir_flows.csv")
print(inventory.to_string(index=False))

# %% [markdown]
# ## 1 · Fill the three blank levels (5')
#
# ✏️ **Exercise** · Three items have no level. Use two rules of the session: personal data is never Public
# here, and a text is Public only once it is published or approved for publication. Return
# `{item id: level}` for the three.

# %%
def fill_blanks(inv: pd.DataFrame) -> dict[str, str]:
    blanks = inv[inv.level.isna()]
    # BEGIN SOLUTION
    out = {}
    for _, r in blanks.iterrows():
        if r.personal_data == 1:
            out[r.id] = "Restricted"
        elif "not yet published" in r["item"].lower() or "draft" in r["item"].lower():
            out[r.id] = "Restricted"
        else:
            out[r.id] = "Public"
    return out
    # END SOLUTION

# %%
key_levels = A.reference("inventory_levels")
try:
    filled = fill_blanks(inventory)
except NotImplementedError:
    filled = {i: key_levels[i] for i in inventory[inventory.level.isna()].id}
    print("(using the reference levels)")
print(filled)
A.check(filled == {i: key_levels[i] for i in filled} and len(filled) == 3, "D07, D09 and D12 classified")
levels = dict(zip(inventory.id, inventory.level))
levels.update(filled)

# %% [markdown]
# ## 2 · The level of each flow (6')
#
# ✏️ **Exercise** · A flow carries one or more items (`items`, separated by `;`). By the policy's highest-level
# principle, a set that combines levels takes the highest. Write `flow_level(items)`; `A.highest` and
# `A.LEVELS` may help.

# %%
def flow_level(items: str) -> str:
    # BEGIN SOLUTION
    return A.highest([levels[i] for i in items.split(";")])
    # END SOLUTION

# %%
key = A.reference("flows_key")
try:
    flows["level"] = flows["items"].map(flow_level)
except NotImplementedError:
    flows["level"] = flows.id.map(lambda i: key[i]["level"])
    print("(using the reference levels)")
print(flows[["id", "source", "target", "items", "level"]].to_string(index=False))
A.check(all(flows.set_index("id").level[i] == key[i]["level"] for i in key), "all fourteen flow levels right")
A.check(flows.set_index("id").level["F11"] == "Restricted", "F11 mixes Public code with Restricted files: Restricted")

# %% [markdown]
# ## 3 · Where each flow may go (6')
#
# ✏️ **Exercise** · Add two columns: `allowed`, the hostings the rule allows for the flow's level, and
# `ok`, whether the flow's `target_hosting` is one of them. `A.HOSTING_ALLOWED` holds the rule.

# %%
def place(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # BEGIN SOLUTION
    df["allowed"] = df.level.map(lambda l: ", ".join(h for h in A.HOSTINGS if A.allowed(l, h)))
    df["ok"] = [A.allowed(l, h) for l, h in zip(df.level, df.target_hosting)]
    # END SOLUTION
    return df

# %%
try:
    placed = place(flows)
except NotImplementedError:
    placed = flows.assign(allowed=flows.id.map(lambda i: ", ".join(key[i]["allowed"])),
                          ok=flows.id.map(lambda i: not key[i]["violation"]))
    print("(using the reference placement)")
print(placed[["id", "target", "level", "target_hosting", "allowed", "ok"]].to_string(index=False))

# %% [markdown]
# ## 4 · The violations and what each breaks (8')
#
# ✏️ **Exercise** · List the flows that break the rule. For each, name the item that makes it break, the
# statement of Lab 1.1 it contradicts (S12, S13 or S15) and one sentence on the fix.

# %%
def violations(df: pd.DataFrame) -> list[dict]:
    # BEGIN SOLUTION
    notes = {
        "F07": ("D05", "S12", "Run OCR inside the Ministry or in a cloud region in the Kingdom"),
        "F09": ("D07", "S13", "Build the dashboard from aggregated counts in the Ministry; no raw logs leave"),
        "F14": ("D09", "S15", "Summarise drafts with a model in the Kingdom; only published texts go external"),
    }
    return [{"flow": i, "item": notes[i][0], "contradicts": notes[i][1], "fix": notes[i][2]}
            for i in df[~df.ok].id]
    # END SOLUTION

# %%
try:
    found = violations(placed)
except NotImplementedError:
    found = [{"flow": i, "item": "", "contradicts": "", "fix": ""} for i, v in key.items() if v["violation"]]
    print("(using the reference list)")
print(pd.DataFrame(found).to_string(index=False))
A.check({f["flow"] for f in found} == {i for i, v in key.items() if v["violation"]},
        "the three violating flows: F07, F09 and F14")
out = A.lab_dir("D1_3") / "flows_classified.csv"
placed.to_csv(out, index=False)
print("saved", out.relative_to(A.LABS).as_posix())

# %% [markdown]
# 🔍 **Look at** F14. The data protection officer assumed (S15) that the regulation documents may go to any
# model. The draft circulars are regulation documents too, but not yet published. An assumption that is never
# checked becomes a violation.
#
# Look also at F04: the published code goes to an external embedding model, and that is allowed. The rule
# does not say "keep everything inside"; it says where each level may go.

# %% [markdown]
# ## ✱ Stretch · Redesign the violating flows
#
# For each violating flow, change `target_hosting` to the least restrictive hosting that is allowed, and say
# what that costs (a new service in the Ministry, a model in the Kingdom with other quality).

# %%
def redesign(df: pd.DataFrame) -> pd.DataFrame:
    # BEGIN SOLUTION
    fixed = df.copy()
    order = ["external", "ksa_cloud", "ministry"]
    for i in fixed.index[~fixed.ok]:
        fixed.loc[i, "target_hosting"] = next(h for h in order if A.allowed(fixed.loc[i, "level"], h))
    fixed["ok"] = [A.allowed(l, h) for l, h in zip(fixed.level, fixed.target_hosting)]
    return fixed
    # END SOLUTION


try:
    fixed = redesign(placed)
    print(fixed[placed.ok == False][["id", "level", "target_hosting", "ok"]].to_string(index=False))
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. A prompt holds a public clause and an applicant's national identity number. What is its level?
# 2. Why is "anonymised" in an item's name not enough to make it Public?
# 3. Which flow would change if the Ministry decided to allow Restricted data in an approved external region?
#
# <details><summary>Answers</summary>
#
# 1. Restricted: the highest level of what it carries.
# 2. The level follows the impact of disclosure, assessed by the data owner; a name is a claim, not an assessment.
# 3. F07 and F09 would become allowed by the rule, and the transfer conditions of the national regulation
#    would then apply to the personal data in them.
# </details>
#
# **Carry forward.** `artifacts/D1_3/flows_classified.csv`. Lab 1.4 starts from the supplied model of Muyassir.
