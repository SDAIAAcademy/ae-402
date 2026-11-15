---
course: "AI Solution Architecture and Platform Design"
code: "AE-402"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-402/index.html"
---

# AI Solution Architecture and Platform Design

معمارية حلول الذكاء الاصطناعي وتصميم المنصات

AI Engineering Track · 4 teaching days + capstone day · 26 hours · Level 400

Turn requirements into tested scenarios, costed options and recorded decisions, then design the shared AI platform many teams build on

Participants practise the architect's loop on AI systems and apply it to the shared platform many teams build on. For a fictional ministry of municipal services with nine product teams and data at three classification levels, they turn requirements into measurable scenarios, draw views as code, cost three options including a non-generative one, keep a decision log, design a model catalogue, gateway, tenancy model, golden paths and showback, enforce a reference design with fitness checks, and review a peer's architecture. Serving optimisation and reliability engineering are left to AE-401 and AE-403.

**Who it is for:** Specialists. Engineers who have completed the level 300 core or can show equivalent work: a production AI system they built, operated and can defend.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Ministry of Municipal Services.** The Ministry of Municipal Services is a fictional ministry whose nine product teams build on Asas, its shared AI platform, with data at three classification levels. Participants architect Muyassir, its building-permits assistant (scenarios, classified flows, views as code, three costed options and a decision log), then design Asas itself: a demand matrix, model admission, a gateway that refuses Restricted data to an external model, tenancy, showback, a golden path, fitness checks and a structured review of the inspections team's design. All data is synthetic and generated with a fixed seed.

## The course

### Day 1: From requirements to architecture

Slides: https://sdaiaacademy.github.io/ae-402/slides/day1.md

- **Session 1: The architect's loop for AI systems**
  - Describe the architect's loop and where an AI system adds steps to it
  - Separate drivers, constraints, concerns and assumptions in a brief
  - Name the stakeholder who owns each concern
  - [Lab 1.1: Drivers, constraints and stakeholders (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D1_1_drivers.ipynb)
- **Session 2: Quality attributes with numbers**
  - Write a scenario with its six parts and a measurable response
  - Express answer quality, privacy and human oversight as targets
  - Test a scenario against measurements
  - [Lab 1.2: Five measurable scenarios (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D1_2_scenarios.ipynb)
- **Session 3: Regulation as a design constraint**
  - Classify a data flow by the highest level it carries
  - Derive placement constraints from classification and transfer rules
  - Find the flows a design must change
  - [Lab 1.3: Classified flows and placement (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D1_3_data_flows.ipynb)
- **Session 4: Views as code**
  - Generate context and container views from a model as code
  - Show hosting and classification on the views
  - Budget one request's latency and cost against the scenarios
  - [Lab 1.4: Views as code and a request budget (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D1_4_views_budget.ipynb)

### Day 2: Options and decisions

Slides: https://sdaiaacademy.github.io/ae-402/slides/day2.md

- **Session 1: Patterns and when each fits**
  - Match a need to a pattern with fit questions
  - Test a non-generative baseline on the same data as a generative one
  - Explain when a classical model serves a need better
  - [Lab 2.1: Patterns and a non-generative baseline (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D2_1_patterns.ipynb)
- **Session 2: Total cost over three years**
  - Build a three-year cost model with build, run, people, capacity and unanswered work
  - Compare options per answered question
  - Test the ranking's sensitivity to volume and token price
  - [Lab 2.2: Three options over three years (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D2_2_three_year_cost.ipynb)
- **Session 3: Lock-in and exit**
  - Price the exit of an option from its lock-in factors
  - Find the weight at which a weighted ranking flips
  - Write procurement requirements a reviewer can verify
  - [Lab 2.3: Exit cost, weights and two requirements (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D2_3_exit_cost.ipynb)
- **Session 4: Decision records**
  - Write a decision record with drivers, options and consequences both ways
  - Set a review trigger someone can test
  - Challenge a peer's record for what a lint cannot see
  - [Lab 2.4: Two decision records and a challenge (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D2_4_decision_records.ipynb)

### Day 3: The shared platform

Slides: https://sdaiaacademy.github.io/ae-402/slides/day3.md

- **Session 1: The platform is a product**
  - Build a demand matrix from usage logs and a team survey
  - Phase platform capabilities by shared demand
  - Spot in the logs what the platform should already prevent
  - [Lab 3.1: A demand matrix from six months of usage (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D3_1_demand_matrix.ipynb)
- **Session 2: Catalogue, admission and the gateway**
  - Admit models on licence, evaluation and data-term evidence
  - Write catalogue entries with the highest level each model may receive
  - Make a gateway refuse Restricted data to an external model
  - [Lab 3.2: Model admission and a gateway that refuses (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D3_2_admission_gateway.ipynb)
- **Session 3: Tenancy and shared capacity**
  - Compare a shared and a per-team tenancy model under incidents
  - Cap a team's share of shared capacity
  - Contain leaked keys and runaway spend with keys and budgets per team
  - [Lab 3.3: Three incidents, two tenancy models (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D3_3_tenancy.ipynb)
- **Session 4: Who pays for which tokens**
  - Allocate invoices to teams by usage, credits and fixed costs included
  - Reconcile a showback with each invoice within 2%
  - Name spend that no tag or owner explains
  - [Lab 3.4: A showback that reconciles (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D3_4_showback.ipynb)

### Day 4: Reference designs and reviews

Slides: https://sdaiaacademy.github.io/ae-402/slides/day4.md

- **Session 1: Golden paths**
  - Turn a team's service into a template other teams generate from
  - Put evaluation, classification checks and tracing on by default
  - Make switching a gate off visible to the platform
  - [Lab 4.1: A golden path from the permits team's service (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D4_1_golden_path.ipynb)
- **Session 2: Fitness functions**
  - Describe a design as data a program can read
  - Write a check for a blocking evaluation gate before deployment
  - Write a placement check that follows fallbacks
  - [Lab 4.2: Two fitness checks over designs as data (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D4_2_fitness_checks.ipynb)
- **Session 3: Structured architecture review**
  - Prioritise scenarios in a utility tree
  - Tell risks, sensitivity points, trade-off points and non-compliance apart
  - Write a review report with a verdict a team can act on
  - [Lab 4.3: A structured review of Kashif's design (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D4_3_review.ipynb)
- **Session 4: Deviations and sponsors**
  - Put numbers on what a deviation breaks and what refusing it costs
  - Decide a deviation with verifiable conditions, an expiry and reopen triggers
  - Explain a trade-off on one page for a sponsor
  - [Lab 4.4: A deviation request, decided and explained on one page (25 min)](https://sdaiaacademy.github.io/ae-402/labs/D4_4_deviation.ipynb)

### Capstone: Capstone project presentations

Slides: https://sdaiaacademy.github.io/ae-402/slides/capstone.md

## Capstone

An architecture for one ministry service and the platform slice it runs on (scenarios, views, options paper, at least six decision records, and a working gateway, catalogue entry, golden path and showback) in a public repository, defended before a panel that includes a data architect. The follow-up task writes three decision records for a system from the participant's own work

**What you submit:** A public GitHub repository link, sent before the defence. The repository holds the scenario sheet, the architecture document with views as code and one request traced end to end, the options paper with total cost, lock-in and sensitivity, at least six dated decision records, and the platform slice (gateway with its refusal test and logs, catalogue entry, golden-path template, showback that reconciles within 2%), with the fitness checks running in its pipeline.

**Rubric:**

- Scenarios and views: 20%
- Options and decisions: 25%
- Platform slice: 25%
- Fitness checks: 15%
- Review: 15%

## Outcomes

- **LO1** Prepare quality-attribute scenarios with measurable targets for answer quality, latency, cost, privacy and human oversight, given the case brief, three interview notes and the data inventory (Applied) Evidence: a scenario sheet a reviewer can test a design against
- **LO2** Design an end-to-end architecture with context, container and data-flow views and a per-request latency and cost budget, given the scenario sheet and the classification of each data flow (Performance) Evidence: an architecture document with views as code and one request traced end to end
- **LO3** Evaluate at least three solution options, including a non-generative baseline, and record the resulting decisions, given weighted criteria, a three-year volume forecast and price ranges (Performance) Evidence: an options paper with total cost, lock-in and sensitivity analysis, and at least six decision records
- **LO4** Design a shared AI platform covering model admission, gateway, tenancy, golden paths and cost attribution, given nine teams, three classification levels, synthetic usage logs and invoices (Performance) Evidence: a design and a working slice whose gateway refuses restricted data to an external model and whose showback reconciles within 2%
- **LO5** Design a reference architecture with fitness functions that check conformance automatically, given a recurring pattern: retrieval over classified documents (Performance) Evidence: a template and two automated checks that fail on a non-conforming design
- **LO6** Review a peer's architecture with a structured trade-off method and decide on a requested deviation, given a peer design, the reference designs and a deviation request (Performance) Evidence: a review report naming risks, sensitivity points and non-compliance, with a recorded decision

## Tools

- **Architecture views as code:** Structurizr DSL, Mermaid, PlantUML
- **Decision record templates:** MADR, a plain Markdown template
- **AI gateway:** LiteLLM, agentgateway
- **Fitness checks and policy:** Open Policy Agent with conftest, tests over infrastructure definitions
- **Project templates:** Copier, Backstage software templates
- **Cost modelling and allocation:** a Python notebook, OpenCost

## Prerequisites

- AE-305 Operating Machine Learning and Language Model Systems
- AE-308 Securing Language Model and Agent Applications
- AE-311 Shaping the Build: Product Sense and Delivery Practice
- Has built and deployed at least one AI service that other people used
- Reads a cloud usage export or bill
- Can name the four national data classification levels

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

---

SDAIA Academy · AI Engineering Track · AI Solution Architecture and Platform Design

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit b2bfbf8
