---
name: executing-plans-preflight
description: Use when starting implementation or executing a plan so git preflight checks run before file edits or task execution.
license: MIT
metadata:
  author: shihyuho
  version: "2.0.0"
---

# Executing Plans Preflight

Run preflight before plan execution or file edits. Any `BLOCK` stops execution until the user resolves it.

## When to Use

Trigger when the user asks to start implementation, execute a plan, or continue coding after planning.

Common phrases:

- `start implementation`
- `implement this plan`
- `start coding`
- `execute plan`
- `run the implementation plan`
- `開始實作`
- `執行計劃`

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
