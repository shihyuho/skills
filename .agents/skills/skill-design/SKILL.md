---
name: skill-design
description: Use when creating, refactoring, or reviewing an Agent Skill and you need strict, portable design rules.
license: MIT
metadata:
  author: shihyuho
  version: "1.3.0"
---

# Skill Design

These are instructions for designing skills as reusable behavior systems.

## Core Rule

- MUST design for reliable agent behavior, not document aesthetics.
- MUST make trigger conditions explicit and searchable.
- MUST keep instructions executable and verifiable.
- NEVER rely on implicit project context.

## Trigger Contract

Use this skill when users ask to:

- create a new skill
- refactor an existing skill
- improve trigger quality or discoverability
- align `SKILL.md`, `README.md`, and `references/`
- remove ambiguity or conflicting guidance

Typical trigger phrases:

- "create a skill for X"
- "design a new skill"
- "refactor this skill"
- "make this skill reusable"
- "align README and SKILL behavior"

## CRITICAL: Writing Mode

- MUST write in imperative voice.
- MUST use `MUST`/`NEVER` for non-negotiables.
- MUST keep sections short and high-signal.
- MUST prefer concrete constraints over abstract advice.
- NEVER use weak modal language for hard rules (`should`, `could`, `may`, `consider`, `usually`).
- NEVER pad with narrative text that does not change execution.

## Information Architecture

- MUST keep `SKILL.md` as execution logic and decision constraints.
- MUST keep `references/` as the single source of heavy schemas/templates.
- MAY add `scripts/` only for repeatable deterministic operations.
- MUST keep file structure minimal and purpose-driven.

## Workflow

### Phase 1 - Define Contract

1. Define who uses the skill and when it triggers.
2. Define non-negotiable behavior and failure boundaries.
3. Define deterministic vs heuristic decisions.

### Phase 2 - Structure Content

1. Write trigger and constraints first.
2. Move bulky detail to `references/`.
3. Keep one source of truth for each schema.

### Phase 3 - Author/Refactor SKILL

1. Tighten description and trigger wording.
2. Convert soft guidance to executable rules.
3. Add explicit anti-generic constraints.
4. Remove duplicate or contradictory instructions.

### Phase 4 - Align README (Human-Facing)

1. Keep README value-first: problem -> value -> example -> activation.
2. Keep implementation internals out of README.
3. Keep claims behavior-accurate.

### Phase 5 - Validate

1. Run available validator for your environment.
2. If no validator exists, run manual consistency checks.
3. Confirm no repository-specific assumptions remain unless explicitly intended.

## README Rules

- In this skill, `README.md` means the skill-level README (for example `skills/<skill-name>/README.md`), not the repository root README.
- `README.md` is not required by Agent Skills Specification.
- `README.md` is recommended for faster human understanding and adoption.
- MUST keep README focused on outcomes, not internal mechanics.

## Anti-Patterns

- Hardcoded local paths as universal defaults.
- Tool lock-in with no fallback path.
- Workflow summary inside frontmatter `description`.
- Duplicated schema definitions across files.
- Long narrative prose with no executable instruction.

## Done Checklist

- `SKILL.md` has explicit trigger contract and hard constraints.
- `README.md` is concise and value-focused.
- `references/` contains heavy details only when needed.
- No stale terms or contradictory rules.
- Validation evidence is recorded (tool-based or manual).
- Example validation command: `npx --yes skills-ref validate <skill-name>`.

## See Also

- [Agent Skills Specification](https://agentskills.io/specification)
