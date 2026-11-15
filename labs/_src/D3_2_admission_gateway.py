# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 3.2 · Model admission and a gateway that refuses
#
# Day 3 · Session 2 (Catalogue, admission and the gateway) · 25 min.
#
# Six models are proposed for the Asas catalogue. You admit them on evidence (licence, the Ministry's own
# Arabic and English evaluations, data terms), write each admitted model's catalogue entry with the highest
# level of data it may receive, then give the supplied gateway the policy it lacks: Restricted data never
# reaches an external model, whatever the request is labelled.
#
# **Reference state.** `data/platform/model_candidates.json`, `data/platform/teams.csv`,
# `data/platform/gateway_tests.json` (nine test requests with the status each must get) and `asas_gateway.py`,
# the supplied gateway. The models behind it are scripted stand-ins (`asas.StandInModel`): the refusal is
# decided before any model is called, so no key and no download are needed. Nothing from Lab 3.1.
#
# **Tasks**
# - [ ] 1 · Admission criteria as code (5')
# - [ ] 2 · Admit four of the six candidates (6')
# - [ ] 3 · Catalogue entries with the level each may receive (4')
# - [ ] 4 · The classification policy, and nine test requests (10')
# - [ ] ✱ Stretch · A fallback that respects placement

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
import asas_gateway as G

cands = A.read_json("platform/model_candidates.json")
print(cands["note"])
print(pd.DataFrame(cands["candidates"]).to_string(index=False))

# %% [markdown]
# ## 1 · Admission criteria as code (5')
#
# ✏️ **Exercise** · Write `admit(candidate)` returning `(True, "")` or `(False, reason)`. The Ministry's
# criteria: the licence allows production use by a government entity; evaluation evidence on **both** the
# Arabic and the English sets, each at or above the capability's threshold; for a model not hosted by the
# Ministry, data kept no longer than 30 days and never used for training; a named owner.

# %%
TH = cands["thresholds"]


def admit(c: dict) -> tuple[bool, str]:
    # BEGIN SOLUTION
    if not c["licence_allows_government_production"]:
        return False, "licence"
    ev = c.get("eval") or {}
    if ev.get("ar") is None or ev.get("en") is None:
        return False, "no Arabic evaluation evidence" if ev.get("ar") is None else "no English evaluation evidence"
    if min(ev["ar"], ev["en"]) < TH[c["capability"]]:
        return False, "evaluation below threshold"
    if c["hosting"] != "ministry" and (c["retention_days"] > 30 or c["trains_on_prompts"]):
        return False, "data terms"
    if not c.get("owner"):
        return False, "no owner"
    return True, ""
    # END SOLUTION

# %% [markdown]
# ## 2 · Admit four of the six candidates (6')

# %%
key = A.reference("admission")
try:
    verdicts = {c["id"]: admit(c) for c in cands["candidates"]}
except NotImplementedError:
    verdicts = {c["id"]: (c["id"] in key["admitted"], key["rejected"].get(c["id"], "")) for c in cands["candidates"]}
    print("(using the reference verdicts)")
for cid, (ok, why) in verdicts.items():
    print(f"{cid:15s} {'admitted' if ok else 'rejected: ' + why}")
A.check(sorted(c for c, (ok, _) in verdicts.items() if ok) == sorted(key["admitted"]), "four models admitted")

# %% [markdown]
# 🔍 **Look at** the two rejections. `ext-mini-r` scores well, and its licence forbids production use: a
# leaderboard would have admitted it. `ksa-vision-x` has no Arabic evidence, so nobody knows how it reads
# Arabic signs in inspection photos; that is a reason to ask for evidence, and a deviation request on Day 4.

# %% [markdown]
# ## 3 · Catalogue entries with the level each may receive (4')
#
# ✏️ **Exercise** · For each admitted model write a catalogue entry: alias (the id), capability, hosting, the
# **highest level of data it may receive** under the placement rule (`A.LEVELS`, `A.allowed`), the evidence,
# the owner, and a review date six months on.

# %%
def catalogue_entry(c: dict) -> dict:
    # BEGIN SOLUTION
    top = max((l for l in A.LEVELS if A.allowed(l, c["hosting"])), key=A.rank)
    return {"alias": c["id"], "model": c["id"], "capability": c["capability"], "hosting": c["hosting"],
            "max_level": top, "evidence": c["eval"], "owner": c["owner"], "review": "2027-05-17"}
    # END SOLUTION

# %%
try:
    catalogue = {c["id"]: catalogue_entry(c) for c in cands["candidates"] if verdicts[c["id"]][0]}
except NotImplementedError:
    level = {"external": "Public", "ksa_cloud": "Restricted", "ministry": "Secret"}
    catalogue = {c["id"]: {"alias": c["id"], "model": c["id"], "capability": c["capability"],
                           "hosting": c["hosting"], "max_level": level[c["hosting"]]}
                 for c in cands["candidates"] if c["id"] in key["admitted"]}
    print("(using reference entries)")
print(pd.DataFrame(catalogue.values())[["alias", "capability", "hosting", "max_level"]].to_string(index=False))
A.check(catalogue["ext-frontier-l"]["max_level"] == "Public" and catalogue["own-open-s"]["max_level"] == "Secret",
        "external models take Public data only; Ministry-hosted models up to Secret")
out = A.lab_dir("D3_2")
(out / "catalogue.json").write_text(json.dumps(catalogue, indent=1), encoding="utf-8")

# %% [markdown]
# ## 4 · The classification policy, and nine test requests (10')
#
# First run the nine tests on the gateway **as supplied**. Then ✏️ **Exercise** · write
# `classification_policy(ctx)`. The level of a request is the highest of: the label it declares, what
# `G.detect_level` finds in its text, and, when it declares nothing, its team's highest level (fail closed).
# If the model's hosting may not receive that level, return `(403, reason)`; otherwise `None`. Store the
# level in `ctx["level"]` so the audit log records it.

# %%
teams = A.read_csv("platform/teams.csv").to_dict("records")
tests = A.read_json("platform/gateway_tests.json")


def build_gateway(policies):
    return G.Gateway(catalogue=catalogue, keys=G.default_keys(teams), models=G.default_models(),
                     price_card={"ext-frontier-l": {"in": 10.0, "out": 40.0},
                                 "ksa-general-m": {"in": 8.0, "out": 24.0}},
                     policies=policies)


def run_tests(gw) -> pd.DataFrame:
    rows = []
    for t in tests:
        r = gw.handle(t["key"], {"model": t["model"], "messages": [{"role": "user", "content": t["text"]}],
                                 "classification": t["declared"]})
        rows.append({"id": t["id"], "key": t["key"], "model": t["model"], "declared": t["declared"],
                     "status": r.status, "expect": t["expect"], "reason": r.reason})
    return pd.DataFrame(rows)


supplied = run_tests(build_gateway([]))
print(supplied.to_string(index=False))
print("wrong on the supplied gateway:", list(supplied[supplied.status != supplied.expect].id))

# %%
def classification_policy(ctx: dict):
    # BEGIN SOLUTION
    levels = [G.detect_level(ctx["text"])]
    levels.append(ctx["request"].get("classification") or ctx["key_info"]["max_level"])
    level = A.highest(levels)
    ctx["level"] = level
    hosting = ctx["entry"]["hosting"]
    if not A.allowed(level, hosting):
        return 403, f"{level} data may not go to a model hosted at '{hosting}'"
    return None
    # END SOLUTION

# %%
gw = build_gateway([classification_policy])
try:
    result = run_tests(gw)
except NotImplementedError:
    result = supplied
    print("(policy not written: showing the supplied gateway again)")
print(result.to_string(index=False))
A.check((supplied.status != supplied.expect).sum() >= 4, "the supplied gateway gets at least four tests wrong")
if result is not supplied:
    A.check((result.status == result.expect).all(), "all nine tests get the status they must get")
    refusals = [a for a in gw.audit if a["status"] == 403]
    print(pd.DataFrame(refusals)[["seq", "team", "alias", "level", "reason", "prompt_sha256"]].to_string(index=False))
    A.check(all("text" not in a for a in gw.audit), "the audit log keeps a hash of the prompt, never its text")
    (out / "refusals.json").write_text(json.dumps(refusals, indent=1), encoding="utf-8")

# %% [markdown]
# 🔍 **Look at** G4. The planning team is a Public team, and it labelled the request Public. The text holds a
# ten-digit identity number. A gateway that trusts labels alone lets it out; the content check catches it. The
# check is deliberately simple and will miss things a person would see: it is a floor, not a proof.

# %% [markdown]
# ## ✱ Stretch · A fallback that respects placement
#
# Give the alias `own-open-s` a fallback to `ksa-general-m`, make the Ministry-hosted stand-in fail every
# second call, and send two Secret requests from the contracts team. What must happen to the second one?

# %%
def fallback_demo() -> list[int]:
    # BEGIN SOLUTION
    cat = {**catalogue, "own-open-s": {**catalogue["own-open-s"], "fallbacks": ["ksa-general-m"]}}
    g = G.Gateway(catalogue=cat, keys=G.default_keys(teams), models=G.default_models(fail_every_own=2),
                  policies=[classification_policy])
    req = {"model": "own-open-s", "messages": [{"role": "user", "content": "Compare the bids for tender 31."}]}
    return [g.handle("k-t06-a", req).status for _ in range(2)]
    # END SOLUTION


try:
    print("statuses:", fallback_demo(), "(the second call must not fall back to a cloud model: 503, not 200)")
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why admit on the Ministry's own Arabic evaluation instead of a public leaderboard?
# 2. A request declares Public and holds an identity number. Which wins, the label or the content?
# 3. Why does the audit log keep a hash of the prompt and not the prompt?
#
# <details><summary>Answers</summary>
#
# 1. The Ministry's tasks, language variety and documents are what the model will see; a leaderboard measures
#    something else, and says nothing about the licence.
# 2. The higher of the two: the policy takes the highest level it can see.
# 3. The log must prove what happened without becoming a second copy of Restricted data; a hash proves that a
#    given prompt was or was not sent.
# </details>
#
# **Carry forward.** `artifacts/D3_2/catalogue.json` and the policy are the gateway slice of the capstone.
