---
name: executing-plans-preflight
description: Use before superpowers:executing-plans or any implementation start — auto-detects and fixes git state issues (branch, dirty files, remote sync) with one confirmation per fix. Trigger on "start implementation", "implement this plan", "start coding", "execute plan", "開始實作", "執行計劃", or any signal that coding is about to begin.
license: MIT
metadata:
  author: shihyuho
  version: "3.0.0"
---

# Executing Plans Preflight

Semi-automatic git state gate. Detects issues, proposes fixes, executes on
confirmation. This skill runs **before** `superpowers:executing-plans` — it
ensures git state is ready, then execution follows.

Not in a git repo? Say `Not a git repository — skipping preflight.` and move on.

## Checks

Run in order. Pass silently when nothing is wrong — only speak up when there is
something to fix.

### 1. Branch Context

Detect default branch via `origin/HEAD`. Fallback: treat `main`/`master` as
default if detection fails.

- **Detached HEAD** → ask which branch to switch to (cannot infer).
- **On default branch** → infer a branch name from the plan in conversation
  (title → kebab-case, prefix with conventional commit type: `feat/`, `fix/`,
  `docs/`, `refactor/`, `perf/`, `test/`, `chore/`, `ci/`, `build/`; default
  `feat/`). Propose it, let user confirm or rename, then `git switch -c`.
  No plan in conversation? Ask directly. Never scan `docs/superpowers/plans/`
  — stale files mislead.
- **Otherwise** → silent pass.

### 2. Worktree Clean

Run `git status --porcelain`. Everything counts as dirty (staged, unstaged,
untracked).

- **Clean** → silent pass.
- **Dirty** → list paths, ask user to resolve or say "continue" to override.
  Record the override — Check 3 needs to know. Don't help with commit/stash;
  that's the user's call, because commit scope and message are conscious
  decisions that shouldn't be buried inside preflight.

### 3. Remote Sync

Run `git fetch`. If fetch fails, warn and continue with local info — don't
claim remote state is fresh when it isn't.

- **No upstream / ahead / up-to-date** → silent pass.
- **Upstream gone** → ask: clear tracking or recreate?
- **Behind/diverged** → propose `git pull --rebase`. If dirty files were
  overridden in Check 2, warn that pull may conflict and offer to skip sync.

New branches from Check 1 have no upstream — that's expected, don't push.

## Report

One-line conclusion after all checks. Each fix gets its own line before it.

```
Switched to `feat/add-auth` (was on main)
Preflight passed. Ready to go.
```

If dirty files were overridden, end with `Proceeding with uncommitted changes.`
instead of `Ready to go.`

## Why these guardrails exist

- **Confirm before executing** — git operations are hard to undo; one wrong
  `switch -c` or `pull --rebase` on the wrong branch can cost real work.
- **Allow dirty override** — blocking unconditionally was v2's biggest friction
  point. The user knows their working state better than preflight does.
- **Never push** — preflight manages local state only. Publishing is a separate,
  deliberate step.
