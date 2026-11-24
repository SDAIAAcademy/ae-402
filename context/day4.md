---
course: "AI Solution Architecture and Platform Design"
code: "AE-402"
version: "2027.2.0"
deck: "day4"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-402/slides/day4.html"
---

# AI Solution Architecture and Platform Design

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

#### [day4#declared-deployed] Declare the platform in reviewed code, and drift becomes a diff you can read

*Infrastructure as code*

| Asas setting | Declared, reviewed | Deployed | How it changed |
| --- | --- | --- | --- |
| fallback of ksa-general-m | own-open-s | ext-frontier-l | by hand in an outage, no ticket |
| reports team budget, SAR a month | 18,000 | 24,000 | by hand, emergency ticket approved |
| audit log retention, days | 365 | 90 | by hand to free storage, no ticket |

3 of 19 settings differ. The placement check passes on the declared file and fails on what runs: Restricted data of the permits and reports teams can reach ext-frontier-l through the fallback.

#### [day4#revert-or-codify] Revert a hand change nobody approved; codify one that was

*Infrastructure as code*

- **Changed by hand in a console.** One person decides and applies; no record of why; the fitness checks never see it; rebuilding in another region depends on memory.
- **Declared under version control.** A second person reviews each change; checks run before it applies; a revert is one commit; the same files rebuild the platform.

> **For the three drifts.** Apply the declared file again for the fallback and the retention, now. Write the reports budget into the code through a reviewed change, then apply.

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
