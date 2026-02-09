# Pattern Documentation Template

Use this template when documenting a detected repetitive workflow pattern.

---

# Pattern: [Pattern Name]

**Detected**: [Date] ([N] occurrences)
**Suggested Skill Name**: [suggested-skill-name]

## Trigger Conditions

When user:
- [Condition 1]
- [Condition 2]
- [Condition 3]

## Workflow

1. **[Step Name]** - [Description]
   - Command: `[command if applicable]`
   - Files: `[files created/modified]`
   - Tools: `[tools used]`

2. **[Step Name]** - [Description]
   - Command: `[command if applicable]`
   - Files: `[files created/modified]`
   - Tools: `[tools used]`

3. **[Step Name]** - [Description]
   - Command: `[command if applicable]`
   - Files: `[files created/modified]`
   - Tools: `[tools used]`

## Examples

### Occurrence 1
[Brief description of first occurrence]
- [Specific details]

### Occurrence 2
[Brief description of second occurrence]
- [Specific details]

### Occurrence 3
[Brief description of third occurrence]
- [Specific details]

## Code/File Templates

### [Template Name]
```[language]
[Code template or file structure that repeats]
```

### [Another Template Name]
```[language]
[Code template or file structure that repeats]
```

## Estimated Time Savings

- Manual: ~[X] minutes per occurrence
- With skill: ~[Y] minutes per occurrence
- Potential savings: ~[X-Y] minutes per use

---

## Guidelines

**What to capture**:
- Exact commands used (bash, git, npm, etc.)
- File/directory patterns and naming conventions
- Code templates and boilerplate
- Decision points (when to do A vs B)
- Tool sequences (read → edit → bash, etc.)

**What NOT to capture**:
- One-off details specific to a single occurrence
- Exploratory steps that don't repeat
- Context that changes each time

**Quality check**:
- Does this pattern repeat 3+ times?
- Are the steps actually similar (semantically)?
- Would automation save meaningful time?
- Is the pattern stable enough to codify?

**Next steps**:
After documenting the pattern, use the **skill-creator** skill to generate an actual skill file from this information.
