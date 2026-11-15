# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 2.2 · Three options over three years
#
# Day 2 · Session 2 (Total cost over three years) · 25 min.
#
# Three ways to build Muyassir: O1, a generative assistant on a model hosted in the Kingdom and paid per token;
# O2, the same on an open-weight model the Ministry hosts; O3, a non-generative guided search with a document
# checklist. You write one cost model, run it on the three-year forecast, then move volume and token price one
# at a time and see which assumption the ranking really depends on.
#
# **Reference state.** `data/options/forecast.csv` (36 months, low, base and high) and
# `data/options/prices.json` (the case's price ranges: **synthetic, not vendor prices**). Nothing from Lab 2.1.
#
# **Tasks**
# - [ ] 1 · Read the forecast and the price ranges (3')
# - [ ] 2 · The cost model, year by year (9')
# - [ ] 3 · Three options at the base forecast (5')
# - [ ] 4 · Sensitivity to volume and token price (8')
# - [ ] ✱ Stretch · The crossover volume

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

import math
import pandas as pd
import asas as A

forecast = A.read_csv("options/forecast.csv")
prices = A.read_json("options/prices.json")
OPTIONS = {o["id"]: o for o in prices["options"]}

# %% [markdown]
# ## 1 · Read the forecast and the price ranges (3')

# %%
print(forecast.groupby("year")[["low", "base", "high"]].sum())
for o in prices["options"]:
    print(o["id"], o["name"], "| coverage", o["coverage"])
print({k: v for k, v in prices.items() if k not in ("options",)})

# %% [markdown]
# ## 2 · The cost model, year by year (9')
#
# ✏️ **Exercise** · Write `year_cost(option, months, price_mult)` for one year (`months` is that year's rows,
# with a column `requests`). Five lines, all from `prices.json`:
#
# 1. **build**, in year 1 only;
# 2. **fixed run** cost and **people** (`people_fte` times `person_year_sar`);
# 3. **tokens**: requests times tokens per request times price per million, times `price_mult`;
# 4. **capacity units** for a Ministry-hosted model: enough units for the **peak** month;
# 5. **unanswered questions**: requests not covered by the option become calls for a share of them
#    (`call_share_of_unanswered` times `call_cost_sar`). A cheap option that answers less moves cost to the
#    contact centre; the Ministry pays both.
#
# Return a dict of the five lines.

# %%
def year_cost(o: dict, months: pd.DataFrame, year: int, price_mult: float = 1.0) -> dict:
    vol = months.requests.sum()
    # BEGIN SOLUTION
    tokens = vol * (o["in_tokens"] * o["sar_per_m_in"] + o["out_tokens"] * o["sar_per_m_out"]) / 1e6 * price_mult
    units = 0.0
    if o.get("unit_capacity_per_month"):
        units = math.ceil(months.requests.max() / o["unit_capacity_per_month"]) * o["unit_sar_per_year"]
    return {
        "build": o["build_sar"] if year == 1 else 0.0,
        "run_and_people": o["fixed_run_sar_per_year"] + o["people_fte"] * prices["person_year_sar"],
        "tokens": tokens,
        "capacity_units": units,
        "unanswered_calls": vol * (1 - o["coverage"]) * prices["call_share_of_unanswered"] * prices["call_cost_sar"],
    }
    # END SOLUTION


def three_years(volume: str = "base", price_mult: float = 1.0) -> pd.DataFrame:
    rows = []
    for oid, o in OPTIONS.items():
        for y in (1, 2, 3):
            months = forecast[forecast.year == y].rename(columns={volume: "requests"})
            try:
                lines = year_cost(o, months, y, price_mult)
            except NotImplementedError:
                lines = {"total": A.reference("three_year_cost")["base_years"][oid][str(y)]}
            rows.append({"option": oid, "year": y, **lines})
    df = pd.DataFrame(rows).fillna(0.0)
    df["total"] = df.drop(columns=["option", "year"]).sum(axis=1) if "build" in df else df["total"]
    return df

# %%
base = three_years()
print(base.round(0).to_string(index=False))
ref = A.reference("three_year_cost")
totals = base.groupby("option").total.sum().round(0)
A.check(all(abs(totals[o] - ref["base"][o]) < 2 for o in OPTIONS), "three-year totals match the reference")

# %% [markdown]
# ## 3 · Three options at the base forecast (5')
#
# ✏️ **Exercise** · Make the options table of the options paper: per option, the three-year total, the cost
# per answered question (total divided by requests times coverage), and the first-year run cost (everything
# but build), to compare with the sponsor's SAR 1.2 million cap (S04).

# %%
def options_table(df: pd.DataFrame) -> pd.DataFrame:
    vol = forecast.base.sum()
    # BEGIN SOLUTION
    rows = []
    for oid, o in OPTIONS.items():
        d = df[df.option == oid]
        y1 = d[d.year == 1].iloc[0]
        rows.append({"option": oid, "three_year_sar": round(d.total.sum()),
                     "sar_per_answered": round(d.total.sum() / (vol * o["coverage"]), 3),
                     "year1_run_sar": round(y1.total - y1.build)})
    return pd.DataFrame(rows)
    # END SOLUTION

# %%
try:
    paper = options_table(base)
except NotImplementedError:
    paper = pd.DataFrame([{"option": k, "three_year_sar": v} for k, v in ref["base"].items()])
    print("(using the reference totals)")
print(paper.to_string(index=False))
A.check(paper.sort_values("three_year_sar").option.iloc[0] == "O1", "O1 is the cheapest at the base forecast")

# %% [markdown]
# 🔍 **Look at** O3. It is the cheapest to build and to run, and the most expensive in total: 30% of questions
# go unanswered and a share of them become calls. The non-generative baseline is a real option for Muyassir and
# it loses here on coverage, the way the generative router lost to the classifier in Lab 2.1.
#
# Look also at the first-year run cost of O1 against the SAR 1.2 million cap: the unanswered calls are counted
# here because the Ministry pays them, though not from the run budget. Say which line the cap covers.

# %% [markdown]
# ## 4 · Sensitivity to volume and token price (8')
#
# ✏️ **Exercise** · Move one assumption at a time: volume `low` and `high`, token price times 0.5 and times 2.
# Return a table with one row per option and one column per case, plus the base. This is the data of a
# tornado chart.

# %%
def sensitivity() -> pd.DataFrame:
    # BEGIN SOLUTION
    cases = {"base": ("base", 1.0), "volume_low": ("low", 1.0), "volume_high": ("high", 1.0),
             "price_low": ("base", 0.5), "price_high": ("base", 2.0)}
    out = {}
    for name, (vol, mult) in cases.items():
        out[name] = three_years(vol, mult).groupby("option").total.sum().round(0)
    return pd.DataFrame(out)
    # END SOLUTION

# %%
try:
    sens = sensitivity()
except NotImplementedError:
    sens = pd.DataFrame(ref["tornado"]).T
    print("(using the reference sensitivity)")
print(sens.astype(int).to_string())
swing = (sens.max(axis=1) - sens.min(axis=1)).astype(int)
print("swing per option:", swing.to_dict())
A.check(abs(sens.loc["O1", "volume_high"] - ref["tornado"]["O1"]["volume_high"]) < 2,
        "O1 at the high forecast matches the reference")
both = three_years("high", 2.0).groupby("option").total.sum().round(0)
print("high volume and double price together:", both.astype(int).to_dict())

# %% [markdown]
# 🔍 **Look at** the two token-price columns of O1: doubling the price moves its three-year total by about
# 3%. Volume moves it by more than half. The ranking does not depend on the token price at this forecast; it
# depends on volume and on coverage. That is where the review trigger of the decision goes.

# %% [markdown]
# ## ✱ Stretch · The crossover volume
#
# At what steady monthly volume would O2 (Ministry-hosted) cost the same as O1 over three years? Try it at the
# base token price and at double the price.

# %%
def crossover(mult: float) -> int | None:
    # BEGIN SOLUTION
    global forecast
    saved = forecast
    try:
        for v in range(100000, 3000001, 10000):
            forecast = saved.assign(base=v)
            t = three_years("base", mult).groupby("option").total.sum()
            if t["O2"] <= t["O1"]:
                return v
        return None
    finally:
        forecast = saved
    # END SOLUTION


try:
    print("base price:", crossover(1.0), "| double price:", crossover(2.0))
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is the cost of unanswered questions part of an option's cost?
# 2. Doubling the token price barely moves O1. What would make the token price matter?
# 3. Which single number would you put in O1's review trigger?
#
# <details><summary>Answers</summary>
#
# 1. The Ministry pays for the calls that a low-coverage option creates; leaving them out favours O3.
# 2. Far more tokens per request (long contexts, agent loops) or far higher volume.
# 3. Monthly requests: O2 overtakes O1 only at high volume and a higher price; the stretch gives the number.
# </details>
#
# **Carry forward.** The options table and the sensitivity table are the cost section of the options paper.
