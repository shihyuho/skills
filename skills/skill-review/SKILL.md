---
name: skill-review
description: "Review a skill against the available skill-authoring rubrics and optionally apply fixes."
license: MIT
disable-model-invocation: true
---

## Invocation input

`$ARGUMENTS` below means the arguments supplied with the user's explicit invocation. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.


Review the skill in `$ARGUMENTS` using `/writing-great-skills` and `/skill-creator:skill-creator` as the guiding rubric. If no skill is given, ask which one first.

`/writing-great-skills` is user-invoked (`disable-model-invocation`) — if the Skill tool won't fire it, read its `SKILL.md` and apply that instead.

Read the target's `SKILL.md` and supporting files, then evaluate against them.

- **Default** — report findings (keep names / paths / `file:line` verbatim): 每個問題一張卡(問題 / 位置 / 建議修法), 依嚴重度排序.
- **`--fix`** — skip the report and apply the fixes directly to the target's files, then summarise what changed.

ARGUMENTS: $ARGUMENTS
