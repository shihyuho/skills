# G.3 Remote Sync Gate

## Purpose

Reduce stale-branch risk by checking sync status with tracking remote before execution.

## Checks

Run in order:

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git status --short --branch
```

## Pass Criteria

- Tracking remote exists, and branch is not behind or diverged from upstream.

## Decision Rules

1. **No tracking remote**
   - Outcome: `SKIP` (per policy `skip_if: no tracking remote`).
   - Action: continue.

2. **Upstream exists and branch is up to date**
   - Outcome: `PASS`.
   - Action: continue.

3. **Upstream exists and branch is ahead only**
   - Outcome: `PASS`.
   - Action: continue.

4. **Upstream exists and branch is behind or diverged**
   - Outcome: `BLOCK`.
   - Action: sync with upstream (`git pull --rebase` or equivalent workflow) before execution.

## Block Action

- Do not start plan execution when branch is behind/diverged from upstream.

## Reporting Fields

- upstream branch (or none)
- `git status --short --branch` summary
- gate outcome (`PASS`/`BLOCK`/`SKIP`)
- next required action
