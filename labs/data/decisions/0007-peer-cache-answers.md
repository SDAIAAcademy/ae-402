# 7. Cache Muyassir's answers to frequent questions

- Status: accepted
- Date: 2026-10-20
- Deciders: Eyad Al-Shuraihi (permits product owner)

## Context and problem statement

Many applicants ask the same requirements questions. Every answer costs tokens and time.

## Decision drivers

- Q2 latency: p95 under 4,000 ms
- Q3 cost: under SAR 0.05 per answer

## Considered options

- No cache
- Cache answers to identical questions for 30 days

## Decision outcome

Chosen option: "Cache answers to identical questions for 30 days", because it makes repeated questions instant
and free.

### Consequences

- Good, because cached answers return in under 100 ms
- Good, because the token bill falls for frequent questions

## Review trigger

If things change.
