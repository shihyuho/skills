# Harvest

Capture important conversation outcomes before they disappear.

## Why It Exists

Technical chats produce high-value output: decisions, trade-offs, lessons, and open questions. Without a capture step, that context is hard to find later and easy to repeat incorrectly.

This skill turns those moments into reusable project memory.

## What It Creates

This skill writes structured notes in `docs/notes/`:

```text
docs/notes/
├── 00-INDEX.md
├── contexts/
└── mocs/
    ├── lessons-learned.md      # created/updated when relevant
    └── <topic>.md              # suggested after 3+ related contexts
```

Each context file is named:

`<context_id>-<topic-slug>.md`

## Quick Flow

1. You trigger harvest (`/harvest` or natural language like "harvest this").
2. AI summarizes decisions, unsolved items, and lessons.
3. AI proposes a filename and asks for confirmation:
   - `1. Use this`
   - `2. Change slug`
   - `3. Cancel`
4. AI creates or smart-merges context notes.
5. AI updates `00-INDEX.md` and related MOCs when needed.

## Example

```text
You: /harvest

AI: Found 2 decisions, 1 unsolved, 1 lesson
    Suggested: contexts/<context_id>-payment-gateway.md
    1. Use this  2. Change slug  3. Cancel

You: 1

AI: ✓ Created: contexts/<context_id>-payment-gateway.md
    ✓ Updated: 00-INDEX.md
```

## Second Brain

Harvest turns important conversation outcomes into reusable project memory in `docs/notes/`.
It keeps decisions, open questions, and lessons connected so future sessions can resume with less repeated work.

## Lessons Learned

Harvest keeps lessons easy to revisit through `mocs/lessons-learned.md`.
It links back to the original context entries, so teams can apply past fixes and avoid repeating the same mistakes.

## Recommended Companion Workflow (Optional)

**Recommended**: pair harvest with `planning-with-files` for complex, multi-step work.

- `planning-with-files` captures in-progress execution details in `task_plan.md`, `findings.md`, and `progress.md`.
- Harvest extracts higher-signal snapshots (`conclusion + evidence + source note`) instead of copying raw planning logs.
- Together, they improve extraction precision for decisions, open questions, and lessons.
- Harvest still works well without `planning-with-files`.

## When to Use

- after a key decision
- after resolving a complex problem
- before ending a productive session
- when you think "we should remember this"

AI may also suggest harvest at natural breakpoints. You stay in control.

## When Not to Use

- trivial chat with no reusable decisions or lessons
- purely mechanical edits with no meaningful context
- conversations you intentionally do not want persisted

## Install

```bash
npx skills add shihyuho/skills --skill harvest
```

## Related Files

- [SKILL.md](SKILL.md) - AI execution workflow
- [references/context-template.md](references/context-template.md) - context schema
- [references/index-template.md](references/index-template.md) - index schema
- [references/moc-template.md](references/moc-template.md) - topic MOC schema
- [references/lessons-learned-moc-template.md](references/lessons-learned-moc-template.md) - lessons MOC schema

## License

MIT
