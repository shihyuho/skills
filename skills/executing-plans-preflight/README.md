# Executing Plans Preflight

Run git preflight checks before implementation starts.

## Why this skill exists

When implementation starts right after planning, it is easy to skip branch, worktree, or remote-state checks. This skill turns those checks into a hard gate instead of a best-effort reminder.

## What it checks

- **Branch Context** - block detached `HEAD` and default-branch execution.
- **Worktree Clean** - block local changes until they are resolved.
- **Remote Sync** - block stale, diverged, or deleted-upstream states.

If the current directory is not a git repository, the checks return `SKIP` rather than blocking by default.

Common triggers include `start implementation`, `implement this plan`, `execute plan`, `開始實作`, and `執行計劃`.

## Execution order

- Run `executing-plans-preflight` first.
- Continue to plan execution only when no check is `BLOCK`.
- If any check is `BLOCK`, stop, show remediation, and wait for user confirmation.

This skill is a precondition for `superpowers:executing-plans`, not a follow-up reminder.

Branch policy keeps a safety fallback: if remote default-branch detection is unavailable but the current branch is `main` or `master`, preflight still blocks.

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

## Related file

- `skills/executing-plans-preflight/SKILL.md`

## License

MIT
