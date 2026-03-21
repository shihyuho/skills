# Lessons Learned Confidence Design

## Goal

Refine `lessons-learned` by adding a lightweight recall-exit mechanism without changing the existing meaning of lesson `confidence`.

This design should reduce repeated recall of weakly applicable lessons without requiring a new archive directory or a more complex lesson state system.

## Problem

The current skill uses `confidence` as a ranking signal during recall, but it does not define what should happen when a lesson becomes weak enough that it should stop participating in normal recall.

That gap creates two related problems:

- a recalled lesson can keep appearing even when it is only weakly useful in current work
- the system does not clearly define what should happen when a lesson becomes weak enough that it should stop participating in normal recall

The immediate user need is not full lesson lifecycle management. The immediate need is a lighter-weight way to reduce repeated exposure to lessons that no longer deserve strong default application.

## Scope

This design covers:

- how to add a recall-exit mechanism without redefining `confidence`
- how `confidence` affects normal recall
- how `confidence` should increase or decrease over time
- how `confidence` changes should appear in the Lessons capture report

## Recommended Approach

Keep the existing `confidence` meaning and add a recall-exit mechanism based on `confidence: 0.0`.

In this model:

- `confidence` keeps its current role as a strength and ranking signal
- `confidence: 0.0` becomes the explicit rule for non-participation in normal recall
- confidence changes happen only during capture or update, not during recall itself

This approach is recommended because:

- it preserves the current skill semantics instead of redefining an existing field
- it fits the current skill structure with minimal schema change
- it solves the repeated-recall problem by allowing weak lessons to exit normal recall
- it avoids overloading the design with a separate archive workflow before it is needed

## Confidence Semantics

`confidence` keeps its existing meaning in `lessons-learned`.

- This design does not redefine `confidence` as objective truth.
- This design does not introduce a new lesson lifecycle state field.
- `confidence` remains the existing strength and ranking signal used during recall.
- `confidence` must not decay solely because a lesson was not used recently.

## Recall Behavior

Normal recall should change in one way:

- cards with `confidence: 0.0` do not participate in normal recall

For all remaining cards, keep the current ranking model:

`tag match -> scope match -> confidence (desc) -> date (desc)`

Recall is read-only with respect to `confidence`:

- do not change `confidence` merely because a lesson was loaded during recall
- do not change `confidence` merely because a lesson was not loaded during recall
- do not change `confidence` merely because a lesson was not used recently

The existing recall limits remain unchanged:

- load `1-3` primary cards
- expand with up to `2` related cards
- load at most `5` cards total

Cards with `confidence: 0.0` remain in lesson storage for explicit historical lookup. They may still be inspected when the user explicitly asks to review cards excluded from normal recall.

## Confidence Changes

- Confidence changes happen only during capture or update, not during recall.
- Confidence changes should normally move `+0.1` or `-0.1`.
- A lesson that should no longer participate in normal recall should move directly to `0.0`.

### Confidence increases

Increase `confidence` (+0.1) during capture or update when:

- the user explicitly confirms the lesson remains useful

### Confidence decreases

Decrease `confidence` (-0.1) during capture or update when:

- the user explicitly corrects the lesson
- the lesson was recalled and later proved inapplicable in practice
- contradicting evidence appears in the current task
- a newer approach weakens how strongly the lesson should participate in recall by default

When a recalled lesson proves only partially inapplicable:

- update the card content first
- then decrease `confidence` only if subsequent capture or update shows the lesson should participate less strongly in recall by default

Do not decrease `confidence` solely because the lesson was not observed recently.

## Updating Existing Cards

When new evidence changes an existing lesson, update the existing card rather than creating a duplicate card.

When a lesson becomes only partially outdated or context-specific:

- update the current card first
- preserve the card ID
- adjust `confidence` only if subsequent capture or update shows the lesson should participate less strongly in recall by default

This follows the current lesson rule that semantically similar lessons should update the existing card instead of creating near-duplicates.

## New Card Defaults

Keep the current source-based defaults for new cards:

- `user-correction` -> `0.7`
- `bug-fix` -> `0.5`
- `retrospective` -> `0.3`

This iteration does not change those defaults.

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
- `Lessons capture report: decision=update, updated=1 (\`db-migration-run-order\`), confidence=0.7->0.6 (weaker applicability in current config)`
- `Lessons capture report: decision=update, updated=1 (\`legacy-bootstrap-flow\`), confidence=0.1->0.0 (excluded from normal recall)`

This reporting keeps confidence changes visible without requiring the user to inspect the full card body.

## Constraints

- keep `confidence` in the inclusive range `0.0-0.9`
- preserve `source -> confidence` defaults for new cards: `user-correction=0.7`, `bug-fix=0.5`, `retrospective=0.3`
- preserve the existing recall size limits
- do not introduce time-based decay in this iteration
- do not require a new archive directory in this iteration
- do not redefine `confidence`

## Verification

Before implementation planning, confirm that the updated skill language will:

- preserve the existing meaning of `confidence` as the current numeric recall-ranking signal
- define `confidence: 0.0` as excluded from normal recall
- preserve current recall ranking for active cards
- make recall read-only with respect to `confidence`
- preserve `source -> confidence` defaults for new cards
- require confidence changes to appear in capture reporting
- avoid adding new storage structures unless explicitly chosen later
