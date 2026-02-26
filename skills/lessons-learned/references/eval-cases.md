# Lessons-Learned Evaluation Cases

Use this set to evaluate trigger quality and behavior quality.

## Targets

- Trigger precision >= 0.85
- Recall usefulness >= 8/10
- Capture compliance >= 9/10
- Related-link creation rate >= 0.8 (when high-value gate is met)

## Prompt Set (12)

### A. Task-Start Trigger (Recall) — 3

1. "Starting now: add retry + timeout to payment webhook calls before coding."
2. "Before I touch DB migrations, load any ordering lessons."
3. "I am about to fix a React Router auth redirect loop after token refresh."

Expected: trigger recall, load 1-3 primary cards, optionally up to 2 related cards.

### B. User-Correction Trigger (Capture) — 3

4. "Correction: run baseline before migrate, not the other way around."
5. "Correction: configure timeout before client initialization."
6. "Correction: validate nullable fields before persistence to avoid partial writes."

Expected: trigger capture, auto-write or update card, upsert index.

### C. Task-End Trigger (Capture) — 3

7. "Task complete. We solved intermittent 504s only after adding jittered exponential backoff."
8. "Done. Deploy passed only after clearing stale feature flags before migration."
9. "Done. Flaky tests stabilized after replacing sleep waits with condition-based waiting."

Expected: evaluate criteria, auto-capture qualifying lessons.

### D. Should-Not-Trigger — 3

10. "What is the default local HTTP port?"
11. "Explain CAP theorem simply."
12. "We had a random outage yesterday but do not know cause or fix yet."

Expected: no recall/capture execution.

## Scoring Rubric

## 1) Trigger Precision

Definitions:

- TP: triggered when expected
- FP: triggered when not expected

Formula:

`precision = TP / (TP + FP)`

Pass: `precision >= 0.85`

## 2) Recall Usefulness

Evaluate task-start cases (1-3), score each 0-10 on:

- relevance of loaded cards
- bounded read behavior
- actionable constraints extracted

Pass: average >= 8.0

## 3) Capture Compliance

Evaluate cases (4-9), score each 0-10 on:

- auto-capture occurs when qualified
- required fields are complete
- tags count is 3-6
- index is updated correctly

Apply penalties for mistaken capture in non-trigger cases (10-12).

Pass: average >= 9.0

## 4) Related-Link Rate

Only on opportunities where high-value gate is met:

- Q: qualified opportunities
- L: opportunities with correct `related` creation

`related_link_rate = L / Q` (if Q > 0)

Pass: `related_link_rate >= 0.8`
