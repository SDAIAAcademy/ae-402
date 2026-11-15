<!-- academy:title -->
# AI Solution Architecture and Platform Design

معمارية حلول الذكاء الاصطناعي وتصميم المنصات

AI Engineering Track · SDAIA Academy · AE-402 · Level 400

REPLACE: one line under the title: what participants can do after the course

Participants practise the architect's loop on AI systems and apply it to the shared platform many teams build on. For a fictional ministry of municipal services with nine product teams and data at three classification levels, they turn requirements into measurable scenarios, draw views as code, cost three options including a non-generative one, keep a decision log, design a model catalogue, gateway, tenancy model, golden paths and showback, enforce a reference design with fitness checks, and review a peer's architecture. Serving optimisation and reliability engineering are left to AE-401 and AE-403.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ae-402/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Prepare quality-attribute scenarios with measurable targets for answer quality, latency, cost, privacy and human oversight, given the case brief, three interview notes and the data inventory | Applied | a scenario sheet a reviewer can test a design against |
| LO2 | Design an end-to-end architecture with context, container and data-flow views and a per-request latency and cost budget, given the scenario sheet and the classification of each data flow | Performance | an architecture document with views as code and one request traced end to end |
| LO3 | Evaluate at least three solution options, including a non-generative baseline, and record the resulting decisions, given weighted criteria, a three-year volume forecast and price ranges | Performance | an options paper with total cost, lock-in and sensitivity analysis, and at least six decision records |
| LO4 | Design a shared AI platform covering model admission, gateway, tenancy, golden paths and cost attribution, given nine teams, three classification levels, synthetic usage logs and invoices | Performance | a design and a working slice whose gateway refuses restricted data to an external model and whose showback reconciles within 2% |
| LO5 | Design a reference architecture with fitness functions that check conformance automatically, given a recurring pattern: retrieval over classified documents | Performance | a template and two automated checks that fail on a non-conforming design |
| LO6 | Review a peer's architecture with a structured trade-off method and decide on a requested deviation, given a peer design, the reference designs and a deviation request | Performance | a review report naming risks, sensitivity points and non-compliance, with a recorded decision |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | From requirements to architecture | The architect's loop for AI systems; Quality attributes with numbers; Regulation as a design constraint; Views as code | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Options and decisions | Patterns and when each fits; Total cost over three years; Lock-in and exit; Decision records | [`slides/day2.html`](slides/day2.html) |
| Day 3 | The shared platform | The platform is a product; Catalogue, admission and the gateway; Tenancy and shared capacity; Who pays for which tokens | [`slides/day3.html`](slides/day3.html) |
| Day 4 | Reference designs and reviews | Golden paths; Fitness functions; Structured architecture review; Deviations and sponsors | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | List drivers, constraints and stakeholders for the permits assistant from the case brief | [`D1_1_list_drivers_constraints.ipynb`](labs/D1_1_list_drivers_constraints.ipynb) |
| 1.2 | Day 1 · Session 2 | Write five measurable scenarios, including answer quality and human oversight | [`D1_2_write_five_measurable.ipynb`](labs/D1_2_write_five_measurable.ipynb) |
| 1.3 | Day 1 · Session 3 | Classify the case's data flows and derive the placement constraints | [`D1_3_classify_case_s.ipynb`](labs/D1_3_classify_case_s.ipynb) |
| 1.4 | Day 1 · Session 4 | Draw context and container views and budget one request's latency and cost | [`D1_4_draw_context_container.ipynb`](labs/D1_4_draw_context_container.ipynb) |
| 2.1 | Day 2 · Session 1 | Match six case needs to patterns and find the one a non-generative design serves better | [`D2_1_match_six_case.ipynb`](labs/D2_1_match_six_case.ipynb) |
| 2.2 | Day 2 · Session 2 | Cost three options and test their sensitivity to volume and token price | [`D2_2_cost_three_options.ipynb`](labs/D2_2_cost_three_options.ipynb) |
| 2.3 | Day 2 · Session 3 | Score exit cost and write two procurement requirements that keep the exit open | [`D2_3_score_exit_cost.ipynb`](labs/D2_3_score_exit_cost.ipynb) |
| 2.4 | Day 2 · Session 4 | Write two records, swap with a peer and challenge consequences and review triggers | [`D2_4_write_two_records.ipynb`](labs/D2_4_write_two_records.ipynb) |
| 3.1 | Day 3 · Session 1 | Build a demand matrix from the synthetic usage logs of nine teams | [`D3_1_build_demand_matrix.ipynb`](labs/D3_1_build_demand_matrix.ipynb) |
| 3.2 | Day 3 · Session 2 | Admit four models and make the supplied gateway refuse restricted data to an external model | [`D3_2_admit_four_models.ipynb`](labs/D3_2_admit_four_models.ipynb) |
| 3.3 | Day 3 · Session 3 | Walk a tenancy model through a leaked key, a noisy neighbour and a runaway agent | [`D3_3_walk_tenancy_model.ipynb`](labs/D3_3_walk_tenancy_model.ipynb) |
| 3.4 | Day 3 · Session 4 | Build a showback from synthetic invoices and tags and name untagged spend | [`D3_4_build_showback_from.ipynb`](labs/D3_4_build_showback_from.ipynb) |
| 4.1 | Day 4 · Session 1 | Turn a supplied retrieval service into a template with evaluation, tracing and classification checks on | [`D4_1_turn_supplied_retrieval.ipynb`](labs/D4_1_turn_supplied_retrieval.ipynb) |
| 4.2 | Day 4 · Session 2 | Write two checks that fail a design lacking an evaluation gate or sending restricted data out | [`D4_2_write_two_checks.ipynb`](labs/D4_2_write_two_checks.ipynb) |
| 4.3 | Day 4 · Session 3 | Review a supplied design for risks, sensitivity points and non-compliance | [`D4_3_review_supplied_design.ipynb`](labs/D4_3_review_supplied_design.ipynb) |
| 4.4 | Day 4 · Session 4 | Decide a deviation request and explain the trade-off on one page for a sponsor | [`D4_4_decide_deviation_request.ipynb`](labs/D4_4_decide_deviation_request.ipynb) |
<!-- /academy:labs -->

## Capstone

An architecture for one ministry service and the platform slice it runs on (scenarios, views, options paper, at least six decision records, and a working gateway, catalogue entry, golden path and showback) in a public repository, defended before a panel that includes a data architect. The follow-up task writes three decision records for a system from the participant's own work

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- AE-305 Operating Machine Learning and Language Model Systems
- AE-308 Securing Language Model and Agent Applications
- AE-311 Shaping the Build: Product Sense and Delivery Practice
- Has built and deployed at least one AI service that other people used
- Reads a cloud usage export or bill
- Can name the four national data classification levels

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Architecture views as code:** Structurizr DSL, Mermaid, PlantUML
- **Decision record templates:** MADR, a plain Markdown template
- **AI gateway:** LiteLLM, agentgateway
- **Fitness checks and policy:** Open Policy Agent with conftest, tests over infrastructure definitions
- **Project templates:** Copier, Backstage software templates
- **Cost modelling and allocation:** a Python notebook, OpenCost
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- Regulation on Personal Data Transfer outside the Kingdom: REPLACE: the address of the official text
- NDMO Data Classification Policy: REPLACE: the address of the official text
- National Cybersecurity Authority (NCA) Cloud Cybersecurity Controls: REPLACE: the address of the official text
- SDAIA AI Ethics Principles: REPLACE: the address of the official text
- National AI Risk Management Framework: REPLACE: the address of the official text
