# G.1 Branch Context Gate

## Purpose

Ensure implementation does not start in risky git branch context.

## Checks

Run in order:

```bash
git branch --show-current
git status --short
```

## Pass Criteria

- Current branch is a named non-main branch.

## Decision Rules

1. **Not a git repository**
   - Outcome: `SKIP` (per policy `skip_if: not a git repository`).
   - Action: continue preflight without branch-context enforcement.

2. **On `main` or `master`**
   - Risk: high.
   - Outcome: `BLOCK`.
   - Action: remind and ask whether to create a feature branch before implementation.
   - Suggested names:
      - `feat/<task-slug>` for feature work
      - `fix/<task-slug>` for bug fixes

3. **Detached HEAD (empty branch name)**
   - Risk: critical.
   - Outcome: `BLOCK`.
   - Action: block implementation and ask the user to create/switch to a named branch first.

4. **On non-main named branch**
   - Risk: acceptable.
   - Outcome: `PASS`.
   - Action: confirm current branch and proceed.

## Reminder Template

```text
準備開始實作前，建議先建立功能分支，避免影響 main/master。要不要現在建立？（推薦）
```

## Reporting Fields

- current branch
- working tree state
- gate outcome (`PASS`/`BLOCK`/`SKIP`)
- next required action
