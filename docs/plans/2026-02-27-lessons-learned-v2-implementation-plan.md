# Lessons-Learned v2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade `skills/lessons-learned/` into a contract-first, Zettelkasten-based self-improvement skill with selective wikilinking and measurable quality benchmarks.

**Architecture:** Keep markdown-native storage (`docs/lessons/_index.md` + atomic cards), strengthen trigger/workflow contracts in `SKILL.md`, expand card schema with `related` links, and add explicit validation artifacts for trigger/capture/recall/linking quality. Do not modify `workflow-orchestration` in this iteration.

**Tech Stack:** Markdown docs, Agent Skills format (`SKILL.md` + `references/` + optional `README.md`), `skills-ref` validator.

---

### Task 1: Establish Baseline and Validation Inputs

**Files:**
- Modify: `skills/lessons-learned/SKILL.md`
- Create: `skills/lessons-learned/references/eval-cases.md`

**Step 1: Capture current trigger contract and workflow sections**

- Read `skills/lessons-learned/SKILL.md` and map current sections into: Trigger, Recall, Capture, Integration, Extensions.

**Step 2: Write evaluation scenario set (12 prompts)**

- Create `skills/lessons-learned/references/eval-cases.md` with:
  - 3 task-start recall prompts
  - 3 user-correction capture prompts
  - 3 task-end capture-worthiness prompts
  - 3 non-trigger prompts

**Step 3: Define scoring rubric**

- In the same file, add precision/recall evaluation rubric and pass thresholds from design doc.

**Step 4: Commit**

```bash
git add skills/lessons-learned/SKILL.md skills/lessons-learned/references/eval-cases.md
git commit -m "docs(lessons-learned): add trigger evaluation cases"
```

### Task 2: Refactor SKILL.md into Contract-First Structure

**Files:**
- Modify: `skills/lessons-learned/SKILL.md`

**Step 1: Rewrite top-level sections**

- Ensure order is:
  1. Trigger Contract
  2. Recall Phase
  3. Capture Phase
  4. Linking Rule
  5. Validation
  6. Integration Guide

**Step 2: Implement index-recovery behavior**

- Add deterministic rule:
  - Missing `_index.md` + no cards => first-run skip recall
  - Missing `_index.md` + existing cards => rebuild index then continue recall

**Step 3: Add token bounds and deterministic limits**

- Hard cap recall to 5 cards (1-3 primary + up to 2 related).

**Step 4: Add negative trigger examples**

- Document at least 3 explicit non-trigger situations.

**Step 5: Validate style consistency**

- Verify imperative tone, explicit MUST/NEVER usage only for true invariants.

**Step 6: Commit**

```bash
git add skills/lessons-learned/SKILL.md
git commit -m "refactor(lessons-learned): tighten trigger and workflow contracts"
```

### Task 3: Extend Card Template for Selective Wikilinks

**Files:**
- Modify: `skills/lessons-learned/references/card-template.md`

**Step 1: Add `related` field to frontmatter template**

- Add `related: []` default and examples with `[[card-id]]` format.

**Step 2: Add guidance for high-value linking gate**

- In template notes, state: create `related` only when 2-of-4 high-value criteria are met.

**Step 3: Add anti-noise constraints**

- Maximum 3 related links per card.

**Step 4: Commit**

```bash
git add skills/lessons-learned/references/card-template.md
git commit -m "docs(lessons-learned): add related-link metadata to card template"
```

### Task 4: Add Linking Heuristics Reference

**Files:**
- Create: `skills/lessons-learned/references/linking-heuristics.md`

**Step 1: Document 2-of-4 high-value criteria**

- Criteria:
  - Cross-task reusability
  - High-cost mistake
  - Critical parameter/decision dependency
  - Connects to >=2 existing cards

**Step 2: Define link suggestion algorithm (docs-level)**

- Suggested deterministic order:
  1. Candidate set by tag overlap
  2. Tie-break by keyword overlap
  3. Keep top 3

**Step 3: Define broken-link handling**

- Missing related target => ignore and warn; do not block recall.

**Step 4: Commit**

```bash
git add skills/lessons-learned/references/linking-heuristics.md
git commit -m "docs(lessons-learned): add selective wikilink heuristics"
```

### Task 5: Add/Align Human README for Discoverability

**Files:**
- Create: `skills/lessons-learned/README.md`

**Step 1: Write value-first README structure**

- Sections:
  - Problem
  - What the skill does
  - Trigger examples
  - Capture/Recall lifecycle
  - Quick examples

**Step 2: Ensure README behavior matches SKILL.md**

- No contradictory workflow, no hidden rules.

**Step 3: Add realistic trigger utterances**

- Include at least 3 user phrases mapping to each trigger type.

**Step 4: Commit**

```bash
git add skills/lessons-learned/README.md
git commit -m "docs(lessons-learned): add human-facing README"
```

### Task 6: Validate and Record Evidence

**Files:**
- Modify: `skills/lessons-learned/SKILL.md`
- Modify: `skills/lessons-learned/references/eval-cases.md`

**Step 1: Run skills validator**

Run:

```bash
npx --yes skills-ref validate ./skills/lessons-learned
```

Expected:

- Validation passes with no schema/frontmatter errors.

**Step 2: Execute manual trigger benchmark pass**

- Run through 12 prompts in `references/eval-cases.md`.
- Record outcomes and precision score in the same file.

**Step 3: Verify linking quality gate**

- Confirm examples satisfy:
  - Related-link creation rate >= 0.8 when criteria met
  - Broken related-link rate = 0 in examples/fixtures

**Step 4: Final commit**

```bash
git add skills/lessons-learned/SKILL.md skills/lessons-learned/references/eval-cases.md
git commit -m "chore(lessons-learned): validate v2 quality gates"
```

### Task 7: Final Review and Handoff

**Files:**
- Review: `docs/plans/2026-02-27-lessons-learned-v2-design.md`
- Review: `skills/lessons-learned/`

**Step 1: Cross-check against design doc acceptance criteria**

- Ensure all design constraints are represented in docs.

**Step 2: Ensure out-of-scope boundaries respected**

- Confirm `workflow-orchestration` unchanged.

**Step 3: Prepare PR summary draft**

- Summarize: trigger contract improvements, linking heuristics, validation evidence.
