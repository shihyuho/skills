# Lessons Learned

Stop your AI agent from making the same mistake twice.

Inspired by an insight shared by Claude's development team: [Boris Cherny on X](https://x.com/bcherny/status/2017742747067945390?s=46&t=_h-W0h9fqgHOfF-XR_F39w).

## Why use this skill

Important fixes are often forgotten after a session ends. This skill turns those moments into durable project memory.

- Capture high-value debugging lessons in a lightweight format
- Keep lessons visible by indexing them in `AGENTS.md`
- Make future agents check relevant lessons before similar work
- Reduce repeated trial-and-error across sessions

## How it works

1. Detects high-value moments (errors, repeated retries, complex fixes)
2. Suggests creating a lesson and asks for user confirmation
3. Writes a lesson to `docs/lessons/YYYY-MM-DD-topic-slug.md`
4. Updates `AGENTS.md` with a one-line summary and link
5. Reuses relevant lessons in later tasks

## Best use cases

Use this skill when:

- The same issue appears more than once
- A bug requires multiple attempts to resolve
- You discover a pattern future agents should follow
- You want project memory to survive across sessions

## Example interaction

```text
AI: I noticed we hit the same async issue twice.
This is worth capturing as a lesson.

Would you like me to create a lesson file and update AGENTS.md?

You: Yes

AI: ✓ Created lesson: docs/lessons/2026-02-06-async-await-loops.md
✓ Updated AGENTS.md with lesson reference
```

## Output format

Lesson file path:

```text
docs/lessons/YYYY-MM-DD-topic-slug.md
```

AGENTS.md index entry:

```markdown
## Lessons Learned

If the current situation is even slightly related to any summary below, the AI MUST read the linked lesson file(s) before proceeding.

- [Avoid await in loops - use Promise.all for independent calls](docs/lessons/2026-02-06-async-await-loops.md)
```

Lesson content template:

- [LESSON_TEMPLATE.md](references/LESSON_TEMPLATE.md)

## Install

Install this skill only:

```bash
npx skills add shihyuho/skills --skill lessons-learned
```

Install all skills from this repository:

```bash
npx skills add shihyuho/skills --skill='*'
```

## Related files

- [SKILL.md](SKILL.md) - Agent-facing rules and behavior
- [LESSON_TEMPLATE.md](references/LESSON_TEMPLATE.md) - Lesson file template

## License

MIT
