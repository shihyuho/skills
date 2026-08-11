---
name: commit
description: "Create one cohesive commit from all or explicitly selected changes, or ask before splitting clearly unrelated concerns."
license: MIT
disable-model-invocation: true
---

# commit

## Invocation input

`$ARGUMENTS` below means the arguments supplied with the user's explicit invocation. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.


## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

You MUST invoke the git-commit-co-author skill before running git commit.

First assess whether the diff clearly spans several unrelated concerns (e.g. a bug fix plus an unrelated rename plus a new doc). Treat a cohesive change that merely touches many files as one concern — bias toward NOT splitting; only flag clear, separable concerns.

**Explicit paths.** When `$ARGUMENTS` names an exact path list, that list is the complete commit scope. Verify every path has a tracked, staged, deleted, or untracked change; a missing or unchanged requested path stops the commit. Assess cohesion only within the selected paths and leave every other staged or unstaged change untouched. Use literal paths after `--`, never globs. Stage the selected paths with `git add -- <paths>`, then commit them with `git commit --only -m "<message>" -- <paths>` so unrelated pre-staged changes remain outside the commit.

Without an explicit path list, retain the all-current-changes behavior below.

- If the selected changes are one concern: create a single git commit. Stage and create it using a single message, calling multiple tools in one response. Do not use any other tools or send any other text besides these tool calls.
- If the diff clearly spans several unrelated concerns: ask the user whether to record one single commit or split into atomic commits (one per concern). Then create the commit(s) accordingly — for the atomic path, stage and commit each concern separately.
