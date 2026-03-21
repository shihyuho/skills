# Lessons Learned Confidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `lessons-learned` documentation so the skill preserves the existing `confidence` meaning, treats `confidence: 0.0` as exclusion from normal recall, and reports confidence changes consistently during capture/update.

**Architecture:** Keep the change documentation-only and centered on the skill's canonical sources. `skills/lessons-learned/SKILL.md` remains the behavioral source of truth, while `skills/lessons-learned/references/card-template.md` and `skills/lessons-learned/README.md` are aligned to the same rules without introducing new storage or lifecycle concepts.

**Tech Stack:** Markdown, skill package metadata, `npx --yes skills-ref validate`

---

## File Map

- Modify: `skills/lessons-learned/SKILL.md` — encode the approved recall-exit and confidence-update rules.
- Modify: `skills/lessons-learned/references/card-template.md` — align template guidance with the new capture/update semantics.
- Modify: `skills/lessons-learned/README.md` — reflect the new recall behavior and reporting at a high level.
- Verify: `docs/superpowers/specs/2026-03-20-lessons-learned-confidence-design.md` — implementation reference only; do not re-edit unless implementation exposes a design gap.

### Task 1: Update the Canonical Skill Spec

**Files:**
- Modify: `skills/lessons-learned/SKILL.md`
- Reference: `docs/superpowers/specs/2026-03-20-lessons-learned-confidence-design.md`

- [ ] **Step 1: Read the approved design and identify every conflicting `confidence` rule in `SKILL.md`**

Check these sections specifically:

- `## Recall Phase`
- `## Capture Phase`
- `### Step 2 — Write the Zettel card`
- `### Step 4 — Confirm with user`
- `## Validation`

Expected conflicts to resolve:

- recall currently ranks on `confidence` but does not state that `confidence: 0.0` is excluded from normal recall
- recall does not explicitly say it is read-only with respect to `confidence`
- capture language allows `+0.1` increases but does not tie score changes clearly to capture/update only
- capture report language does not require previous/new confidence values and exclusion wording for `0.0`

- [ ] **Step 2: Edit `SKILL.md` to encode the approved recall behavior**

Make these exact rule changes:

- add that cards with `confidence: 0.0` do not participate in normal recall
- add that cards with `confidence: 0.0` remain stored under `docs/lessons/` for explicit historical lookup
- keep ranking order for all active cards as `tag match -> scope match -> confidence (desc) -> date (desc)`
- state that recall is read-only with respect to `confidence`
- preserve legacy fallback from `source` only for cards missing `confidence`

- [ ] **Step 3: Edit `SKILL.md` capture/update rules**

Document these behaviors explicitly:

- confidence changes happen only during capture/update, never during recall
- `+0.1` is allowed only when the user explicitly confirms the lesson remains useful
- `-0.1` applies when later evidence shows the lesson is less applicable
- if a lesson is only partially outdated, update the card content first and lower `confidence` only if default recall participation should weaken
- set `confidence` directly to `0.0` only when the card should stop participating in normal recall
- do not decrease confidence solely because a lesson was not used recently

- [ ] **Step 4: Update `SKILL.md` capture reporting examples and validation rules**

Ensure the canonical skill text requires:

- confidence transition reporting as `old->new`
- `none-><value>` for newly created cards
- explicit wording when a card becomes excluded from normal recall
- validation that `confidence` remains numeric and in range `0.0-0.9`

- [ ] **Step 5: Run local validation for the edited skill**

Run: `npx --yes skills-ref validate skills/lessons-learned`

Expected: validation succeeds with no schema or packaging errors.

- [ ] **Step 6: Leave commit creation for the final integrated pass**

Do not create an intermediate commit unless the implementation grows beyond this small documentation scope.

### Task 2: Align the Card Template Guidance

**Files:**
- Modify: `skills/lessons-learned/references/card-template.md`
- Reference: `skills/lessons-learned/SKILL.md`

- [ ] **Step 1: Find template guidance that conflicts with the new confidence rules**

Look for text that currently implies:

- confidence only increases and never exits recall
- confidence changes can happen without capture/update context
- `0.0` has no explicit meaning

- [ ] **Step 2: Edit the template field guidance**

Update the `confidence` guidance so it matches the canonical skill:

- initialize by `source`
- change confidence during capture/update only
- allow `+0.1` only for explicit user confirmation
- allow `-0.1` when later evidence weakens applicability
- define `0.0` as excluded from normal recall while still stored on disk

- [ ] **Step 3: Keep the template concise and subordinate to `SKILL.md`**

Do not copy the whole policy into the template. Keep only the minimum guidance needed to create or update cards correctly.

- [ ] **Step 4: Re-run local validation**

Run: `npx --yes skills-ref validate skills/lessons-learned`

Expected: validation still succeeds after the template wording change.

- [ ] **Step 5: Leave commit creation for the final integrated pass**

Do not create an intermediate commit unless the implementation grows beyond this small documentation scope.

### Task 3: Align the Public README

**Files:**
- Modify: `skills/lessons-learned/README.md`
- Reference: `skills/lessons-learned/SKILL.md`

- [ ] **Step 1: Update high-level lifecycle wording**

Adjust README language so it reflects, at a high level:

- `confidence: 0.0` excludes a card from normal recall
- cards remain stored for history
- confidence changes are reported when memory is written or updated

- [ ] **Step 2: Keep README non-canonical but non-conflicting**

Preserve the existing reminder that `SKILL.md` is the source of truth. Avoid introducing extra lifecycle terms or implementation details not present in `SKILL.md`.

- [ ] **Step 3: Validate the skill package again**

Run: `npx --yes skills-ref validate skills/lessons-learned`

Expected: validation succeeds with README updates included.

- [ ] **Step 4: Leave commit creation for the final integrated pass**

Do not create an intermediate commit unless the implementation grows beyond this small documentation scope.

### Task 4: Final Verification and Integration Check

**Files:**
- Verify: `skills/lessons-learned/SKILL.md`
- Verify: `skills/lessons-learned/references/card-template.md`
- Verify: `skills/lessons-learned/README.md`
- Verify: `docs/superpowers/specs/2026-03-20-lessons-learned-confidence-design.md`

- [ ] **Step 1: Re-read the final files against the spec checklist**

Confirm all of these are true:

- `confidence` meaning was preserved
- `confidence: 0.0` excludes cards from normal recall
- cards at `confidence: 0.0` still remain stored for explicit historical lookup
- active-card ranking order stayed unchanged
- recall is explicitly read-only with respect to `confidence`
- source-based defaults stayed `0.7 / 0.5 / 0.3`
- capture report includes confidence transitions and `0.0` exclusion wording

- [ ] **Step 2: Run final package validation**

Run: `npx --yes skills-ref validate skills/lessons-learned`

Expected: PASS

- [ ] **Step 3: Inspect the final diff for drift outside the intended scope**

Run: `git diff -- skills/lessons-learned/SKILL.md skills/lessons-learned/references/card-template.md skills/lessons-learned/README.md docs/superpowers/specs/2026-03-20-lessons-learned-confidence-design.md`

Expected: only documentation and skill-package wording changes related to confidence recall exit and capture/update semantics.

- [ ] **Step 4: Commit the integrated documentation pass**

```bash
git add skills/lessons-learned/SKILL.md skills/lessons-learned/references/card-template.md skills/lessons-learned/README.md
git commit -m "docs(lessons-learned): align confidence handling docs"
```

## Notes for the Implementer

- Keep changes small and documentation-only.
- Do not add new directories, new metadata fields, or archive behavior.
- Do not change `README.md` at the repo root; this work does not add or remove skills or commands.
- Prefer one final commit if the work stays small, even though task-level commit examples are included above.
- Use `skills/lessons-learned/SKILL.md` as the behavioral source of truth whenever the README or template could be interpreted differently.
