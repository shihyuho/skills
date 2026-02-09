# Time to Skill

Turn repetitive workflows into reusable skills automatically.

Inspired by: [If you do something more than once a day, turn it into a skill](https://x.com/bcherny/status/2017742748984742078?s=20) — Boris Cherny

## Why use this skill

Repetitive workflows are automation opportunities hiding in plain sight. This skill helps your AI agent spot them before you do.

- Detect patterns you might not notice yourself (semantic analysis, not just command matching)
- Get notified when a workflow has been repeated 3+ times
- Document patterns for skill creation
- Build project-specific skill libraries effortlessly

This pattern works great for teams: once detected, workflows become shareable skills that benefit everyone.

## How it works

1. AI monitors your tasks and identifies repetitive patterns
2. After 3 similar workflows, suggests creating a skill
3. Documents the pattern with workflow details
4. Delegates to the `skill-creator` skill for actual skill generation
5. You review and refine the generated skill

**Note**: This skill focuses on **detection only**. It hands off to `skill-creator` for the actual skill creation.

## Best use cases

Use this skill when:

- You've performed similar tasks 3+ times in a session
- You notice yourself repeating the same workflow
- You want to standardize team practices
- You're building a library of project-specific skills

## Example interaction

```text
AI: I noticed you've created React components with the same structure 3 times.

Pattern detected:
- Create component file: src/components/[Name].tsx
- Create test file: src/components/[Name].test.tsx  
- Create story file: src/components/[Name].stories.tsx

This workflow appears repetitive and could be automated as a skill.

Would you like to create a skill for this workflow?

You: Yes

AI: Great! I've documented the pattern.

Would you like me to:
1. Use the skill-creator skill to generate a complete skill (recommended)
2. Save the pattern documentation for manual creation later

Which would you prefer?

You: 1

AI: [Uses skill-creator to generate the skill...]

✓ Created skill: .agents/skills/create-react-component/SKILL.md

The skill is ready to use. Next time you need a React component, 
I'll detect the pattern and suggest using this skill.
```

## Output format

Pattern documentation:

```markdown
# Pattern: React Component Creation

**Detected**: 2026-02-09 (3 occurrences)
**Suggested Skill Name**: create-react-component

## Trigger Conditions
- User requests creating a new React component
- Needs component + test + story files

## Workflow
1. Create TypeScript component with props interface
2. Create Jest test file with basic setup
3. Create Storybook story file

## Estimated Time Savings
- Manual: ~10 minutes per component
- With skill: ~2 minutes per component  
- Potential savings: ~8 minutes per use
```

Pattern template: [PATTERN_TEMPLATE.md](references/PATTERN_TEMPLATE.md)

## Install

Install this skill only:

```bash
npx skills add shihyuho/skills --skill time-to-skill
```

Install all skills from this repository:

```bash
npx skills add shihyuho/skills --skill='*'
```

## OpenCode Plugin

This skill comes with an optional OpenCode plugin that makes the AI **proactive**.

### How it works
The plugin injects a system prompt reminder at the start of every session. It instructs the AI to monitor for:
1. Similar task patterns (using semantic analysis)
2. Repeated workflows (3+ occurrences)
3. User explicit requests ("turn this into a skill")

When these triggers occur, the AI will automatically suggest creating a skill.

### Installation
Follow the [OpenCode Plugin Installation Guide](../../.opencode/INSTALL.md).

## Works with skill-creator

**time-to-skill** detects patterns → **skill-creator** generates skill files

| This skill | skill-creator |
|-----------|---------------|
| ✅ Detects repetition | ✅ Creates SKILL.md files |
| ✅ Documents patterns | ✅ Generates proper structure |
| ✅ Suggests automation | ✅ Implements workflows |

## Related files

- [SKILL.md](SKILL.md) - Agent-facing rules and behavior
- [PATTERN_TEMPLATE.md](references/PATTERN_TEMPLATE.md) - Pattern documentation template

## License

MIT
