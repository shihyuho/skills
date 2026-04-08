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
| Branch naming | Infer from plan context in conversation, suggest, user confirms or renames | Reduces typing while keeping control |
| Branch prefix | Follow conventional commits types (`feat/`, `fix/`, `docs/`, `refactor/`, `perf/`, `test/`, `chore/`, `ci/`, `build/`) | Consistent with project conventions |
| Report format | One-line conclusion, no C1/C2/C3 table | Less noise |
| Relationship to executing-plans | Preflight triggers before `executing-plans`; stated explicitly in skill description | Clear ordering without modifying superpowers |
| Skill name | Keep `executing-plans-preflight` unchanged | Renaming has high cost, low benefit |

## Check Flow

Run checks in order. Each check either passes silently or proposes a single
action and waits for confirmation before moving on.

Checks are not fully independent — later checks may reference earlier results
(e.g., Check 3 needs to know if dirty files were overridden in Check 2).

### Pre-check: Git Repository

```bash
git rev-parse --is-inside-work-tree
```

If not a git repo: output `Not a git repository — skipping preflight.` and
proceed. No further checks.

### 1. Branch Context

```bash
git branch --show-current
# Detect default branch from origin/HEAD
git remote get-url origin >/dev/null 2>&1 && DEFREMOTE=origin || DEFREMOTE=$(git remote | head -1)
git symbolic-ref "refs/remotes/${DEFREMOTE:-origin}/HEAD" 2>/dev/null | sed "s|^refs/remotes/${DEFREMOTE:-origin}/||"
```

| Situation | Action |
|-----------|--------|
| Detached HEAD | Ask: "Detached HEAD. Switch to which branch?" (cannot infer) |
| On default branch | Infer branch name from conversation context, ask: "You're on `main`. Switch to `feat/xxx`? (or type a different name)" → execute `git switch -c <name>` |
| Not default branch, not detached HEAD | Silent pass |

**Default branch detection fallback:** If `origin/HEAD` detection fails, treat
`main` and `master` as default branches.

**Branch name inference:**
- If the current conversation has a plan (just written or just read), derive the
  name from the plan title. Infer conventional commit type from plan content
  (e.g., a plan about fixing something → `fix/`, about adding a feature → `feat/`).
- If no plan context exists in the conversation, ask the user directly.
- Do not scan `docs/superpowers/plans/` to guess — stale plan files will mislead.

### 2. Worktree Clean

```bash
git status --porcelain
```

`git status --porcelain` output includes staged, unstaged modified, and
untracked files. All are considered dirty.

| Situation | Action |
|-----------|--------|
| Clean | Silent pass |
| Dirty | List dirty paths, ask: "There are uncommitted changes. Please resolve them and let me know when ready, or say 'continue' to proceed anyway." |

If the user says "continue" (override):
- Record that dirty files were overridden (needed by Check 3).
- Proceed to next check.

The skill does not help with commit or stash — that is the user's responsibility.

### 3. Remote Sync

```bash
git fetch 2>/dev/null
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git status --short --branch
```

If `git fetch` fails, warn that remote state may be outdated, then continue
with local upstream information.

| Situation | Action |
|-----------|--------|
| No upstream | Silent pass |
| Upstream gone | Ask: "Upstream deleted. Clear tracking or recreate?" → execute |
| Behind/diverged (no dirty override) | Ask: "Behind remote by N commits. `git pull --rebase`?" → execute on confirm |
| Behind/diverged (dirty override active) | Ask: "Behind remote by N commits, but there are uncommitted changes — `git pull --rebase` may fail or conflict. Pull anyway, or skip sync?" |
| Ahead/up-to-date | Silent pass |

### New branch after Check 1

If Check 1 just created a new branch via `git switch -c`, the branch has no
upstream. Check 3 will see "no upstream" and silent pass. This is expected —
preflight does not push.

## Report Format

No C1/C2/C3 table.

**All checks pass silently (nothing to fix):**

```
Preflight passed — on `feat/xxx`, clean, synced. Ready to go.
```

**Fixes were applied:**

```
Switched to `feat/add-auth` (was on main)
Pulled 3 commits from origin
Preflight passed. Ready to go.
```

**Dirty files overridden, sync skipped:**

```
Switched to `feat/add-auth` (was on main)
Preflight passed. Proceeding with uncommitted changes.
```

Each applied fix gets one line. The final line is always the conclusion,
reflecting the true state — no beautification.

## Guardrails

- Run preflight before any plan execution or file edits.
- Never execute a fix without user confirmation first.
- Allow user to override dirty worktree and proceed.
- If `git fetch` fails, warn but continue with local state (do not claim remote
  is fresh).
- Detached HEAD and upstream-gone always require user input (cannot auto-infer).
- Do not push branches — preflight manages local state only.

## Out of Scope

- Worktree creation/management (user does not use worktrees regularly).
- Lesson recall integration (handled by `lessons-learned` skill separately).
- Plan loading or execution (handled by `executing-plans` skill).
- Committing or stashing dirty files (user's responsibility).
- Pushing branches or setting upstream tracking.

## Migration

Replace `skills/executing-plans-preflight/SKILL.md` contents entirely. Bump
version to `3.0.0`. Update `README.md` to match new behavior.
