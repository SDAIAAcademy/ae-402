# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 1.1 · Drivers, constraints and stakeholders
#
# Day 1 · Session 1 (The architect's loop for AI systems) · 25 min.
#
# You are Raneem Al-Shubaili, solution architect at the (fictional) Ministry of Municipal Services. Before any
# box is drawn for Muyassir, the building-permits assistant, you sort what the brief and three interviews say
# into drivers, constraints, concerns and assumptions, name who holds each one, and find the constraint that
# was said only once, in passing, and rules out half the obvious designs.
#
# **Reference state.** `data/case/brief.md`, three notes in `data/case/interviews/` and twenty statements in
# `data/case/statements.csv`, each tagged `[Sxx]` in the text where it was said. Nothing from another lab.
#
# **AI policy.** Do this first sort without an assistant: it is the judgement the supervised check tests.
#
# **Tasks**
# - [ ] 1 · Read the brief and the three notes (5')
# - [ ] 2 · Sort twenty statements (8')
# - [ ] 3 · Name the owner of each concern (5')
# - [ ] 4 · The hidden constraint and what it rules out (7')
# - [ ] ✱ Stretch · Write two statements the notes are missing

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

# %% [markdown]
# ## 1 · Read the brief and the three notes (5')
#
# Read the four texts below once, without taking notes. Then look at the twenty statements: each one is a
# sentence somebody said, tagged where they said it.

# %%
print(A.read_text("case/brief.md"))
for f in sorted((A.DATA / "case/interviews").glob("*.md")):
    print(f.read_text(encoding="utf-8"))
statements = A.read_csv("case/statements.csv")
print(statements.to_string(index=False))

# %% [markdown]
# ## 2 · Sort twenty statements (8')
#
# ✏️ **Exercise** · Give each statement one kind:
#
# | Kind | It is |
# |---|---|
# | `driver` | a goal the system exists to reach, ideally with a number |
# | `constraint` | a decision already taken that the design must obey (a law, a policy, a budget, a fixed system) |
# | `concern` | a worry of a stakeholder that the design must answer |
# | `assumption` | something believed but not checked |
# | `noise` | true, but no architecture decision depends on it |
#
# Return a dict `{"S01": "driver", ...}` with all twenty.

# %%
KINDS = {"driver", "constraint", "concern", "assumption", "noise"}


def sort_statements() -> dict[str, str]:
    # BEGIN SOLUTION
    return {"S01": "driver", "S02": "driver", "S03": "constraint", "S04": "constraint", "S05": "concern",
            "S06": "driver", "S07": "concern", "S08": "assumption", "S09": "constraint", "S10": "concern",
            "S11": "noise", "S12": "constraint", "S13": "constraint", "S14": "concern", "S15": "assumption",
            "S16": "driver", "S17": "constraint", "S18": "noise", "S19": "assumption", "S20": "concern"}
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
key = A.reference("drivers_key")
try:
    kinds = sort_statements()
except NotImplementedError:
    kinds = {i: v["kind"] for i, v in key.items()}
    print("(using the reference sort)")
assert set(kinds) == set(key) and set(kinds.values()) <= KINDS, "one kind for each of the twenty statements"
agree = sum(kinds[i] == key[i]["kind"] for i in key)
diff = statements.assign(yours=statements.id.map(kinds), reference=statements.id.map(lambda i: key[i]["kind"]))
differ = diff[diff.yours != diff.reference]
print(differ.to_string(index=False) if len(differ) else "all twenty agree with the reference")
A.check(agree >= 17, f"{agree} of 20 agree with the reference sort (17 or more to pass)")
A.check(kinds["S12"] == "constraint", "S12, the applicant files rule, is a constraint")

# %% [markdown]
# 🔍 **Look at** the rows where you differ. A disagreement is worth a minute only when it would change a
# design decision: S10 (traffic doubles) as a concern or a driver changes nothing; S15 as a fact instead of an
# assumption sends published and unpublished texts to the same model.

# %% [markdown]
# ## 3 · Name the owner of each concern (5')
#
# ✏️ **Exercise** · A concern without an owner is never closed. For each statement you sorted as a
# `concern`, name the stakeholder who holds it, from: `sponsor`, `permits team`, `inspectors`,
# `data protection officer`, `applicants`, `engineering offices`, `permit staff`.

# %%
def concern_owners(kinds: dict[str, str]) -> dict[str, str]:
    # BEGIN SOLUTION
    owners = {"S05": "sponsor", "S07": "inspectors", "S10": "permits team", "S14": "applicants",
              "S20": "permit staff"}
    return {i: owners[i] for i, k in kinds.items() if k == "concern"}
    # END SOLUTION

# %%
try:
    owners = concern_owners(kinds)
except NotImplementedError:
    owners = {i: key[i]["owner"] for i, k in kinds.items() if k == "concern"}
    print("(using the reference owners)")
stakeholders = pd.DataFrame([{"concern": i, "owner": o, "text": statements.set_index("id").text[i]}
                             for i, o in owners.items()])
print(stakeholders.to_string(index=False))
right = sum(o == key[i]["owner"] for i, o in owners.items())
A.check(right >= len(owners) - 1, f"{right} of {len(owners)} owners match the reference")

# %% [markdown]
# ## 4 · The hidden constraint and what it rules out (7')
#
# S12 was said once, in passing, by the data protection officer. Below are six designs the room proposed
# in the first ten minutes. ✏️ **Exercise** · Return the ids of the designs S12 or S13 rules out, and for
# each one the statement that rules it out.

# %%
DESIGNS = {
    "A": "Send scanned deeds and site plans to an external OCR service, keep the text in the Ministry",
    "B": "Answer every question with an external frontier model, applicant context included",
    "C": "Answer with a model hosted in the Kingdom through the Asas gateway",
    "D": "Embed the published building code with an external embedding model",
    "E": "Send conversation logs to an external analytics service for a weekly dashboard",
    "F": "Keep conversation logs in the Ministry's log store with a 90-day expiry",
}


def ruled_out() -> dict[str, str]:
    # BEGIN SOLUTION
    return {"A": "S12", "B": "S12", "E": "S13"}
    # END SOLUTION

# %%
try:
    out = ruled_out()
except NotImplementedError:
    out = {"A": "S12", "B": "S12", "E": "S13"}
    print("(using the reference answer)")
for d, s in sorted(out.items()):
    print(f"{d} ruled out by {s}: {DESIGNS[d]}")
A.check(set(out) == {"A", "B", "E"}, "designs A, B and E are ruled out; C, D and F stay open")
drivers_sheet = pd.DataFrame([{"id": i, "kind": k, "owner": owners.get(i, key[i]["owner"]),
                               "text": statements.set_index("id").text[i]} for i, k in sorted(kinds.items())])
path = A.lab_dir("D1_1") / "drivers.csv"
drivers_sheet.to_csv(path, index=False)
print("saved", path.relative_to(A.LABS).as_posix())

# %% [markdown]
# Why E: conversation logs are personal data (S13) and the analytics service is outside the Kingdom; the
# 90-day rule also means the copy there must expire. Why not D: the building code is published (D01), so S12
# does not touch it. S15 is still an assumption until the data protection officer confirms which texts are
# really published: Lab 1.3 finds one that is not.

# %% [markdown]
# ## ✱ Stretch · Two statements the notes are missing
#
# Write two statements an architect would need and nobody said: for example who owns the building code
# index, or what happens when the permits system is down. Give each a kind and the person you would ask.

# %%
def missing_statements() -> list[dict]:
    # BEGIN SOLUTION
    return [
        {"text": "When the permits system is down, status questions get a clear message and a hand-over",
         "kind": "concern", "ask": "permits team"},
        {"text": "The building code index is refreshed within one day of a new circular", "kind": "driver",
         "ask": "permits team"},
    ]
    # END SOLUTION


try:
    print(pd.DataFrame(missing_statements()).to_string(index=False))
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is S04 (the SAR 1.2 million cap) a constraint and not a driver?
# 2. S08 says most questions are about 40 topics. What would you measure before relying on it?
# 3. Which statement, if it turned out false, would reopen the most decisions?
#
# <details><summary>Answers</summary>
#
# 1. Nobody builds Muyassir to spend SAR 1.2 million: the cap bounds the options, it is not a goal.
# 2. Count the topics in a month of contact-line questions or of the pilot's 400 requests before any design
#    depends on a short list.
# 3. S12: if applicant files could leave the Kingdom, designs A and B would come back.
# </details>
#
# **Carry forward.** `artifacts/D1_1/drivers.csv`. Lab 1.2 starts from the reference sheet, not from yours.
