# PR #12 Follow-up Issue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create one GitHub tracking issue that captures the reviewed PR #12 follow-up findings and starts a concrete discussion about fix order and contract alignment.

**Architecture:** Build the issue body from the approved spec, verify the referenced files and findings still match the repository, then create a single GitHub issue with a discussion-oriented structure. The work stays documentation-only: no source files are modified as part of issue creation.

**Tech Stack:** GitHub CLI (`gh`), Markdown issue body, repository docs under `docs/superpowers/`

---

### Task 1: Verify the evidence that will be cited in the issue

**Files:**
- Read: `docs/superpowers/specs/2026-03-18-pr12-followup-issue-design.md`
- Read: `skills/ultrabrain/SKILL.md`
- Read: `commands/ultrabrain-recall.md`
- Read: `commands/ultrabrain-groom.md`
- Read: `evals/ultrabrain-evals.json`
- Read: `evals/scripts/check_ultrabrain_thin_card.py`

- [ ] **Step 1: Re-read the approved spec**

Read: `docs/superpowers/specs/2026-03-18-pr12-followup-issue-design.md`
Expected: Clear issue structure, findings, and proposed discussion questions.

- [ ] **Step 2: Re-check the canonical contract in the skill**

Read: `skills/ultrabrain/SKILL.md`
Expected: Confirm staged recall, map taxonomy, thin-card rewrite-first rules, and source-note provenance-only rules are still present.

- [ ] **Step 3: Re-check downstream artifacts cited in findings**

Read: `commands/ultrabrain-recall.md`, `commands/ultrabrain-groom.md`, `evals/ultrabrain-evals.json`, and `evals/scripts/check_ultrabrain_thin_card.py`.
Expected: Evidence still matches the planned issue body.

- [ ] **Step 4: Note any wording changes needed before issue creation**

Update the draft issue wording if any current file content is more nuanced than the original review summary.

### Task 2: Draft the issue body as a standalone Markdown artifact

**Files:**
- Create: `docs/superpowers/issues/`
- Create: `docs/superpowers/issues/2026-03-18-pr12-followup-tracking.md`
- Reference: `docs/superpowers/specs/2026-03-18-pr12-followup-issue-design.md`

- [ ] **Step 1: Create the issue draft directory**

Run:

```bash
mkdir -p "docs/superpowers/issues"
```

Expected: `docs/superpowers/issues/` exists and is ready for the draft file.

- [ ] **Step 2: Create the issue draft file**

Write a Markdown issue body with these sections:

```md
## Summary
## Findings
### High priority
### Medium priority
## Proposed Discussion Questions
## Recommended Fix Order
```

- [ ] **Step 3: Fill in the five findings with evidence-backed wording**

For each finding, include:

- the concrete mismatch or risk
- why it matters
- whether it is a confirmed inconsistency, validation gap, regression risk, or open decision
- a short evidence list with exact file paths

- [ ] **Step 4: Keep open questions separate from confirmed inconsistencies**

Use explicit wording such as:

- `Confirmed inconsistency:` when files clearly disagree
- `Open decision:` when canonical behavior is still not fully settled

- [ ] **Step 5: Add the discussion questions as their own section**

Create a dedicated `## Proposed Discussion Questions` section with these three questions:

1. Is `skills/ultrabrain/SKILL.md` the canonical source of truth for post-PR #12 behavior when `commands/` or `evals/` disagree?
2. Should `decision=skip` be added to the canonical capture contract, or should eval 8 be narrowed to the existing decision set?
3. Should fixes land in one follow-up PR or as a small ordered sequence of PRs?

- [ ] **Step 6: Add the recommended fix order as a separate section**

Create a dedicated `## Recommended Fix Order` section with this four-step sequence:

1. clarify the canonical contract where it is still ambiguous
2. update `evals/ultrabrain-evals.json` to match that contract
3. update `commands/` files so invocation guidance matches the skill
4. tighten machine checks such as `evals/scripts/check_ultrabrain_thin_card.py`

Do not collapse this section into general discussion prompts.

### Task 3: Create the GitHub issue from the draft

**Files:**
- Read: `docs/superpowers/issues/2026-03-18-pr12-followup-tracking.md`

- [ ] **Step 1: Review the final draft once before posting**

Read: `docs/superpowers/issues/2026-03-18-pr12-followup-tracking.md`
Expected: No placeholders, no unsupported claims, no implementation scope creep.

- [ ] **Step 2: Create the issue with GitHub CLI**

Run:

```bash
gh issue create --title "track PR #12 follow-up inconsistencies and fix order" --body-file "docs/superpowers/issues/2026-03-18-pr12-followup-tracking.md"
```

Expected: CLI returns a new GitHub issue URL.

- [ ] **Step 3: Capture the resulting issue URL**

Record the issue number and URL in the session response so the user can open it directly.

### Task 4: Start the discussion with a concise synthesis

**Files:**
- Read: `docs/superpowers/issues/2026-03-18-pr12-followup-tracking.md`

- [ ] **Step 1: Prepare the initial discussion stance**

Use this position in the user-facing response after issue creation:

- canonical skill contract should be clarified first
- evals should be aligned next
- commands and helper checks should follow

- [ ] **Step 2: Present the recommended first three fixes**

List these likely first moves in the user-facing response as a discussion starter, while keeping the issue body's four-step fix order intact:

1. decide whether `decision=skip` belongs in the canonical capture contract
2. fix eval 4 taxonomy mismatch to match the agreed contract
3. update `commands/ultrabrain-recall.md` wording to better reflect staged recall

- [ ] **Step 3: Ask whether to proceed from discussion into code fixes**

After the issue is created, ask the user which decision they want to make next:

- settle the canonical contract first
- split follow-up work into separate issues or PRs
- or choose the first concrete fix to implement

### Task 5: Verify completion

**Files:**
- Read: `docs/superpowers/issues/2026-03-18-pr12-followup-tracking.md`

- [ ] **Step 1: Confirm issue was created successfully**

Expected: A valid GitHub issue URL exists.

- [ ] **Step 2: Confirm the posted issue matches the spec**

Check that the issue contains:

- one tracking issue only
- all five findings
- `## Proposed Discussion Questions` with the three planned questions
- `## Recommended Fix Order` with the four planned steps in spec order

- [ ] **Step 3: Report back with the URL and next discussion options**

Return the issue URL and the recommended next decision point for follow-up work.
