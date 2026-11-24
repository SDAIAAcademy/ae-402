# Changes

## 2027.2.0 (2026-11-24)

- Added: `strangler-facade` and `facade-week5` (day 2, session 3): moving from a legacy system to a new one capability by capability behind a routing facade, with rollback by route and retirement in steps, read from a week of graded samples.
- Added: `declared-deployed` and `revert-or-codify` (day 4, session 2): declaring the platform in reviewed code, reading drift between declared and deployed settings, and deciding whether to revert or codify a hand change.
- Merged: the yearly export test from `test-the-exit` into `requirements` (day 2); the slide `test-the-exit` is removed.
- Questions: `d2-facade-hold` and `d4-drift-codify` added to the practice bank.
- Data and scripts: `labs/_tools/enquiry_facade.py` writes `labs/data/migration/`; `labs/_tools/gateway_drift.py` writes `labs/data/infra/`.
- Sources: Strangler Fig (Martin Fowler); OpenTofu, Command: plan.
