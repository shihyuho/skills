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

## Flow

```bash
git rev-parse --is-inside-work-tree
```

```
git repo? ── no ──► report all checks as SKIP
    │
   yes
    ▼
C1 Branch Context → C2 Worktree Clean → C3 Remote Sync
```

Run checks in order. Report evidence and one decision per check: `PASS`, `SKIP`, or `BLOCK`.

## Check 1: Branch Context

```bash
git remote get-url origin >/dev/null 2>&1 && DEFREMOTE=origin || DEFREMOTE=$(git remote | head -1)
git symbolic-ref "refs/remotes/${DEFREMOTE:-origin}/HEAD" 2>/dev/null | sed "s|^refs/remotes/${DEFREMOTE:-origin}/||"
git branch --show-current
```

```
Detached HEAD? ── yes ──► BLOCK
    │
   no
    ▼
No default branch detected? ── yes ──► Current branch is main/master?
    │
   no                                      │yes
    ▼                                      ▼
On default branch? ── yes ──► BLOCK      BLOCK
    │                                      │
   no                                      no
    ▼
PASS
```

Detect the default branch from `origin`, or from the first available remote. If default-branch detection fails and the current branch is `main` or `master`, return `BLOCK`. Otherwise, return `SKIP`.

- `BLOCK` on detached `HEAD`; remediation: switch to a named branch.
- `BLOCK` on the default branch; remediation: create or switch to a feature branch such as `feat/...` or `fix/...`.

## Check 2: Worktree Clean

```bash
git status --porcelain
```

```
Any dirty paths? ── no ──► PASS
    │
   yes
    ▼
BLOCK until dirty paths are resolved
```

If any path is dirty, return `BLOCK`, report the dirty paths, and ask the user to resolve them before re-running preflight.

Suggested remediations can include `git stash`, `git commit`, removing generated output, or otherwise clearing the dirty paths. Do not treat `stash` and `commit` as the only valid choices.

## Check 3: Remote Sync

```bash
git fetch 2>/dev/null
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git status --short --branch
```

```
Tracking remote? ── no ──► SKIP
    │
   yes
    ▼
Upstream is [gone]? ── yes ──► BLOCK
    │
   no
    ▼
Behind or diverged? ── yes ──► BLOCK
    │
   no
    ▼
Ahead or up-to-date? ── yes ──► PASS
    │
   no
    ▼
BLOCK
```

Try `git fetch` first. If it fails, report that failure as evidence and continue with the local upstream status. Do not claim remote refs are fresh when fetch failed.

- `SKIP` if the branch has no upstream.
- `BLOCK` if upstream is `[gone]`; remediation: recreate the upstream branch or clear/reset the upstream reference.
- `BLOCK` if the branch is behind or diverged; remediation: sync first, typically with `git pull --rebase`.
- `BLOCK` on any other unexpected status until the output is understood.

## Report Contract

Use this report shape:

```
- [C1] Branch Context: PASS/BLOCK/SKIP
- [C2] Worktree Clean: PASS/BLOCK/SKIP
- [C3] Remote Sync:   PASS/BLOCK/SKIP
```

For each check, include the evidence used to make the decision. If any check is `BLOCK`:

- list the blocking reason
- propose exact remediation commands when possible
- require explicit user confirmation before plan execution continues

## Guardrails

- MUST run preflight before any plan execution or file edits.
- MUST evaluate git context first.
- MUST report evidence and a decision for every check.
- MUST stop plan execution on any `BLOCK`.
- MUST propose exact remediation commands when possible.
- MUST wait for explicit user confirmation before continuing after a `BLOCK`.
