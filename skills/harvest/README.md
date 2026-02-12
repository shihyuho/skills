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

## Behavior Guarantees

- **Never auto-executes**: write operations happen only after explicit confirmation.
- **Smart merge by context**: repeated harvest in one context updates the same file via `context_id`.
- **Merge-stable entries**: Decisions/Questions/Lessons use stable IDs for safer repeated updates.
- **Stable fallback**: when no session/thread ID exists, `context_id` falls back to `YYYYMMDDHHmmss`.
- **Index discipline**: updates recent changes, decisions, questions, lessons, and stats.
- **Link-only lessons MOC**: `mocs/lessons-learned.md` stores links to anchors, not duplicated lesson bodies.
- **Snapshot persistence**: when planning files are used as sources, this skill stores concise snapshots in context notes (not full copies).
- **High-signal output**: concise notes intended to stay useful months later.
- **List-first readability**: context content defaults to lists; tables are used only for short, comparable fields.
- **No `.base` syntax ownership**: when `obsidian-bases` is available, base-file generation is delegated automatically.

## Lesson Review Scope

- During harvest runs, AI reviews existing lessons (when available) before writing/merging context notes.
- If you opt into the AGENTS/CLAUDE lessons hook, this review can also run before future tasks.

## Recommended Companion Workflow (Optional)

**Recommended**: pair harvest with `planning-with-files` for complex, multi-step work.

- `planning-with-files` captures in-progress research and execution details.
- This skill captures durable outcomes (decisions, unsolved items, lessons) into `docs/notes/`.
- This skill still works fully without `planning-with-files`.
- If planning files are outside your Obsidian vault (for example, vault rooted at `docs/notes`), this skill should store provenance as plain text notes instead of external wikilinks.

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
- [references/bases-generation-spec.md](references/bases-generation-spec.md) - semantic contract for default Bases output
- [references/agents-lessons-section.md](references/agents-lessons-section.md) - optional pre-task lessons hook
- [references/initialization-manifest.md](references/initialization-manifest.md) - initialization inventory (paths/files/checklist)
- [scripts/context_id.py](scripts/context_id.py) - context ID resolver (Python stdlib only)

## License

MIT
