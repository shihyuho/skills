# Skill Best Practice

Create new skills and refactor existing ones into clear, maintainable, behavior-accurate packages.

## Why This Skill Exists

When a skill grows over time, it often becomes harder to run: too many branches, duplicated rules, and drift between `SKILL.md`, `README.md`, and references.

This skill gives AI a practical playbook to build skills from scratch and evolve them safely over time.

## What It Helps You Do

- Design a new skill with strong trigger quality and workflow clarity
- Audit an existing skill before editing
- Keep must-have behavior while simplifying structure
- Align `SKILL.md`, `README.md`, `references/`, and command files
- Standardize command naming conventions
- Add or verify validation steps (`skills-ref`)

## Typical Use Cases

- "Create a skill for this workflow"
- "Design a new skill for this project"
- "This skill is too slow, optimize it"
- "Refactor this skill but keep behavior the same"
- "The README and SKILL are inconsistent"
- "Clean up command naming and docs"

## Workflow Summary

1. Decide scope: private local skill or distributable skill
2. For creation: define triggers, non-negotiables, and file structure
3. For refactor: audit behavior contract and pain points
4. Align `SKILL.md`, `README.md`, references, and commands
5. Validate with `skills-ref` and consistency searches

## Validation

```bash
npx --yes skills-ref validate ./.agnets/skills/skill-best-practice
```

## Local Usage

Keep this folder in-project at `.agnets/skills/skill-best-practice/`.
This skill is intended for project-local usage and is not meant for public distribution by default.

## Related Files

- [SKILL.md](SKILL.md)
- [../../../AGENTS.md](../../../AGENTS.md)

## License

MIT
