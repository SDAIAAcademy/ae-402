# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 4.4 · A deviation request, decided and explained on one page
#
# Day 4 · Session 4 (Deviations and sponsors) · 25 min.
#
# Rabah Al-Mujil, lead of the inspections team, asks the board to let Kashif send inspection photos to an
# external vision model for twelve months. It breaks placement rule P-01, and refusing it has a cost too. You
# put numbers on both, decide (refuse, approve as asked, or approve with conditions and an expiry), and write
# the one page Dr. Afrah Al-Dughaither, the sponsor, will read. Then you choose your capstone service.
#
# **Reference state.** `data/deviation/request.md`, `data/deviation/facts.json`,
# `data/deviation/photo_sample.csv` (400 labelled photos and what the on-device detector flagged, synthetic)
# and `capstone/briefs/`. Nothing from Lab 4.3.
#
# **Tasks**
# - [ ] 1 · What the request breaks, and what refusing costs (6')
# - [ ] 2 · Decide, with conditions, an expiry and what reopens it (7')
# - [ ] 3 · One page for the sponsor (7')
# - [ ] 4 · Choose your capstone service (5')
# - [ ] ✱ Stretch · The deviation as a gateway policy that expires

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
from datetime import date
import pandas as pd
import asas as A
import asas_gateway as G

print(A.read_text("deviation/request.md"))
facts = A.read_json("deviation/facts.json")
photos = A.read_csv("deviation/photo_sample.csv")
print({k: v for k, v in facts.items() if k != "note"})

# %% [markdown]
# ## 1 · What the request breaks, and what refusing costs (6')
#
# ✏️ **Exercise** · From the sample and the facts, return a dict with: the share of photos that hold Restricted
# content (a face, a plate or a document); Restricted photos a month that would leave the Kingdom **as asked**;
# the share of photos the on-device detector passes as clean; Restricted photos a month that would still leave
# if only clean photos went (the detector's misses); and the inspector time a month that refusing costs, in
# SAR, against reports drafted with Kashif.

# %%
def numbers() -> dict:
    # BEGIN SOLUTION
    n = len(photos)
    restricted = (photos.has_face | photos.has_plate | photos.has_document).astype(bool)
    clean = photos.detector_flags == 0
    per_month = facts["photos_per_month"]
    reports = per_month / facts["photos_per_report"]
    saved_min = facts["manual_minutes_per_report"] - facts["assisted_minutes_per_report"]
    return {"restricted_share": round(restricted.mean(), 4),
            "restricted_out_as_asked": round(restricted.mean() * per_month),
            "clean_share": round(clean.mean(), 4),
            "restricted_out_if_clean_only": round((restricted & clean).sum() / n * per_month),
            "refusal_cost_sar_month": round(reports * saved_min / 60 * facts["inspector_cost_sar_per_hour"]),
            "ext_vision_sar_month_clean_only": round(clean.mean() * per_month * facts["ext_vision_sar_per_photo"])}
    # END SOLUTION

# %%
ref = A.reference("deviation")
try:
    num = numbers()
except NotImplementedError:
    num = {"restricted_share": ref["restricted_share"], "restricted_out_as_asked": 5445,
           "clean_share": ref["sent_share"], "restricted_out_if_clean_only": 90,
           "refusal_cost_sar_month": 96000, "ext_vision_sar_month_clean_only": 234}
    print("(using the reference numbers)")
print(num)
A.check(abs(num["restricted_share"] - ref["restricted_share"]) < 1e-3 and num["restricted_out_if_clean_only"] == 90,
        "about 30% of photos are Restricted; sending only clean photos still lets about 90 a month out")

# %% [markdown]
# 🔍 **Look at** the two numbers the request did not give: 5,445 Restricted photos a month as asked, and about
# 90 a month even with the detector, an estimate from 2 misses in 400 photos, so the true figure could be
# several times higher or lower. "We would ask inspectors to avoid people in photos" is not a control. A
# detector is, and it is not perfect.

# %% [markdown]
# ## 2 · Decide, with conditions, an expiry and what reopens it (7')
#
# ✏️ **Exercise** · Return the decision record. `decision` is `refused`, `approved` or `approved with
# conditions`. A deviation is a time-boxed decision: give an `expires` date no more than six months after the
# request, `conditions` a reviewer can verify (each with a number), the `residual_risk` in numbers and who
# accepts it, an `owner`, and `reopen_if`: the events that bring it back to the board early.

# %%
def decide(num: dict) -> dict:
    # BEGIN SOLUTION
    return {
        "id": "DR-2026-07", "date": "2026-11-09", "status": "accepted",
        "decision": "approved with conditions",
        "scope": "Kashif, inspections team (T03), photos to ext-vision-q",
        "conditions": [
            "Only photos the on-device detector passes as clean are sent: about 65% of photos",
            "Flagged photos stay on the manual path and never reach ext-vision-q: 100% of them, checked weekly "
            "in the gateway log",
            "The gateway admits ext-vision-q for key k-t03-a only, with a budget of SAR 400 a month",
            "The detector is re-measured on 1,000 labelled photos within 30 days; misses above 3% of Restricted photos end the deviation",
            "The provider keeps photos 30 days or less and does not train on them",
        ],
        "residual_risk": f"about {num['restricted_out_if_clean_only']} Restricted photos a month may leave the "
                         "Kingdom through detector misses; accepted by the data protection officer, Hadeel "
                         "Al-Sharhan, for the period only",
        "expires": "2027-03-31",
        "owner": "Rabah Al-Mujil",
        "reopen_if": ["ksa-vision-x publishes Arabic evaluation evidence at or above 0.80",
                      "the detector's measured miss rate on Restricted photos exceeds 3%",
                      "any flagged photo appears in the ext-vision-q log"],
        "rejected": {"refused": f"costs about SAR {num['refusal_cost_sar_month']:,} a month of inspector time "
                                "until February 2027 at the earliest",
                     "approved as asked": f"about {num['restricted_out_as_asked']:,} Restricted photos a month "
                                          "abroad, for twelve months"},
    }
    # END SOLUTION

# %%
try:
    rec = decide(num)
except NotImplementedError:
    rec = None
    print("(exercise not done)")
if rec:
    print(pd.Series({k: v for k, v in rec.items() if k not in ("conditions", "reopen_if", "rejected")}).to_string())
    for c in rec["conditions"]:
        print(" -", c)
    A.check(rec["decision"] in ("refused", "approved", "approved with conditions"), "a decision is taken")
    if rec["decision"] != "refused":
        A.check(date.fromisoformat(rec["expires"]) <= date(2027, 5, 2), "it expires within six months")
        A.check(len(rec["conditions"]) >= 3 and all(re.search(r"\d", c) for c in rec["conditions"]),
                "at least three conditions, each with a number a reviewer can check")
        A.check(len(rec.get("reopen_if", [])) >= 2 and rec.get("owner"), "it has an owner and reopen triggers")
    A.check(bool(re.search(r"\d", rec.get("residual_risk", ""))) or rec["decision"] == "refused",
            "the residual risk is stated in numbers, with who accepts it")

# %% [markdown]
# Whether 90 photos a month is acceptable is not the architect's call. The architect makes the number visible
# and names who must accept it: the owner of the data, with the data management office.

# %% [markdown]
# ## 3 · One page for the sponsor (7')
#
# ✏️ **Exercise** · Write the page Dr. Afrah reads before the board: the decision in the first sentence, the
# trade-off in numbers (time saved, photos that may leave), what she is asked to accept, and when it ends. At
# most 250 words, and none of the board's jargon: she should not need to know what a fitness check, a gateway
# or p95 is.

# %%
JARGON = ["fitness", "gateway", "p95", "tenancy", "ATAM", "alias", "P-01", "k-t03-a", "fallback", "SLO"]


def sponsor_page(rec: dict, num: dict) -> str:
    # BEGIN SOLUTION
    hours = round(num["refusal_cost_sar_month"] / facts["inspector_cost_sar_per_hour"])
    return f"""# Inspection photos and an overseas vision service: decision for 9 November

**We recommend approving the inspections team's request under conditions until 31 March 2027, and not for
the twelve months asked.**

**What it gives.** Kashif drafts inspection reports from photos. Without a vision service that reads Arabic
signs, inspectors type every report: about {hours:,} inspector hours a month, worth about
SAR {num['refusal_cost_sar_month']:,}. No service in the Kingdom has shown it reads Arabic well enough yet; the
first may in February 2027.

**What it risks.** About 30% of photos show faces, car plates or documents. Sent as asked, about
{num['restricted_out_as_asked']:,} such photos a month would go abroad. Under our conditions, a check on the
tablet holds those photos back; it lets about 1 in 60 of them through, so about
{num['restricted_out_if_clean_only']} a month may still go abroad.

**What you are asked to accept.** That residual, until the end of March, with the data protection officer's
agreement.

**How it ends.** On 31 March 2027, or earlier if a service in the Kingdom passes our Arabic test or the check
on the tablet lets through more than 3 in 100 of the photos it should hold back. The inspections team lead owns the conditions.
"""
    # END SOLUTION

# %%
try:
    page = sponsor_page(rec, num) if rec else None
except NotImplementedError:
    page = None
    print("(exercise not done)")
if page:
    print(page)
    words = len(re.findall(r"\w+", page))
    found = [j for j in JARGON if j.lower() in page.lower()]
    A.check(words <= 250, f"{words} words, within 250")
    A.check(not found, "no board jargon" + (f" (found {found})" if found else ""))
    A.check(str(num["restricted_out_if_clean_only"]) in page, "the residual is on the page in numbers")
    out = A.lab_dir("D4_4")
    (out / "sponsor_page.md").write_text(page, encoding="utf-8")
    import json
    (out / "DR-2026-07.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
    print("saved", (out / "sponsor_page.md").relative_to(A.LABS).as_posix())

# %% [markdown]
# ## 4 · Choose your capstone service (5')
#
# Read the three briefs in `capstone/briefs/`. ✏️ **Exercise** · Return your choice: the brief's file name
# (`reports`, `contact` or `staff`), the level of its most sensitive data flow, and the title of the first
# decision record you expect to write.

# %%
BRIEFS = {p.stem: p.read_text(encoding="utf-8") for p in sorted((A.LABS / "capstone/briefs").glob("*.md"))}
for k, v in BRIEFS.items():
    print(f"--- {k}\n{v.splitlines()[0]}\n{v.splitlines()[2]}")


def my_capstone() -> dict:
    # BEGIN SOLUTION
    return {"service": "contact", "most_sensitive_level": "Restricted",
            "first_decision": "Transcribe calls on the Ministry-hosted speech model, not a cloud service"}
    # END SOLUTION

# %%
try:
    choice = my_capstone()
    A.check(choice["service"] in BRIEFS and choice["most_sensitive_level"] in A.LEVELS and choice["first_decision"],
            f"capstone service chosen: {choice['service']}")
except NotImplementedError:
    print("(choose before you leave: the capstone day starts from it)")

# %% [markdown]
# ## ✱ Stretch · The deviation as a gateway policy that expires
#
# A deviation that lives only in a document is forgotten. Write it as a gateway policy: `ext-vision-q` is
# allowed for the inspections team's key only, only for requests marked `"detector": "clean"`, and only until
# the expiry date; everything else gets 403. Show that the same clean request is refused the day after expiry.

# %%
def deviation_demo() -> list[int]:
    # BEGIN SOLUTION
    today = {"value": date(2026, 12, 1)}

    def dr_2026_07(ctx):
        if ctx["alias"] != "ext-vision-q":
            return None
        if ctx["team"] != "T03" or ctx["request"].get("detector") != "clean":
            return 403, "DR-2026-07 covers clean photos from the inspections team only"
        if today["value"] > date.fromisoformat(rec["expires"]):
            return 403, "DR-2026-07 expired"
        return None

    teams = A.read_csv("platform/teams.csv").to_dict("records")
    gw = G.Gateway(catalogue={"ext-vision-q": {"model": "ext-vision-q", "hosting": "external"}},
                   keys=G.default_keys(teams), models={"ext-vision-q": A.StandInModel("ext-vision-q", "external", 900)},
                   policies=[dr_2026_07])
    photo = {"model": "ext-vision-q", "messages": [{"role": "user", "content": "photo PH0001"}]}
    out = [gw.handle("k-t03-a", {**photo, "detector": "clean"}).status,
           gw.handle("k-t03-a", {**photo, "detector": "flagged"}).status,
           gw.handle("k-t02-a", {**photo, "detector": "clean"}).status]
    today["value"] = date(2027, 4, 1)
    out.append(gw.handle("k-t03-a", {**photo, "detector": "clean"}).status)
    return out
    # END SOLUTION


try:
    print("clean, flagged, other team, after expiry:", deviation_demo())
except (NotImplementedError, TypeError):
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does a deviation need an expiry when the standard it breaks has none?
# 2. Who accepts the residual risk, and why not the architect?
# 3. What did the sponsor's page leave out on purpose?
#
# <details><summary>Answers</summary>
#
# 1. It is a decision taken for a reason that will change (here, evidence for a model in the Kingdom); without
#    an expiry it becomes the new standard by default.
# 2. The owner of the data, through the data management office: the architect makes the risk visible and
#    bounded; accepting it is a governance decision.
# 3. The mechanism (gateway, detector design, review tags): she decides on outcomes, numbers and a date.
# </details>
#
# **Carry forward.** `artifacts/D4_4/DR-2026-07.json` and `sponsor_page.md` are an example of the decision
# records and sponsor page your capstone repository holds.
