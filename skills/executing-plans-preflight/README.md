# Executing Plans Preflight

Semi-automatic git state gate for implementation sessions.

## Why this skill exists

Starting implementation without checking git state leads to working on the
wrong branch, committing to main, or diverging from remote. This skill
catches those issues and fixes them with one confirmation per fix.

## What it checks

1. **Branch Context** — detects detached HEAD or default branch, proposes
   switching to a feature branch with a name inferred from the plan context.
2. **Worktree Clean** — detects uncommitted changes, asks user to resolve or
   override.
3. **Remote Sync** — detects stale/diverged upstream, proposes pull with
   awareness of dirty worktree state.

Outside a git repository, preflight is skipped entirely.

## How it works

- Detect → Propose fix → Wait for one confirmation → Execute → Next check.
- Checks that pass get no output. Only issues and applied fixes are reported.
- The user can override dirty worktree and proceed.
- Preflight manages local state only — it never pushes.

## Example

```text
You're on `main`. Switch to `feat/add-auth`? (or type a different name)
> yes

Switched to `feat/add-auth` (was on main)
Preflight passed. Ready to go.
```

## Installation

```bash
npx skills add shihyuho/skills --skill executing-plans-preflight -g
```

## License

MIT
