# executing-plans-preflight v3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the executing-plans-preflight skill from an audit-report style to a semi-automatic auto-fix gate.

**Architecture:** Single SKILL.md rewrite — the skill is a prompt-based agent skill with no runtime code. The SKILL.md defines all behavior. README.md provides the public-facing description.

**Tech Stack:** Markdown (SKILL.md), git CLI commands embedded in skill instructions.

**Spec:** `docs/superpowers/specs/2026-04-08-executing-plans-preflight-v3-design.md`

---

## File Map

- Modify: `skills/executing-plans-preflight/SKILL.md` — full rewrite
- Modify: `skills/executing-plans-preflight/README.md` — update to match v3
- Modify: `README.md` (project root) — update skill description line

---

### Task 1: Rewrite SKILL.md — Frontmatter and Trigger Section

**Files:**
- Modify: `skills/executing-plans-preflight/SKILL.md:1-27`

- [ ] **Step 1: Replace frontmatter**

Update version to `3.0.0` and revise the description to reflect the auto-fix
gate role and its relationship to `executing-plans`:

```yaml
---
name: executing-plans-preflight
description: Use before superpowers:executing-plans or any implementation start — auto-detects and fixes git state issues (branch, dirty files, remote sync) with one confirmation per fix.
license: MIT
metadata:
  author: shihyuho
  version: "3.0.0"
---
```

- [ ] **Step 2: Rewrite the opening and trigger section**

Replace everything from the title through the "When to Use" section:

```markdown
# Executing Plans Preflight

Semi-automatic git state gate. Detects issues, proposes fixes, executes on
confirmation. Runs before plan execution or any implementation start.

## When to Use

Trigger before `superpowers:executing-plans` or when the user starts coding.
This skill runs first; `executing-plans` follows after preflight passes.

Common phrases:

- `start implementation`
- `implement this plan`
- `start coding`
- `execute plan`
- `run the implementation plan`
- `開始實作`
- `執行計劃`
```

- [ ] **Step 3: Verify frontmatter is valid**

Run: `npx --yes skills-ref validate skills/executing-plans-preflight`
Expected: validation passes (or only warns about content changes in progress)

- [ ] **Step 4: Commit**

```bash
git add skills/executing-plans-preflight/SKILL.md
git commit -m "feat(executing-plans-preflight): rewrite frontmatter and trigger section for v3"
```

---

### Task 2: Rewrite SKILL.md — Pre-check and Check 1 (Branch Context)

**Files:**
- Modify: `skills/executing-plans-preflight/SKILL.md`

- [ ] **Step 1: Write the pre-check section**

Add after the trigger section:

```markdown
## Pre-check: Git Repository

```bash
git rev-parse --is-inside-work-tree
```

If not inside a git repository, output:

```
Not a git repository — skipping preflight.
```

Then proceed without further checks.
```

- [ ] **Step 2: Write Check 1 — Branch Context**

```markdown
## Check 1: Branch Context

```bash
git branch --show-current
git remote get-url origin >/dev/null 2>&1 && DEFREMOTE=origin || DEFREMOTE=$(git remote | head -1)
git symbolic-ref "refs/remotes/${DEFREMOTE:-origin}/HEAD" 2>/dev/null | sed "s|^refs/remotes/${DEFREMOTE:-origin}/||"
```

| Situation | Action |
|-----------|--------|
| Detached HEAD | Ask: "Detached HEAD — switch to which branch?" (cannot infer) |
| On default branch | Infer branch name from conversation context, propose switch (see Branch Name Inference below) |
| Otherwise | Silent pass |

**Default branch detection fallback:** If `origin/HEAD` detection fails, treat
`main` and `master` as default branches.

### Branch Name Inference

When the user is on the default branch and needs to switch:

1. If the current conversation has a plan (just written or just read), derive
   the branch name from the plan title.
2. Infer the conventional commit type prefix from plan content:
   `feat/`, `fix/`, `docs/`, `refactor/`, `perf/`, `test/`, `chore/`, `ci/`,
   `build/`. Default to `feat/` if unclear.
3. Propose: "You're on `main`. Switch to `<type>/<inferred-name>`? (or type a
   different name)"
4. On confirmation, execute `git switch -c <name>`.
5. If no plan context exists in the conversation, ask the user directly for a
   branch name.

Do not scan `docs/superpowers/plans/` to guess — stale plan files will mislead.
```

- [ ] **Step 3: Commit**

```bash
git add skills/executing-plans-preflight/SKILL.md
git commit -m "feat(executing-plans-preflight): add pre-check and branch context check"
```

---

### Task 3: Rewrite SKILL.md — Check 2 (Worktree Clean)

**Files:**
- Modify: `skills/executing-plans-preflight/SKILL.md`

- [ ] **Step 1: Write Check 2 — Worktree Clean**

```markdown
## Check 2: Worktree Clean

```bash
git status --porcelain
```

All output counts as dirty: staged, unstaged modified, and untracked files.

| Situation | Action |
|-----------|--------|
| Clean | Silent pass |
| Dirty | List dirty paths, then ask: "There are uncommitted changes. Please resolve them and let me know when ready, or say 'continue' to proceed anyway." |

If the user says "continue":
- Record internally that dirty files were overridden (Check 3 needs this).
- Proceed to Check 3.

The skill does not assist with commit or stash — resolving dirty state is the
user's responsibility.
```

- [ ] **Step 2: Commit**

```bash
git add skills/executing-plans-preflight/SKILL.md
git commit -m "feat(executing-plans-preflight): add worktree clean check with override"
```

---

### Task 4: Rewrite SKILL.md — Check 3 (Remote Sync)

**Files:**
- Modify: `skills/executing-plans-preflight/SKILL.md`

- [ ] **Step 1: Write Check 3 — Remote Sync**

```markdown
## Check 3: Remote Sync

```bash
git fetch 2>/dev/null
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git status --short --branch
```

If `git fetch` fails, warn: "Fetch failed — remote state may be outdated."
Then continue with local upstream information.

| Situation | Action |
|-----------|--------|
| No upstream | Silent pass |
| Upstream gone | Ask: "Upstream deleted. Clear tracking or recreate?" → execute chosen action |
| Behind/diverged, no dirty override | Ask: "Behind remote by N commits. `git pull --rebase`?" → execute on confirm |
| Behind/diverged, dirty override active | Ask: "Behind remote by N commits, but there are uncommitted changes — `git pull --rebase` may fail or conflict. Pull anyway, or skip sync?" |
| Ahead or up-to-date | Silent pass |

If Check 1 just created a new branch, it has no upstream. Check 3 sees
"no upstream" and passes silently. This is expected — preflight does not push.
```

- [ ] **Step 2: Commit**

```bash
git add skills/executing-plans-preflight/SKILL.md
git commit -m "feat(executing-plans-preflight): add remote sync check with dirty-aware pull warning"
```

---

### Task 5: Rewrite SKILL.md — Report Format and Guardrails

**Files:**
- Modify: `skills/executing-plans-preflight/SKILL.md`

- [ ] **Step 1: Write the report format section**

```markdown
## Report Format

No C1/C2/C3 table. Each applied fix gets one line. The final line is always a
conclusion reflecting the true state.

**All checks pass silently:**

```
Preflight passed — on `feat/xxx`, clean, synced. Ready to go.
```

**Fixes were applied:**

```
Switched to `feat/add-auth` (was on main)
Pulled 3 commits from origin
Preflight passed. Ready to go.
```

**Dirty files overridden:**

```
Switched to `feat/add-auth` (was on main)
Preflight passed. Proceeding with uncommitted changes.
```
```

- [ ] **Step 2: Write the guardrails section**

```markdown
## Guardrails

- MUST run preflight before any plan execution or file edits.
- MUST NOT execute a fix without user confirmation first.
- MUST allow user to override dirty worktree and proceed.
- MUST warn if `git fetch` fails, then continue with local state.
- MUST NOT push branches — preflight manages local state only.
- MUST NOT help with commit or stash — resolving dirty state is the user's
  responsibility.
```

- [ ] **Step 3: Remove all old content**

Delete any remaining v2 content (old Check 1/2/3 sections, old Report Contract,
old Guardrails, old Flow diagram). The file should now contain only the v3
sections written in Tasks 1–5.

- [ ] **Step 4: Validate the skill**

Run: `npx --yes skills-ref validate skills/executing-plans-preflight`
Expected: validation passes

- [ ] **Step 5: Commit**

```bash
git add skills/executing-plans-preflight/SKILL.md
git commit -m "feat(executing-plans-preflight): add report format and guardrails, remove v2 content"
```

---

### Task 6: Update README files

**Files:**
- Modify: `skills/executing-plans-preflight/README.md`
- Modify: `README.md` (project root)

- [ ] **Step 1: Rewrite the skill README**

Replace the entire content of `skills/executing-plans-preflight/README.md`:

```markdown
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

## Relationship to executing-plans

This skill runs **before** `superpowers:executing-plans`. It ensures git state
is ready, then `executing-plans` takes over for plan execution.

## Example

```text
You're on `main`. Switch to `feat/add-auth`? (or type a different name)
> yes

Switched to `feat/add-auth` (was on main)
Preflight passed. Ready to go.
```

## License

MIT
```

- [ ] **Step 2: Update root README skill description**

Change the executing-plans-preflight line in the root `README.md` from:

```
- **[executing-plans-preflight](skills/executing-plans-preflight/)** - Run extensible preflight checks before superpowers:executing-plans, with branch safety as the default gate.
```

To:

```
- **[executing-plans-preflight](skills/executing-plans-preflight/)** - Semi-automatic git state gate — detects and fixes branch, dirty files, and remote sync issues before implementation starts.
```

- [ ] **Step 3: Validate**

Run: `npx --yes skills-ref validate skills/executing-plans-preflight`
Expected: validation passes

- [ ] **Step 4: Commit**

```bash
git add skills/executing-plans-preflight/README.md README.md
git commit -m "docs(executing-plans-preflight): update READMEs for v3"
```
