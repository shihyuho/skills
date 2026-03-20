# Lessons Learned Confidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `lessons-learned` so `confidence` means application strength, `0.0` exits normal recall, canonical confidence levels are documented, and capture reporting includes confidence transitions.

**Architecture:** Keep this as a documentation-first change inside the existing `skills/lessons-learned` package. The implementation updates the canonical rules in `SKILL.md`, aligns supporting guidance in `references/card-template.md` and `README.md`, and verifies the published skill package still validates with `skills-ref`.

**Tech Stack:** Markdown, skill package validation via `npx --yes skills-ref validate`

---

## File Structure

- Modify: `skills/lessons-learned/SKILL.md` — canonical behavior for confidence semantics, recall filtering, capture/update rules, and capture reporting
- Modify: `skills/lessons-learned/references/card-template.md` — card template guidance for canonical confidence levels and reporting-aligned defaults
- Modify: `skills/lessons-learned/README.md` — user-facing explanation aligned with the new confidence model
- Reference only: `docs/superpowers/specs/2026-03-20-lessons-learned-confidence-design.md` — approved source of truth for planning

### Task 1: Update Canonical Skill Rules

**Files:**
- Modify: `skills/lessons-learned/SKILL.md`
- Reference: `docs/superpowers/specs/2026-03-20-lessons-learned-confidence-design.md`

- [ ] **Step 1: Read the confidence-related sections that need replacement**

Read these sections in `skills/lessons-learned/SKILL.md`:
- Trigger-adjacent recall rules
- `Recall Phase`
- `Step 2 — Write the Zettel card`
- `Step 4 — Confirm with user`
- `Validation`

Expected: identify every sentence that still treats `confidence` as a generic ranking number or free-form `+0.1` adjustment.

- [ ] **Step 2: Rewrite confidence semantics in the canonical spec file**

Update `skills/lessons-learned/SKILL.md` so it states:
- `confidence` means application strength, not objective truth
- canonical values are `0.0`, `0.3`, `0.5`, `0.7`, `0.9`
- untouched legacy non-canonical values are tolerated temporarily
- edited legacy values normalize to the nearest canonical value, ties round downward
- no bulk migration is required

- [ ] **Step 3: Update recall behavior**

Edit the `Recall Phase` to say:
- cards with `confidence: 0.0` do not participate in normal recall
- remaining cards still rank by `tag match -> scope match -> confidence (desc) -> date (desc)`
- `confidence: 0.0` cards remain available only for explicit inactive-lesson lookup

- [ ] **Step 4: Replace free-form confidence adjustment rules**

In `Step 2 — Write the Zettel card`, replace the current `+0.1` language with canonical transition rules:
- new cards keep `source -> confidence` defaults (`0.7`, `0.5`, `0.3`)
- updates choose the canonical value that best matches the new evidence
- small changes usually move one level
- stronger evidence may move multiple levels
- lessons that should leave normal recall move directly to `0.0`

- [ ] **Step 5: Add capture reporting requirements**

Update `Step 4 — Confirm with user` so capture reports include confidence transitions when confidence changes:
- updated cards report `<old>-><new> + reason`
- new cards report `none-><new>`
- `0.0` transitions explicitly say the card is excluded from normal recall
- update the old capture report example near `skills/lessons-learned/SKILL.md:177` so it reflects confidence transition reporting

- [ ] **Step 6: Update field descriptions that still use the old meaning**

Edit the card field table in `skills/lessons-learned/SKILL.md` so the `confidence` row describes application strength and no longer describes confidence as only a generic ranking number.

- [ ] **Step 7: Align validation bullets**

Update the `Validation` section to check:
- `confidence` stays within `0.0-0.9`
- new and edited cards use canonical values only
- `0.0` cards are excluded from normal recall
- capture reporting rules mention confidence transitions where applicable
- recall limits stay unchanged and this iteration does not add archive directories or time-based decay

- [ ] **Step 8: Review the edited skill for contradictions**

Read `skills/lessons-learned/SKILL.md` end-to-end after editing.

Expected: no remaining references to `+0.1` adjustments, no contradictions between `Recall Phase`, `Capture Phase`, and `Validation`.

### Task 2: Align Supporting Documentation

**Files:**
- Modify: `skills/lessons-learned/references/card-template.md`
- Modify: `skills/lessons-learned/README.md`
- Reference: `skills/lessons-learned/SKILL.md`

- [ ] **Step 1: Update the card template confidence guidance**

Revise `skills/lessons-learned/references/card-template.md` to match the canonical rules:
- `confidence` means application strength
- new cards initialize from `source -> confidence`
- new and edited cards use canonical values only
- remove `+0.1` guidance
- mention `0.0` as inactive for normal recall

- [ ] **Step 2: Update the template validation checklist**

Adjust the checklist in `skills/lessons-learned/references/card-template.md` to reflect:
- canonical confidence values for new/edited cards
- `confidence` still ranges `0.0-0.9`
- no contradictory `+0.1` language remains

- [ ] **Step 3: Refresh the README explanation**

Update `skills/lessons-learned/README.md` so the high-level description matches the new model:
- confidence prioritizes how strongly a lesson should be applied
- inactive lessons (`0.0`) do not join normal recall
- confidence changes can happen when usage evidence strengthens or weakens a lesson

- [ ] **Step 4: Review for cross-file consistency**

Read these files together:
- `skills/lessons-learned/SKILL.md`
- `skills/lessons-learned/references/card-template.md`
- `skills/lessons-learned/README.md`

Expected: the same confidence vocabulary appears across all three files, and no support file contradicts the canonical `SKILL.md` rules.

### Task 3: Validate the Skill Package

**Files:**
- Validate: `skills/lessons-learned/`

- [ ] **Step 1: Run skill validation**

Run: `npx --yes skills-ref validate skills/lessons-learned`

Expected: validation passes for the updated skill package.

- [ ] **Step 2: If validation fails, fix the documented cause**

Address only the reported issue in:
- `skills/lessons-learned/SKILL.md`
- `skills/lessons-learned/references/card-template.md`
- `skills/lessons-learned/README.md`

Then rerun:
`npx --yes skills-ref validate skills/lessons-learned`

Expected: validation passes cleanly.

- [ ] **Step 3: Sanity-check the final diff**

Review the diff for the touched files and confirm it reflects the approved spec only.

Expected: no accidental changes outside the `lessons-learned` skill package and its planning artifact.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/2026-03-20-lessons-learned-confidence-implementation.md skills/lessons-learned/SKILL.md skills/lessons-learned/references/card-template.md skills/lessons-learned/README.md
git commit -m "docs(lessons-learned): align confidence model with application strength"
```

Expected: one commit containing the documentation and skill-spec updates.

## Verification Checklist

- `skills/lessons-learned/SKILL.md` defines `confidence` as application strength
- `skills/lessons-learned/SKILL.md` excludes `confidence: 0.0` from normal recall
- `skills/lessons-learned/SKILL.md` replaces `+0.1` language with canonical transitions
- `skills/lessons-learned/references/card-template.md` matches the new canonical confidence model
- `skills/lessons-learned/README.md` reflects the same semantics at a high level
- `npx --yes skills-ref validate skills/lessons-learned` passes
