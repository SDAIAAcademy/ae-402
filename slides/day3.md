---
course: "AI Solution Architecture and Platform Design"
code: "AE-402"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-402/slides/day3.html"
---

# AI Solution Architecture and Platform Design

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
