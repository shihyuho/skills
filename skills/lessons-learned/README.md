# Lessons Learned

Teach your AI agent to stop repeating the same mistakes.

Inspired by a share from Claude Code team: [Boris Cherny on X](https://x.com/bcherny/status/2017742747067945390?s=46&t=_h-W0h9fqgHOfF-XR_F39w).

## Why this skill

Most agent sessions lose useful lessons after the task ends. This skill turns mistakes into reusable project memory.

- Capture hard-won fixes as lightweight lessons
- Sync lessons into `AGENTS.md` so they stay visible
- Force review of relevant lessons before similar tasks
- Reduce repeated debugging loops over time

## What it does

1. Detects high-value moments (errors, retries, complex fixes)
2. Suggests creating a lesson and asks for confirmation
3. Writes a lesson file to `docs/lessons/YYYY-MM-DD-topic-slug.md`
4. Updates `AGENTS.md` with a one-line summary and link
5. Reuses those lessons in future related tasks

## Best use cases

Use this skill when:

- The same issue happened more than once
- A bug took multiple attempts to fix
- You found a pattern you want future agents to follow
- You want project memory to survive across sessions

## Example interaction

```text
AI: I noticed we hit the same async issue twice.
This is worth saving as a lesson.

Would you like me to create a lesson file and update AGENTS.md?

You: Yes

AI: ✓ Created lesson: docs/lessons/2026-02-06-async-await-loops.md
✓ Updated AGENTS.md with lesson reference
```

## Output format

Lesson file:

```text
docs/lessons/YYYY-MM-DD-topic-slug.md
```

AGENTS.md index entry:

```markdown
## Lessons Learned

- [Avoid await in loops - use Promise.all for independent calls](docs/lessons/2026-02-06-async-await-loops.md)
```

Lesson content template:

- [LESSON_TEMPLATE.md](references/LESSON_TEMPLATE.md)

## Install

Install this skill only:

```bash
npx skills add shihyuho/skills --skill lessons-learned
```

Install all skills in this repository:

```bash
npx skills add shihyuho/skills --skill='*'
```

## Related files

- [SKILL.md](SKILL.md) - Agent-facing behavior and rules
- [LESSON_TEMPLATE.md](references/LESSON_TEMPLATE.md) - Lesson file template

## License

MIT
