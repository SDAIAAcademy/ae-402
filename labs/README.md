# AI Solution Architecture and Platform Design: labs

Hands-on notebooks for the SDAIA Academy course **AE-402 AI Solution Architecture and Platform Design**. Every
lab works on the **Ministry of Municipal Services**, a fictional ministry whose nine product teams build on
**Asas (أساس)**, its shared AI platform. Days 1 and 2 architect **Muyassir (مُيسِّر)**, the building-permits
assistant; Days 3 and 4 design Asas itself and review **Kashif (كاشف)**, the inspections team's assistant. Each
lab starts from a supplied reference state in `data/`, so none depends on an earlier one.

**No model, no key, no download.** These are architecture labs: they compute costs, check designs, run a
gateway and replay incidents. Where a model would answer, a scripted stand-in (`asas.StandInModel`) returns a
labelled text and counts tokens, which is all a gateway, a quota or a showback needs. A laptop CPU or a Colab
CPU runtime is enough.

## Quick start

**Google Colab.** Open a notebook from the [course page](https://sdaiaacademy.github.io/ae-402/) or directly at
`https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/<notebook>.ipynb`, and run the
first cell: it clones this repository and installs `requirements-colab.txt` (Copier; Colab has the rest).

**Locally**
```bash
git clone https://github.com/SDAIAAcademy/ae-402
cd ae-402/labs
uv sync                        # creates the environment from pyproject.toml (uv.lock pins every version)
uv run prepare_data.py         # optional: rewrites data/ (seed 402, the same bytes as committed)
uv run jupyter lab
```

Every source in `_src/` is also a script: `uv run _src/D3_2_admission_gateway.py` runs a lab's solution end to
end. `ASAS_QUICK=1` shortens the few loops that take more than a second.

## Notebooks

| Day | Session | Notebook | Builds |
|---|---|---|---|
| 1 | The architect's loop for AI systems | [`D1_1_drivers.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D1_1_drivers.ipynb) | drivers and constraints from a brief and three interviews |
| 1 | Quality attributes with numbers | [`D1_2_scenarios.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D1_2_scenarios.ipynb) | five scenarios tested on 400 pilot requests |
| 1 | Regulation as a design constraint | [`D1_3_data_flows.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D1_3_data_flows.ipynb) | fourteen classified flows and their placement |
| 1 | Views as code | [`D1_4_views_budget.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D1_4_views_budget.ipynb) | context and container views, a per-request budget |
| 2 | Patterns and when each fits | [`D2_1_patterns.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D2_1_patterns.ipynb) | a classifier against a recorded generative run |
| 2 | Total cost over three years | [`D2_2_three_year_cost.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D2_2_three_year_cost.ipynb) | three options costed, with sensitivity |
| 2 | Lock-in and exit | [`D2_3_exit_cost.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D2_3_exit_cost.ipynb) | exit cost and a weighted score that can flip |
| 2 | Decision records | [`D2_4_decision_records.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D2_4_decision_records.ipynb) | decision records, and a flawed peer record |
| 3 | The platform is a product | [`D3_1_demand_matrix.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D3_1_demand_matrix.ipynb) | a demand matrix from six months of usage |
| 3 | Catalogue, admission and the gateway | [`D3_2_admission_gateway.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D3_2_admission_gateway.ipynb) | model admission and a gateway that refuses |
| 3 | Tenancy and shared capacity | [`D3_3_tenancy.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D3_3_tenancy.ipynb) | three incidents under two tenancy models |
| 3 | Who pays for which tokens | [`D3_4_showback.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D3_4_showback.ipynb) | a showback that reconciles with the invoices |
| 4 | Golden paths | [`D4_1_golden_path.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D4_1_golden_path.ipynb) | a Copier template with its gates on |
| 4 | Fitness functions | [`D4_2_fitness_checks.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D4_2_fitness_checks.ipynb) | two checks over five design files |
| 4 | Structured architecture review | [`D4_3_review.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D4_3_review.ipynb) | a review of Kashif's design with a verdict |
| 4 | Deviations and sponsors | [`D4_4_deviation.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-402/blob/main/labs/D4_4_deviation.ipynb) | a deviation decided, a page for the sponsor |

Exercises are marked **✏️ Exercise** and raise `NotImplementedError` until you fill them in; the notebook still
runs to the end, using the supplied reference result where your answer is missing. Complete versions are in
`solutions/`. Cells marked **✱ Stretch** are optional. Self-checks print ✅ or ❌. Outputs go to
`artifacts/<lab>/`; delete `artifacts/` before running the course's `academy check`.

The notebooks are generated from the percent-format sources in `_src/` by `_tools/py2nb.py`
(`uv run python _tools/py2nb.py` from `labs/`), which also writes `solutions/`. Edit the sources, not the
notebooks.

## The case data

Synthetic and deterministic (seed 402), written by `prepare_data.py`. Every person, team, model id, price and
number is invented; the classification levels and the placement rule follow the national rules in spirit, and
the rule P-01 below is the case's own, stricter than the national minimum.

| Data | Folder | Contents |
|---|---|---|
| Case | `data/case/` | the brief, three interview notes, statements to sort, the data inventory, Muyassir's flows and request hops |
| Pilot | `data/pilot/` | 400 pilot requests with latency, quality, cost, privacy and oversight fields |
| Options | `data/options/` | needs, 3,000 labelled citizen reports, a recorded generative run (**synthetic**), forecast, prices, exit factors, criteria |
| Decisions | `data/decisions/` | the decision record template and a peer's flawed record |
| Platform | `data/platform/` | nine teams, keys, six months of usage, invoices of three providers, the price card, model candidates, gateway tests |
| Services | `data/services/` | the permits team's retrieval service, the golden path's service and gates, Kashif's documents and evaluation set |
| Designs | `data/designs/` | five teams' designs as JSON |
| Review | `data/review/` | Kashif's scenarios and the board's twelve observations |
| Deviation | `data/deviation/` | the deviation request, its facts and 400 labelled photos (metadata only) |
| Reference | `data/reference/` | the reference result of every step, the safety net of each notebook |
| Capstone | `capstone/` | what the capstone repository holds, and three service briefs |

**Placement rule P-01.** Public data may go to the Ministry data centre, a cloud region in the Kingdom or an
external host; Restricted data to the first two; Secret data to the Ministry data centre only. `asas.allowed`
implements it.

## Helpers

| Module | What it gives |
|---|---|
| `asas.py` | paths, `reference(name)`, `check(cond, msg)`, `lab_dir(name)`, loaders, the levels and `allowed(level, hosting)`, `StandInModel`, `sar()` |
| `asas_gateway.py` | the supplied gateway: keys, catalogue, rate limits, budgets, policies, fallback re-checked against policies, tool mediation, an audit log with a hash of each prompt and never its text |
| `asas_tenancy.py` | a minute-by-minute replay of one working hour with three incidents, for Lab 3.3 |

**Optional: a hosted model behind the gateway.** `asas.upstream_from_env()` returns an OpenAI-compatible client
when `ASAS_UPSTREAM_URL`, `ASAS_UPSTREAM_KEY` and `ASAS_UPSTREAM_MODEL` are set (for example a free model on
OpenRouter). No lab needs it, and it was not exercised when the course was built.

**Windows and long folder paths.** If an import fails with "The filename or extension is too long", keep the
virtual environment in a short folder: set `UV_PROJECT_ENVIRONMENT` to a short path before `uv sync`.

## For the trainer: what is planted

- Lab 1.2: the pilot fails latency (p95 4,866 ms against 4,000), privacy (one leak, request P0288) and oversight
  (46 of 53 approvals, against 99%).
- Lab 1.3: flows F07, F09 and F14 break the placement rule.
- Lab 2.4: the peer's record 0007 has flaws the lab lists in `reference/peer_record_flaws.json`.
- Lab 3.1: the reports team sent 47,556 requests to the external model in May and June; `k-legacy-01` has no owner.
- Lab 3.2: the supplied gateway lets four forbidden requests through (G2, G3, G4, G6).
- Lab 3.4: the price card misses an August credit and a September price cut.
- Lab 4.2: reports_triage evaluates after deployment; staff_assistant and inspections (through a fallback) send
  Restricted data out.
- Lab 4.3: Kashif uses a vision model that was not admitted, and evaluates in English only.
