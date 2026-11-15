# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 3.4 · A showback that reconciles with the invoices
#
# Day 3 · Session 4 (Who pays for which tokens) · 25 min.
#
# Nisreen Al-Mehaimeed, the finance and cost lead, wants each team to see what its AI use costs before anyone
# is charged for it. You build the showback twice: first by pricing usage with the platform's price card, which
# fails to reconcile with the invoices in three months, then by allocating each invoice line to teams by usage.
# You name the spend that no tag explains, and the outcome's test is applied: the showback reconciles with every
# invoice within 2%.
#
# **Reference state.** `data/platform/usage.csv`, `keys.csv`, `invoices.csv` (three providers, six months) and
# `price_card.json`, all synthetic. Nothing from earlier labs.
#
# **Tasks**
# - [ ] 1 · A showback priced with the price card (6')
# - [ ] 2 · Reconcile it with each invoice (5')
# - [ ] 3 · Allocate the invoices instead (8')
# - [ ] 4 · Name the untagged spend (6')
# - [ ] ✱ Stretch · Is token count the right key for the data centre?

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
keys = A.read_csv("platform/keys.csv")
invoices = A.read_csv("platform/invoices.csv")
card = A.read_json("platform/price_card.json")
usage["month"] = usage.date.str[:7]
HOSTING = {"ext-frontier-l": "external", "ksa-general-m": "ksa_cloud", "ksa-vision-x": "ksa_cloud",
           "own-open-s": "ministry", "own-embed-m": "ministry", "own-speech-s": "ministry"}
PROVIDER = {"external": "External Provider", "ksa_cloud": "In-Kingdom Cloud", "ministry": "Ministry Data Centre"}
usage["provider"] = usage.model.map(HOSTING).map(PROVIDER)
print(invoices.groupby(["provider", "month"]).amount_sar.sum().unstack().round(0))
print(card["note"])

# %% [markdown]
# ## 1 · A showback priced with the price card (6')
#
# ✏️ **Exercise** · Price each usage row with the card (SAR per million input and output tokens); give the
# Ministry Data Centre's fixed cost to its models' rows in proportion to their tokens. Attribute rows to the
# team in `team_tag`; leave untagged rows as `untagged` for now. Return `usage` with a `card_sar` column.

# %%
def price_with_card(u: pd.DataFrame) -> pd.DataFrame:
    u = u.copy()
    # BEGIN SOLUTION
    pm = card["per_million"]
    u["card_sar"] = [(r.in_tokens * pm[r.model]["in"] + r.out_tokens * pm[r.model]["out"]) / 1e6
                     if r.model in pm else 0.0 for r in u.itertuples()]
    own = u.provider == "Ministry Data Centre"
    tok = (u.in_tokens + u.out_tokens).where(own, 0)
    month_tok = tok.groupby(u.month).transform("sum")
    u.loc[own, "card_sar"] = (card["ministry_fixed_per_month"] * tok / month_tok)[own]
    # END SOLUTION
    return u

# %%
try:
    priced = price_with_card(usage)
except NotImplementedError:
    priced = None
    print("(exercise not done: steps 2 and 4 use the allocation of step 3 only)")
if priced is not None:
    print(priced.assign(team=priced.team_tag.fillna("untagged")).pivot_table(
        index="team", columns="month", values="card_sar", aggfunc="sum").round(0))

# %% [markdown]
# ## 2 · Reconcile it with each invoice (5')
#
# ✏️ **Exercise** · Per provider and month, compare the card-priced total with the invoice total. Return a table
# with both, the difference in percent, and whether it is within 2%.

# %%
def reconcile(u: pd.DataFrame, col: str) -> pd.DataFrame:
    # BEGIN SOLUTION
    ours = u.groupby(["provider", "month"])[col].sum()
    bill = invoices.groupby(["provider", "month"]).amount_sar.sum()
    t = pd.DataFrame({"showback": ours, "invoice": bill}).fillna(0.0)
    t["diff_pct"] = (100 * (t.showback - t.invoice) / t.invoice).round(2)
    t["within_2pct"] = t.diff_pct.abs() <= 2
    return t.reset_index()
    # END SOLUTION

# %%
if priced is not None:
    try:
        rec_card = reconcile(priced, "card_sar")
        print(rec_card[~rec_card.within_2pct].to_string(index=False))
        A.check((~rec_card.within_2pct).sum() == 3, "three invoices do not reconcile with the price card")
    except NotImplementedError:
        print("(exercise not done)")

# %% [markdown]
# 🔍 **Look at** the three months. August: the In-Kingdom Cloud gave an onboarding credit the card does not know.
# September and October: the External Provider cut its output price and the card was not updated. A showback
# that reprices usage drifts from the bill; finance stops trusting it the first month it does.

# %% [markdown]
# ## 3 · Allocate the invoices instead (8')
#
# ✏️ **Exercise** · Share every invoice line among the usage rows it covers: a model's input-token line by the
# rows' input tokens, its output line by output tokens, the data centre's fixed line by tokens of
# Ministry-hosted models, a credit (a line with no model) by the rows' card value on that provider. Return `usage` with an
# `alloc_sar` column. Then attribute each row to the **owner of its key** (`keys.csv`), not to its tag.

# %%
def allocate(u: pd.DataFrame) -> pd.DataFrame:
    u = u.copy()
    pm = card["per_million"]
    u["value"] = [(r.in_tokens * pm[r.model]["in"] + r.out_tokens * pm[r.model]["out"]) / 1e6
                  if r.model in pm else 0.0 for r in u.itertuples()]
    u["alloc_sar"] = 0.0
    # BEGIN SOLUTION
    for line in invoices.itertuples():
        m = u.month == line.month
        if line.model == "own-*":
            sel, w = m & (u.provider == line.provider), u.in_tokens + u.out_tokens
        elif pd.isna(line.model):  # a credit: no model
            sel, w = m & (u.provider == line.provider), u.value
        else:
            sel = m & (u.model == line.model)
            w = u.in_tokens if line.line.endswith("input tokens") else u.out_tokens
        total = w[sel].sum()
        if total:
            u.loc[sel, "alloc_sar"] += line.amount_sar * w[sel] / total
    # END SOLUTION
    u["team"] = u.key_id.map(dict(zip(keys.key_id, keys.team))).fillna("")
    return u

# %%
try:
    alloc = allocate(usage)
    rec = reconcile(alloc, "alloc_sar")
except NotImplementedError:
    alloc = None
    print("(exercise not done)")
if alloc is not None:
    print(rec.to_string(index=False))
    A.check(rec.within_2pct.all(), "every invoice reconciles within 2%")
    showback = alloc[alloc.team != ""].groupby("team").alloc_sar.sum().round(2)
    ref = A.reference("showback")
    A.check(all(abs(showback[t] - v) < 0.05 for t, v in ref["by_team"].items()), "team totals match the reference")
    print(showback.sort_values(ascending=False).map(A.sar))

# %% [markdown]
# ## 4 · Name the untagged spend (6')
#
# ✏️ **Exercise** · Two kinds of spend have no team tag. Rows with a blank tag whose key has an owner: attribute
# them (already done by the key) and count them. Rows whose key has no owner: name the key, its spend and the
# capability it calls. Return a dict.

# %%
def untagged(a: pd.DataFrame) -> dict:
    # BEGIN SOLUTION
    known = a[a.team_tag.isna() & (a.team != "")]
    orphan = a[a.team == ""]
    return {"blank_tag_known_key_rows": int(len(known)),
            "blank_tag_known_key_sar": round(float(known.alloc_sar.sum()), 2),
            "orphan_keys": sorted(orphan.key_id.unique()),
            "orphan_sar": round(float(orphan.alloc_sar.sum()), 2),
            "orphan_capabilities": sorted(orphan.capability.unique())}
    # END SOLUTION

# %%
ref = A.reference("showback")
try:
    named = untagged(alloc) if alloc is not None else None
except NotImplementedError:
    named = None
if named is None:
    named = {"orphan_keys": ["k-legacy-01"], "orphan_sar": ref["unallocated_legacy_key"],
             "blank_tag_known_key_rows": ref["untagged_rows_with_known_key"]}
    print("(using the reference)")
print(named)
A.check(named["orphan_keys"] == ["k-legacy-01"] and abs(named["orphan_sar"] - ref["unallocated_legacy_key"]) < 0.05,
        f"k-legacy-01 holds SAR {ref['unallocated_legacy_key']:,.2f} that no team owns")
total = ref["invoice_total"]
print(f"orphan share of the six months' invoices: {100 * named['orphan_sar'] / total:.2f}%")
if alloc is not None:
    out = A.lab_dir("D3_4") / "showback.csv"
    alloc.groupby(["month", "team"]).alloc_sar.sum().round(2).unstack().to_csv(out)
    print("saved", out.relative_to(A.LABS).as_posix())

# %% [markdown]
# The orphan key is small, and that is the point: nobody owns it, so nobody would notice it growing, and it
# calls a cloud model that can receive Restricted data. The fix is not in the showback: no key without an owner.

# %% [markdown]
# ## ✱ Stretch · Is token count the right key for the data centre?
#
# The contact team's speech model counts many tokens per call and takes most of the fixed cost. Allocate the
# data-centre line by requests instead and compare the contact team's share. Which key would you defend, and why?

# %%
def by_requests() -> pd.Series:
    # BEGIN SOLUTION
    own = alloc[alloc.provider == "Ministry Data Centre"]
    fixed = invoices[invoices.provider == "Ministry Data Centre"].amount_sar.sum()
    by_tok = own.groupby("team").alloc_sar.sum() / fixed
    by_req = own.groupby("team").requests.sum() / own.requests.sum()
    return pd.DataFrame({"share_by_tokens": by_tok.round(3), "share_by_requests": by_req.round(3)})
    # END SOLUTION


try:
    print(by_requests())
except (NotImplementedError, AttributeError, TypeError):
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why allocate the invoice rather than price usage with a card?
# 2. Why attribute by key owner and not by tag?
# 3. Why showback before chargeback?
#
# <details><summary>Answers</summary>
#
# 1. The invoice is what the Ministry pays; a card drifts with every price change and credit.
# 2. The gateway knows the key for every call; a tag is whatever the caller remembered to send.
# 3. Teams see and question their costs before money moves; the allocation keys get argued and fixed while
#    nobody's budget depends on them.
# </details>
#
# **Carry forward.** `artifacts/D3_4/showback.csv` is the showback of the capstone's platform slice.
