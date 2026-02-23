# G.2 Worktree Clean Gate

## Purpose

Ensure implementation starts from a clean working tree to avoid mixing unrelated changes.

## Checks

Run:

```bash
git status --porcelain
```

## Pass Criteria

- `git status --porcelain` is empty, or all dirty paths are inside the allowed dirty-directory whitelist.

## Decision Rules

1. **Working tree clean**
   - Outcome: `PASS`.
   - Action: continue.

2. **Working tree has changes**
   - Classify dirty paths into `whitelisted` and `non-whitelisted`.
   - If `non-whitelisted` is empty -> `PASS`.
   - If any `non-whitelisted` exists -> `BLOCK`.
   - Action: ask user to resolve non-whitelisted changes, then re-run preflight.

## Allowed Dirty Directory Whitelist

Dirty paths under these patterns do not block G.2:

- `docs/plans/**`

Evaluation rule:

1. Parse dirty paths from `git status --porcelain`.
2. Match each dirty path against whitelist patterns.
3. If every dirty path matches whitelist -> `PASS`.
4. Otherwise -> `BLOCK`.

Reporting requirements:

- Report whitelist patterns.
- Report `whitelisted` and `non-whitelisted` path lists.
- If blocked, provide concrete remediation actions for non-whitelisted paths.

## Block Action

- Do not start plan execution while non-whitelisted uncommitted changes remain.

## Reporting Fields

- `git status --porcelain` output summary
- gate outcome (`PASS` or `BLOCK`)
- next required action
- matched/unmatched whitelist path summary
