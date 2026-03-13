# UltraBrain Skill Strengthening Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `skills/ultrabrain/SKILL.md` so the skill produces more self-contained cards, treats source notes strictly as provenance, and repositions lens maps as review-oriented rather than primary recall navigation.

**Architecture:** Keep the current UltraBrain structure and workflow, but refine the instruction language in the card, source-note, and recall sections. Introduce a two-layer quality model: a universal self-contained rule for all cards, plus stronger guidance for reusable lessons and heuristics. Reframe `by-source-moc` and `by-confidence-moc` as optional review lenses instead of first-class recall entry points.

**Tech Stack:** Markdown skill package, `skills-ref` validator, repo documentation files

---

## Chunk 1: Refine Core Skill Rules

### Task 1: Add universal card self-contained guidance

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`
- Reference: `docs/2026-03-12-ultrabrain-skill-design.md`

- [ ] Add a new rule in the card section defining the minimum self-contained standard for all cards.
- [ ] Add explicit wording that short cards are acceptable, but thin cards are not.
- [ ] State that concise cards are acceptable, but cards must remain understandable without reading the source note.
- [ ] Explicitly forbid hiding critical context, definitions, or applicability only in the source layer.

### Task 2: Add stronger guidance for reusable lessons

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`
- Reference: `docs/2026-03-12-ultrabrain-first-round-review.md`

- [ ] Add a small subsection for reusable lessons, decision rules, and heuristics.
- [ ] Instruct the skill to include the rule, the triggering context, and when to apply it.
- [ ] Keep this guidance lightweight so non-lesson cards do not become rigid templates.

## Chunk 2: Tighten Source And Recall Boundaries

### Task 3: Clarify source note non-goals

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] In the source note section, add explicit wording that source notes do not compensate for incomplete cards.
- [ ] Add a reverse check near the source-note creation criteria: if a card needs the source to be understandable, improve the card before deciding to keep the source.
- [ ] Preserve the existing provenance-first model and avoid turning source notes into archives.
- [ ] Review the source-note template wording so it still reads as provenance support rather than a background-dump destination.

### Task 4: Reposition lens maps as review lenses

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] Update every place where lens maps are framed: the default map list, the lens map definitions, and the recall workflow.
- [ ] Make `by-source-moc` and `by-confidence-moc` read as optional review pages.
- [ ] Avoid language that makes them feel like default first-pass navigation alongside `home`, domain MOCs, and `lessons-moc`.
- [ ] Add a brief explanation of when these review lenses are useful.

## Chunk 3: Validate And Document

### Task 5: Re-read the full skill for consistency

**Files:**
- Modify: `skills/ultrabrain/SKILL.md`

- [ ] Check for contradictions between card rules, capture flow, source-note rules, and recall workflow.
- [ ] Ensure the new wording strengthens existing behavior instead of changing the whole skill model.

### Task 6: Validate the skill package

**Files:**
- Verify: `skills/ultrabrain/SKILL.md`

- [ ] Run `npx --yes skills-ref validate skills/ultrabrain`.
- [ ] If validation fails, fix the skill and rerun the same command.
- [ ] Summarize exactly what changed and what behavior should improve.
