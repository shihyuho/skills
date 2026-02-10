# Agent Skills Repository

This repository contains AI agent skills following the [Agent Skills format](https://agentskills.io/). Each skill provides packaged instructions for AI coding agents.

## Repository Structure

```
skills/
├── README.md                 # Repository index
├── package.json              # Metadata
└── skills/                   # Skills directory
    └── {skill-name}/         # Individual skill (kebab-case)
        ├── SKILL.md          # AI instructions (required)
        ├── README.md         # Human-readable documentation
        ├── references/       # Supporting docs (optional)
        └── scripts/          # Helper scripts (optional)
```

## Commands

This is a documentation-only repository. No build/test/lint commands are needed.

### Validation

Use the [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) tool to validate skills:

```bash
skills-ref validate ./skills/skill-name
```

## Writing Style Guidelines

### General Principles

- **Language**: All documentation in English
- **Tone**: Professional but approachable, direct and concise
- **Audience**: AI agents (SKILL.md) and humans (README.md)
- **Format**: Markdown with clear structure and hierarchy

### SKILL.md Requirements

SKILL.md files are instructions for AI agents. Follow the [Agent Skills specification](https://agentskills.io/specification).

#### YAML Frontmatter (Required)

```yaml
---
name: skill-name                    # kebab-case, max 64 chars
description: What this skill does and when to use it. Include trigger keywords.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---
```

**Frontmatter rules**:
- `name`: Must match directory name, lowercase, hyphens only
- `description`: 1-1024 chars, include both "what" and "when"
- Keep metadata consistent across all skills

#### Body Structure

```markdown
# Skill Name

Brief introduction (1-2 sentences).

## Overview

- Bullet points for key capabilities
- What problems this skill solves
- Core principle or philosophy

## When to Trigger

Clear list of situations when AI should use this skill:
- Specific error patterns
- Task types
- User requests

## Workflow

Step-by-step instructions:
1. **Step name** - What to do
2. **Step name** - What to do

Use **bold** for step names, code blocks for examples.

## [Additional Sections]

- Examples
- Best Practices
- Limitations
- See Also

## See Also

- Link to templates in references/
- Link to related files
```

**SKILL.md guidelines**:
- Keep under 500 lines (move details to references/)
- Use imperative mood for instructions ("Create file", not "Creates file")
- Include concrete examples with code blocks
- Specify mandatory vs optional behaviors clearly
- Use **bold** for emphasis on key terms
- Use `code` for file names, commands, variables

### README.md (Skill-Level)

Each skill should have a README.md for human readers. The goal is to **attract users** by showing value first, technical details later.

**README vs SKILL.md**

| Aspect | README.md (Human) | SKILL.md (AI) |
|--------|-------------------|---------------|
| **Audience** | Potential users browsing GitHub | AI agents executing tasks |
| **Goal** | Attract and convince | Instruct and guide |
| **Tone** | Marketing, conversational | Technical, imperative |
| **Examples** | Dialogue scenarios | Code snippets and workflows |
| **Length** | Concise (100-200 lines) | Detailed (300-500 lines) |
| **Focus** | Value proposition | Implementation details |

**Core Principles for README:**

1. **Problem-First**: Lead with user pain points, not technical features
2. **Show AI Intelligence**: Demonstrate what AI does automatically, not what users need to configure
3. **Use Scenarios**: Show real conversations and workflows, not just API documentation
4. **Progressive Disclosure**: Hook → Value → Scenarios → Features → How to Start

**Example**: See [`skills/fanfuaji/README.md`](skills/fanfuaji/README.md) for a complete implementation.

### References and Templates

Files in `references/` directory:

- Use descriptive ALL_CAPS names for templates (e.g., `LESSON_TEMPLATE.md`)
- Include usage guidelines within the template itself
- Keep templates concise with placeholder text in `[brackets]`
- Add guidelines section at bottom of template

## Naming Conventions

### Files and Directories

- **Skill directories**: `kebab-case` (e.g., `lessons-learned`)
- **SKILL.md**: Always uppercase `SKILL.md`
- **README.md**: Always uppercase `README.md`
- **Templates**: `UPPERCASE_WITH_UNDERSCORES.md`
- **Other references**: `kebab-case.md`

### Generated Files (in User Projects)

When skills instruct AI to create files in user projects:

- **Date-based files**: `YYYY-MM-DD-topic-slug.md` (e.g., `2026-02-06-async-loops.md`)
- **Directories**: `lowercase` (e.g., `lessons/`)
- **slugs**: `kebab-case`, 2-4 words max

## Formatting Standards

### Markdown

- **Headers**: Use ATX style (`#`, `##`, not underlines)
- **Lists**: Use `-` for unordered, numbers for ordered
- **Code blocks**: Always specify language (````markdown`, ```bash`, ```yaml`)
- **Links**: Use reference-style for repeated links, inline for one-offs
- **Emphasis**: `**bold**` for key terms, `*italic*` rarely (prefer bold or `code`)
- **Line length**: No hard limit, but break long lines at natural points (after sentences)

### Code Blocks

````markdown
```bash
# Good: Include comment explaining context
npx skills add shihyuho/skills
```

```yaml
# Good: Show complete, valid example
---
name: example-skill
description: Example description
---
```
````

### Examples and Interactions

Show AI-user interactions with clear formatting:

````markdown
**AI Suggestion**:
```
I noticed we hit the same issue twice.
Would you like me to create a lesson-learned entry?
```

**User**: Yes

**AI Response**:
```
✓ Created lesson: lessons/2026-02-06-example.md
✓ Updated AGENTS.md
```
````

## Writing Instructions for AI

When writing SKILL.md instructions:

### Be Explicit

❌ **Bad**: "Update the file appropriately"
✅ **Good**: "Add one line to the `## Lessons Learned` section in AGENTS.md"

### Use Imperative Mood

❌ **Bad**: "The AI should create a file"
✅ **Good**: "Create a file at `lessons/YYYY-MM-DD-topic.md`"

### Specify Mandatory Behaviors

Use clear markers:
- **Must**, **Required**, **Mandatory** for non-negotiable steps
- **Should**, **Recommended** for best practices
- **May**, **Optional**, **Can** for discretionary actions

### Provide Templates

Instead of describing format, show it:

❌ **Bad**: "Use a date-based filename with a topic slug"
✅ **Good**: "Naming: `lessons/YYYY-MM-DD-topic-slug.md`"

### Include Confirmation Patterns

For interactive workflows, specify exact prompts:

```markdown
**Template**:
```
I noticed [specific situation].
Would you like me to [specific action]?
```
```

## Error Handling

Since this is a documentation repo, focus on preventing common mistakes:

### Validation Checklist

Before committing new skills:

1. [ ] YAML frontmatter is valid
2. [ ] `name` field matches directory name
3. [ ] `description` is clear and includes trigger keywords
4. [ ] SKILL.md is under 500 lines
5. [ ] Examples are concrete and actionable
6. [ ] Templates are in `references/` directory
7. [ ] README.md provides human-friendly overview
8. [ ] All links are valid (no broken references)

### Common Pitfalls

- **Don't** use relative paths that go up (e.g., `../../file`)
- **Don't** reference files outside the skill directory
- **Don't** use ambiguous language ("probably", "might", "usually")
- **Do** be specific about file locations and formats
- **Do** provide complete, copy-paste-ready examples

## Agent Skills Format Compliance

This repository follows the [Agent Skills specification](https://agentskills.io/specification):

- ✅ Flat structure under `skills/` directory
- ✅ Each skill has `SKILL.md` with YAML frontmatter
- ✅ Progressive disclosure (metadata → instructions → resources)
- ✅ File references use relative paths from skill root
- ✅ Optional `references/`, `scripts/`, `assets/` directories

## Contributing

When adding new skills:

1. Create directory: `skills/new-skill-name/`
2. Add `SKILL.md` with YAML frontmatter
3. Add `README.md` for human readers
4. Add templates to `references/` if needed
5. **Update root `README.md` skills list**
6. Validate with `skills-ref validate ./skills/new-skill-name`

When adding new OpenCode plugins:

1. Create plugin file: `.opencode/plugins/your-plugin.js`
2. Update `.opencode/INSTALL.md` with installation steps
3. **Update root `README.md` OpenCode Plugins list**

## License

MIT
