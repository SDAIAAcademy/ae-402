---
course: "AI Solution Architecture and Platform Design"
code: "AE-402"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-402/"
---

# AI Solution Architecture and Platform Design

Turn requirements into tested scenarios, costed options and recorded decisions, then design the shared AI platform many teams build on

Participants practise the architect's loop on AI systems and apply it to the shared platform many teams build on. For a fictional ministry of municipal services with nine product teams and data at three classification levels, they turn requirements into measurable scenarios, draw views as code, cost three options including a non-generative one, keep a decision log, design a model catalogue, gateway, tenancy model, golden paths and showback, enforce a reference design with fitness checks, and review a peer's architecture. Serving optimisation and reliability engineering are left to AE-401 and AE-403.

- **Audience:** Specialists. Engineers who have completed the level 300 core or can show equivalent work: a production AI system they built, operated and can defend.
- **Prerequisites:** AE-305 Operating Machine Learning and Language Model Systems; AE-308 Securing Language Model and Agent Applications; AE-311 Shaping the Build: Product Sense and Delivery Practice; Has built and deployed at least one AI service that other people used; Reads a cloud usage export or bill; Can name the four national data classification levels
- **Case study:** Ministry of Municipal Services: The Ministry of Municipal Services is a fictional ministry whose nine product teams build on Asas, its shared AI platform, with data at three classification levels. Participants architect Muyassir, its building-permits assistant (scenarios, classified flows, views as code, three costed options and a decision log), then design Asas itself: a demand matrix, model admission, a gateway that refuses Restricted data to an external model, tenancy, showback, a golden path, fitness checks and a structured review of the inspections team's design. All data is synthetic and generated with a fixed seed.

## Outcomes

- LO1 (Applied): Prepare quality-attribute scenarios with measurable targets for answer quality, latency, cost, privacy and human oversight, given the case brief, three interview notes and the data inventory
- LO2 (Performance): Design an end-to-end architecture with context, container and data-flow views and a per-request latency and cost budget, given the scenario sheet and the classification of each data flow
- LO3 (Performance): Evaluate at least three solution options, including a non-generative baseline, and record the resulting decisions, given weighted criteria, a three-year volume forecast and price ranges
- LO4 (Performance): Design a shared AI platform covering model admission, gateway, tenancy, golden paths and cost attribution, given nine teams, three classification levels, synthetic usage logs and invoices
- LO5 (Performance): Design a reference architecture with fitness functions that check conformance automatically, given a recurring pattern: retrieval over classified documents
- LO6 (Performance): Review a peer's architecture with a structured trade-off method and decide on a requested deviation, given a peer design, the reference designs and a deviation request

## Day 1: From requirements to architecture

Drivers, scenarios with numbers, classified flows and views as code for Muyassir

#### [day1#title] From requirements to architecture

*SDAIA Academy · AI Solution Architecture and Platform Design*

Day 1: Drivers, scenarios with numbers, classified flows and views as code for Muyassir

AI Engineering Track · 4 teaching days + capstone day · 4 sessions · 4 labs · AE-402

#### [day1#agenda] From requirements to architecture

*Today*

- **Session 1 · The architect's loop for AI systems**: The loop an architect runs on an AI system, starting from drivers, constraints and the people who hold them
- **Session 2 · Quality attributes with numbers**: Quality-attribute scenarios with a measure a reviewer can compute, answer quality and oversight included
- **Session 3 · Regulation as a design constraint**: Classification levels and transfer rules as inputs that decide where each data flow may be processed
- **Session 4 · Views as code**: Context and container views generated from one model, and one request budgeted for latency and cost

#### [day1#setup-check] Every lab runs on a laptop processor or in Colab, with no key

*Before Session 1*

```bash
# file: labs/
uv sync
uv run prepare_data.py
uv run jupyter lab
```

In Colab, the first cell of each notebook clones the course and installs what is missing.

- The data is synthetic and already in `labs/data/`; the generator rebuilds the same files.
- No model is downloaded. Where a lab needs a model, a scripted stand-in answers, labelled as such.
- Each lab starts from supplied reference files: missing a lab never blocks the next one.

### Session 1: The architect's loop for AI systems

#### [day1#s1] The architect's loop for AI systems

*Session 1*

- Describe the architect's loop and where an AI system adds steps to it
- Separate drivers, constraints, concerns and assumptions in a brief
- Name the stakeholder who owns each concern

#### [day1#architects-loop] Architecture is a loop from drivers to decisions, then back

*The architect's loop*

1. **1 · Drivers** goals, constraints, concerns
2. **2 · Scenarios** targets with numbers
3. **3 · Options** three, costed
4. **4 · Decisions** recorded, with triggers
5. **5 · Review** tested against scenarios

Views are drawn all along the loop. A review that finds a failed scenario sends you back to step 3, not to a slide tool.

#### [day1#what-ai-adds] An AI system adds four attributes a classic design rarely names

*What changes for AI systems*

- **Answer quality.** Correctness varies by question type, language and model version.
- **Cost per request.** Tokens make cost a function of each prompt, not of a server count.
- **Data in prompts.** Every prompt is a data flow to wherever the model runs.
- **Human oversight.** Some answers must go to a person, by design.

> **What goes wrong.** These four are discovered after launch, by a complaint, a bill or a data protection officer.

#### [day1#the-ministry] One ministry, nine product teams, one shared platform

*The case study*

- **9** product teams on Asas, the shared AI platform
- **3** classification levels in use: Public, Restricted, Secret
- **38,000** building-permit applications a year

The Ministry of Municipal Services is fictional and its data synthetic. Days 1 and 2 architect **Muyassir**, the building-permits assistant; Days 3 and 4 design **Asas** itself.

#### [day1#four-kinds] Drivers, constraints, concerns and assumptions need different handling

*Sorting what people say*

| Kind | What it is | From the Muyassir interviews | What you do with it |
| --- | --- | --- | --- |
| **Driver** | A goal the system exists for | Median permit cycle from 21 to 10 days | Turn it into a measure |
| **Constraint** | A decision already taken | The permits system offers reads only | Obey it; record its owner |
| **Concern** | A stakeholder's worry | "Only an inspector can approve" | Answer it with a scenario |
| **Assumption** | Believed, not checked | Most questions cover 40 topics | Test it before relying on it |

#### [day1#stakeholders] A concern without an owner is never closed

*Stakeholders*

| Owner | Concern |
| --- | --- |
| Sponsor | No wrong requirement told to a citizen |
| Inspectors | The assistant must never sound as if it approves |
| Applicants | Know it is an assistant; reach a person |
| Permit staff | Logs must not rank their performance |
| Permits team | Traffic doubles after a fee change |

- **The owner signs the scenario.** When the inspectors' concern becomes a scenario with a target, the inspectors agree the target. That is how a concern gets closed.

#### [day1#said-once] The constraint that matters most was said once, in passing

*The hidden constraint*

**Data protection officer:** Applicant files hold national identity numbers, deeds and site plans. They are Restricted, and they do not leave the Kingdom: not for storage, not for processing, not for a quick look by a model.

- **Ruled out.** An external OCR service for deeds; an external model with applicant context; logs to an external dashboard.
- **Still open.** A model hosted in the Kingdom; an external embedding of the published code.

#### [day1#deliverables] Every lab produces a piece of an architecture a panel can test

*The course in one ladder*

1. **Scenarios**: with numbers (Day 1)
2. **Views**: as code (Day 1)
3. **Options**: and decisions (Day 2)
4. **Platform**: slice (Day 3)
5. **Checks**: and review (Day 4)

#### [day1#check-constraint] Which statement is a constraint?

*Checkpoint*

**Question:** Four sentences from the Muyassir notes. Which one is a constraint the design must obey?

- A. Cut the median permit cycle from 21 to 10 days
- B. The permits system offers a read interface only this year
- C. Inspectors fear the assistant will sound as if it approves
- D. Most questions are about the same 40 topics

#### [day1#lab-1-1] Drivers, constraints and stakeholders

Lab 1.1 · 25 min

Sort twenty statements from the Muyassir brief and three interview notes into drivers, constraints, concerns and assumptions, name each concern's owner, and find the constraint said once that rules out three designs.

[D1_1_drivers.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D1_1_drivers.ipynb)

- [ ] Read the brief and the three notes (5 min)
- [ ] Sort twenty statements (8 min)
- [ ] Name the owner of each concern (5 min)
- [ ] The hidden constraint and what it rules out (7 min)
- [ ] ✱ Stretch: Write two statements the notes are missing

### Session 2: Quality attributes with numbers

#### [day1#s2] Quality attributes with numbers

*Session 2*

- Write a scenario with its six parts and a measurable response
- Express answer quality, privacy and human oversight as targets
- Test a scenario against measurements

#### [day1#ai-attributes] Five attributes carry most of Muyassir's risk

*Quality attributes for AI*

- **Answer quality.** Share of correct answers, per question type and language
- **Latency.** A percentile of the end-to-end time
- **Cost.** Per answer, from tokens and the price card
- **Privacy.** Answers that expose another person's data
- **Human oversight.** Cases that must reach a person, and do
- **And the classics.** Availability, security, modifiability stay

#### [day1#six-parts] A scenario has six parts, and the last one carries a number

*The scenario*

1. **Source** an engineering office
2. **Stimulus** asks any question
3. **Environment** a normal working day
4. **Artefact** Muyassir via the gateway
5. **Response** a complete answer
6. **Measure** p95 ≤ 4,000 ms

> **Testable.** The measure names a metric that is recorded, a statistic and a target.

#### [day1#vague-to-measure] "Fast, accurate and available" becomes three measures

*From the brief*

| The brief says | The scenario measures | Who measures it |
| --- | --- | --- |
| fast | p95 of end-to-end latency ≤ 4,000 ms on a normal day | gateway logs |
| accurate | share of correct answers to requirements questions ≥ 0.90 | reviewers on a sample |
| available at all times | share of working-hours requests accepted ≥ 0.995 over a month | the platform team |

> **What goes wrong.** A target nobody measures. The lab's lint flags availability: the pilot never recorded it, so the platform team owes a measurement.

#### [day1#quality-by-type] Measure answer quality per question type, on a reviewed sample

*Answer quality is a number*

- A reviewer marks each pilot answer correct or not, against the building code.
- The scenario names the slice: requirements questions, 197 of the 400.
- Fee questions are 26 of 400: too few to claim anything about them yet.

**0.92** correct on requirements questions in the pilot; target 0.90

#### [day1#oversight-number] Human oversight becomes the share of cases that reach a person

*Oversight is a number too*

- applicant: Will my extension be approved if I move the stairs?
- rule: approval question: only an inspector decides
- answer: I cannot approve designs. An inspector can review it; shall I book a hand-over?

**46 of 53** approval questions offered a person in the pilot

> **Target 0.99.** The pilot reaches 0.87: it fails.

#### [day1#privacy-sum] For privacy, count the leaks: a mean hides the one that matters

*Choose the statistic*

**1 of 400** pilot answers showed another applicant's file (request P0288)

- Mean leak rate: 0.0025. It looks like success.
- Sum of leaks with a target of zero: it fails, as it should.
- One leak of a deed is a reportable incident, not a rate.

#### [day1#pilot-results] Tested against 400 pilot requests, three of five scenarios fail

*Measured in Lab 1.2*

| Scenario | Measure | Pilot | Result |
| --- | --- | --- | --- |
| Q1 answer quality | mean correct, requirements ≥ 0.90 | 0.919 | passes |
| Q2 latency | p95 ≤ 4,000 ms | 4,866 | fails |
| Q3 cost | mean ≤ SAR 0.05 per answer | 0.022 | passes |
| Q4 privacy | leaks = 0 | 1 | fails |
| Q5 oversight | approval questions offered a person ≥ 0.99 | 0.868 | fails |

#### [day1#check-scenario] Which scenario can a reviewer test?

*Checkpoint*

**Question:** Four drafts for the inspectors' concern. Which one can be tested against pilot data?

- A. Muyassir never sounds as if it approves a design
- B. At least 99% of all answers offer a person
- C. At least 99% of approval questions get an offer of a person
- D. The prompt tells the model that only inspectors approve

#### [day1#lab-1-2] Five measurable scenarios

Lab 1.2 · 25 min

Rewrite the brief's vague targets, write five scenarios for answer quality, latency, cost, privacy and human oversight, and test each against 400 pilot requests.

[D1_2_scenarios.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D1_2_scenarios.ipynb)

- [ ] The six parts of a scenario (4 min)
- [ ] Fix the brief's three vague targets (6 min)
- [ ] Write five scenarios, answer quality and oversight included (8 min)
- [ ] Test them on the pilot measurements (7 min)
- [ ] ✱ Stretch: A scenario for the fee-change peak

### Session 3: Regulation as a design constraint

#### [day1#s3] Regulation as a design constraint

*Session 3*

- Classify a data flow by the highest level it carries
- Derive placement constraints from classification and transfer rules
- Find the flows a design must change

#### [day1#four-levels] Four levels, set by the impact of unauthorised disclosure

*National data classification*

| Level | Impact of disclosure | In the Ministry |
| --- | --- | --- |
| Top Secret | high | none in this case |
| Secret | medium | tender documents, land disputes, state land surveys |
| Restricted | low | applicant files, status records, conversation logs |
| Public | none | the published building code, fee schedule, zoning maps |

#### [day1#three-principles] Open by default, highest level wins, classify at creation

*Three principles that shape designs*

- **Open by default.** Data is accessible unless its nature or sensitivity requires more protection.
- **Highest level.** A dataset that combines levels takes the highest of them. A prompt is such a dataset.
- **Timely.** Data is classified when created or received, so a new log needs a level on day one.

#### [day1#transfer-rules] Transfer abroad is a regulated path, not a hosting preference

*Personal data outside the Kingdom*

- **Adequacy.** The competent authority publishes the countries and organisations that give an appropriate level of protection.
- **Safeguards.** Otherwise, in set cases: standard contractual clauses, binding common rules or an accreditation certificate.
- **Onward transfer.** The Law still applies when data moves on from the first recipient.

> **For the architecture.** Each flow that could leave the Kingdom names its path, or does not leave.

#### [day1#placement-rule] Each level maps to where its data may be processed

*The Ministry's own rule*

| Level | Ministry data centre | Cloud region in the Kingdom | External service |
| --- | --- | --- | --- |
| Public | yes | yes | yes |
| Restricted | yes | yes | no |
| Secret | yes | no | no |

Asas policy P-01. It is the case's rule, stricter by choice than the minimum the national texts set.

#### [day1#prompt-is-a-flow] A prompt is a data flow, and it takes the level of what it holds

*Prompts carry data*

- question: Which documents are still missing from my application?
- retrieved: clause 4.2 of the published code (Public)
- status read: application record with identity number (Restricted)
- prompt level: Restricted: the highest of its parts
- placement: Ministry or a cloud region in the Kingdom only

#### [day1#three-violations] Three of Muyassir's fourteen flows break the rule

*Measured in Lab 1.3*

| Flow | Carries | Goes to | Breaks |
| --- | --- | --- | --- |
| F07 | scanned deeds and site plans | external OCR | S12, applicant files stay in the Kingdom |
| F09 | conversation logs | external analytics | S13, logs are personal data |
| F14 | unpublished draft circulars | external summary model | S15, an unchecked assumption |

> **Allowed, and worth saying so.** F04 sends the published code to an external embedding model.

#### [day1#ethics-inputs] Ethics principles enter the design as scenarios, not as a final check

*Responsible AI from the start*

- **Privacy and security.** Q4: no answer shows another applicant's file.
- **Transparency and explainability.** S14: citizens know it is an assistant; answers cite the clause.
- **Accountability and responsibility.** Q5: approvals stay with an inspector, by measure.

#### [day1#check-flow-level] Where may this flow go?

*Checkpoint*

**Question:** A missing-documents check sends the published building code, an applicant's form with identity number and a site plan to a model. Under the Ministry's rule, where may the model run?

- A. In the Ministry or in a cloud region in the Kingdom
- B. Anywhere, since most of the prompt is the published code
- C. Only in the Ministry's own data centre
- D. Anywhere, once the identity number is masked

#### [day1#lab-1-3] Classified flows and placement

Lab 1.3 · 25 min

Complete the data inventory, give each of Muyassir's fourteen flows its level, derive where it may be processed, and find the three flows that break the Ministry's placement rule.

[D1_3_data_flows.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D1_3_data_flows.ipynb)

- [ ] Fill the three blank levels (5 min)
- [ ] The level of each flow (6 min)
- [ ] Where each flow may go (6 min)
- [ ] The violations and what each breaks (8 min)
- [ ] ✱ Stretch: Redesign the violating flows

### Session 4: Views as code

#### [day1#s4] Views as code

*Session 4*

- Generate context and container views from a model as code
- Show hosting and classification on the views
- Budget one request's latency and cost against the scenarios

#### [day1#c4-levels] Each view answers one question for one audience

*Views*

- **Context.** Who and what does the system talk to? Sponsors read this.
- **Container.** What runs where, and how do the parts talk? Architects and security.
- **Data flow.** Which data, at which level, goes where? The data protection officer.
- **Request trace.** One request through every hop, with time and cost.

#### [day1#muyassir-context] In the context view, Muyassir is one box

*Muyassir's context*

**Applicant** citizen or office → **Muyassir** permits assistant on Asas → **Permits system** status, read only

- **National single sign-on.** signs the applicant in
- **Contact centre.** takes hand-overs
- **Inspector.** reviews and approves

#### [day1#views-as-code] Generate views from one model, so a pull request changes them

*Views as code*

```text
# file: views/containers.mmd
flowchart LR
  subgraph muyassir["Muyassir"]
    gateway["Asas gateway<br/>hosting: ministry"]
    answer_model["Answer model<br/>hosting: ksa_cloud"]
  end
  gateway -->|routes by classification| answer_model
```

- One model file holds elements and relations; every view is generated.
- A change of hosting is a diff a reviewer sees.
- A check can read the same model: Day 4 does.

#### [day1#hosting-on-boxes] Write hosting on every box, so placement can be read off the view

*The container view*

| Container | Technology | Hosting |
| --- | --- | --- |
| Muyassir service | Python | ministry |
| Asas gateway | AI gateway | ministry |
| Regulations index | vector and keyword index | ministry |
| Reranker | cross-encoder | ministry |
| Answer model | ksa-general-m | ksa_cloud |
| Log store | object store, 90-day expiry | ministry |

#### [day1#request-hops] Two hops hold most of the time of a request

*One request traced*

| Item | Value |
| --- | --- |
| Answer model | 2,900 ms |
| Reranker | 650 ms |
| Status read | 400 ms |
| Retrieval | 180 ms |
| Portal, sign-on, gateway | 160 ms |

p95 per hop, from the supplied hop measurements (synthetic). The log write is off the user's path.

#### [day1#budget-result] The request costs half its budget and runs 290 ms over its time

*The budget*

- **4,290 ms** sum of p95s on the user's path; target 4,000
- **SAR 0.025** per request, from tokens and the price card; target 0.05
- **3,640 ms** without the reranker for status questions

#### [day1#sum-is-bound] A sum of p95s is an upper bound; check it against one measurement

*Reading a budget*

- Slow tails of different hops rarely meet in one request, so the sum overstates.
- Retries and queues add time no single hop shows, so the sum can also understate.
- The pilot measured 4,866 ms end to end: here the bound was not pessimistic.

> **What goes wrong.** A budget built from p50s. It fits on paper, and half the users wait longer.

#### [day1#check-budget] Which change can bring Muyassir under 4,000 ms?

*Checkpoint*

**Question:** The sum of p95s is 4,290 ms: model 2,900, reranker 650, status read 400, the rest 340. Which single change most likely brings the p95 under 4,000 ms without a new model?

- A. Write the conversation log faster
- B. Tune the index for a faster median query
- C. Add a second gateway check before the model
- D. Skip reranking for status questions and send fewer clauses

#### [day1#lab-1-4] Views as code and a request budget

Lab 1.4 · 25 min

Generate Muyassir's context and container views as Mermaid from one model file, then trace a request through eight hops and add up its latency and cost against the scenarios.

[D1_4_views_budget.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D1_4_views_budget.ipynb)

- [ ] Read the model of Muyassir (3 min)
- [ ] The context view as Mermaid (7 min)
- [ ] The container view, with hosting on every box (7 min)
- [ ] One request end to end: latency and cost (8 min)
- [ ] ✱ Stretch: Cut the request to fit 4,000 ms

#### [day1#wrap-up] Three things to keep

*Day 1*

- **Sort before you design.** Constraints said once rule out designs; find them first.
- **Numbers make scenarios testable.** A metric, a statistic and a target, owned by the stakeholder.
- **Classification decides placement.** Every flow has a level, and every box shows where it runs.

#### [day1#next] Tomorrow: three options, their cost over three years, and the decisions

*Day 2*

- Keep `artifacts/D1_2/scenarios.json` and `artifacts/D1_4/architecture.md`: the capstone reuses their shape.
- Read the three-year forecast in `labs/data/options/` once before the first session.
- Bring one decision from your own work that nobody wrote down.

## Day 2: Options and decisions

Patterns, three options costed over three years, lock-in and a decision log

#### [day2#title] Options and decisions

*SDAIA Academy · AI Solution Architecture and Platform Design*

Day 2: Patterns, three options costed over three years, lock-in and a decision log

AI Engineering Track · 4 teaching days + capstone day · 4 sessions · 4 labs · AE-402

#### [day2#agenda] Options and decisions

*Today*

- **Session 1 · Patterns and when each fits**: Six architecture patterns for AI needs, and the fit questions that choose between them
- **Session 2 · Total cost over three years**: Three-year total cost with every line the Ministry pays, and the assumptions the ranking depends on
- **Session 3 · Lock-in and exit**: Where lock-in sits, what leaving costs, how weights mislead, and contract terms that keep the exit open
- **Session 4 · Decision records**: Decision records with both kinds of consequence and a trigger that says when to reopen them

#### [day2#review-day1] Which finding of Day 1 changes the options you may draw today?

*Review of Day 1*

**Question:** Day 1 produced a scenario sheet, fourteen classified flows and a request budget. Which finding most limits today's options for Muyassir's answer model?

- A. The request costs SAR 0.025, half of its cost target
- B. The reranker takes 650 ms of the p95
- C. Prompts with applicant context are Restricted and stay in the Kingdom
- D. One pilot answer showed another applicant's file

### Session 1: Patterns and when each fits

#### [day2#s1] Patterns and when each fits

*Session 1*

- Match a need to a pattern with fit questions
- Test a non-generative baseline on the same data as a generative one
- Explain when a classical model serves a need better

#### [day2#six-patterns] Six patterns cover most of what the Ministry's teams ask for

*Patterns*

| Pattern | Fits when | A need at the Ministry |
| --- | --- | --- |
| Retrieval | answers come from changing documents, with a citation | permit questions from the code |
| Agentic | several steps whose order depends on results | pre-check of a submission |
| Fine-tuned | a stable output form, high volume, thousands of examples | standard inspection letters |
| Classical | a label from a fixed list, labelled data, speed and cost matter | routing citizen reports |
| Batch | the answer is needed in hours, over many records | nightly backlog summaries |
| Event-driven | something must happen when a record changes | status-change notices |

#### [day2#fit-questions] Five questions choose the pattern before anyone names a model

*Choosing by questions, not habit*

1. **What is the output?** A label, a cited answer, a document, an action.
2. **Are there labelled examples?** Thousands change the options.
3. **Who is waiting?** A person in seconds, a process in minutes, nobody until morning.
4. **How many steps,** and does each depend on the last?
5. **How does the data change?** Stable, weekly, live.

#### [day2#knowledge-or-form] Retrieval brings knowledge; fine-tuning shapes form

*A common confusion*

- **Retrieval.** The building code changes with each circular. Retrieval reads today's version and cites it. Updating means re-indexing, not retraining.
- **Fine-tuning.** Inspection letters follow one house style. 9,000 approved letters can teach the form; facts still come from the inspector's notes.

> **What goes wrong.** Tuning a model on the code to "know" it: the next circular makes the model wrong and nobody can see where.

#### [day2#agent-when] Choose an agent only when the next step depends on the last result

*Agentic*

- task: pre-check submission 2027-114 for missing documents
- step 1: read the forms: building type is a commercial extension
- step 2: so query the permits system for the fire-safety approval
- result: approval missing
- output: two documents missing, with the clauses that require them

#### [day2#nobody-waiting] Batch and event-driven designs move work off the user's path

*When nobody is waiting*

- **Batch.** Thirty district summaries a night: run them together at off-peak capacity, retry failures, and nobody sees a latency.
- **Event-driven.** A status change publishes an event; a notifier reacts. 40,000 notices a month, and no applicant has to ask.

Every status notice that is sent is a status call that is not made: the driver S02 is served by an event, not by a chat.

#### [day2#integration] APIs for questions, events for changes

*Integration*

| Interface | Muyassir uses it for | Design rule |
| --- | --- | --- |
| Read API of the permits system | status of one application | read only (S09); timeouts and a hand-over |
| Status-change events | notices to applicants | at-least-once, so notices are idempotent |
| Gateway API (OpenAI-compatible) | every model call | one door for credentials, quotas and audit |

#### [day2#classifier-wins] For routing reports, a classifier beats the generative model

*Measured in Lab 2.1*

| On the same 600 test reports | Accuracy | Mean latency | SAR a month, 95,000 reports |
| --- | --- | --- | --- |
| Classifier, character n-grams | 0.938 | 0.1 ms | 0 |
| Generative model (recorded) | 0.908 | 1,340 ms | 156 |

The classifier trains in seconds on a laptop processor; it is also right more often in Arabic: 0.951 against 0.903.

#### [day2#always-a-baseline] Cost one option without a generative model, every time

*The non-generative baseline*

- It shows what the generative model must beat, in quality and in cost.
- It is the fallback when the model is down or over budget.
- Sometimes it wins outright, as for report routing.
- When it loses, say on what: for Muyassir, it answers 70% of questions against 92%.

#### [day2#check-pattern] Which pattern for the street-light reports?

*Checkpoint*

**Question:** The reports team wants each report routed to one of six departments, within seconds, at 95,000 reports a month, with 24,000 labelled reports from last year. Which design do you cost first?

- A. A classifier trained on the labelled reports
- B. Retrieval over past reports, then a generated answer
- C. An agent that reads the report and calls department tools
- D. A frontier model with a routing prompt

#### [day2#lab-2-1] Patterns and a non-generative baseline

Lab 2.1 · 25 min

Match six case needs to patterns, train a classifier on 2,400 citizen reports on a laptop processor and compare it with a recorded generative run on the same 600 test reports.

[D2_1_patterns.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D2_1_patterns.ipynb)

- [ ] Six patterns, six fit questions (4 min)
- [ ] Match six needs to patterns (6 min)
- [ ] Train a classifier on 2,400 reports (8 min)
- [ ] Compare it with the recorded generative run (7 min)
- [ ] ✱ Stretch: Errors by language

### Session 2: Total cost over three years

#### [day2#s2] Total cost over three years

*Session 2*

- Build a three-year cost model with build, run, people, capacity and unanswered work
- Compare options per answered question
- Test the ranking's sensitivity to volume and token price

#### [day2#three-options] Three options, one of them without a generative model

*Muyassir's options*

- **O1 · Hosted in the Kingdom.** A model in a cloud region of the Kingdom, paid per token. Answers 92% of questions.
- **O2 · Ministry-hosted.** An open-weight model on the Ministry's accelerators, paid per server. Answers 92%.
- **O3 · Non-generative.** Guided search and a document checklist. Answers 70%.

Prices are the case's synthetic ranges, not vendor prices.

#### [day2#cost-lines] Five lines make a three-year cost, and the last one is often forgotten

*Total cost of ownership*

| Line | What it holds | Moves with |
| --- | --- | --- |
| Build | first year only | scope |
| Run and people | platform fees, the team that operates it | time |
| Tokens | requests × tokens × price | volume and price |
| Capacity units | servers sized for the peak month | peak volume, in steps |
| Unanswered work | questions not answered become calls | volume and coverage |

#### [day2#base-result] At the base forecast, O1 costs least over three years

*Measured in Lab 2.2*

| Option | Three years, SAR | Per answered question | Year-1 run, SAR |
| --- | --- | --- | --- |
| O1 hosted in the Kingdom | 6.25 million | 1.08 | 1.40 million |
| O2 Ministry-hosted | 7.59 million | 1.31 | 1.71 million |
| O3 non-generative | 11.92 million | 2.71 | 2.27 million |

Year-1 run includes the calls from unanswered questions. Without them, O1 runs at about SAR 1.0 million, under the SAR 1.2 million cap.

#### [day2#tornado] Volume moves O1's total by half; token price by 3%

*Sensitivity, one assumption at a time*

| Item | Value |
| --- | --- |
| Volume high | +58% |
| Volume low | -20% |
| Token price ×2 | +3% |
| Token price ×0.5 | -2% |

O1's three-year total against its base of SAR 6.25 million (Lab 2.2, step 4).

#### [day2#crossover] The Ministry-hosted model wins only at high volume and double prices

*When would O2 win?*

**900,000** requests a month, steady, at double the token price: O2 matches O1

- At the base price there is no crossover below three million a month.
- The high forecast reaches 900,000 only in its last month.
- So the decision has a trigger: volume, then price.

#### [day2#ranges-not-points] Show ranges and their sources, never one confident number

*Reading cost models*

- Every price has a source and the date it was read.
- Every volume has an owner who will defend it.
- Every option is costed with the same lines.

> **What goes wrong.** An options paper that costs the favourite option in detail and the others on a napkin. Reviewers spot it from the number of lines.

#### [day2#check-tco] What should the options paper argue about?

*Checkpoint*

**Question:** In Lab 2.2, doubling the token price moves O1's three-year total by 3%, the high forecast by 58%, and O3 loses on unanswered calls. Where should the sponsor's meeting spend its time?

- A. Negotiating the token price
- B. Cutting the build cost of O1
- C. Choosing O3 because it is cheapest to run
- D. The volume forecast and how many questions each option answers

#### [day2#lab-2-2] Three options over three years

Lab 2.2 · 25 min

Cost a hosted, a Ministry-hosted and a non-generative option on a 36-month forecast, then move volume and token price one at a time.

[D2_2_three_year_cost.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D2_2_three_year_cost.ipynb)

- [ ] Read the forecast and the price ranges (3 min)
- [ ] The cost model, year by year (9 min)
- [ ] Three options at the base forecast (5 min)
- [ ] Sensitivity to volume and token price (8 min)
- [ ] ✱ Stretch: The crossover volume

### Session 3: Lock-in and exit

#### [day2#s3] Lock-in and exit

*Session 3*

- Price the exit of an option from its lock-in factors
- Find the weight at which a weighted ranking flips
- Write procurement requirements a reviewer can verify

#### [day2#where-lockin] Lock-in sits in the data and the contract, rarely in the model

*Lock-in*

- **Data.** Indexes and logs in a store with no bulk export
- **Contract.** Minimum terms and early-exit fees
- **Formats.** Prompts and tools in one provider's shape
- **Evidence.** Evaluation sets kept only in a vendor console

#### [day2#exit-costs] The cheapest option to run is the dearest to leave

*Measured in Lab 2.3*

| Option | Exit cost, SAR |
| --- | --- |
| O1 hosted in the Kingdom | 540,000 |
| O3 non-generative | 357,500 |
| O2 Ministry-hosted | 322,500 |

| Item | Value |
| --- | --- |
| Vector store, no export | 250,000 |
| Early-exit fee | 167,500 |
| Prompt formats | 70,000 |
| Evaluation in console | 52,500 |

Person-months at SAR 35,000 plus fees, from the case's exit factors.

#### [day2#weights-pitfalls] Weights are opinions; report how far they can move

*Weighted criteria*

- **Double counting.** Three-year cost and exit cost are both money; say so, or merge them.
- **Ordinal scores.** A 4 is not twice a 2; small score gaps are noise.
- **Hidden weights.** A criterion left out has weight zero, by decision.
- **Rank reversal.** Find the weight at which the leader changes, and print it.

#### [day2#flip-weight] Weigh exit cost at 0.13 instead of 0.10, and O2 overtakes O1

*Measured in Lab 2.3*

- **4.20** O1's weighted score at an exit weight of 0.10
- **4.10** O2's weighted score at the same weights
- **0.13** exit-cost weight at which O2 leads

> **A fragile ranking.** A three-point change of one weight reverses it. The decision record says so.

#### [day2#requirements] A procurement requirement keeps the exit open only if it can be verified

*Buying the exit down*

**Weak (weak example):** The provider will make data available where possible.

**Verifiable (good example):** The provider shall export all indexed documents, their embeddings and metadata in JSON Lines or Parquet within 10 working days of a request, at no extra charge.

#### [day2#test-the-exit] Test the export once a year, or the requirement is only paper

*An exit is a design artefact*

1. **Request** a full export
2. **Load** it into the Ministry's index
3. **Re-run** the evaluation set
4. **Record** time taken and gaps

#### [day2#check-lockin] Which requirement removes O1's largest exit cost?

*Checkpoint*

**Question:** O1's largest exit factor is its managed vector store with no bulk export (SAR 250,000). Which requirement removes it?

- A. The service shall expose an OpenAI-compatible interface
- B. The provider shall export the index, embeddings and metadata in JSON Lines within 10 working days
- C. The contract shall allow exit with 90 days' notice
- D. The provider shall give reasonable help on exit

#### [day2#lab-2-3] Exit cost, weights and two requirements

Lab 2.3 · 25 min

Price each option's exit, fold it into the weighted score, find the weight that flips the ranking and write two requirements that keep the exit open.

[D2_3_exit_cost.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D2_3_exit_cost.ipynb)

- [ ] Exit cost per option (6 min)
- [ ] The weighted score, exit cost included (6 min)
- [ ] The weight that flips the ranking (6 min)
- [ ] Two procurement requirements that keep the exit open (7 min)
- [ ] ✱ Stretch: A third requirement for the evaluation data

### Session 4: Decision records

#### [day2#s4] Decision records

*Session 4*

- Write a decision record with drivers, options and consequences both ways
- Set a review trigger someone can test
- Challenge a peer's record for what a lint cannot see

#### [day2#why-records] A decision record is written for the architect who reopens it

*Decision records*

- **The next architect.** Why O1, what it cost, what would change it.
- **The auditor.** Who decided, on which drivers, on which date.
- **The panel.** The capstone asks for six, dated, in the repository.

#### [day2#record-shape] MADR's sections, plus a trigger that says when to reopen

*The template*

1. **Context** the question
2. **Drivers** with ids
3. **Options** two or more
4. **Outcome** and why
5. **Consequences** good and bad
6. **Trigger** a number or a date

#### [day2#record-one] Record one names the fragile ranking as a bad consequence

*From Lab 2.4*

```markdown
<!-- file: 0001.md -->
## Decision outcome
Chosen option: "O1", because it is the cheapest over three years
(SAR 6.25 million against 7.59 and 11.92), meets S12 and goes live first.

### Consequences
- Good, because no accelerator servers to buy or operate
- Bad, because it is the dearest option to leave (SAR 540,000)
- Bad, because an exit-cost weight of 0.13 puts O2 first

## Review trigger
Reopen if monthly requests exceed 600,000 or the input price
rises above SAR 12 per million.
```

#### [day2#triggers] A trigger fires on a measurement or a date

*Review triggers*

| Cannot fire | Can fire |
| --- | --- |
| If things change | If monthly requests exceed 600,000 |
| When quality drops | If Q1 falls below 0.90 on the monthly sample of 200 |
| Revisit periodically | On 2027-12-31 |
| If the vendor raises prices | If input tokens cost more than SAR 12 per million |

#### [day2#the-log] Six records make a log when they share an index and a status

*The decision log*

- One file per decision, numbered, never renumbered.
- Status: proposed, accepted, or superseded by a later number.
- An index with each record's trigger, so triggers are watched in one place.
- Records are reviewed in pull requests like code.

#### [day2#peer-challenge] The lint finds missing parts; the reviewer finds missing consequences

*The peer challenge*

- lint: no bad consequence; the review trigger has no number or date
- reviewer: A cached answer can outlive a new circular for 30 days. Who carries that?
- reviewer: Q1 answer quality is not a driver, and a stale answer is a wrong answer.

#### [day2#check-record] Which line makes this record reviewable?

*Checkpoint*

**Question:** A record chooses to skip the reranker for status questions. Its trigger reads "revisit if quality drops". Which replacement makes it a trigger someone can act on?

- A. Revisit when the product owner feels quality has dropped
- B. Revisit every three years
- C. Reopen if Q1 on mixed questions falls below 0.90 on the monthly sample of 200
- D. Reopen if p95 latency rises above 4,000 ms

#### [day2#lab-2-4] Two decision records and a challenge

Lab 2.4 · 25 min

Record where Muyassir's model runs and why status questions skip the reranker, lint both, then challenge a peer's record on its consequences and trigger.

[D2_4_decision_records.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D2_4_decision_records.ipynb)

- [ ] Read the template and run the lint (4 min)
- [ ] Record one: where Muyassir's model runs (8 min)
- [ ] Record two: no reranking for status questions (6 min)
- [ ] Challenge a peer's record (7 min)
- [ ] ✱ Stretch: The decision log index

#### [day2#wrap-up] Three things to keep

*Day 2*

- **Cost a baseline.** A non-generative option shows what the model must beat, and sometimes wins.
- **Find what the ranking depends on.** Volume and coverage, not token price, at Muyassir's scale.
- **Record the cost of a choice.** Bad consequences and a trigger that can fire.

#### [day2#next] Tomorrow: nine teams, one platform, and who pays for which tokens

*Day 3*

- Keep `artifacts/D2_4/`: the two records start your decision log.
- Look at `labs/data/platform/usage.csv`: six months of nine teams.
- Think of one shared service in your own organisation that teams avoid. Why?

## Day 3: The shared platform

Asas as a product: demand, admission, a gateway that refuses, tenancy and showback

#### [day3#title] The shared platform

*SDAIA Academy · AI Solution Architecture and Platform Design*

Day 3: Asas as a product: demand, admission, a gateway that refuses, tenancy and showback

AI Engineering Track · 4 teaching days + capstone day · 4 sessions · 4 labs · AE-402

#### [day3#agenda] The shared platform

*Today*

- **Session 1 · The platform is a product**: The shared platform treated as a product with nine teams as users, phased by their measured demand
- **Session 2 · Catalogue, admission and the gateway**: Admission to the model catalogue on evidence, and a gateway that enforces placement by classification
- **Session 3 · Tenancy and shared capacity**: Tenancy as a set of controls that keep one team's incident inside that team
- **Session 4 · Who pays for which tokens**: Cost attribution that reconciles with the invoices, shown to teams before anyone is charged

#### [day3#review-day2] What does record one's review trigger watch?

*Review of Day 2*

**Question:** Decision record 1 hosts Muyassir's model in a cloud region of the Kingdom. Lab 2.2 found that volume moves the three-year cost by half and token price by 3%. What should its trigger watch first?

- A. The provider's token price
- B. Monthly requests, against a threshold below the crossover
- C. The build cost of O1
- D. A single wrong answer reported in the press

### Session 1: The platform is a product

#### [day3#s1] The platform is a product

*Session 1*

- Build a demand matrix from usage logs and a team survey
- Phase platform capabilities by shared demand
- Spot in the logs what the platform should already prevent

#### [day3#platform-product] A platform's users are teams, and they can choose not to use it

*The platform as a product*

- **Users.** Nine product teams with different data levels and needs.
- **A roadmap from demand.** What most teams use and ask for, phased.
- **Measured by use.** Adoption and the teams' satisfaction, not features shipped.

> **What goes wrong.** A platform built as a project: a list of features, delivered, and avoided by the teams it was for.

#### [day3#asas-today] Asas served nine teams on six models in six months

*Six months of logs*

- **3,312** daily usage rows, May to October 2026
- **8 of 9** teams use or ask for chat
- **1** key with no owner, still calling a model

#### [day3#demand-matrix] Two capabilities serve most teams; four serve one team each

*Measured in Lab 3.1*

| Item | Value |
| --- | --- |
| Chat | 8 teams |
| Embeddings | 5 |
| Batch | 3 |
| Classification, vision, speech, agent tools | 1 each |

Teams that use a capability or ask for it in the survey, out of nine.

#### [day3#phasing] Build shared what most teams need; pave a road for the rest

*Phasing*

| Phase | Capabilities | Rule |
| --- | --- | --- |
| Phase 1 | chat, embeddings | five or more teams |
| Phase 2 | batch | two to four teams |
| Team-owned | classification, vision, speech, agent tools | one team: a template, not a service |

#### [day3#logs-breach] For two months, a Restricted team called the external model

*What the logs show*

**47,556** requests from the reports team (Restricted) to the external model, May and June

- Citizen reports carry phone numbers and locations.
- The gateway kept no prompt text, by design: what was sent cannot be read back.
- The prompt template of those months can be, and the team can say what it held.

#### [day3#check-phase] Should Asas build a shared vision service now?

*Checkpoint*

**Question:** Only the inspections team uses vision, and its candidate model has no Arabic evaluation. The team asks the platform to offer vision to everyone. What does the platform do first?

- A. Build a shared vision service for all nine teams
- B. Refuse, since vision is not in phase 1
- C. Add the vision model to the catalogue now
- D. Give the team a paved road to its own vision service, and ask for Arabic evidence

#### [day3#lab-3-1] A demand matrix from six months of usage

Lab 3.1 · 25 min

Build a teams-by-capabilities matrix from six months of synthetic gateway logs and a survey, phase the platform's capabilities and find the placement breach in the logs.

[D3_1_demand_matrix.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D3_1_demand_matrix.ipynb)

- [ ] Read six months of usage (4 min)
- [ ] The demand matrix: used and asked for (8 min)
- [ ] Phase the platform's capabilities (6 min)
- [ ] What the logs show that the platform should have stopped (7 min)
- [ ] ✱ Stretch: Growth by capability

### Session 2: Catalogue, admission and the gateway

#### [day3#s2] Catalogue, admission and the gateway

*Session 2*

- Admit models on licence, evaluation and data-term evidence
- Write catalogue entries with the highest level each model may receive
- Make a gateway refuse Restricted data to an external model

#### [day3#admission] A model enters the catalogue on evidence, not on a leaderboard

*Model admission*

1. **Licence** government production use allowed
2. **Evaluation** the Ministry's Arabic and English sets
3. **Data terms** retention, no training on prompts
4. **Owner** and a review date

#### [day3#admitted] Four of six candidates are admitted; the best scorer is not

*Measured in Lab 3.2*

| Candidate | Arabic / English | Hosting | Verdict |
| --- | --- | --- | --- |
| ext-frontier-l | 0.91 / 0.93 | external | admitted, Public data only |
| ksa-general-m | 0.86 / 0.88 | cloud in the Kingdom | admitted, up to Restricted |
| own-open-s, own-embed-m | 0.79 / 0.82, 0.88 / 0.90 | Ministry | admitted, up to Secret |
| ext-mini-r | 0.84 / 0.89 | external | rejected: research-only licence |
| ksa-vision-x | none / 0.81 | cloud in the Kingdom | rejected: no Arabic evidence |

#### [day3#gateway-duties] One door for every model call, with five duties

*The gateway*

- **Credentials.** A key per team; provider keys never leave the gateway.
- **Quotas and budgets.** Per key: requests a minute, spend.
- **Fallback.** Another admitted model when one fails, under the same policies.
- **Tool mediation.** Only the tools a team is allowed reach the model.
- **Audit.** Who, which model, which level, which decision.
- **And now: policy.** Classification decides where a request may go.

#### [day3#policy-code] The level of a request is the highest it shows, declares or defaults to

*Lab 3.2, step 4*

```python
# file: Lab 3.2
def classification_policy(ctx):
    levels = [G.detect_level(ctx["text"])]
    levels.append(ctx["request"].get("classification")
                  or ctx["key_info"]["max_level"])   # fail closed
    level = A.highest(levels)
    ctx["level"] = level
    hosting = ctx["entry"]["hosting"]
    if not A.allowed(level, hosting):
        return 403, f"{level} data may not go to a model hosted at '{hosting}'"
```

#### [day3#nine-tests] The supplied gateway passed four forbidden requests; the policy stops all four

*Measured in Lab 3.2*

| Test | Request | Supplied | With the policy |
| --- | --- | --- | --- |
| G2 | Restricted, declared, to the external model | 200 | 403 |
| G3 | Restricted team, nothing declared, external model | 200 | 403 |
| G4 | declared Public, holds an identity number | 200 | 403 |
| G6 | Secret tender text to the cloud model | 200 | 403 |
| G1, G5, G7, G8 | allowed placements | 200 | 200 |

#### [day3#audit-hash] Log the decision and a hash of the prompt, never the prompt

*The audit log*

- seq 4: team T05 · alias ext-frontier-l · level Restricted · 403
- reason: Restricted data may not go to a model hosted at 'external'
- prompt: sha256 cf48bdcd010a953f

A log full of prompts is a second copy of Restricted data, with its own retention rule. A hash proves whether a given text was sent.

#### [day3#fallback-placement] A fallback must pass the same policy as the first choice

*Fallback*

- request: contracts team, Secret, alias own-open-s
- own-open-s: busy (stand-in failure)
- fallback: ksa-general-m refused: Secret may not go to ksa_cloud
- answer: 503, no model available

#### [day3#check-gateway] What should the gateway do with this request?

*Checkpoint*

**Question:** The planning team (Public) labels a request Public and sends it to the external model. The text reads: "Owner 1048837265 asks whether plot 17 can be rezoned."

- A. Pass it: the team and the label are both Public
- B. Pass it, and mask the number in the audit log
- C. Refuse it: the content shows an identity number, so the request is Restricted
- D. Pass it with a warning to the team

#### [day3#lab-3-2] Model admission and a gateway that refuses

Lab 3.2 · 25 min

Admit four of six candidate models on evidence, write their catalogue entries and add the classification policy that makes the supplied gateway refuse Restricted data to an external model.

[D3_2_admission_gateway.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D3_2_admission_gateway.ipynb)

- [ ] Admission criteria as code (5 min)
- [ ] Admit four of the six candidates (6 min)
- [ ] Catalogue entries with the level each may receive (4 min)
- [ ] The classification policy, and nine test requests (10 min)
- [ ] ✱ Stretch: A fallback that respects placement

### Session 3: Tenancy and shared capacity

#### [day3#s3] Tenancy and shared capacity

*Session 3*

- Compare a shared and a per-team tenancy model under incidents
- Cap a team's share of shared capacity
- Contain leaked keys and runaway spend with keys and budgets per team

#### [day3#isolation-levels] Tenancy is a choice of what teams share and what each gets alone

*Tenancy*

| Model | Teams share | Each team gets | Fits |
| --- | --- | --- | --- |
| Pooled | key, budget, capacity | nothing | a pilot |
| Per-team controls | capacity, under caps | a key, a budget, a capped share | Public and Restricted teams |
| Dedicated | the gateway only | its own model deployment | Secret teams with steady load |

#### [day3#three-incidents] Three incidents test three different controls

*One hour, three incidents*

- **Leaked key.** The planning team's key calls the external model 400 times a minute for 15 minutes.
- **Noisy neighbour.** The contact team's batch floods the Ministry-hosted model with 300 extra requests a minute.
- **Runaway agent.** An inspections agent loops for 40 minutes at six times the tokens per call.

#### [day3#incident-results] Under per-team controls, no bystander loses a request

*Measured in Lab 3.3*

| Incident | Tenancy | Worst bystander, own model | Worst bystander, paid models |
| --- | --- | --- | --- |
| Noisy neighbour | pooled | 83.1% | 100% |
| Leaked key | pooled | 100% | 61.7% |
| Runaway agent | pooled | 100% | 43.3% |
| All three | per team | 100% | 100% |

Share of requests served, for the worst-off team that caused nothing.

#### [day3#control-map] Each incident needs its own control; the tenancy model is the set

*Which control for which incident*

| Control | Contains | Does nothing for |
| --- | --- | --- |
| A cap on each team's share of capacity | noisy neighbour | spend |
| A budget per key | runaway agent | capacity |
| A key per team, revoked on a spike | leaked key | a slow, legitimate overload |

#### [day3#blast-radius] One team's incident should stay that team's incident

*The principle*

**5 minutes** without paid models for the planning team, until its new key

- Revocation costs the team whose key leaked; nobody else.
- Keys are scoped to the models of the team's level: a leaked Public key reaches no Restricted model.
- Rotation is routine, so revoking is not a crisis.

#### [day3#check-tenancy] Which control stops this from harming other teams?

*Checkpoint*

**Question:** The contact team's nightly batch moves to working hours and asks the Ministry-hosted model for more than twice its capacity. Budgets are untouched; the other teams' answers slow down. Which control fixes it?

- A. A lower budget on the contact team's key
- B. Revoke the contact team's key
- C. A cap on any team's share of the Ministry-hosted model
- D. Fall back to a cloud model when the queue is long

#### [day3#lab-3-3] Three incidents, two tenancy models

Lab 3.3 · 25 min

Replay an hour with a leaked key, a noisy neighbour and a runaway agent under the pilot's shared model and under a per-team model you design, and measure the harm to bystanders.

[D3_3_tenancy.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D3_3_tenancy.ipynb)

- [ ] Replay the three incidents on the shared model (5 min)
- [ ] A capped share of the Ministry-hosted model (7 min)
- [ ] Your tenancy model: keys, budgets, revocation (6 min)
- [ ] The incident table: who was harmed (7 min)
- [ ] ✱ Stretch: The cap that costs the culprit least

### Session 4: Who pays for which tokens

#### [day3#s4] Who pays for which tokens

*Session 4*

- Allocate invoices to teams by usage, credits and fixed costs included
- Reconcile a showback with each invoice within 2%
- Name spend that no tag or owner explains

#### [day3#showback-first] Show teams their costs before anyone is charged

*Cost attribution*

- **Showback.** Each team sees what its use cost, at any granularity. Nothing moves between budgets.
- **Chargeback.** The costs are sent to the teams' budgets. Allocation keys now move money.

> **Order.** Run showback until the teams stop disputing the allocation keys; then decide about chargeback.

#### [day3#card-drift] A showback priced with a price card drifts from the bill

*Measured in Lab 3.4*

| Invoice | Showback by card | Invoice | Off by | Why |
| --- | --- | --- | --- | --- |
| In-Kingdom Cloud, August | 5,136 | 4,636 | 10.8% | an onboarding credit |
| External Provider, September | 3,772 | 3,401 | 10.9% | output price cut |
| External Provider, October | 3,935 | 3,550 | 10.9% | output price cut |

#### [day3#allocate-invoice] Share each invoice line by the usage it covers

*Allocate, do not reprice*

1. **Token lines** by the rows' tokens of that model
2. **Credits** by the rows' value on that provider
3. **Fixed cost** by an allocation key you defend
4. **Team** by the key's owner

**0.00%** difference from each of the 18 invoices after allocation; the outcome asks for 2% or less

#### [day3#untagged] Untagged spend comes in two kinds, and only one has an owner

*Untagged spend*

- **Blank tag, known key.** 116 rows, SAR 13,950: the key's owner is known, so the gateway attributes them.
- **Orphan key.** `k-legacy-01`: SAR 558 over six months, chat on a cloud model, owned by nobody.

> **The fix is a rule, not a report.** No key without an owner, and a key without one is revoked.

#### [day3#allocation-key] The allocation key is a decision: tokens and requests disagree

*The data centre's fixed cost*

- **70.7%** of the data centre's cost to the contact team, by tokens
- **24.1%** of it to the same team, by requests

Speech counts many tokens per call. Which key reflects what the servers actually spend their time on? Measure it, then record the choice.

#### [day3#check-showback] Why does the August showback miss the invoice?

*Checkpoint*

**Question:** Priced with the platform's card, August's In-Kingdom Cloud showback is SAR 500 above the invoice. Every token is accounted for. What is the right fix?

- A. Add a correction line of SAR -500 to the unallocated bucket
- B. Update the price card for August
- C. Ask teams to tag their calls better
- D. Allocate the invoice lines, the credit included, to the usage they cover

#### [day3#lab-3-4] A showback that reconciles

Lab 3.4 · 25 min

Build a showback from synthetic invoices, usage and tags, see a price-card version fail to reconcile, allocate the invoices instead within 2% and name the untagged spend.

[D3_4_showback.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D3_4_showback.ipynb)

- [ ] A showback priced with the price card (6 min)
- [ ] Reconcile it with each invoice (5 min)
- [ ] Allocate the invoices instead (8 min)
- [ ] Name the untagged spend (6 min)
- [ ] ✱ Stretch: Is token count the right key for the data centre?

#### [day3#wrap-up] Three things to keep

*Day 3*

- **Build from demand.** Shared services for most teams, paved roads for the rest.
- **Policy at the door.** The gateway refuses by classification, content included, and logs no text.
- **Contain and attribute.** Per-team controls keep incidents local; showback allocates the real bill.

#### [day3#next] Tomorrow: a golden path, fitness checks, a review and a deviation

*Day 4*

- Keep `artifacts/D3_2/` and `artifacts/D3_4/`: the capstone's platform slice starts there.
- Read the inspections team's design in `labs/data/designs/`: you review it in Session 3.
- Choose which of the three capstone services you would take.

## Day 4: Reference designs and reviews

A golden path, fitness checks, a structured review and a deviation decided on one page

#### [day4#title] Reference designs and reviews

*SDAIA Academy · AI Solution Architecture and Platform Design*

Day 4: A golden path, fitness checks, a structured review and a deviation decided on one page

AI Engineering Track · 4 teaching days + capstone day · 4 sessions · 4 labs · AE-402

#### [day4#agenda] Reference designs and reviews

*Today*

- **Session 1 · Golden paths**: A golden path makes the compliant way the easy way: a template with its gates on by default
- **Session 2 · Fitness functions**: Fitness functions turn the reference design's rules into checks that fail a build
- **Session 3 · Structured architecture review**: A structured review weighs a design against its prioritised scenarios, not a checklist
- **Session 4 · Deviations and sponsors**: A deviation is a time-boxed decision with conditions, explained to a sponsor in numbers

#### [day4#review-day3] Which control contains a leaked key to one team?

*Review of Day 3*

**Question:** Asas moves from one shared key to per-team keys. The planning team's key leaks and calls the external model 400 times a minute. What keeps the other eight teams served?

- A. Revoking that team's key when its rate spikes, under per-team budgets
- B. A cap on each team's share of the Ministry-hosted model
- C. A larger shared budget for the hour
- D. A showback that names the planning team

### Session 1: Golden paths

#### [day4#s1] Golden paths

*Session 1*

- Turn a team's service into a template other teams generate from
- Put evaluation, classification checks and tracing on by default
- Make switching a gate off visible to the platform

#### [day4#golden-path] Make the compliant way the easiest way to start

*Golden paths*

- **A working start.** A service a team generates in minutes, not a document it reads.
- **Gates on by default.** Evaluation, classification checks and tracing come with it.
- **Optional, and visible.** A team may leave the path; the platform sees who did and why.

> **What goes wrong.** A golden path that is harder than doing it yourself. Teams route around it, and the gates go with it.

#### [day4#hard-coded] What one team hard-coded becomes the template's questions

*Lab 4.1, step 1*

| In the permits service | In the template | Guard rail |
| --- | --- | --- |
| `SERVICE = "permits-rag"` | service_name | required |
| `TEAM = "T01"` | team | required |
| `LEVEL = "Restricted"` | classification | three choices |
| `MODEL = "ksa-general-m"` | model_alias | must be allowed for the level |
| `python eval.py`, by hand | eval_gate, eval_min_score | on, and 0.80 or more |

#### [day4#validator] The template refuses a placement before any code exists

*A guard rail in the template*

```yaml
# file: copier.yml
model_alias:
  type: str
  choices: [ext-frontier-l, ksa-general-m, own-open-s]
  default: ksa-general-m
  validator: >-
    {% set hosting = {'ext-frontier-l': 'external', ...} %}
    {% if hosting[model_alias] not in ok[classification] %}
    {{ classification }} data may not go to {{ model_alias }}{% endif %}
```

- refused: Validation error for question 'model_alias': Restricted data may not go to ext-frontier-l (external)

#### [day4#three-gates] Kashif's generated service passes three gates nobody on its team wrote

*Measured in Lab 4.1*

- evaluation: pass · retrieval hit rate 1.00 against 0.85 on 10 questions
- classification: pass · Restricted data to ksa-general-m (ksa_cloud)
- tracing: pass · 2 spans, no question text
- pipeline: exit code 0

The trace line carries the service, the team, the level and a hash of the question.

#### [day4#gate-off] A gate may be switched off, with a reason, in a register

*A visible exit*

- evaluation: off · switched off by the team: no evaluation set yet; due 2026-12-15
- classification: pass
- tracing: pass

- Without a reason, the template refuses.
- The pipeline passes and says so.
- The platform's register lists every service with a gate off, its team and its date.

#### [day4#template-update] A template copied once stops at the day it was copied

*Template plus update*

- **Copied.** Each service drifts; a fix to the gates reaches nobody who started before it.
- **Generated and updated.** The service records its answers; `copier update` brings later template changes, and conflicts show as a diff.

#### [day4#check-golden] Why did the reports team's service miss the new gate?

*Checkpoint*

**Question:** In March the platform adds an Arabic evaluation gate to the template. Services generated after March have it; the reports team's service, generated in January, does not. What went wrong?

- A. The reports team should have read the release notes
- B. The template should have had more questions
- C. The service was treated as a one-time copy, with no update path from the template
- D. The gateway should run the evaluation

#### [day4#lab-4-1] A golden path from the permits team's service

Lab 4.1 · 25 min

Turn the permits team's retrieval service into a Copier template whose questions refuse a disallowed placement, generate Kashif's service from it and run its three gates as the pipeline would.

[D4_1_golden_path.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D4_1_golden_path.ipynb)

- [ ] What the permits team hard-coded (4 min)
- [ ] The template: questions with guard rails (9 min)
- [ ] Generate Kashif's service and run its gates (7 min)
- [ ] A register of the gates switched off (5 min)
- [ ] ✱ Stretch: Refuse an evaluation set without Arabic

### Session 2: Fitness functions

#### [day4#s2] Fitness functions

*Session 2*

- Describe a design as data a program can read
- Write a check for a blocking evaluation gate before deployment
- Write a placement check that follows fallbacks

#### [day4#fitness-function] A fitness function turns a sentence in a standard into a failing build

*Fitness functions*

1. **Standard** "Restricted data never leaves the Kingdom"
2. **Design as data** components, hosting, flows, levels
3. **Check** a function over the file
4. **Pipeline** exit code 1 stops the merge

#### [day4#design-data] The design names hosting, levels and pipeline stages

*A design file*

```json
// file: designs/inspections.json
{"service": "kashif", "team": "T03", "classification": "Restricted",
 "components": [
  {"id": "vision", "kind": "model", "model": "ksa-vision-x",
   "hosting": "ksa_cloud", "fallback": "vision_ext"},
  {"id": "vision_ext", "kind": "model", "model": "ext-vision-q", "hosting": "external"}],
 "flows": [{"id": "F2", "from": "kashif", "to": "vision", "level": "Restricted"}],
 "pipeline": [{"stage": "test"},
  {"stage": "evaluate", "blocking": true, "min_score": 0.8, "sets": ["en"]},
  {"stage": "deploy"}]}
```

#### [day4#fitness-results] Two checks fail three of five designs, each for a different reason

*Measured in Lab 4.2*

| Design | Evaluation gate | Placement | Why |
| --- | --- | --- | --- |
| permits_reference | pass | pass | the reference |
| zoning_public | pass | pass | Public data may go to an external model |
| reports_triage | fail | pass | evaluate runs after deploy and does not block |
| staff_assistant | pass | fail | an employee's leave record to an external model |
| inspections | pass | fail | Restricted photos reach an external model through the fallback |

#### [day4#follow-fallback] Follow every fallback: it is where the data goes when things fail

*The placement check*

- F2: kashif → vision · Restricted
- vision: ksa-vision-x · ksa_cloud · allowed
- fallback: vision_ext · ext-vision-q · external · not allowed
- FAIL: kashif: flow F2 sends Restricted data to vision_ext (fallback of vision), hosted external

#### [day4#policy-as-code] The language of the check matters less than where it runs

*Same idea, other tools*

| Tool | Checks | Runs |
| --- | --- | --- |
| A Python function (the lab) | design files | a test in the pipeline |
| Open Policy Agent with conftest | JSON, YAML, infrastructure files, in Rego | the pipeline, as a command |
| Tests over infrastructure definitions | the deployed resources' code | the pipeline |

#### [day4#check-limits] A check is only as true as the design file

*What a check cannot see*

- A file that says "ksa_cloud" for a service deployed abroad passes.
- An evaluation set in the wrong language passes check 1.
- A design that meets every rule may still miss its scenarios.

- **So.** Checks catch what can be read from the file on every commit; a review asks whether the file and the design are right, once per design.

#### [day4#check-fitness] Should the placement check fail this design?

*Checkpoint*

**Question:** The planning team's zoning assistant sends questions about published zoning plans, classified Public, to the external model. A colleague proposes failing every design with an external model, to be safe.

- A. Yes: external models are a risk whatever the data
- B. Pass it with a warning that cannot be silenced
- C. Send every external design to the board for review
- D. No: the check enforces the rule by level, and Public data may go to an external host

#### [day4#lab-4-2] Two fitness checks over designs as data

Lab 4.2 · 25 min

Write two checks over five teams' design files, one for a blocking evaluation gate and one for the placement of every classified flow, and run them as a pipeline step that fails three designs.

[D4_2_fitness_checks.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D4_2_fitness_checks.ipynb)

- [ ] Read a design as data (4 min)
- [ ] Check 1: a blocking evaluation gate before deployment (7 min)
- [ ] Check 2: every flow is placed where its level may go (8 min)
- [ ] Run both as a pipeline step (6 min)
- [ ] ✱ Stretch: A third check: the evaluation includes Arabic

### Session 3: Structured architecture review

#### [day4#s3] Structured architecture review

*Session 3*

- Prioritise scenarios in a utility tree
- Tell risks, sensitivity points, trade-off points and non-compliance apart
- Write a review report with a verdict a team can act on

#### [day4#atam] Review against prioritised scenarios, not against a checklist

*A structured review*

1. **Drivers** the business goals and constraints
2. **Utility tree** scenarios by importance and difficulty
3. **Analysis** the approaches against the leading scenarios
4. **Findings** risks, non-risks, sensitivity and trade-off points
5. **Risk themes** tied to the drivers

#### [day4#utility-tree] Three scenarios lead: Arabic quality, privacy and security

*Kashif's utility tree*

| Scenario | Attribute | Importance | Difficulty |
| --- | --- | --- | --- |
| Q1 · Arabic shop signs read correctly in 90% of the Ministry's set | answer quality | H | H |
| P1 · no photo with faces or plates processed outside the Kingdom | privacy | H | M |
| S1 · a leaked key contained to one client within 30 minutes | security | H | M |
| O1 · every filed report approved by its inspector | oversight | H | L |
| L1 · a draft on the tablet within 5 s at p95 on 4G | latency | M | H |

Five of eight scenarios; cost, availability and operability follow.

#### [day4#five-tags] Five tags, each telling the team something different to do

*What a finding is*

| Tag | Means | Kashif example |
| --- | --- | --- |
| Non-compliance | breaks a written standard | R02 · photos fall back to an external model |
| Risk | may keep a scenario from being met | R03 · evaluation in English only |
| Sensitivity point | one parameter a scenario depends on | R04 · the vision call takes 3,800 of 5,000 ms |
| Trade-off point | one decision, two attributes in opposite directions | R05 · compressing photos: faster, cheaper, worse at small Arabic text |
| Non-risk | a decision that meets a scenario | R06 · the inspector approves every report |

#### [day4#r01-r03] A checklist finds the broken rule; a reviewer finds the empty gate

*Two findings about Arabic*

- **R01 · non-compliance.** The vision model was not admitted: no Arabic evaluation evidence. Any checklist catches it.
- **R03 · risk.** An evaluation gate exists and blocks. It runs on English, and the signs are Arabic. Only someone who read Q1 sees it.

#### [day4#verdict] Not approved, with the four themes that would change the verdict

*Measured in Lab 4.3*

**2 · 3 · 2 · 2 · 3** non-compliance, risks, sensitivity points, trade-off points, non-risks

- **Q1** Arabic quality unproven: R01, R03
- **P1** photos can leave the Kingdom: R02
- **S1** one key for two clients: R10
- **M1** no owner for prompt templates: R08

#### [day4#check-review] How should the board tag this observation?

*Checkpoint*

**Question:** "A 10% sample review of approved reports is the only check that inspectors' approvals are real." The oversight scenario requires every filed report to carry an approval.

- A. Non-compliance
- B. A sensitivity point: whether approvals mean anything rests on that one rate
- C. A non-risk, since every report is approved
- D. A trade-off point

#### [day4#lab-4-3] A structured review of Kashif's design

Lab 4.3 · 25 min

Review the inspections team's design: order its scenarios in a utility tree, tag twelve observations, group the risks into themes and write the report with its verdict.

[D4_3_review.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D4_3_review.ipynb)

- [ ] The utility tree: which scenarios lead (6 min)
- [ ] Tag the twelve observations (8 min)
- [ ] Risk themes, tied to scenarios (5 min)
- [ ] The review report and its verdict (6 min)
- [ ] ✱ Stretch: Which finding becomes a fitness check?

### Session 4: Deviations and sponsors

#### [day4#s4] Deviations and sponsors

*Session 4*

- Put numbers on what a deviation breaks and what refusing it costs
- Decide a deviation with verifiable conditions, an expiry and reopen triggers
- Explain a trade-off on one page for a sponsor

#### [day4#deviation] A deviation is a decision record with an expiry

*Deviations*

- **Conditions.** Each with a number a reviewer can check.
- **Residual risk.** In numbers, and who accepts it.
- **Expiry.** A date, and the events that reopen it sooner.

> **What goes wrong.** A deviation without an expiry becomes the new standard by default, with nobody having decided that.

#### [day4#request-numbers] The request has a cost either way, and the request names neither

*Measured in Lab 4.4*

- **SAR 96,000** a month of inspector time if refused: 800 hours
- **5,445** Restricted photos a month abroad if approved as asked
- **about 90** a month still abroad if only photos the detector passes are sent

#### [day4#three-options] Approve with conditions, until the evidence in the Kingdom arrives

*Three answers*

| Answer | Gives | Costs |
| --- | --- | --- |
| Refuse | the rule kept whole | SAR 96,000 a month of inspector time, until February 2027 at least |
| Approve as asked | drafts for every photo | 5,445 Restricted photos a month abroad, for twelve months |
| Approve with conditions, until 31 March 2027 | drafts for about 65% of photos | about 90 a month through detector misses, accepted by the data owner |

#### [day4#sponsor-page] The decision first, the trade-off in numbers, and a date it ends

*One page for a sponsor*

- The recommendation in the first sentence.
- What it gives and what it risks, in hours, riyals and photos.
- What she is asked to accept, by name.
- When and how it ends.

- **Left out on purpose.** Gateway, fallback, p95, fitness check. The lab's self-check fails the page if any of them appear, or if it runs past 250 words.

#### [day4#deviation-policy] A deviation the gateway enforces ends on its date

*The stretch of Lab 4.4*

- 200: inspections key, photo the detector passed, December 2026
- 403: inspections key, flagged photo
- 403: another team's key, photo the detector passed
- 403: inspections key, photo the detector passed, 1 April 2027: expired

#### [day4#capstone-choice] Choose one of three services; all run on Asas

*Your capstone*

- **Citizen reports.** 95,000 reports a month, routing and replies. Restricted: phones, locations, photos.
- **Call summaries.** 40,000 calls a month. Restricted: voices, names, identity numbers read aloud.
- **Staff policies.** 6,000 questions a month. Public policies, Restricted employee records.

#### [day4#check-deviation] What is missing from this approval?

*Checkpoint*

**Question:** "DR-2026-07: approved. The inspections team may send clean photos to ext-vision-q. Owner: Rabah Al-Mujil. Conditions: the detector runs on every photo; flagged photos stay on the manual path."

- A. An expiry, and the events that would bring it back to the board
- B. An owner for the conditions
- C. Any conditions at all
- D. The scope of what is allowed

#### [day4#lab-4-4] A deviation request, decided and explained on one page

Lab 4.4 · 25 min

Measure the inspections team's request to send photos to an external vision model, decide it with conditions and an expiry, write the sponsor's one page and choose your capstone service.

[D4_4_deviation.ipynb](https://sdaiaacademy.github.io/ae-402/labs/D4_4_deviation.ipynb)

- [ ] What the request breaks, and what refusing costs (6 min)
- [ ] Decide, with conditions, an expiry and what reopens it (7 min)
- [ ] One page for the sponsor (7 min)
- [ ] Choose your capstone service (5 min)
- [ ] ✱ Stretch: The deviation as a gateway policy that expires

#### [day4#wrap-up] Three things to keep

*Day 4*

- **Paths, not documents.** A template with its gates on is a standard teams actually follow.
- **Checks and reviews.** Checks catch what the file shows, every commit; a review asks whether the design is right.
- **Bounded exceptions.** A deviation has conditions, a residual someone accepts and a date it ends.

#### [day4#next] Next: build your service's architecture and defend it before the panel

*Capstone day*

- Start a public repository from `labs/capstone/README.md`; commit early, the history counts.
- Bring a peer's design to review: the review is 15% of the rubric.
- Prepare for the panel to change one classification level or the volume forecast.

## Capstone: Capstone project presentations

Ten minutes of architecture and eight of questions, with one classification or forecast changed by the panel

#### [capstone#title] Capstone project presentations

*SDAIA Academy · AI Solution Architecture and Platform Design*

Capstone: Ten minutes of architecture and eight of questions, with one classification or forecast changed by the panel

AI Engineering Track · 4 teaching days + capstone day · 10 min talk and demo · 8 min Q&A · AE-402

#### [capstone#agenda] How the defences run

*Capstone*

- **Expectations and final prep**: the rubric, the panel's change, a last check of the repository
- **Defences**: ten minutes of talk, eight of questions, each timed
- **Review and closing**: what the room learned, the follow-up task

#### [capstone#rubric] Five criteria, 100 points

*How the repository is scored*

| Item | Value |
| --- | --- |
| Scenarios and views | 20% |
| Options and decisions | 25% |
| Platform slice | 25% |
| Fitness checks | 15% |
| Review | 15% |

> **Pass:** 70% overall, and at least 60% on this rubric and on the supervised checks. The repository is 60% of the result, the defence 20%, the supervised checks 20%.

#### [capstone#format] Ten minutes of architecture, then eight minutes of questions

*The defence*

- **3 min · the service.** Drivers, the leading scenarios with their targets, the data-flow view with every level.
- **4 min · the decisions.** The options paper's numbers, two decision records, and the platform slice running: one refused request.
- **3 min · the checks and the review.** The pipeline failing a bad design; the peer review's verdict.

> **AI-full.** Any assistant was allowed in the repository; the questions are where you show the decisions are yours.

#### [capstone#panel-change] The panel changes one input; you name the decisions it reopens

*During the questions*

- **A classification.** "The call recordings are now Secret." Which placements, models, keys and costs change?
- **The volume forecast.** "Year three is three times the base." Which option wins now, and which review trigger fired?

> **What the panel listens for.** Record numbers, not a fresh opinion: the decision records whose triggers fire, and what each would become.

#### [capstone#running-order] Who defends when

*Running order*

| # | Participant | Service and repository |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final prep · 20 minutes

*Before the first defence*

Clone your repository into a new folder and run its pipeline. If the checks or the refusal test fail there, they fail for the panel.

#### [capstone#now-presenting] Talk

*Now defending*

##### Questions

#### [capstone#review] What the room learned

*After the defences*

- **The decision most reopened.** Which record did the panel's changes reopen most often?
- **The best refusal.** Whose gateway or check refused the most with the least code?
- **The cheapest option that won.** Where did the non-generative option hold its own?

#### [capstone#what-next] The follow-up task, and the AE Expert badge

*After the course*

- **Follow-up task.** Within a month, write three decision records for a system from your own work, each with good and bad consequences and a review trigger.
- **Keep the repository.** It is the evidence the AE Expert badge looks at.
- **Next in the track:** AE-401 Inference Performance and Cost Engineering, and AE-403 Reliability Engineering for AI Services.

#### [capstone#thanks] Thank you

*SDAIA Academy*

AI Solution Architecture and Platform Design
