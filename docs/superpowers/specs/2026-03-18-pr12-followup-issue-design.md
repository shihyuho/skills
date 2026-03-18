# PR #12 Follow-up Issue Design

## Goal

Create one GitHub tracking issue that captures the key follow-up findings from PR #12 and starts a focused discussion on how to resolve them in the right order.

The issue should help maintainers answer two questions:

1. Which behaviors are the intended canonical contract for `ultrabrain` after PR #12?
2. Which repo artifacts (`commands/`, `evals/`, helper scripts) have not yet caught up to that contract?

## Scope

This design covers:

- the structure and intent of one tracking issue
- the issue body contents
- the discussion framing for next steps

This design does not cover:

- implementing the fixes
- splitting work into PRs yet
- changing the canonical `ultrabrain` rules directly

## Background

PR #12 introduced several connected changes to `ultrabrain`:

- staged recall instead of a single recall step before planning
- a clearer map taxonomy centered on `home`, `domain maps`, `lessons-moc`, `general-moc`, and `review lenses`
- a stronger thin-card rule requiring `decision=rewrite-first`
- source notes as provenance-only
- modularization of detailed conventions into `references/`

The review found that the main skill and README mostly align, but several related artifacts may still reflect older assumptions or incomplete follow-through.

## Recommended Approach

Use a single tracking issue rather than opening multiple issues immediately.

Why this is the recommended approach:

- the problems are coupled and came from one conceptual change set
- some items may disappear once the canonical contract is clarified
- maintainers can agree on fix order before splitting work

Alternative approaches considered but not chosen:

- one bug issue for only the highest-severity item: too narrow for the current ambiguity set
- one issue per finding immediately: too fragmented before the contract and priorities are aligned

## Issue Structure

The issue body should use these sections:

## Summary

Briefly state that PR #12 improved the `ultrabrain` model but appears to have left follow-up inconsistencies across `commands/`, `evals/`, and validation helpers.

## Findings

List the five findings in priority order.

### High priority

1. `evals/ultrabrain-evals.json` eval 4 still validates a `troubleshooting lens` concept that no longer matches the new taxonomy.
2. `commands/ultrabrain-recall.md` still frames recall as a one-shot pre-planning action instead of staged recall.
3. `skills/ultrabrain/SKILL.md` does not formally define `decision=skip`, but eval 8 assumes it is valid.

### Medium priority

4. `evals/scripts/check_ultrabrain_thin_card.py` does not catch several thin-card violations the spec now forbids.
5. `commands/ultrabrain-groom.md` may underspecify grooming now that detailed rules live in `skills/ultrabrain/references/map-grooming.md`.

Each finding should include:

- why it matters
- whether it is a design issue, inconsistency, validation gap, or regression risk
- file references for evidence

## Proposed Discussion Questions

The issue should explicitly ask maintainers to align on these decisions:

1. Is `skills/ultrabrain/SKILL.md` the canonical source of truth for post-PR #12 behavior when `commands/` or `evals/` disagree?
2. Should `decision=skip` be added to the canonical capture contract, or should eval 8 be narrowed to the existing decision set?
3. Should fixes land in one follow-up PR or as a small ordered sequence of PRs?

## Recommended Fix Order

Recommend this order in the issue body:

1. Clarify the canonical contract where it is still ambiguous.
2. Update `evals/ultrabrain-evals.json` to match that contract.
3. Update `commands/` files so invocation guidance matches the skill.
4. Tighten machine checks such as `evals/scripts/check_ultrabrain_thin_card.py`.

This order reduces the chance of fixing downstream artifacts against the wrong rule set.

## Issue Tone

The issue should be framed as follow-up alignment work, not as a rejection of PR #12.

Tone goals:

- factual
- specific
- evidence-backed
- open to discussion where the contract is genuinely undecided

Avoid:

- blaming language
- vague claims without file references
- proposing implementation details before agreement on the contract

## Draft Outcome

If the issue works well, the immediate output is not code. The immediate output is agreement on:

- which findings are real
- which are highest priority
- which behavior definition is canonical
- whether any findings should be split into separate follow-up issues

## Verification

Before creating the issue:

- confirm the file references still exist in the current branch
- ensure the issue body distinguishes confirmed inconsistencies from open design questions
- ensure the proposed fix order flows from contract clarification to downstream alignment

## Constraints

- create one GitHub issue only
- include the reviewed findings from PR #12
- start the discussion in the issue body itself rather than posting only a raw defect list
- do not make code changes as part of issue creation
