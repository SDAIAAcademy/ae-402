# /// script
# requires-python = ">=3.11"
# dependencies = ["copier>=9.4"]
# ///
# %% [markdown]
# # Lab 4.1 · A golden path from the permits team's service
#
# Day 4 · Session 1 (Golden paths) · 25 min.
#
# The permits team wrote a retrieval service for Muyassir. It works, and everything another team would change
# is hard-coded in it; its evaluation is a script someone may run. Faris Al-Hothali wants it as the platform's
# golden path: a Copier template any team can generate a service from, with the evaluation gate, the
# classification check and tracing **on by default**, and a way to switch the evaluation off that everyone can
# see. You write the template's questions and their guard rails, generate Kashif's service from it, and run
# its gates as the pipeline would.
#
# **Reference state.** `data/services/permits_rag/` (the permits team's service), `data/services/golden_path/`
# (the service and gates already rewritten to read `service.json`) and `data/services/inspections_kb/`
# (Kashif's documents and evaluation set), all synthetic. Model calls are scripted stand-ins: no key, no
# download. Nothing from Day 3.
#
# **Tasks**
# - [ ] 1 · What the permits team hard-coded (4')
# - [ ] 2 · The template: questions with guard rails (9')
# - [ ] 3 · Generate Kashif's service and run its gates (7')
# - [ ] 4 · A register of the gates switched off (5')
# - [ ] ✱ Stretch · Refuse an evaluation set without Arabic

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

import json, re, shutil
import copier
import asas as A

SRC = A.DATA / "services"
print((SRC / "permits_rag/service.py").read_text(encoding="utf-8")[:900])

# %% [markdown]
# ## 1 · What the permits team hard-coded (4')
#
# ✏️ **Exercise** · Return the names of the constants in `permits_rag/service.py` that another team would have
# to change: they become the template's questions. `TOP_K` is a tuning choice the platform keeps fixed.

# %%
def hard_coded() -> list[str]:
    # BEGIN SOLUTION
    text = (SRC / "permits_rag/service.py").read_text(encoding="utf-8")
    names = re.findall(r"^([A-Z_]+) = ", text, flags=re.M)
    return [n for n in names if n not in ("HERE", "TOP_K", "STOP")]
    # END SOLUTION

# %%
ref = A.reference("golden_path")
try:
    found = hard_coded()
except NotImplementedError:
    found = ref["hard_coded"]
    print("(using the reference list)")
print(found)
A.check(sorted(found) == sorted(ref["hard_coded"]), "four values become questions: service, team, level, model")

# %% [markdown]
# 🔍 **Look at** what the service does not have: nothing checks that `MODEL` may receive `LEVEL` data, nothing
# is traced, and `eval.py` runs only when someone remembers. A template that copied this would copy its gaps.

# %% [markdown]
# ## 2 · The template: questions with guard rails (9')
#
# ✏️ **Exercise** · Return the two files only you can write. `copier.yml` asks for `service_name`, `team`,
# `classification` (Public, Restricted or Secret), `model_alias` (the three chat models of the catalogue),
# `eval_min_score` (default 0.85), `eval_gate` (default **true**) and `gate_off_reason` (asked only when the gate
# is off, and required then). Two validators: the model's hosting must allow the level (placement rule P-01),
# and `eval_min_score` may not go below 0.8. `template/service.json.jinja` writes the answers into the service's
# settings, with `top_k` 3 and `tracing` always true. The rest of the template (the service, its gates, a
# README) is supplied.

# %%
def template_files() -> dict[str, str]:
    # BEGIN SOLUTION
    copier_yml = """\
_subdirectory: template
service_name:
  type: str
  help: The service's name, in lower case with hyphens
  validator: "{% if not service_name %}a service name is required{% endif %}"
team:
  type: str
  help: The owning team (T01 to T09)
  validator: "{% if not team %}an owning team is required{% endif %}"
classification:
  type: str
  help: The highest level of data the service handles
  choices: [Public, Restricted, Secret]
  default: Restricted
model_alias:
  type: str
  help: The catalogue alias of the chat model, reached through the gateway
  choices: [ext-frontier-l, ksa-general-m, own-open-s]
  default: ksa-general-m
  validator: >-
    {% set hosting = {'ext-frontier-l': 'external', 'ksa-general-m': 'ksa_cloud', 'own-open-s': 'ministry'} %}
    {% set ok = {'Public': ['external', 'ksa_cloud', 'ministry'], 'Restricted': ['ksa_cloud', 'ministry'],
                 'Secret': ['ministry']} %}
    {% if hosting[model_alias] not in ok[classification] %}{{ classification }} data may not go to
    {{ model_alias }} ({{ hosting[model_alias] }}){% endif %}
eval_min_score:
  type: float
  default: 0.85
  validator: "{% if eval_min_score < 0.8 %}the platform's floor is 0.80{% endif %}"
eval_gate:
  type: bool
  help: Block deployment when the evaluation fails
  default: true
gate_off_reason:
  type: str
  when: "{{ not eval_gate }}"
  validator: "{% if not gate_off_reason %}switching the evaluation gate off needs a reason{% endif %}"
"""
    service_json = """\
{
 "service_name": "{{ service_name }}",
 "team": "{{ team }}",
 "classification": "{{ classification }}",
 "model_alias": "{{ model_alias }}",
 "top_k": 3,
 "tracing": true,
 "evaluation": {"enabled": {{ eval_gate | lower }}, "min_score": {{ eval_min_score }},
                "off_reason": "{{ gate_off_reason | default('') }}"}
}
"""
    return {"copier.yml": copier_yml, "template/service.json.jinja": service_json}
    # END SOLUTION

# %%
OUT = A.lab_dir("D4_1", reset=True)
TPL = OUT / "asas-retrieval-template"


def build_template(files: dict[str, str]) -> Path:
    (TPL / "template").mkdir(parents=True, exist_ok=True)
    for name in ("service.py", "checks.py", "README.md.jinja"):
        shutil.copy(SRC / "golden_path" / name, TPL / "template" / name)
    (TPL / "template/docs").mkdir(exist_ok=True)
    (TPL / "template/docs/example.md").write_text("# Example\n\nReplace with the team's documents.\n", encoding="utf-8")
    (TPL / "template/eval_set.jsonl").write_text(
        json.dumps({"question": "Replace this example", "expected": "example"}) + "\n", encoding="utf-8")
    (TPL / "template/{{ _copier_conf.answers_file }}.jinja").write_text(
        "# Written by Copier: lets `copier update` bring template changes to this service\n"
        "{{ _copier_answers|to_nice_yaml -}}\n", encoding="utf-8")
    for name, text in files.items():
        (TPL / name).write_text(text, encoding="utf-8")
    return TPL


def generate(name: str, answers: dict) -> Path:
    dst = OUT / "services" / name
    copier.run_copy(str(TPL), str(dst), data={"service_name": name, **answers}, defaults=True, quiet=True,
                    overwrite=True)
    return dst


try:
    files = template_files()
except NotImplementedError:
    files = None
    print("(template not written: steps 3 and 4 cannot generate a service)")
if files:
    build_template(files)
    refused = []
    for bad in ({"team": "T09", "classification": "Restricted", "model_alias": "ext-frontier-l"},
                {"team": "T05", "classification": "Public", "model_alias": "ext-frontier-l", "eval_min_score": 0.5}):
        try:
            generate("should-not-exist", bad)
        except ValueError as e:
            refused.append(str(e))
    print("\n".join(refused))
    A.check(len(refused) == 2, "the template refuses Restricted data to an external model and a score below 0.80")

# %% [markdown]
# ## 3 · Generate Kashif's service and run its gates (7')
#
# ✏️ **Exercise** · Generate `kashif-kb` for the inspections team (T03, Restricted, `ksa-general-m`, default
# gates), replace the template's example document and evaluation set with Kashif's from
# `inspections_kb/`, and run `python checks.py` in the generated folder as the pipeline would. Return the
# process's exit code and output.

# %%
def kashif_service() -> tuple[int, str]:
    # BEGIN SOLUTION
    svc = generate("kashif-kb", {"team": "T03", "classification": "Restricted", "model_alias": "ksa-general-m"})
    shutil.rmtree(svc / "docs")
    shutil.copytree(SRC / "inspections_kb/docs", svc / "docs")
    shutil.copy(SRC / "inspections_kb/eval_set.jsonl", svc / "eval_set.jsonl")
    run = subprocess.run([sys.executable, "checks.py"], cwd=svc, capture_output=True, text=True)
    return run.returncode, run.stdout + run.stderr
    # END SOLUTION

# %%
if files:
    try:
        code, output = kashif_service()
        print(output)
        A.check(code == 0 and "evaluation      pass" in output, "Kashif's service passes its three gates")
        cfg = json.loads((OUT / "services/kashif-kb/service.json").read_text(encoding="utf-8"))
        A.check(cfg["evaluation"]["enabled"] and cfg["tracing"], "the gates are on without anyone asking for them")
        print((OUT / "services/kashif-kb/traces.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    except NotImplementedError:
        print("(exercise not done)")

# %% [markdown]
# 🔍 **Look at** the trace line: the service, the team, the level and a hash of the question, never its text.
# The inspections team wrote none of that; it came with the path. That is the whole argument for a golden path:
# the easy way and the compliant way are the same way.

# %% [markdown]
# ## 4 · A register of the gates switched off (5')
#
# A team may switch its evaluation gate off, with a reason. Two more teams generate services below, one of them
# with the gate off. ✏️ **Exercise** · Faris wants the list: return one row per generated service whose
# evaluation is off, with its team and the reason, read from each `service.json`.

# %%
if files:
    generate("zoning-qa", {"team": "T05", "classification": "Public", "model_alias": "ext-frontier-l"})
    generate("waste-routes", {"team": "T04", "classification": "Public", "model_alias": "ksa-general-m",
                              "eval_gate": False, "gate_off_reason": "no evaluation set yet; due 2026-12-15"})
    run = subprocess.run([sys.executable, "checks.py"], cwd=OUT / "services/waste-routes", capture_output=True,
                         text=True)
    print(run.stdout, "exit code", run.returncode, "(the gate is off, so the pipeline passes, and says so)")


def gates_off(root: Path) -> list[dict]:
    # BEGIN SOLUTION
    rows = []
    for f in sorted(root.glob("*/service.json")):
        cfg = json.loads(f.read_text(encoding="utf-8"))
        if not cfg["evaluation"]["enabled"]:
            rows.append({"service": cfg["service_name"], "team": cfg["team"],
                         "reason": cfg["evaluation"]["off_reason"]})
    return rows
    # END SOLUTION

# %%
if files:
    try:
        register = gates_off(OUT / "services")
        print(register)
        A.check([r["service"] for r in register] == ["waste-routes"] and "2026-12-15" in register[0]["reason"],
                "one service runs without its evaluation gate, and the register says why and until when")
    except NotImplementedError:
        print("(exercise not done)")

# %% [markdown]
# A gate that can be switched off silently is a suggestion. A gate that is on by default, needs a reason to
# switch off and shows up in a register is a standard with a visible exit, which is what a deviation is (Session 4).

# %% [markdown]
# ## ✱ Stretch · Refuse an evaluation set without Arabic
#
# Kashif's evaluation set is in English, and its users read Arabic. Add a question `eval_languages` (choices
# `ar`, `en`, `ar+en`, default `ar+en`) whose validator refuses `en`, and show that the template now refuses it.

# %%
def arabic_required() -> str:
    # BEGIN SOLUTION
    extra = """eval_languages:
  type: str
  choices: [ar, en, ar+en]
  default: ar+en
  validator: "{% if 'ar' not in eval_languages %}the Ministry's users read Arabic: evaluate in Arabic{% endif %}"
"""
    (TPL / "copier.yml").write_text(files["copier.yml"] + extra, encoding="utf-8")
    try:
        generate("english-only", {"team": "T03", "eval_languages": "en"})
        return "accepted"
    except ValueError as e:
        return str(e)
    # END SOLUTION


try:
    print(arabic_required())
except (NotImplementedError, TypeError):
    print("(stretch not done)")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is the evaluation gate a default and not a recommendation in the template's README?
# 2. Why put the placement rule in the template's validator when the gateway enforces it anyway?
# 3. A team copies the template once and never updates it. What does it miss?
#
# <details><summary>Answers</summary>
#
# 1. Teams take the default; a recommendation is what people skip under a deadline.
# 2. It fails at generation, before any code or data exists; the gateway is the second line, not the only one.
# 3. Every later fix to the gates. Copier records the answers so `copier update` can bring changes to generated
#    services; a copy has no way back to the template.
# </details>
#
# **Carry forward.** `artifacts/D4_1/asas-retrieval-template/` is the golden-path template of the capstone's
# platform slice.
