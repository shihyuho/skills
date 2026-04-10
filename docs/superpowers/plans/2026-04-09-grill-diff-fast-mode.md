# grill-diff Fast Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a multi-strategy fast mode to grill-diff that auto-advances clean files and grills the user only when issues are found.

**Architecture:** Modify the existing grill-diff skill (prompt-based, no code). SKILL.md gets rewritten to include mode selection, strategy toolbox, and fast mode flow. README.md updated to document new usage.

**Tech Stack:** Markdown (prompt engineering). No runtime code.

**Prerequisite:** Before modifying SKILL.md, invoke `skill-creator` and `write-a-skill` skills to load current authoring guidelines (per AGENTS.md global constraint).

---

## File Structure

- Modify: `skills/grill-diff/SKILL.md` — core skill instructions, currently 19 lines
- Modify: `skills/grill-diff/README.md` — user-facing documentation, currently 31 lines

---

### Task 1: Rewrite SKILL.md — Mode Selection & Diff Scope

**Files:**
- Modify: `skills/grill-diff/SKILL.md`

- [ ] **Step 1: Invoke skill-creator and write-a-skill**

Run both skills to load current authoring guidelines before making changes.

- [ ] **Step 2: Rewrite frontmatter and description**

Update the SKILL.md frontmatter to reflect both modes:

```yaml
---
name: grill-diff
description: Review git changed files using deep interactive grilling or fast multi-strategy self-review. Deep mode interrogates every aspect of each change one question at a time. Fast mode applies multiple reviewer personas internally, only stopping for interaction when issues are found.
---
```

- [ ] **Step 3: Write mode selection logic**

Replace the current opening instruction with mode selection:

```markdown
Determine the review mode:
- If the user clearly indicates fast (e.g. "快速掃", "fast"), use fast mode.
- If the user clearly indicates deep (e.g. "仔細烤", "grill", "deep"), use deep mode.
- If ambiguous (including bare /grill-diff with no modifier), ask the user which mode they want.
```

- [ ] **Step 4: Write diff scope as two independent dimensions**

Replace the current 4-item scope list with two dimensions:

```markdown
Determine the diff scope along two independent dimensions:

**File scope** (which files to review):
- If the user explicitly lists file paths, review only those files.
- Otherwise, review all changed files.

**Diff baseline** (what to compare against, in priority order):
1. If there are staged changes, use those (git diff --cached).
2. Otherwise, if there are unstaged changes, use those (git diff).
3. If the user specifies a branch (e.g. "against develop"), diff against that branch.
4. If the user provides a PR URL, use that.
5. Otherwise, diff the current branch against the default branch.

These combine: e.g. "fast against develop src/auth.ts" reviews only src/auth.ts diffed against develop.
```

- [ ] **Step 5: Commit**

```bash
git add skills/grill-diff/SKILL.md
git commit -m "feat(grill-diff): add mode selection and two-dimension diff scope"
```

---

### Task 2: Add Strategy Toolbox to SKILL.md

**Files:**
- Modify: `skills/grill-diff/SKILL.md`

- [ ] **Step 1: Write the strategy toolbox section**

Add after the diff scope section. The wording must emphasize genuine question switching — not going through the motions:

```markdown
## Strategy Toolbox

When running fast mode, select at least 3 of these reviewer personas per file. The value of multiple strategies is forcing yourself to ask genuinely different questions about the same code — each persona triggers a different reasoning path. Do not go through the motions. Switch your line of questioning completely between strategies.

| ID | Persona | Core Question |
|----|---------|---------------|
| verify | 正向驗證 — Developer | 「這段 code 說要做 X，它真的做到了嗎？」 |
| nitpick | 挑毛病 — Skeptic | 「這裡一定有 bug，在哪？」 |
| newcomer | 新人視角 — Junior engineer | 「我第一次看這段，我看得懂嗎？」 |
| attacker | 攻擊者 — Red team | 「我要怎麼讓這段 code 壞掉？」 |
| revert | 刪除挑戰 — Minimalist | 「把這個改動 revert 掉，什麼會壞？」 |
| maintainer | 維護者未來視角 — You in 6 months | 「半年後改這段的人會罵什麼？」 |
| senior | Review 老手 — Senior reviewer | 「PR review 我會問什麼？」 |

Selection guidance (not hard rules):
- verify: relevant for almost every file.
- attacker: prioritize for files handling user input, auth, APIs.
- newcomer: prioritize for complex logic, new modules.
- revert: prioritize for files with many scattered changes.
- The rest: your judgment based on the file.

This list may evolve — strategies can be added, merged, or removed based on effectiveness.
```

- [ ] **Step 2: Commit**

```bash
git add skills/grill-diff/SKILL.md
git commit -m "feat(grill-diff): add strategy toolbox with 7 reviewer personas"
```

---

### Task 3: Add Fast Mode Flow to SKILL.md

**Files:**
- Modify: `skills/grill-diff/SKILL.md`

- [ ] **Step 1: Write the fast mode flow section**

Add after the strategy toolbox:

```markdown
## Fast Mode Flow

Ask if there is a related spec or plan file (same as deep mode). If provided, use it as background knowledge for all strategy personas.

Read all changed files first to build the full picture before starting per-file review.

For each changed file:

1. Pick 3+ strategies appropriate for this file. Output your selection with a short rationale:
   src/auth.ts → verify, attacker, revert (handles auth + scattered changes)

2. Run each strategy as a complete review pass. Genuinely switch your line of questioning — the core question for each persona should drive a different analysis, not a rephrased version of the same one.

3. Output results. Compress clean files to one line:
   ✓ src/api.ts — verify, attacker, newcomer: all clean
   Expand files with issues:
   src/auth.ts → verify, attacker, revert (handles auth + scattered changes)
   verify: clean
   attacker: ⚠️ token validation can be bypassed with empty string
   revert: clean

4. All clean → auto-advance to next file.

5. Any issue found → enter grill mode: interrogate the user one question at a time, probing every aspect of the finding until shared understanding is reached. When multiple findings exist across strategies, address them in whatever order is most natural. Then continue to next file.

If a spec/plan was provided, flag changes that obviously contradict the spec or large modifications with no spec coverage. Small related refactoring (renaming, formatting) is acceptable — do not over-report.

If a question can be answered by exploring the codebase, specs, or tests, explore them yourself instead of asking.

Flag any change that isn't required to achieve the stated goal. Probe: "What breaks if we revert this?"
```

- [ ] **Step 2: Commit**

```bash
git add skills/grill-diff/SKILL.md
git commit -m "feat(grill-diff): add fast mode flow with multi-strategy self-review"
```

---

### Task 4: Preserve Deep Mode Section in SKILL.md

**Files:**
- Modify: `skills/grill-diff/SKILL.md`

- [ ] **Step 1: Add deep mode section**

Add after the fast mode flow. This preserves the current grill-diff behavior as a named mode:

```markdown
## Deep Mode

Review changed files one by one. For each file, interrogate every aspect of the diff — one question at a time — until reaching shared understanding before moving to the next file.

Ask if there is a related spec or plan file to understand the goal of the changes. Read through all changed files to understand the full picture, then go through the files one at a time.

If a question can be answered by exploring the codebase, specs, or tests, explore them yourself instead of asking.

Flag any change that isn't required to achieve the stated goal. Probe: "What breaks if we revert this?"
```

- [ ] **Step 2: Review the complete SKILL.md**

Read the full SKILL.md top to bottom. Verify:
- Mode selection is at the top
- Diff scope follows
- Strategy toolbox follows
- Fast mode flow follows
- Deep mode follows
- No duplication between sections
- No contradictions

- [ ] **Step 3: Commit**

```bash
git add skills/grill-diff/SKILL.md
git commit -m "feat(grill-diff): add deep mode section preserving current behavior"
```

---

### Task 5: Update README.md

**Files:**
- Modify: `skills/grill-diff/README.md`

- [ ] **Step 1: Rewrite README.md**

Update to document both modes:

```markdown
# grill-diff

Review git changes using deep interactive grilling or fast multi-strategy self-review.

## Modes

- **Fast mode** — Agent applies multiple reviewer personas internally per file. Clean files are auto-advanced. Issues trigger interactive grilling.
- **Deep mode** — File-by-file interactive interrogation of every aspect (original grill-diff behavior).

## How It Works

1. **Select mode** — fast or deep. If not specified, you'll be asked.
2. **Determine diff scope** — staged changes > unstaged changes > specified branch > PR URL > default branch. Optionally specify files to narrow scope.
3. **Gather context** — asks if there is a related spec or plan file.
4. **Read all changed files** — builds the full picture before starting.
5. **Review file by file:**
   - **Fast:** Agent self-reviews with 3+ strategy personas, shows results. Clean → next. Issue → grill mode.
   - **Deep:** Asks one question at a time about every aspect of each change.
6. **Flag unnecessary changes** — challenges any change not required by the stated goal.

## Usage

```
/grill-diff
/grill-diff fast
/grill-diff deep
```

Against a specific target:

```
/grill-diff fast against develop
/grill-diff deep against develop
```

Narrow to specific files:

```
/grill-diff fast src/auth.ts src/api.ts
/grill-diff fast against develop src/auth.ts
```

Review a pull request:

```
/grill-diff fast https://github.com/org/repo/pull/123
```

## Installation

```bash
npx skills add shihyuho/skills --skill=grill-diff
```
```

- [ ] **Step 2: Commit**

```bash
git add skills/grill-diff/README.md
git commit -m "docs(grill-diff): update README for fast/deep modes"
```

---

### Task 6: Verify & Update Project README

**Files:**
- Modify: `README.md` (project root, if grill-diff description needs updating)

- [ ] **Step 1: Check project root README.md**

Read the project root `README.md` and check if the grill-diff description needs updating to mention fast mode. Per AGENTS.md: "If you add, remove, or rename anything under `skills/` or `commands/`, update the corresponding lists in `README.md` in the same change." This is a modification, not an add/remove/rename, so only update if the description is inaccurate.

- [ ] **Step 2: Update if needed and commit**

If the description needs updating:

```bash
git add README.md
git commit -m "docs: update grill-diff description in project README"
```

If no update needed, skip this step.

---

### Task 7: Manual Testing

- [ ] **Step 1: Test fast mode**

Run `/grill-diff fast` on a branch with known changes. Verify:
- Mode selection works (fast is recognized)
- Strategy selection is shown with rationale
- Clean files are compressed to one line
- Files with issues enter grill mode

- [ ] **Step 2: Test deep mode**

Run `/grill-diff deep` on the same branch. Verify current behavior is unchanged.

- [ ] **Step 3: Test ambiguous invocation**

Run bare `/grill-diff`. Verify it asks which mode to use.

- [ ] **Step 4: Test file scope + branch combination**

Run `/grill-diff fast against main src/some-file.ts`. Verify both dimensions work together.
