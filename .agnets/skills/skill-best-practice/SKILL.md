---
name: skill-best-practice
description: Use when creating a new Agent Skill or refactoring an existing one, especially when aligning SKILL.md, README.md, references, commands, and validation workflow.
license: MIT
metadata:
  author: shihyuho
  version: "1.1.0"
---

# Skill Best Practice

Create or evolve skills into clear, maintainable, and behavior-accurate packages without breaking their core contract.

## Overview

- Support both **new skill creation** and **existing skill refactor/optimization**.
- Keep behavior guarantees explicit while reducing branching complexity.
- Align all related surfaces: `SKILL.md`, `README.md`, `references/`, `commands/`, and root docs.
- Validate every iteration with objective checks before finalizing.

## Scope

- This is a **project-local private practice skill** at `.agnets/skills/skill-best-practice/`.
- Do not assume publication; only prepare public distribution when user explicitly requests it.
- For new skills, decide target location first:
  - private/local: `.agnets/skills/<skill-name>/`
  - distributable: `skills/<skill-name>/`

## When to Trigger

Use this skill when users ask to:

- create a new skill from scratch
- optimize or refactor an existing skill
- simplify complex skill workflow while preserving behavior
- align skill docs and references after major workflow changes
- standardize command naming/layout for a skill
- add validation workflow for skills quality gates

Typical trigger phrases:

- "create a skill for X"
- "design a new skill"
- "refactor this skill"
- "this skill is too slow"
- "rework the skill design"
- "align README and SKILL behavior"
- "clean up command structure for this skill"

## Workflow

### Track A: Create New Skill

1. **Intent and scope check**
   - Confirm whether the new skill is private/local or distributable.
   - Define trigger phrases, must-have behavior, and non-negotiables.

2. **Structure planning**
   - Create minimal structure: `SKILL.md` (+ `README.md` for this repository style).
   - Add `references/` only when details are too heavy for `SKILL.md`.
   - Add `scripts/` only when deterministic execution is needed repeatedly.

3. **Author SKILL.md first**
   - Write precise frontmatter (`name`, `description`, metadata).
   - Make trigger conditions explicit and searchable.
   - Use deterministic, step-by-step workflow with mandatory checks.

4. **Author README.md**
   - Keep it value-first and concise for human readers.
   - Include practical use cases and realistic examples.

5. **Integrate and validate**
   - For distributable skills, update root `README.md` skill list.
   - Validate target skill:

```bash
npx --yes skills-ref validate ./<skill-path>
```

### Track B: Refactor / Optimize Existing Skill

1. **Baseline audit**
   - Read target `SKILL.md`, `README.md`, and `references/` files.
   - List current behavior contract (must keep), pain points (must improve), and constraints.
   - Mark non-negotiables explicitly (confirmation gates, safety checks, naming requirements).

2. **Reference benchmark**
   - Find 1-2 comparable skills with similar goals.
   - Extract reusable patterns only (phase split, routing table, template authority, naming).
   - Avoid copying structure blindly; map patterns to the target skill context.

3. **Phase plan (P0/P1/P2)**
   - **P0**: correctness and safety (contract clarity, mandatory checks, routing accuracy).
   - **P1**: structure and readability (flow simplification, section clarity, reduced branchiness).
   - **P2**: ecosystem polish (README alignment, command docs, naming conventions, CI validation).
   - Define done criteria for each phase before editing.

4. **Refactor SKILL.md first**
   - Keep frontmatter precise (`name`, `description`, metadata).
   - Tighten trigger section and non-negotiables.
   - Prefer deterministic routing (tables or explicit conditions) over prose-only branching.
   - Keep templates/references as the single source of schema.

5. **Align supporting docs**
   - Update skill `README.md` to be concise and value-first for humans.
   - Ensure examples match real behavior (no stale promises).
   - Align terminology across `SKILL.md`, `README.md`, and `references/`.

6. **Align command surface (when applicable)**
   - Prefer flat prefixed command files: `{skill-name}-{command-name}.md`.
   - Ensure command frontmatter has clear `description`.
   - Keep command instructions atomic (one command, one workflow).

7. **Repository integration**
   - Update root `README.md` skill list with one concise value proposition.
   - If command naming rules changed, update repository guidance docs.

8. **Verification and completion**
   - Run:

```bash
npx --yes skills-ref validate ./<skill-path>
```

   - Search for stale terms, outdated command names, and broken references.
   - Confirm output is behavior-accurate and free of contradictory instructions.

## Refactor Rules

- Preserve behavior contract first; optimize wording second.
- Keep docs in English unless repository policy says otherwise.
- Do not add optional sections if they stay empty.
- Do not duplicate reference schemas in multiple files.
- Prefer low-churn edits that maximize clarity.
- Keep trigger descriptions explicit enough for reliable skill discovery.

## Output Checklist

- Updated `<skill-path>/SKILL.md`
- Updated `<skill-path>/README.md` (if needed)
- Updated `<skill-path>/references/*` (if needed)
- Updated root `README.md` entry (only for distributable skills)
- Validation result included (`skills-ref validate`)

## See Also

- [Agent Skills Specification](https://agentskills.io/specification)
