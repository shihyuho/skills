# Executing Plans Preflight

Run a preflight gate before implementation with policy-driven execution.

## Why this skill exists

When implementation starts right after planning, it is easy to skip critical checks. This skill makes pre-execution validation explicit, repeatable, and policy-driven.

## What it does

Before implementation, AI evaluates gate policy in `references/preflight-gates.md` and executes gate details from `references/gates/*.md`.

Current policy includes:

```bash
# G.1 branch context
git branch --show-current

# G.2 worktree cleanliness
git status --short

# G.3 remote sync (when upstream exists)
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git status --short --branch
```

## Integration with Plan Execution

Use this ordering when a user asks to execute a plan:

1. Run `executing-plans-preflight` first.
2. If preflight passes, continue with `superpowers:executing-plans`.
3. If preflight blocks, pause execution and resolve blockers first.

This turns preflight into a hard precondition, not a best-effort reminder.

## Example behavior

### Case 1: On main

```text
Current branch: main
Working tree: clean

準備開始實作前，建議先建立功能分支，避免影響 main/master。要不要現在建立？（推薦）
```

### Case 2: On feature branch

```text
Current branch: feat/security-hardening
Working tree: clean

Branch context looks good. Proceeding with implementation.
```

### Case 3: Detached HEAD

```text
Current branch: (detached)

Implementation is blocked until we switch to a named branch.
```

## Trigger phrases

- "start implementation"
- "implement this plan"
- "start coding"
- "開始實作"
- "執行計劃"
- "execute plan"
- "run the implementation plan"

## Related Files

- [SKILL.md](./SKILL.md)
- [references/preflight-gates.md](./references/preflight-gates.md)
- [references/gates/g1-branch-context.md](./references/gates/g1-branch-context.md)
- [references/gates/g2-worktree-clean.md](./references/gates/g2-worktree-clean.md)
- [references/gates/g3-remote-sync.md](./references/gates/g3-remote-sync.md)

## License

MIT
