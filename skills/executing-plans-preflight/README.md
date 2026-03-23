# Executing Plans Preflight

Run git preflight checks before implementation starts.

## Why this skill exists

When implementation starts right after planning, it is easy to skip branch, worktree, or remote-state checks. This skill makes them a hard gate.

## What it checks

- **Branch Context** - block detached `HEAD` and default-branch execution.
- **Worktree Clean** - block local changes until they are resolved.
- **Remote Sync** - block stale, diverged, or deleted-upstream states.

Outside a git repository, the checks return `SKIP`.

Common triggers: `start implementation`, `implement this plan`, `execute plan`, `開始實作`, `執行計劃`.

## Execution order

- Run the preflight checks first.
- Continue to plan execution only when no check is `BLOCK`.
- If any check is `BLOCK`, stop, show remediation, and wait for user confirmation.

Run this before plan execution starts. If default-branch detection fails, local `main` or `master` still blocks; otherwise that check skips.

## Example

```text
- [C1] Branch Context: BLOCK
  Evidence: default branch is main; current branch is main
  Remediation: git switch -c feat/my-change

- [C2] Worktree Clean: PASS
  Evidence: git status --porcelain returned no paths

- [C3] Remote Sync: SKIP
  Evidence: no upstream tracking branch
```

## License

MIT
