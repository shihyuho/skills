# Harvest

Capture important conversation outcomes before they disappear.

## Why It Exists

Technical chats produce high-value output: decisions, trade-offs, lessons, and open questions. Without a capture step, that context is hard to find later and easy to repeat incorrectly.

Harvest turns those moments into reusable project memory.

## What It Creates

Harvest writes structured notes in `docs/notes/`:

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

1. You trigger Harvest (`/harvest` or natural language like "harvest this").
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

## Behavior Guarantees

- **Never auto-executes**: write operations happen only after explicit confirmation.
- **Smart merge by context**: repeated harvest in one context updates the same file via `context_id`.
- **Stable fallback**: when no session/thread ID exists, `context_id` falls back to `YYYYMMDDHHmmss`.
- **Index discipline**: updates recent changes, decisions, questions, lessons, and stats.
- **Link-only lessons MOC**: `mocs/lessons-learned.md` stores links to anchors, not duplicated lesson bodies.
- **High-signal output**: concise notes intended to stay useful months later.

## Lesson Review Scope

- During Harvest runs, AI reviews existing lessons (when available) before writing/merging context notes.
- If you opt into the AGENTS/CLAUDE lessons hook, this review can also run before future tasks.

## When to Use

- after a key decision
- after resolving a complex problem
- before ending a productive session
- when you think "we should remember this"

AI may also suggest Harvest at natural breakpoints. You stay in control.

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
- [references/CONTEXT_TEMPLATE.md](references/CONTEXT_TEMPLATE.md) - context schema
- [references/INDEX_TEMPLATE.md](references/INDEX_TEMPLATE.md) - index schema
- [references/MOC_TEMPLATE.md](references/MOC_TEMPLATE.md) - topic MOC schema
- [references/LESSONS_LEARNED_MOC_TEMPLATE.md](references/LESSONS_LEARNED_MOC_TEMPLATE.md) - lessons MOC schema
- [references/CONTEXTS_BASE_TEMPLATE.base](references/CONTEXTS_BASE_TEMPLATE.base) - Obsidian Bases view template
- [references/MOCS_BASE_TEMPLATE.base](references/MOCS_BASE_TEMPLATE.base) - Obsidian Bases MOCs view template
- [references/AGENTS_LESSONS_SECTION.md](references/AGENTS_LESSONS_SECTION.md) - optional pre-task lessons hook

## License

MIT
