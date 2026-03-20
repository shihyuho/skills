# Lessons Learned Confidence Design

## Goal

Refine `lessons-learned` so lesson `confidence` means application strength rather than objective truth.

This design should reduce repeated recall of weakly applicable lessons without requiring a new archive directory or a more complex lesson state system.

## Problem

The current skill defines `confidence` as a ranking signal during recall, but it does not clearly define what the score means in practice.

That ambiguity creates two related problems:

- a recalled lesson can keep appearing even when it is only weakly useful in current work
- the system does not clearly define what should happen when a lesson becomes weak enough that it should stop participating in normal recall

The immediate user need is not full lesson lifecycle management. The immediate need is a lighter-weight way to reduce repeated exposure to lessons that no longer deserve strong default application.

## Scope

This design covers:

- the meaning of `confidence` in `lessons-learned`
- how `confidence` affects normal recall
- how `confidence` should increase or decrease over time
- how `confidence` changes should appear in the Lessons capture report

This design does not cover:

- adding a new `archived/` storage directory
- redesigning the full lesson card schema around multiple lifecycle states
- introducing cooldown windows or recency decay
- changing the hard recall limits for primary and related cards

## Recommended Approach

Define `confidence` as application strength.

In this model, `confidence` answers this question:

> When this lesson matches the current task, how strongly should the agent apply it by default?

This approach is recommended because:

- it matches the user's intended semantics for the score descriptions
- it fits the current skill structure with minimal schema change
- it solves the repeated-recall problem by allowing weak lessons to be downgraded to non-participation in normal recall
- it avoids overloading the design with a separate archive workflow before it is needed

## Alternative Approaches Considered

### 1. `confidence` as objective truth

Not chosen because the score descriptions under discussion are about application behavior, not factual correctness.

Examples such as "Suggested but not enforced" and "Treat as default project behavior" describe how strongly a lesson should be used, not whether it is universally true.

### 2. Add explicit status fields now (`active`, `paused`, `archived`)

Not chosen for this iteration because it would expand the lesson model, `_index.md` behavior, and rebuild rules before there is a proven need.

The simpler approach is to use `confidence: 0.0` as the inactive threshold for normal recall while preserving cards in storage.

### 3. Add cooldown or recency decay

Not chosen because the current issue is not that old lessons are forgotten too slowly. The issue is that some lessons should be applied less strongly after contradictory evidence or weaker applicability.

Time-based decay would solve a different problem and risks penalizing useful but infrequent lessons.

## Confidence Semantics

`confidence` represents application strength, not objective truth.

- A low-confidence lesson may still be valid, but should be applied cautiously.
- A high-confidence lesson should be treated as a stronger default unless the current context conflicts.
- `confidence` must not decay solely because a lesson was not used recently.

Use these canonical levels:

| Score | Meaning | Behavior |
|---|---|---|
| `0.0` | Inactive | Excluded from normal recall |
| `0.3` | Tentative | Suggested but not enforced |
| `0.5` | Moderate | Applied when relevant |
| `0.7` | Strong | Preferred unless context conflicts |
| `0.9` | Core | Treat as default project behavior |

This design uses canonical anchor values rather than requiring fully arbitrary floating-point steps.

- New or updated cards should use only these canonical values: `0.0`, `0.3`, `0.5`, `0.7`, `0.9`.
- Existing non-canonical values may remain temporarily for backward compatibility during transition work.
- If an existing non-canonical value is edited, it should be normalized to the nearest canonical value as part of that update.
- If a value sits exactly between two canonical levels, normalize downward to the more conservative level.
- This design does not require a one-time bulk migration of untouched non-canonical cards.

## Recall Behavior

Normal recall should change in one way:

- cards with `confidence: 0.0` do not participate in normal recall

For all remaining cards, keep the current ranking model:

`tag match -> scope match -> confidence (desc) -> date (desc)`

The existing recall limits remain unchanged:

- load `1-3` primary cards
- expand with up to `2` related cards
- load at most `5` cards total

Cards with `confidence: 0.0` remain in lesson storage for explicit historical lookup. They may still be inspected when the user explicitly asks to review inactive lessons.

## Confidence Changes

Confidence changes should move between canonical levels, not by arbitrary numeric increments such as `+0.1` or `-0.1`.

When confidence changes, select the canonical value that best matches the new evidence.

- Small weakening or strengthening should typically move one canonical level.
- Strong contradictory or validating evidence may justify moving multiple levels in a single update.
- A lesson that should no longer participate in normal recall should move directly to `0.0`.

This replaces free-form incremental adjustment for new and edited cards in this design.

### Confidence increases

Increase `confidence` when:

- the lesson is validated again in a similar context
- the same pattern helps across multiple tasks
- the user explicitly confirms the lesson remains useful

### Confidence decreases

Decrease `confidence` when:

- the user explicitly corrects the lesson
- the lesson is recalled but proves inapplicable in practice
- contradicting evidence appears in the current task
- a newer approach weakens the lesson's default applicability

Do not decrease `confidence` solely because the lesson was not observed recently.

## Updating Existing Cards

When new evidence changes how strongly an existing lesson should be applied, update the existing card rather than creating a duplicate card.

This follows the current lesson rule that semantically similar lessons should update the existing card instead of creating near-duplicates.

## New Card Defaults

New cards should preserve the current `source -> confidence` defaults, but expressed as canonical values:

- `user-correction` -> `0.7`
- `bug-fix` -> `0.5`
- `retrospective` -> `0.3`

This keeps initial confidence assignment aligned with current skill behavior while fitting the canonical-level model.

If a confidence change brings a card to `0.0`:

- keep the file in `docs/lessons/`
- exclude it from normal recall
- do not require moving it into a separate archive directory in this iteration

This preserves history while keeping the active recall set focused.

## Lessons Capture Report

If a capture or update changes `confidence`, the Lessons capture report should include:

- the card ID
- the previous confidence value
- the new confidence value
- a short reason for the change

For new cards, use `none-><value>` as the confidence transition format.

If `confidence` becomes `0.0`, the report must explicitly state that the card is excluded from normal recall.

Example report lines:

- `Lessons capture report: decision=create, created=1 (\`api-timeout-retry-pattern\`), confidence=none->0.5 (new reusable pattern)`
- `Lessons capture report: decision=update, updated=1 (\`db-migration-run-order\`), confidence=0.7->0.5 (weaker applicability in current config)`
- `Lessons capture report: decision=update, updated=1 (\`legacy-bootstrap-flow\`), confidence=0.3->0.0 (excluded from normal recall)`

This reporting keeps confidence changes visible without requiring the user to inspect the full card body.

## Constraints

- keep `confidence` in the inclusive range `0.0-0.9`
- use canonical confidence values for new and edited cards: `0.0`, `0.3`, `0.5`, `0.7`, `0.9`
- preserve `source -> confidence` defaults for new cards: `user-correction=0.7`, `bug-fix=0.5`, `retrospective=0.3`
- preserve the existing recall size limits
- do not introduce time-based decay in this iteration
- do not require a new archive directory in this iteration
- do not redefine `confidence` as objective truth

## Verification

Before implementation planning, confirm that the updated skill language will:

- define `confidence` consistently as application strength
- define canonical confidence transitions clearly enough to replace ad hoc `+0.1` adjustments for new and edited cards
- define `confidence: 0.0` as excluded from normal recall
- preserve current recall ranking for active cards
- preserve `source -> confidence` defaults for new cards
- require confidence changes to appear in capture reporting
- avoid adding new storage structures unless explicitly chosen later
