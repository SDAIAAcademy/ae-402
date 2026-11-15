---
course: "AI Solution Architecture and Platform Design"
code: "AE-402"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-402/slides/day2.html"
---

# AI Solution Architecture and Platform Design

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
