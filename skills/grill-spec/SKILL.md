---
name: grill-spec
description: Use after completing a plan or spec via writing-plans or brainstorming skills, before presenting it to the user for review. Inserts a grill-me stress-test step to catch design blind spots. Also triggers when a spec or design document is ready for user review, or when about to ask the user to review a finished design. Does NOT trigger for code review, PR review, or inline design discussions.
---

# Grill Spec

Before presenting a spec or design document to the user for review, offer to stress-test it with grill-me first. Grilling catches design blind spots — untested assumptions, missing edge cases, weak trade-off reasoning. Without this step, the user ends up doing the stress-testing themselves.

## Steps

1. **Check grill-me dependency** — if grill-me is not installed, ask user if they want to install it (see [references/install-grill-me.md](references/install-grill-me.md) for installation paths). If user declines, skip grilling entirely.

2. **Ask and invoke** — ask the user if they'd like to stress-test the spec with grill-me before their review. If user agrees, invoke grill-me with the spec file path. If user declines, proceed directly to user review.

3. **Offer spec updates** — when grilling completes, if the session produced new insights or decision changes, ask: "Want me to update the spec with any of the insights from this session?" If nothing new came up, skip this and proceed to user review.

## Example

```
[Spec is ready — about to hand to user for review]

Agent: Before your review, want me to stress-test the spec with grill-me?
       It catches untested assumptions and edge cases.
User: Sure, go ahead.

[Invokes grill-me with spec path: docs/design/auth-redesign.md]
[grill-me asks several questions, user answers each]

Agent: Grilling done. We uncovered a gap in the token rotation policy.
       Want me to update the spec with that?
User: Yes, add it.
Agent: Done. Ready for your full review.
```

## Scope

**Applies to:** standalone spec or design documents — e.g. files produced by writing-plans or brainstorming skills, `docs/design/*.md`, architecture decision records.

**Does NOT apply to:** code review, PR review, PR descriptions, commit messages, or design discussions embedded in conversation.

## Skip Policy

The user can always skip grilling. If they seem pressed for time, briefly explain the value ("stress-tests design assumptions before your review"), then ask if they'd like to skip. Respect their answer — the user owns the process, not the skill.
