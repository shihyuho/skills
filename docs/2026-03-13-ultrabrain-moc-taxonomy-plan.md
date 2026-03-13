# UltraBrain MOC Taxonomy Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `skills/ultrabrain/SKILL.md` so its map taxonomy is defined in `Core Model`, its navigation rules stay in `Map Structure`, and its maintenance guidance in `MOC Grooming` becomes map-class specific without preserving a separate troubleshooting class.

**Architecture:** Keep the current `ultrabrain` storage model and recall workflow, but refactor the documentation structure around a shared taxonomy. Add `Map Classes` to `Core Model`, simplify `Map Structure` into navigation rules, and rewrite `MOC Grooming` by map class so `domain maps`, `lessons-moc`, `general-moc`, and `review lenses` stop competing for the same conceptual role.

**Tech Stack:** Markdown skill package, `skills-ref` validator

---

## Chunk 1: Establish Shared Taxonomy

### Task 1: Define map classes in Core Model

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`
- Reference: `docs/2026-03-13-ultrabrain-moc-taxonomy-design.md`

- [ ] Add a `Map Classes` subsection under `Core Model`.
- [ ] Define `home` as the entry page and define `domain maps`, `lessons-moc`, `general-moc`, and `review lenses` as the key map classes.
- [ ] Explicitly state that `domain maps`, `lessons-moc`, and `general-moc` form the default recall path.
- [ ] State that `review lenses` are views over knowledge, not canonical homes for it.

### Task 2: Align terminology around default recall paths

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] Add wording that `domain maps`, `lessons-moc`, and `general-moc` are the default recall path.
- [ ] Add wording that `review lenses` are conditional views used only when the task context calls for them.
- [ ] Remove or rewrite any line that implies all maps are equivalent first-pass navigation pages.

## Chunk 2: Refactor Navigation Sections

### Task 3: Narrow Map Structure to navigation relationships

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] Rewrite `Map Structure` so it describes navigation flow rather than re-defining taxonomy.
- [ ] Express the default navigation as `home -> relevant map -> cards`.
- [ ] Clarify that review lenses can link to existing cards or maps without becoming the primary home of those cards.
- [ ] Keep examples, but ensure they reinforce role differences instead of flattening everything into one list.

### Task 4: Re-anchor Recall Workflow to the new taxonomy

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] Update `Map recall` wording so map choice follows the new taxonomy.
- [ ] Route debugging-style tasks to the relevant domain map rather than a separate troubleshooting class.
- [ ] Keep review lenses restricted to provenance review or uncertainty review.
- [ ] Preserve the existing gap-driven planning loop while making the map-priority rules clearer.

## Chunk 3: Rewrite MOC Grooming By Map Class

### Task 5: Replace generic grooming rules with class-specific rules

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] Rewrite `MOC Grooming` into separate subsections for `home`, `default recall maps`, and `review lenses`.
- [ ] For `home`, focus on clarity, scanability, and resisting content sprawl.
- [ ] For `default recall maps`, focus on boundary hygiene, duplicate-entry reduction, and stable recall paths.
- [ ] For `review lenses`, focus on preserving audit value without displacing primary navigation.

### Task 6: Keep split/create/update guidance consistent with the new classes

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] Re-home any generic create/update/split rules under the most appropriate map-class subsection.
- [ ] Make sure the guidance still supports manual-trigger grooming rather than automatic restructuring after every capture.
- [ ] Ensure the wording does not imply that every map class should be split or expanded using the same thresholds.

## Chunk 4: Verify Consistency

### Task 7: Re-read the full skill for conceptual consistency

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] Check that `Core Model`, `Map Structure`, `Recall Workflow`, and `MOC Grooming` now use one shared taxonomy.
- [ ] Check that `lessons-moc`, `general-moc`, and domain maps remain the default recall path everywhere they are referenced.
- [ ] Check that review lenses remain clearly secondary in all sections.

### Task 8: Validate the skill package

**Files:**
- Verify: `skills/ultrabrain/SKILL.md`

- [ ] Run `npx --yes skills-ref validate skills/ultrabrain`.
- [ ] If validation fails, fix the wording or structure and rerun the same command.
- [ ] Summarize which conceptual ambiguities were removed by the taxonomy rewrite.
