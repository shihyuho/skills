---
name: browse
description: "Open the current repository in a browser, preferring the current branch when it exists on the remote."
license: MIT
disable-model-invocation: true
---

## Invocation input

`$ARGUMENTS` below means the arguments supplied with the user's explicit invocation. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.


## Context

- Current branch: !`git branch --show-current`

## Your task

Open the repository in the browser with `gh browse`. Run only the calls below and send no other text.

- If `$ARGUMENTS` is given, pass it straight through to `gh browse`.
- Otherwise, if the current branch is non-empty and `git ls-remote --exit-code --heads origin <branch>` succeeds, run `gh browse --branch <branch>`; else run `gh browse`.

$ARGUMENTS
