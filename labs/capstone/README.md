# Capstone · an architecture for one ministry service and its platform slice

Choose one of the three services in `briefs/` (Lab 4.4, step 4). All of them run on Asas; all data is
synthetic. You work alone, in a public GitHub repository of your own, and defend it before a panel that
includes a data architect: 10 minutes of talk, 8 of questions.

## What the repository holds

| Part | Rubric | Where it starts |
|---|---|---|
| Scenario sheet: five or more quality-attribute scenarios with measurable targets | Scenarios and views, 20 | Lab 1.2 |
| Architecture document: context, container and data-flow views as code, every flow classified, one request traced end to end with its latency and cost budget | Scenarios and views | Labs 1.3 and 1.4 |
| Options paper: three options, one non-generative, three-year cost, lock-in and exit cost, sensitivity | Options and decisions, 25 | Labs 2.1 to 2.3 |
| At least six dated decision records, each with good and bad consequences and a review trigger | Options and decisions | Lab 2.4 |
| Platform slice: a catalogue entry, the gateway with its refusal test and its logs, the golden-path template your service is generated from, a showback that reconciles within 2% | Platform slice, 25 | Labs 3.2, 3.4 and 4.1 |
| A design file and the fitness checks, running in the repository's pipeline | Fitness checks, 15 | Lab 4.2 |
| A review of a peer's design, with a verdict | Review, 15 | Lab 4.3 |

## Authenticity

The panel reads the commit history, the dates on the decision records and the gateway logs (which keep a hash
of each prompt, never its text). During the defence the panel changes one classification level or the volume
forecast; you name the decisions it reopens and what each would become.

## AI use

AI-full: you may use any assistant to build the repository. You defend every decision yourself.

## Follow-up task

Within a month, write three decision records for a system from your own work, in the same template.
