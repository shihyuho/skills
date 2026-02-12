# Skill Design

Design and refactor agent skills with strict, portable rules.

## Why Skills Fail

- Triggers are vague.
- Workflows drift from real behavior.
- Rules are descriptive, not executable.
- Repo-local assumptions leak into reusable skills.

## Design Goals

This section captures current design thinking for skills in this repository.
It is an optimization direction, not a frozen contract.

- Keep trigger contracts explicit and searchable.
- Keep instructions imperative and testable.
- Separate human-facing value (`README.md`) from agent execution (`SKILL.md`).
- Keep heavy schemas in `references/`.

## When to Use

- "Create a skill for this workflow"
- "Refactor this skill"
- "Make this skill reusable"
- "Align README and SKILL behavior"
- "Remove ambiguity in this skill"

## Quick Process

1. Define trigger contract and non-negotiables.
2. Structure files (`SKILL.md`, optional `README.md`, optional `references/`, optional `scripts/`).
3. Rewrite rules into MUST/NEVER constraints.
4. Remove generic fluff and repo-specific leakage.
5. Validate consistency.

## Validation

Use available tooling in your environment. If no validator exists, run manual checks:

- trigger wording is explicit and searchable
- instructions are executable
- schema ownership is not duplicated
- no accidental repository-specific assumptions

## See Also

- [Agent Skills Specification](https://agentskills.io/specification)
- [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator)

## Related Files

- [SKILL.md](SKILL.md)

## License

MIT
