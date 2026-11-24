---
course: "AI Solution Architecture and Platform Design"
code: "AE-402"
version: "2027.2.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-402/slides/day1.html"
---

# AI Solution Architecture and Platform Design

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
