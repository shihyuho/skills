# Agent Skills Repository

This repository contains AI agent skills following the
[Agent Skills format](https://agentskills.io/).

## Lessons Learned

**MUST** use the `lessons-learned` skill before any execution

## Repository Structure

```text
skills/
├── README.md                 # Repository index
├── package.json              # Metadata
├── commands/                 # Reusable command entrypoints
└── skills/                   # Skills directory
    └── {skill-name}/
        ├── SKILL.md
        ├── README.md
        ├── references/
        └── scripts/
```

## Commands

This is a documentation-first repository. No build/test/lint pipeline is
required for routine edits.

### Command Design Guidelines

- Treat command files as trigger entrypoints.
- Keep behavior definitions in `skills/<skill-name>/SKILL.md`.
- Reference SKILL phase/section names instead of duplicating logic.
- Do not redefine bootstrap file lists, validation checklists, or extraction
  criteria in `commands/*.md`.
- Keep command-specific context brief and non-authoritative.
- When adding, removing, or renaming files under `commands/`, update and verify
  the commands list in root `README.md` in the same change.

## Validation

Validate changed skills with
[skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref):

```bash
npx --yes skills-ref validate ./skills/skill-name
```

## Writing Guidelines

### General

- **Language**: English
- **Tone**: Professional, direct, concise
- **Audience**: AI agents (`SKILL.md`) and humans (`README.md`)

### `SKILL.md`

Follow the [Agent Skills specification](https://agentskills.io/specification).

Required frontmatter template:

```yaml
---
name: skill-name
description: What this skill does and when to use it. Include trigger keywords.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---
```

Rules:

- `name` matches directory name; lowercase and hyphens only.
- `description` is 1-1024 chars and includes both what/when.
- Keep `SKILL.md` under 500 lines; move heavy detail to `references/`.
- Use imperative instructions and explicit mandatory wording.
- Include concrete examples when behavior is non-obvious.

### Skill-Level `README.md`

- Write for human readers with value-first framing.
- Prefer scenario-based explanation over API-style dumps.
- Keep it concise; point detailed execution logic to `SKILL.md`.

### `references/`

- Use `lowercase-dash` file names.
- Keep templates concise with placeholders.
- Place detailed examples and long-form guidance here.

## Naming Conventions

- Skill directories: `kebab-case` (e.g., `lessons-learned`).
- Skill subdirectories: do not use `_`-prefixed names under `skills/`; use
  `.`-prefixed names when needed (e.g., `.templates`).
- Fixed file names: `SKILL.md`, `README.md`.
- Command files: `{skill-name}-{command-name}.md`.
- Reference files: `lowercase-dash.md` (or `.base` when format requires it).

## Formatting Standards

- Headers: ATX (`#`, `##`, ...).
- Lists: `-` for unordered; numbered for ordered.
- Code blocks: always use language labels.
- Emphasis: `**bold**` for key terms; use backticks for file paths/commands.
- Break long lines at natural boundaries for readability.

## Contribution Checklist

When adding or changing a skill:

1. Update files under `skills/<skill-name>/`.
2. Update root `README.md` skills list if needed.
3. If `commands/` changed, update root `README.md` commands list.
4. Run `npx --yes skills-ref validate ./skills/<skill-name>`.

## License

MIT
