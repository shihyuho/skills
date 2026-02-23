# G.2 Worktree Clean Gate

## Purpose

Ensure implementation starts from a clean working tree to avoid mixing unrelated changes.

## Checks

Run:

```bash
git status --porcelain
```

## Pass Criteria

- `git status --porcelain` output is empty.

## Decision Rules

1. **Working tree clean**
   - Outcome: `PASS`.
   - Action: continue.

2. **Working tree has changes**
   - Outcome: `BLOCK`.
   - Action: ask user to resolve changes before execution (commit, stash, or intentional cleanup), then re-run preflight.

## Practical Handling: `docs/plans/*` Is Commonly Dirty

In plan-first workflows, `docs/plans/*` is often modified before implementation starts.

Recommended handling order:

1. **Preferred: commit plan artifacts first**
   - Create a dedicated docs/planning commit before implementation commits.
   - Benefit: keeps implementation history atomic and preflight reproducible.

2. **Alternative: temporary stash for plan files**
   - Stash plan-only changes, run preflight and implementation, then restore when needed.
   - Use when plan notes are still being refined and should not be committed yet.

3. **Avoid by default: silently allowing dirty `docs/plans/*`**
   - Do not auto-pass G.2 just because changes are docs-only.
   - If a team wants this behavior, define it explicitly in policy (`run_if`/`skip_if`) rather than ad hoc exceptions.

## Block Action

- Do not start plan execution while uncommitted changes remain.

## Reporting Fields

- `git status --porcelain` output summary
- gate outcome (`PASS` or `BLOCK`)
- next required action
