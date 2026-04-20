---
name: grill-me-quick
description: Grill the user's plan or design in quick mode, auto-deciding confident calls and asking only when uncertain or high-risk. Uses Chain-of-Verification via independent subagents to validate factual claims when confidence is borderline. Invoke only when the user explicitly asks to "grill me quick" or runs the skill manually — do not trigger automatically from adjacent topics like design review, planning, or stress-testing.
disable-model-invocation: true
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Grill Me Quick

Apply the `grill-me` skill to the user's target.

```
for each grill-me question:
  decision point?
    ├ no  → continue
    └ yes → draft answer (tag each claim as `load-bearing` or `peripheral`)
              ↓
            self-score two axes (1–10):
              • fact   — are the claims true?
              • reason — is the argument sound for this context?
              ↓
            confidence = min(fact, reason)   # if fact is N/A, use reason alone
              ↓
            escalate to subagent verification if:
              • confidence is borderline (5–7) AND draft has factual claims, OR
              • high blast radius AND draft has factual claims
              ↓
            (if escalated)
              dispatch one subagent per claim, in parallel
              → aggregate verdicts → update `fact`
              → recompute `confidence = min(fact, reason)`
              ↓
            passes gate?
              ├ yes → lock in; surface {question, alternatives, scores+rationale, answer}
              │         if escalation fired:
              │           any deviation (refuted/uncertain/re-tagged)
              │             → include `verification:` block listing only deviations
              │           otherwise
              │             → add "N claims verified" to rationale
              └ no  → ask user
```

## Claim tagging

Each factual statement in the draft must be tagged as either:

- **load-bearing** — removing it would invalidate the decision.
- **peripheral** — supporting detail; the decision still holds without it.

Tagging *is* identification. An untagged sentence is not a claim and will not be verified. Do not tag subjective or hedged statements ("team is familiar", "usually works well").

## Claim granularity

- **Load-bearing** claims must be *atomic*: each one verifiable on its own. If a subagent would have to branch ("true for X, false for Y"), split first.
- **Peripheral** claims may be composite when natural to state, as long as each composite is verifiable end-to-end by a single subagent.

Heuristic: if stating it takes more than one "and", it is probably two claims — atomize if load-bearing.

## Escalation

Default: self-score both axes and let the gate decide. This keeps the skill *quick*. Escalate only when self-score is borderline (5–7), or blast radius is high with factual claims present (even at 8–10).

Accepted tradeoff: if the main agent is overconfident AND wrong on a factual claim (Dunning–Kruger), the escalation path will not catch it. For quick mode this is acceptable.

When escalated, follow [references/verification.md](references/verification.md) for the subagent pack, output schema, and aggregation rules.

## Confidence gates

- **8–10** → lock in.
- **5–7** → lock in if reversible and low blast radius; otherwise ask user.
- **1–4** → ask user.

## When to escalate

| Situation | Action |
|---|---|
| `confidence` 5–7 AND draft has factual claims | Escalate |
| High blast radius AND draft has factual claims | Escalate (even at 8–10) |
| Pure judgment, no factual claims | Skip; `fact` = N/A, decide on `reason` alone |
| `confidence` 8–10 AND low blast radius | Skip, lock in |
| `confidence` 1–4 | Skip, ask user |
