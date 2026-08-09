---
name: push
description: "Push the current branch to origin with a safety gate for direct default-branch pushes."
license: MIT
disable-model-invocation: true
---

# push

## Invocation input

`$ARGUMENTS` below means the arguments supplied with the user's explicit invocation. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.


## Context

- Current git status: !`git status`
- Current branch: !`git branch --show-current`
- Default branch: !`git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || true`
- Recent commits: !`git log --oneline -10`
- Unpushed commits: !`git log @{u}..HEAD --oneline 2>/dev/null || true`

## Your task

Push the current branch to origin.

**Safety gate:** If the current branch equals the default branch shown above, STOP before pushing and use the AskUserQuestion tool to get explicit confirmation that pushing directly to the default branch is intended. Only after the user confirms, run `git push`. If the current branch is NOT the default branch, push immediately without asking.

When pushing without confirmation (non-default branch), do it in a single message. Do not use any other tools or send any other text besides the push.
