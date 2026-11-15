<!-- academy:title -->
# AI Solution Architecture and Platform Design

معمارية حلول الذكاء الاصطناعي وتصميم المنصات

AI Engineering Track · SDAIA Academy · AE-402 · Level 400

Turn requirements into tested scenarios, costed options and recorded decisions, then design the shared AI platform many teams build on

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

**Ministry of Municipal Services (fictional).** Nine product teams build on Asas, the Ministry's shared AI platform, with data at three national classification levels (Public, Restricted, Secret). Days 1 and 2 architect Muyassir, the building-permits assistant: drivers and constraints from a brief and three interview notes, five measurable scenarios tested on 400 pilot requests, fourteen classified data flows, views generated as code, three options costed over three years (one of them non-generative) and a decision log. Days 3 and 4 design Asas itself: a demand matrix from six months of usage logs, model admission, a gateway that refuses Restricted data to an external model, a tenancy model walked through three incidents, a showback that reconciles with the invoices, a golden-path template, fitness checks and a structured review of the inspections team's design with its deviation request.

All data is synthetic and written by `labs/prepare_data.py` with a fixed seed; model ids, prices and people are invented. The placement rule the labs enforce (Public anywhere, Restricted in the Ministry or a cloud region in the Kingdom, Secret in the Ministry only) is the case's own policy, stricter by choice than the minimum the national texts set.

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Drivers, constraints and stakeholders | [`D1_1_drivers.ipynb`](labs/D1_1_drivers.ipynb) |
| 1.2 | Day 1 · Session 2 | Five measurable scenarios | [`D1_2_scenarios.ipynb`](labs/D1_2_scenarios.ipynb) |
| 1.3 | Day 1 · Session 3 | Classified flows and placement | [`D1_3_data_flows.ipynb`](labs/D1_3_data_flows.ipynb) |
| 1.4 | Day 1 · Session 4 | Views as code and a request budget | [`D1_4_views_budget.ipynb`](labs/D1_4_views_budget.ipynb) |
| 2.1 | Day 2 · Session 1 | Patterns and a non-generative baseline | [`D2_1_patterns.ipynb`](labs/D2_1_patterns.ipynb) |
| 2.2 | Day 2 · Session 2 | Three options over three years | [`D2_2_three_year_cost.ipynb`](labs/D2_2_three_year_cost.ipynb) |
| 2.3 | Day 2 · Session 3 | Exit cost, weights and two requirements | [`D2_3_exit_cost.ipynb`](labs/D2_3_exit_cost.ipynb) |
| 2.4 | Day 2 · Session 4 | Two decision records and a challenge | [`D2_4_decision_records.ipynb`](labs/D2_4_decision_records.ipynb) |
| 3.1 | Day 3 · Session 1 | A demand matrix from six months of usage | [`D3_1_demand_matrix.ipynb`](labs/D3_1_demand_matrix.ipynb) |
| 3.2 | Day 3 · Session 2 | Model admission and a gateway that refuses | [`D3_2_admission_gateway.ipynb`](labs/D3_2_admission_gateway.ipynb) |
| 3.3 | Day 3 · Session 3 | Three incidents, two tenancy models | [`D3_3_tenancy.ipynb`](labs/D3_3_tenancy.ipynb) |
| 3.4 | Day 3 · Session 4 | A showback that reconciles | [`D3_4_showback.ipynb`](labs/D3_4_showback.ipynb) |
| 4.1 | Day 4 · Session 1 | A golden path from the permits team's service | [`D4_1_golden_path.ipynb`](labs/D4_1_golden_path.ipynb) |
| 4.2 | Day 4 · Session 2 | Two fitness checks over designs as data | [`D4_2_fitness_checks.ipynb`](labs/D4_2_fitness_checks.ipynb) |
| 4.3 | Day 4 · Session 3 | A structured review of Kashif's design | [`D4_3_review.ipynb`](labs/D4_3_review.ipynb) |
| 4.4 | Day 4 · Session 4 | A deviation request, decided and explained on one page | [`D4_4_deviation.ipynb`](labs/D4_4_deviation.ipynb) |
<!-- /academy:labs -->

## Capstone

An architecture for one ministry service and the platform slice it runs on (scenarios, views, options paper, at least six decision records, and a working gateway, catalogue entry, golden path and showback) in a public repository, defended before a panel that includes a data architect. The follow-up task writes three decision records for a system from the participant's own work

**Submission:** a public GitHub repository link, sent before the defence; `labs/capstone/README.md` lists what it holds and `labs/capstone/briefs/` the three services to choose from. The defence is a 10-minute talk and 8 minutes of questions before a panel that includes a data architect.

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

### National references

- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [Regulation on Personal Data Transfer outside the Kingdom (SDAIA)](https://sdaia.gov.sa/Documents/RegulationonPersonalDataEN.pdf)
- [Data Classification Policy (National Data Management Office, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf)
- [Cloud Cybersecurity Controls (National Cybersecurity Authority)](https://nca.gov.sa/en/regulatory-documents/controls-list/ccc/)
- [AI Ethics Principles (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)
- [National AI Risk Management Framework, executive summary (SDAIA, April 2026)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf)

### Architecture methods

- [The Architecture Tradeoff Analysis Method (Software Engineering Institute)](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/)
- [The C4 model for visualising software architecture](https://c4model.com/)
- [Structurizr DSL documentation](https://docs.structurizr.com/dsl)
- [MADR: Markdown Architectural Decision Records](https://adr.github.io/madr/)
- [Architectural fitness function (Thoughtworks Technology Radar)](https://www.thoughtworks.com/radar/techniques/architectural-fitness-function)
- [CNCF Platforms White Paper (TAG App Delivery)](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### Platform tools (examples, interchangeable)

- [LiteLLM: virtual keys, budgets and rate limits](https://docs.litellm.ai/docs/proxy/virtual_keys)
- [LiteLLM: guardrails quick start](https://docs.litellm.ai/docs/proxy/guardrails/quick_start)
- [LiteLLM: fallbacks](https://docs.litellm.ai/docs/proxy/reliability)
- [agentgateway documentation](https://agentgateway.dev/docs/)
- [Conftest](https://www.conftest.dev/)
- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs)
- [Copier documentation](https://copier.readthedocs.io/en/stable/)
- [Backstage software templates](https://backstage.io/docs/features/software-templates/)
- [OpenCost documentation](https://opencost.io/docs/)
- [FinOps Framework: invoicing and chargeback](https://www.finops.org/framework/capabilities/invoicing-chargeback/)
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf and https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf
- Regulation on Personal Data Transfer outside the Kingdom: https://sdaia.gov.sa/Documents/RegulationonPersonalDataEN.pdf
- NDMO Data Classification Policy: https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf
- National Cybersecurity Authority (NCA) Cloud Cybersecurity Controls: https://nca.gov.sa/en/regulatory-documents/controls-list/ccc/
- SDAIA AI Ethics Principles: https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf
- National AI Risk Management Framework: https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf (the English executive summary; the full text is published in Arabic)
