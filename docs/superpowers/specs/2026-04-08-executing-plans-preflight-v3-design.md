# executing-plans-preflight v3 — Auto-Fix Gate

## Problem

Current preflight (v2) acts as an auditor: it reports BLOCK/PASS/SKIP with a
three-line C1/C2/C3 table, then waits for the user to manually fix each issue.
This causes unnecessary round-trips, verbose output, and friction before every
implementation session.

Additionally, the skill overlaps awkwardly with `superpowers:using-git-worktrees`
(which creates a clean branch + workspace automatically), but the user's actual
workflow is to stay in the current working directory and switch branches — not
use worktrees. The skill should serve that workflow directly.

## Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Approach | Auto-fix gate (detect → propose → confirm → execute) | Removes manual remediation round-trips |
| Interaction | Semi-automatic — each fix needs one user confirmation | Safe but minimal friction |
| Branch naming | Infer from plan title/filename, suggest, user confirms or renames | Reduces typing while keeping control |
| Report format | One-line conclusion, no C1/C2/C3 table | Less noise |

## Check Flow

Run checks in order. Each check either passes silently or proposes a single
action and waits for confirmation before moving on.

### 1. Branch Context

```
git branch --show-current
detect default branch from origin/HEAD
```

| Situation | Action |
|-----------|--------|
| Detached HEAD | Ask: "Detached HEAD. Switch to which branch?" (cannot infer) |
| On default branch | Infer branch name from plan context, ask: "You're on `main`. Switch to `feat/xxx`? (or type a different name)" → execute `git switch -c <name>` |
| On feature branch | Silent pass |

Branch name inference:
- If a plan file exists, derive from its title/filename (e.g., `2026-04-08-add-auth-plan.md` → `feat/add-auth`)
- If no plan context, ask directly

### 2. Worktree Clean

```
git status --porcelain
```

| Situation | Action |
|-----------|--------|
| Clean | Silent pass |
| Dirty | List dirty paths, ask: "Stash, commit, or something else?" → execute chosen action |

### 3. Remote Sync

```
git fetch 2>/dev/null
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git status --short --branch
```

| Situation | Action |
|-----------|--------|
| No upstream | Silent pass |
| Upstream gone | Ask: "Upstream deleted. Clear tracking or recreate?" → execute |
| Behind/diverged | Ask: "Behind remote by N commits. `git pull --rebase`?" → execute on confirm |
| Ahead/up-to-date | Silent pass |

## Report Format

No more C1/C2/C3 table.

**All checks pass with no fixes needed:**

```
Preflight passed — on `feat/xxx`, clean, synced. Ready to go.
```

**Fixes were applied:**

```
Switched to `feat/add-auth` (was on main)
Pulled 3 commits from origin
Preflight passed. Ready to go.
```

Each applied fix gets one line. The final line is always the conclusion.

## Guardrails

- Run preflight before any plan execution or file edits.
- Never execute a fix without user confirmation first.
- If `git fetch` fails, warn but continue with local state (do not claim remote is fresh).
- Detached HEAD and upstream-gone always require user input (cannot auto-infer).

## Out of Scope

- Worktree creation/management (user does not use worktrees regularly).
- Lesson recall integration (handled by `lessons-learned` skill separately).
- Plan loading or execution (handled by `executing-plans` skill).

## Migration

Replace `skills/executing-plans-preflight/SKILL.md` contents entirely. Bump
version to `3.0.0`. Update `README.md` to match new behavior.
