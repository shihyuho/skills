---
name: executing-plans-preflight
description: Use before superpowers:executing-plans or any implementation start — auto-detects and fixes git state issues (branch, dirty files, remote sync) with one confirmation per fix.
license: MIT
metadata:
  author: shihyuho
  version: "3.0.0"
---

# Executing Plans Preflight

Semi-automatic git state gate. Detects issues, proposes fixes, executes on
confirmation. Runs before plan execution or any implementation start.

## When to Use

Trigger before `superpowers:executing-plans` or when the user starts coding.
This skill runs first; `executing-plans` follows after preflight passes.

Common phrases:

- `start implementation`
- `implement this plan`
- `start coding`
- `execute plan`
- `run the implementation plan`
- `開始實作`
- `執行計劃`

## Pre-check: Git Repository

```bash
git rev-parse --is-inside-work-tree
```

If not inside a git repository, output:

```
Not a git repository — skipping preflight.
```

Then proceed without further checks.

## Check 1: Branch Context

```bash
git branch --show-current
git remote get-url origin >/dev/null 2>&1 && DEFREMOTE=origin || DEFREMOTE=$(git remote | head -1)
git symbolic-ref "refs/remotes/${DEFREMOTE:-origin}/HEAD" 2>/dev/null | sed "s|^refs/remotes/${DEFREMOTE:-origin}/||"
```

| Situation | Action |
|-----------|--------|
| Detached HEAD | Ask: "Detached HEAD — switch to which branch?" (cannot infer) |
| On default branch | Infer branch name from conversation context, propose switch (see Branch Name Inference below) |
| Otherwise | Silent pass |

**Default branch detection fallback:** If `origin/HEAD` detection fails, treat
`main` and `master` as default branches.

### Branch Name Inference

When the user is on the default branch and needs to switch:

1. If the current conversation has a plan (just written or just read), derive
   the branch name from the plan title.
2. Infer the conventional commit type prefix from plan content:
   `feat/`, `fix/`, `docs/`, `refactor/`, `perf/`, `test/`, `chore/`, `ci/`,
   `build/`. Default to `feat/` if unclear.
3. Propose: "You're on `main`. Switch to `<type>/<inferred-name>`? (or type a
   different name)"
4. On confirmation, execute `git switch -c <name>`.
5. If no plan context exists in the conversation, ask the user directly for a
   branch name.

Do not scan `docs/superpowers/plans/` to guess — stale plan files will mislead.

## Check 2: Worktree Clean

```bash
git status --porcelain
```

All output counts as dirty: staged, unstaged modified, and untracked files.

| Situation | Action |
|-----------|--------|
| Clean | Silent pass |
| Dirty | List dirty paths, then ask: "There are uncommitted changes. Please resolve them and let me know when ready, or say 'continue' to proceed anyway." |

If the user says "continue":
- Record internally that dirty files were overridden (Check 3 needs this).
- Proceed to Check 3.

The skill does not assist with commit or stash — resolving dirty state is the
user's responsibility.

## Check 3: Remote Sync

```bash
git fetch 2>/dev/null
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git status --short --branch
```

If `git fetch` fails, warn: "Fetch failed — remote state may be outdated."
Then continue with local upstream information.

| Situation | Action |
|-----------|--------|
| No upstream | Silent pass |
| Upstream gone | Ask: "Upstream deleted. Clear tracking or recreate?" → execute chosen action |
| Behind/diverged, no dirty override | Ask: "Behind remote by N commits. `git pull --rebase`?" → execute on confirm |
| Behind/diverged, dirty override active | Ask: "Behind remote by N commits, but there are uncommitted changes — `git pull --rebase` may fail or conflict. Pull anyway, or skip sync?" |
| Ahead or up-to-date | Silent pass |

If Check 1 just created a new branch, it has no upstream. Check 3 sees
"no upstream" and passes silently. This is expected — preflight does not push.

## Report Format

No C1/C2/C3 table. Each applied fix gets one line. The final line is always a
conclusion reflecting the true state.

**All checks pass silently:**

```
Preflight passed — on `feat/xxx`, clean, synced. Ready to go.
```

**Fixes were applied:**

```
Switched to `feat/add-auth` (was on main)
Pulled 3 commits from origin
Preflight passed. Ready to go.
```

**Dirty files overridden:**

```
Switched to `feat/add-auth` (was on main)
Preflight passed. Proceeding with uncommitted changes.
```

## Guardrails

- MUST run preflight before any plan execution or file edits.
- MUST NOT execute a fix without user confirmation first.
- MUST allow user to override dirty worktree and proceed.
- MUST warn if `git fetch` fails, then continue with local state.
- MUST NOT push branches — preflight manages local state only.
- MUST NOT help with commit or stash — resolving dirty state is the user's
  responsibility.
