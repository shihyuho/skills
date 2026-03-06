# Lessons-Learned Fusion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver the approved fusion roadmap for `skills/lessons-learned` with phased risk control (P0/P1/P2), including `confidence`-based recall ranking and removal of `eval-cases`.

**Architecture:** Apply a docs-first evolution strategy. First simplify and de-duplicate runtime rules in `SKILL.md` (P0), then add `confidence` data model and ranking behavior with template/validation alignment (P1), and finally add conditional evolution mechanics (P2) without introducing heavy infrastructure.

**Tech Stack:** Markdown skill spec (`SKILL.md`), markdown references, `skills-ref` validator (`npx --yes skills-ref validate ./skills/lessons-learned`), git.

---

### Task 1: Baseline Snapshot and Safety Check

**Files:**
- Read: `skills/lessons-learned/SKILL.md`
- Read: `skills/lessons-learned/references/card-template.md`
- Read: `skills/lessons-learned/references/eval-cases.md`

**Step 1: Record current status**

Run: `git status --short`
Expected: clean or known pre-existing local changes listed.

**Step 2: Capture baseline validator result**

Run: `npx --yes skills-ref validate ./skills/lessons-learned`
Expected: `Valid skill: ./skills/lessons-learned`.

**Step 3: Document baseline evidence**

- Add baseline command output and timestamp to `progress.md`.

**Step 4: Commit baseline note (optional but recommended)**

```bash
git add progress.md
git commit -m "chore(plan): record lessons-learned baseline validation"
```

### Task 2: P0 Rule Slimming in SKILL.md

**Files:**
- Modify: `skills/lessons-learned/SKILL.md`
- Reference: `docs/plans/2026-03-04-lessons-learned-fusion-design.md`

**Step 1: Simplify related-link policy language**

- Keep only high-signal constraints: high relevance only, max 1-2 links.
- Keep broken-target handling as non-blocking warning.

**Step 2: Simplify index recovery wording**

- Keep one direct rule: missing `_index.md` with existing cards => rebuild from frontmatter.
- Keep first-run behavior explicit.

**Step 3: Remove Benchmark Targets from SKILL body**

- Delete the `## Benchmark Targets` section entirely.

**Step 4: Merge duplicated policy text**

- Consolidate duplicate expectations across Trigger/Integration/Validation areas.
- Ensure one source of truth per rule intent.

**Step 5: Validate skill syntax**

Run: `npx --yes skills-ref validate ./skills/lessons-learned`
Expected: `Valid skill: ./skills/lessons-learned`.

**Step 6: Commit P0 rule slimming**

```bash
git add skills/lessons-learned/SKILL.md
git commit -m "refactor(lessons-learned): slim and de-duplicate runtime rules"
```

### Task 3: Remove eval-cases Artifact

**Files:**
- Delete: `skills/lessons-learned/references/eval-cases.md`
- Modify (if needed): `skills/lessons-learned/SKILL.md`

**Step 1: Delete evaluation case file**

- Remove `skills/lessons-learned/references/eval-cases.md`.

**Step 2: Remove stale references**

- Search for `eval-cases.md` references in `skills/lessons-learned/`.
- Remove or update any stale pointers.

**Step 3: Re-run validator**

Run: `npx --yes skills-ref validate ./skills/lessons-learned`
Expected: `Valid skill: ./skills/lessons-learned`.

**Step 4: Commit file removal**

```bash
git add skills/lessons-learned/SKILL.md
git rm skills/lessons-learned/references/eval-cases.md
git commit -m "chore(lessons-learned): remove eval-cases reference artifact"
```

### Task 4: P1 Confidence Rules in SKILL.md

**Files:**
- Modify: `skills/lessons-learned/SKILL.md`

**Step 1: Add confidence field contract**

- Define `confidence` in card schema expectations.
- Define valid range and semantics (e.g., confidence as relevance weight).

**Step 2: Add source-based confidence initialization**

- `user-correction = 0.7`
- `bug-fix = 0.5`
- `retrospective = 0.3`

**Step 3: Update recall ranking order**

- Set ranking order to:
  `tag -> scope -> confidence(desc) -> date(desc)`.

**Step 4: Add confidence reinforcement rule**

- Keep positive update rule: useful confirmation `+0.1` with max `0.9`.

**Step 5: Validate and commit**

Run: `npx --yes skills-ref validate ./skills/lessons-learned`
Expected: valid skill output.

```bash
git add skills/lessons-learned/SKILL.md
git commit -m "feat(lessons-learned): add confidence initialization and ranking"
```

### Task 5: P1 Template and Validation Alignment

**Files:**
- Modify: `skills/lessons-learned/references/card-template.md`
- Modify: `skills/lessons-learned/SKILL.md`

**Step 1: Add confidence to card template frontmatter**

- Add `confidence: <0.1-0.9>` example field.
- Add guideline for initialization and adjustment boundaries.

**Step 2: Align validation rules**

- Ensure template checklist and SKILL validation mention the same required fields.
- Ensure confidence range and behavior are consistent in both places.

**Step 3: Run validator and manual consistency check**

Run: `npx --yes skills-ref validate ./skills/lessons-learned`
Expected: valid skill output.

Manual check:
- No conflicting range statements.
- No missing required field mismatch.

**Step 4: Commit P1 alignment**

```bash
git add skills/lessons-learned/SKILL.md skills/lessons-learned/references/card-template.md
git commit -m "docs(lessons-learned): align confidence field across template and validation"
```

### Task 6: P2 Conditional Evolution Rules

**Files:**
- Modify: `skills/lessons-learned/SKILL.md`

**Step 1: Add scope promotion policy**

- Define manual promotion path: `feature -> module -> project`.
- Add promotion trigger criteria as human-reviewed conditions.

**Step 2: Add conditional confidence decay policy**

- Document as disabled-by-default.
- Add activation condition language (only after observing low-value accumulation).
- Add decay rule example: monthly `-0.05`, lower bound `0.2`.

**Step 3: Add observability note (lightweight only)**

- Clarify no new CLI subsystem, no daemon, no background hooks.

**Step 4: Validate and commit**

Run: `npx --yes skills-ref validate ./skills/lessons-learned`
Expected: valid skill output.

```bash
git add skills/lessons-learned/SKILL.md
git commit -m "feat(lessons-learned): add conditional evolution policies"
```

### Task 7: Final Verification and Handoff Notes

**Files:**
- Modify: `progress.md`
- Optional update: `findings.md`

**Step 1: Run final verification suite**

Run:

```bash
npx --yes skills-ref validate ./skills/lessons-learned && git status --short
```

Expected:
- skill validator passes
- git status shows only intended changes

**Step 2: Verify acceptance checklist**

- SKILL reduced and de-duplicated
- confidence rules traceable in recall ordering
- template and validation synchronized
- no heavy infra introduced
- `eval-cases.md` removed as approved

**Step 3: Write execution summary**

- Update `progress.md` with completed tasks and verification outputs.
- Add any reusable lesson candidates for post-task capture.

**Step 4: Commit handoff documentation**

```bash
git add progress.md findings.md
git commit -m "docs: record lessons-learned fusion rollout verification"
```

## Risks and Mitigations

1. **Risk:** Removing too much detail in P0 makes behavior ambiguous.
   **Mitigation:** Keep explicit examples where ambiguity could occur; validate with skills-ref after each edit.

2. **Risk:** Confidence semantics differ between SKILL and template.
   **Mitigation:** Single alignment task (Task 5) with explicit manual consistency check.

3. **Risk:** P2 rules are interpreted as mandatory immediately.
   **Mitigation:** Mark decay as disabled-by-default and activation-gated in wording.

## Definition of Done

- `skills/lessons-learned/SKILL.md` implements P0/P1/P2 approved design.
- `skills/lessons-learned/references/card-template.md` includes `confidence` and aligned validation guidance.
- `skills/lessons-learned/references/eval-cases.md` is removed.
- `npx --yes skills-ref validate ./skills/lessons-learned` passes at final state.
- Progress evidence is recorded in `progress.md`.
