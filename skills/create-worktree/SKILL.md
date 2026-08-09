---
name: create-worktree
description: "Create and continue work in an isolated, descriptively named Git worktree."
license: MIT
disable-model-invocation: true
---

# create-worktree

## Invocation input

`$ARGUMENTS` below means the arguments supplied with the user's explicit invocation. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.


## Context

- Current branch: !`git branch --show-current`
- Current git status: !`git status --short`
- Existing worktrees: !`git worktree list`
- Recent commits: !`git log --oneline -10`

## Your task

Create a worktree for the work at hand and continue in it. The decision that matters is its **name**: it names both the directory and the branch, so pick something that reads well as a branch name.

**Name.** With `$ARGUMENTS`, derive `<name>` from what the argument describes — treat it as a description of the work, not as a literal name, unless it already reads like a slug. Without one, derive it from the task this session is about to start: what the user just asked for, the plan under discussion, or the uncommitted changes in Context. Keep `<name>` short, ASCII, and valid as a branch name (`git check-ref-format --branch <name>`), e.g. `feat/create-worktree-command`, `fix/null-deref`. If neither the arguments nor the session says what the work is, ask the user one short question — don't invent a placeholder.

**Where.** Always `~/code/worktrees/<repo>/<name>`, where `<repo>` is the repository name — the directory name of its main working tree, not of the worktree you may currently be in. A `/` in `<name>` just nests another level. Never place a worktree inside the repository's own working tree.

**Base.** Default to a fresh base — `git fetch` then branch from `origin/<default-branch>` — so the worktree doesn't inherit the current branch's in-progress state. Branch from the current `HEAD` instead when the work builds on commits that exist only there, and note which base you picked. Uncommitted changes never carry over; if the task depends on them, say so before creating anything.

**Before creating.** Read Context first:
- **Name collision** — if `<name>` already exists as a branch, as a registered worktree, or as a non-empty directory at the target path, don't work around it with a variant name. Say which it is and offer to use the existing one instead.
- **Branch already checked out** — a branch can live in only one worktree at a time. If `<name>` is checked out elsewhere, say where; don't force it.

Create it in one step so the branch and the worktree can't drift apart: `git worktree add -b <name> <path> <base>`.

Once it exists, switch into it if the session can, and report the path, branch, and base in one line. Then pick up the task that prompted it.

$ARGUMENTS
