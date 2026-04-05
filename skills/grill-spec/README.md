# Grill Spec

Stress-test specs and design docs with [grill-me](https://github.com/mattpocock/skills) before user review.

## Why this skill exists

When a spec is "done" and goes straight to user review, the user ends up doing the stress-testing themselves — finding untested assumptions, missing edge cases, and weak trade-off reasoning. This skill inserts a grill-me step before that handoff, so the spec arrives already battle-tested.

## How it works

1. **Check dependency** — verifies grill-me is installed; offers to help install if missing.
2. **Ask and invoke** — asks the user if they want to stress-test the spec before review. Only proceeds with consent.
3. **Offer updates** — if grilling uncovered new insights, asks if the spec should be updated.

## When it triggers

After completing a plan or spec (e.g. via writing-plans or brainstorming), before presenting it to the user for review.

Does **not** trigger for code review, PR review, or inline design discussions.

## Example

```text
Agent: Before your review, want me to stress-test the spec with grill-me?
User: Sure, go ahead.

[grill-me asks several questions, user answers each]

Agent: Grilling done. We uncovered a gap in the token rotation policy.
       Want me to update the spec with that?
User: Yes, add it.
Agent: Done. Ready for your full review.
```

## Prerequisites

Requires the [grill-me](https://github.com/mattpocock/skills) skill. See [references/install-grill-me.md](references/install-grill-me.md) for installation options.

## How to start

```bash
npx skills add shihyuho/skills --skill grill-spec
```

## License

MIT
