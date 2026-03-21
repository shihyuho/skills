# Writing Agents MD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new `writing-agents-md` skill that teaches models to keep `AGENTS.md` / `CLAUDE.md` minimal, non-redundant, and focused on global non-discoverable constraints.

**Architecture:** Create one new skill package under `skills/writing-agents-md/` with a concise `SKILL.md` and small reference files for principles, checklist, and examples. Keep the main skill body focused on trigger conditions, review/rewrite workflow, and retention heuristics; move extended rationale and examples into `references/`. Update `README.md` in the same change so the published skill list stays in sync.

**Tech Stack:** Markdown skill package, repository README, `skills-ref` validation

---

## Chunk 1: Define Skill Package Content

### Task 1: Create the new skill directory content

**Files:**
- Create: `skills/writing-agents-md/SKILL.md`
- Create: `skills/writing-agents-md/references/principles.md`
- Create: `skills/writing-agents-md/references/checklist.md`
- Create: `skills/writing-agents-md/references/examples.md`

- [ ] Draft frontmatter with `name: writing-agents-md` and a trigger-oriented description.
- [ ] Write a concise overview explaining that global rule files should contain only non-discoverable, globally relevant, stable constraints.
- [ ] Add a workflow that reviews existing content and classifies each item as keep/delete/rewrite/move-to-skill.
- [ ] Add guardrails against `/init`-style repo summaries, stale file-path tours, and anchoring to legacy technologies.
- [ ] Put detailed rationale and examples in `references/` instead of bloating `SKILL.md`.

### Task 2: Encode practical keep/delete heuristics

**Files:**
- Modify: `skills/writing-agents-md/SKILL.md`
- Modify: `skills/writing-agents-md/references/checklist.md`
- Modify: `skills/writing-agents-md/references/examples.md`

- [ ] Add a discoverability test: if the model can learn it by reading repo files, do not keep it globally.
- [ ] Add a relevance test: if the instruction only matters for some tasks, move it to a skill instead.
- [ ] Add a rot-risk test: if the statement names paths, modules, or patterns likely to change, prefer deleting or narrowing it.
- [ ] Include examples of good retained rules (`uv`, WSL, cache traps, legacy landmines).
- [ ] Include examples of removable noise (scripts, tech stack, architecture overviews, directory tours).

## Chunk 2: Integrate With Repo Metadata

### Task 3: Update repository README

**Files:**
- Modify: `README.md`

- [ ] Add `writing-agents-md` to the `Available Skills` list with a short description.
- [ ] Keep README ordering and style consistent with existing entries.
- [ ] Verify there are no other repo index files that need the same update for a new skill.

## Chunk 3: Validate And Review

### Task 4: Validate the new skill package

**Files:**
- Verify: `skills/writing-agents-md/SKILL.md`

- [ ] Run `npx --yes skills-ref validate skills/writing-agents-md`.
- [ ] If validation fails, fix the package and rerun the same command.
- [ ] Re-read the final `SKILL.md` and ensure it stays concise rather than drifting into a repo-handbook.

### Task 5: Pressure-test the skill behavior lightly

**Files:**
- Verify: `skills/writing-agents-md/SKILL.md`
- Reference: `skills/writing-agents-md/references/examples.md`

- [ ] Draft 2-3 realistic prompts that would require rewriting or pruning an `AGENTS.md` / `CLAUDE.md` file.
- [ ] Check that the skill wording prefers deletion and skill-splitting over repo-summary generation.
- [ ] Summarize any obvious gaps before considering follow-up eval automation.
