# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 1.4 · Views as code and a request budget
#
# Day 1 · Session 4 (Views as code) · 25 min.
#
# You generate Muyassir's context and container views as Mermaid text from one model file, so the diagrams
# change in a pull request like any other code, then trace one request through every hop and add up its
# latency and its cost against scenario Q2 (p95 under 4,000 ms) and Q3 (under SAR 0.05).
#
# **Reference state.** `data/case/muyassir_model.json` (people, external systems, containers, relations) and
# `data/case/request_hops.csv` (measured p50 and p95 per hop, tokens, the case's price card). Nothing from
# earlier labs.
#
# **Tasks**
# - [ ] 1 · Read the model of Muyassir (3')
# - [ ] 2 · The context view as Mermaid (7')
# - [ ] 3 · The container view, with hosting on every box (7')
# - [ ] 4 · One request end to end: latency and cost (8')
# - [ ] ✱ Stretch · Cut the request to fit 4,000 ms

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

model = A.read_json("case/muyassir_model.json")
hops = A.read_csv("case/request_hops.csv")

# %% [markdown]
# ## 1 · Read the model of Muyassir (3')
#
# One file holds the elements and the relations. Both views below are generated from it: a box drawn by
# hand in a slide tool cannot be checked, a box generated from a model can.

# %%
for kind in ("people", "external_systems", "containers"):
    print(kind, [e["id"] for e in model[kind]])
print(len(model["relations"]), "relations, for example", model["relations"][0])
inside = {c["id"] for c in model["containers"]}

# %% [markdown]
# ## 2 · The context view as Mermaid (7')
#
# ✏️ **Exercise** · The context view shows Muyassir as **one** box, with the people and external systems
# around it. Write `context_view(model)` returning Mermaid `flowchart LR` text: one node per person, per
# external system and one for the system; one edge `a -->|label| b` per relation, where any container is
# replaced by the system. Drop edges that become a box talking to itself, and duplicates.

# %%
def context_view(m: dict) -> str:
    # BEGIN SOLUTION
    sid = m["system"]["id"]
    lines = ["flowchart LR"]
    for p in m["people"]:
        lines.append(f'  {p["id"]}(["{p["name"]}"])')
    lines.append(f'  {sid}["{m["system"]["name"]}: {m["system"]["description"]}"]')
    for e in m["external_systems"]:
        lines.append(f'  {e["id"]}[("{e["name"]}")]')
    seen = set()
    for a, b, label, _ in m["relations"]:
        a2, b2 = (sid if a in inside else a), (sid if b in inside else b)
        if a2 != b2 and (a2, b2) not in seen:
            seen.add((a2, b2))
            lines.append(f"  {a2} -->|{label}| {b2}")
    return "\n".join(lines)
    # END SOLUTION

# %%
def edges(text: str) -> set[tuple[str, str]]:
    return set(re.findall(r"^\s*(\w+) -->\|[^|]*\| (\w+)\s*$", text, re.M))


try:
    context = context_view(model)
except NotImplementedError:
    context = A.read_text("reference/context_view.mmd")
    print("(using the reference view)")
print(context)
ctx_edges = edges(context)
A.check(not any(a in inside or b in inside for a, b in ctx_edges), "no container appears in the context view")
A.check(("applicant", "muyassir") in ctx_edges and ("muyassir", "permits") in ctx_edges,
        "applicant to Muyassir, Muyassir to the permits system")

# %% [markdown]
# ## 3 · The container view, with hosting on every box (7')
#
# ✏️ **Exercise** · Now open the box. Write `container_view(model)`: a `subgraph` for Muyassir holding one
# node per container, labelled with its name, technology and **hosting** (`ministry`, `ksa_cloud`,
# `external`), and every relation as an edge with its label and protocol. Hosting on every box is what lets
# a reviewer check placement against Lab 1.3 by reading the diagram.

# %%
def container_view(m: dict) -> str:
    # BEGIN SOLUTION
    lines = ["flowchart LR"]
    for p in m["people"]:
        lines.append(f'  {p["id"]}(["{p["name"]}"])')
    lines.append(f'  subgraph {m["system"]["id"]}["{m["system"]["name"]}"]')
    for c in m["containers"]:
        lines.append(f'    {c["id"]}["{c["name"]}<br/>{c["tech"]}<br/>hosting: {c["hosting"]}"]')
    lines.append("  end")
    for e in m["external_systems"]:
        lines.append(f'  {e["id"]}[("{e["name"]}<br/>hosting: {e["hosting"]}")]')
    for a, b, label, proto in m["relations"]:
        lines.append(f"  {a} -->|{label}, {proto}| {b}")
    return "\n".join(lines)
    # END SOLUTION

# %%
try:
    containers = container_view(model)
except NotImplementedError:
    containers = A.read_text("reference/container_view.mmd")
    print("(using the reference view)")
print(containers)
A.check(edges(containers) == {(a, b) for a, b, _, _ in model["relations"]}, "every relation is an edge")
A.check(containers.count("hosting:") == len(model["containers"]) + len(model["external_systems"]),
        "hosting is written on every container and external system")
views = A.lab_dir("D1_4") / "views"
views.mkdir(exist_ok=True)
(views / "context.mmd").write_text(context + "\n", encoding="utf-8")
(views / "containers.mmd").write_text(containers + "\n", encoding="utf-8")
print("saved views/context.mmd and views/containers.mmd: paste either into any Mermaid viewer")

# %% [markdown]
# ## 4 · One request end to end (8')
#
# The request: an applicant asks "what is still missing from my application?". It passes the portal, the
# token check, a status read, retrieval, reranking, the gateway and the answer model; the log is written
# afterwards, off the user's path. ✏️ **Exercise** · Write `budget(hops)`: the sum of p50 and of p95 over the
# hops on the user's path (leave out the asynchronous one), and the cost of the request from tokens and the
# price card. Return a dict with `p50_sum_ms`, `p95_sum_ms` and `cost_sar`.

# %%
def budget(h: pd.DataFrame) -> dict:
    # BEGIN SOLUTION
    sync = h[~h.step.str.contains("asynchronous")]
    cost = (h.in_tokens / 1e6 * h.sar_per_m_in + h.out_tokens / 1e6 * h.sar_per_m_out).sum()
    return {"p50_sum_ms": int(sync.p50_ms.sum()), "p95_sum_ms": int(sync.p95_ms.sum()), "cost_sar": round(float(cost), 5)}
    # END SOLUTION

# %%
try:
    b = budget(hops)
except NotImplementedError:
    b = A.reference("budget")
    print("(using the reference budget)")
print(hops[["component", "step", "p50_ms", "p95_ms"]].to_string(index=False))
print(b)
ref = A.reference("budget")
A.check(b["p95_sum_ms"] == ref["p95_sum_ms"] and abs(b["cost_sar"] - ref["cost_sar"]) < 1e-6,
        f"p95 sum {ref['p95_sum_ms']} ms, cost SAR {ref['cost_sar']}")
over = b["p95_sum_ms"] - 4000
print(f"Q2 target 4000 ms: the request is over by {over} ms on the sum of p95s; Q3 (SAR 0.05) holds")
doc = A.lab_dir("D1_4") / "architecture.md"
doc.write_text("# Muyassir: views and one request\n\n## Context\n\n```mermaid\n" + context + "\n```\n\n"
               "## Containers\n\n```mermaid\n" + containers + "\n```\n\n## One request\n\n"
               + A.md_table(hops[["component", "step", "p50_ms", "p95_ms"]]) + "\n", encoding="utf-8")
print("saved", doc.relative_to(A.LABS).as_posix())

# %% [markdown]
# 🔍 **Look at** which hops dominate: the answer model and the reranker hold 3,550 of the 4,290 ms. The sum of
# p95s is an upper bound (the slow tails rarely meet in one request), but it is the budget a reviewer can
# defend. Measure the end-to-end p95 too before you cut anything: the pilot measured 4,866 ms, so here the
# bound is not pessimistic.

# %% [markdown]
# ## ✱ Stretch · Cut the request to fit 4,000 ms
#
# Status questions need no reranking of twenty clauses. Which hop do you remove for them, what is their new
# p95 sum, and which scenario do you have to re-test after the change?

# %%
def cut() -> dict:
    # BEGIN SOLUTION
    kept = hops[(hops.component != "reranker") & ~hops.step.str.contains("asynchronous")]
    return {"removed": "reranker", "p95_sum_ms": int(kept.p95_ms.sum()), "retest": "Q1 answer quality"}
    # END SOLUTION


try:
    print(cut())
except NotImplementedError:
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does the context view show Muyassir as a single box?
# 2. Why is hosting written on the container boxes and not in a separate table?
# 3. Can you add p95s to get the p95 of the request? What does the sum give you instead?
#
# <details><summary>Answers</summary>
#
# 1. It answers "who and what does the system talk to?"; its inside is the container view's question.
# 2. A reviewer checks placement against the classified flows by reading one picture, and a change of hosting
#    shows in the diff of the view.
# 3. Not exactly: tails rarely coincide, so the sum is an upper bound. It is a safe budget, and an end-to-end
#    measurement then says how much slack the bound hides.
# </details>
#
# **Carry forward.** `artifacts/D1_4/architecture.md` is the shape of the architecture document of the capstone.
