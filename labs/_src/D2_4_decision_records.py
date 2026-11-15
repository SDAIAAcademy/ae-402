# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# %% [markdown]
# # Lab 2.4 · Two decision records and a challenge
#
# Day 2 · Session 4 (Decision records) · 25 min.
#
# You record two of Muyassir's decisions in the course's template (MADR with a review trigger), check them with
# a lint, then challenge a peer's record the way the room will: is every consequence there, the bad ones
# included, and would anyone know when to reopen it?
#
# **Reference state.** `data/decisions/template.md`, a peer's record `data/decisions/0007-peer-cache-answers.md`,
# and the numbers of Days 1 and 2 quoted below. Nothing from earlier labs is loaded.
#
# **AI policy.** An assistant may question your record; it does not write the decision.
#
# **Tasks**
# - [ ] 1 · Read the template and run the lint (4')
# - [ ] 2 · Record one: where Muyassir's model runs (8')
# - [ ] 3 · Record two: no reranking for status questions (6')
# - [ ] 4 · Challenge a peer's record (7')
# - [ ] ✱ Stretch · The decision log index

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
import asas as A

# %% [markdown]
# ## 1 · Read the template and run the lint (4')
#
# The template is MADR's structure (context, drivers, options, outcome, consequences) with one section this
# course adds: **Review trigger**, a measurable condition or a date that reopens the decision. `render` turns a
# dict into the Markdown file; `lint` reads a Markdown record the way a reviewer does.

# %%
print(A.read_text("decisions/template.md"))

SECTIONS = ["## Context and problem statement", "## Decision drivers", "## Considered options",
            "## Decision outcome", "### Consequences", "## Review trigger"]


def render(r: dict) -> str:
    lines = [f"# {r['number']}. {r['title']}", "", f"- Status: {r['status']}", f"- Date: {r['date']}",
             f"- Deciders: {r['deciders']}", "", "## Context and problem statement", "", r["context"], "",
             "## Decision drivers", ""] + [f"- {d}" for d in r["drivers"]] + ["", "## Considered options", ""]
    lines += [f"- {o}" for o in r["options"]] + ["", "## Decision outcome", "",
                                                 f"Chosen option: \"{r['chosen']}\", because {r['because']}", "",
                                                 "### Consequences", ""]
    lines += [f"- Good, because {g}" for g in r["good"]] + [f"- Bad, because {b}" for b in r["bad"]]
    lines += ["", "## Review trigger", "", r["trigger"], ""]
    return "\n".join(lines)


def lint(md: str) -> list[str]:
    problems = [f"missing section: {s}" for s in SECTIONS if s not in md]
    if not re.search(r"^- Date: \d{4}-\d{2}-\d{2}", md, re.M):
        problems.append("no date in the form YYYY-MM-DD")
    options = re.findall(r"^- ", md.split("## Considered options")[-1].split("## Decision outcome")[0], re.M)
    if len(options) < 2:
        problems.append("fewer than two considered options")
    if "Bad, because" not in md:
        problems.append("no bad consequence: every real decision has one")
    trigger = md.split("## Review trigger")[-1].strip() if "## Review trigger" in md else ""
    if not re.search(r"\d", trigger):
        problems.append("the review trigger has no number or date: nobody can tell when it fires")
    if not re.search(r"\b(Q\d|S\d\d)\b", md):
        problems.append("no driver is tied to a scenario (Q1..Q5) or a statement (S01..S20)")
    return problems

# %% [markdown]
# ## 2 · Record one: where Muyassir's model runs (8')
#
# The facts. Lab 2.2: at the base forecast O1 (a model hosted in the Kingdom, paid per token) costs about
# SAR 6.25 million over three years, O2 (Ministry-hosted) SAR 7.59 million; O2 catches up only near 900,000
# requests a month at double the token price. Lab 2.3: O1 is the dearest to leave (SAR 540,000) and the
# ranking flips to O2 when exit cost weighs 0.13 instead of 0.10. Lab 1.3: Restricted prompts may go to a cloud
# region in the Kingdom (S12 holds). ✏️ **Exercise** · Fill the record as a dict with the keys `render` uses.

# %%
def record_hosting() -> dict:
    # BEGIN SOLUTION
    return {
        "number": 1, "title": "Host Muyassir's answer model in a cloud region in the Kingdom (O1)",
        "status": "accepted", "date": "2026-11-17", "deciders": "Raneem Al-Shubaili (architect), Faris Al-Hothali (Asas)",
        "context": "Muyassir needs a generative answer model for Restricted prompts. Three options were costed over "
                   "three years on the base forecast (Lab 2.2) and scored with exit cost (Lab 2.3).",
        "drivers": ["S12: applicant files stay in the Kingdom", "S04: first-year run cost under SAR 1.2 million",
                    "Q1 answer quality and Q2 latency", "Three-year cost and exit cost"],
        "options": ["O1: model hosted in the Kingdom, paid per token", "O2: open-weight model hosted by the Ministry",
                    "O3: guided search and a document checklist"],
        "chosen": "O1",
        "because": "it is the cheapest over three years (SAR 6.25 million against 7.59 and 11.92), meets S12 and "
                   "goes live first.",
        "good": ["first-year run cost is under the cap without the contact-centre line",
                 "no accelerator servers to buy or operate"],
        "bad": ["it is the dearest option to leave (SAR 540,000) until the export and notice requirements are signed",
                "the ranking is fragile: an exit-cost weight of 0.13 instead of 0.10 puts O2 first"],
        "trigger": "Reopen if monthly requests exceed 600,000, if the price per million input tokens rises above "
                   "SAR 12, or if the contract is not signed with the two exit requirements of Lab 2.3 by 2027-03-31.",
    }
    # END SOLUTION

# %%
try:
    r1 = record_hosting()
except NotImplementedError:
    r1 = None
    print("(exercise not done: the lint runs on the template instead)")
md1 = render(r1) if r1 else A.read_text("decisions/template.md")
print(md1)
print("lint:", lint(md1) or "clean")
if r1:
    A.check(not lint(md1), "record one passes the lint")

# %% [markdown]
# ## 3 · Record two: no reranking for status questions (6')
#
# Lab 1.4's stretch: without the reranker, status questions fit 4,000 ms (3,640 ms on the sum of p95s). The
# reranker exists for answer quality. ✏️ **Exercise** · Record the decision, its bad consequence and the
# trigger that would bring the reranker back.

# %%
def record_reranker() -> dict:
    # BEGIN SOLUTION
    return {
        "number": 2, "title": "Skip reranking for status questions", "status": "accepted", "date": "2026-11-17",
        "deciders": "Raneem Al-Shubaili (architect), Eyad Al-Shuraihi (permits)",
        "context": "The p95 sum of a request is 4,290 ms against Q2's 4,000 ms. The reranker takes 650 ms and status "
                   "questions read one record, not twenty clauses.",
        "drivers": ["Q2 latency: p95 under 4,000 ms", "Q1 answer quality"],
        "options": ["Keep the reranker for every question", "Skip it for status questions",
                    "A faster, smaller reranker for every question"],
        "chosen": "Skip it for status questions",
        "because": "status answers come from one record, and the p95 sum falls to 3,640 ms.",
        "good": ["Q2 holds for status questions with 360 ms to spare"],
        "bad": ["a status question that also asks about a requirement gets unranked clauses",
                "two code paths to test instead of one"],
        "trigger": "Reopen if Q1 on mixed status-and-requirements questions falls below 0.90 on the monthly "
                   "sample of 200 answers.",
    }
    # END SOLUTION

# %%
try:
    r2 = record_reranker()
    md2 = render(r2)
    print(md2)
    A.check(not lint(md2), "record two passes the lint")
except NotImplementedError:
    r2 = None
    print("(exercise not done)")
out = A.lab_dir("D2_4")
for r in (r1, r2):
    if r:
        (out / f"{r['number']:04d}.md").write_text(render(r), encoding="utf-8")

# %% [markdown]
# ## 4 · Challenge a peer's record (7')
#
# In the room you swap records with a neighbour. Here, the permits team's record 0007 stands in. Run the lint,
# then do what the lint cannot. ✏️ **Exercise** · Return your challenges: each a sentence a reviewer would
# write in the pull request. Look for a missing bad consequence, a trigger nobody can test, and a driver that
# should be there and is not.

# %%
peer = A.read_text("decisions/0007-peer-cache-answers.md")
print(peer)
print("lint:", lint(peer))


def challenge(md: str) -> list[str]:
    # BEGIN SOLUTION
    return [
        "Consequences: add the bad one. A cached answer can outlive a new circular for up to 30 days; who "
        "carries that, and how is the cache cleared when a circular is published?",
        "Review trigger: 'if things change' cannot fire. Reopen when the cache hit rate falls below a number, "
        "or on the date of the next circular.",
        "Drivers: Q1 answer quality is missing; a stale answer is a wrong answer.",
    ]
    # END SOLUTION

# %%
try:
    mine = challenge(peer)
except NotImplementedError:
    mine = A.reference("peer_record_flaws")
    print("(using the reference challenges)")
for c in mine:
    print("-", c)
text = " ".join(mine).lower()
A.check("consequence" in text and "trigger" in text, "the challenges name the missing consequence and the trigger")
A.check(len(lint(peer)) >= 2, "the lint finds at least two problems in record 0007")

# %% [markdown]
# 🔍 **Look at** what the lint did not find: the missing driver Q1. A record can pass every format check and
# still hide the consequence that matters. The lint is the floor of a review, not the review.

# %% [markdown]
# ## ✱ Stretch · The decision log index
#
# The outcome asks for at least six records. Write the index of the log: number, title, status, date and
# trigger of each record you have, in a Markdown table, and list four more decisions Muyassir needs.

# %%
def log_index() -> str:
    # BEGIN SOLUTION
    rows = [r for r in (r1, r2) if r]
    lines = ["| # | Title | Status | Date | Trigger |", "|---|---|---|---|---|"]
    lines += [f"| {r['number']} | {r['title']} | {r['status']} | {r['date']} | {r['trigger'][:60]}... |" for r in rows]
    lines += ["", "Still to record: log retention and access (S13, S20); OCR inside the Kingdom (F07); "
              "hand-over to the contact centre (Q5); the evaluation set and its owner (Q1)."]
    return "\n".join(lines)
    # END SOLUTION


try:
    print(log_index())
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why must every accepted record have a bad consequence?
# 2. What makes a review trigger testable?
# 3. Record one cites the flip weight of Lab 2.3. Why put a weakness of the analysis into the record?
#
# <details><summary>Answers</summary>
#
# 1. A decision without a cost was not a choice; the bad consequence is what the next architect needs to know.
# 2. A number someone measures or a date, with the measurement named.
# 3. So whoever reopens it knows the ranking was close and which assumption to argue about.
# </details>
#
# **Carry forward.** `artifacts/D2_4/0001.md` and `0002.md` start the capstone's decision log.
