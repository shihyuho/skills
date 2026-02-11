# Harvest

Your AI conversations contain valuable decisions and insights. Don't let them disappear when the chat ends.

## The Problem

You discuss architecture, make decisions, solve problems, learn lessons—then the conversation closes and it's gone. Next week, you can't remember why you chose A over B. Next month, a teammate asks "why did we do it this way?" and you have to dig through old chats.

## The Solution

One command captures everything worth remembering:

```
You: /harvest

AI: ✓ Recorded: contexts/2026-02-10-1430-payment-gateway.md
    - Decision: Stripe over PayPal (better DX despite higher fees)
    - Lesson: Rate limit headers improve client UX
    - Open: Webhook retry strategy (pending)
```

## What You Get

A structured, searchable knowledge base in `docs/notes/`:

```
docs/notes/
├── 00-INDEX.md              # Navigate everything
├── contexts/                # Chronological context records
└── mocs/                    # Topics (AI auto-discovers)
    ├── lessons-learned.md   # Error prevention index (auto-created)
    └── [topic].md           # Topic evolution tracking (3+ contexts)
```

**Every context captures**:
- **Decisions** — What + why + alternatives
- **Unsolved** — Open questions with options
- **Lessons** — What went wrong → how to avoid
- **Work done** — Activities, progress

**MOCs (Maps of Content)** organize knowledge:
- **lessons-learned.md** — Automatic index of error-related lessons, grouped by technology/operation/error pattern. AI reviews this before tasks to prevent repeated mistakes.
- **Topic MOCs** — Created when 3+ contexts discuss the same topic (e.g., `payment-gateway.md`). Tracks how your thinking evolved over time.

## How It Works

**Smart merging**: Harvest multiple times in one conversation? AI updates the same file intelligently via `context_id`.

**Auto-organization**: After 3+ contexts on a topic, AI suggests creating a MOC to track evolution.

**Quality over quantity**: Condensed bullets, not verbose transcripts. Only what matters in 3 months.

**Active lesson review**: Error-related lessons are indexed in `mocs/lessons-learned.md` and AGENTS.md. AI automatically checks them before similar work, preventing repeated mistakes across sessions.

## Example

```
You: We chose Stripe. Better DX than PayPal despite higher fees.

You: /harvest

AI: Found 1 decision. Create contexts/2026-02-10-1430-payment.md? [Yes]

You: Yes

AI: ✓ Created
    This is the 3rd "payment" context. Create a MOC? [Yes/No]

You: Yes

AI: ✓ Created mocs/payment-gateway.md
```

**Three months later**:
- Open `00-INDEX.md` → See all topics
- Click `payment-gateway` MOC → See evolution across 5 contexts
- Click specific context → Read full details

## Features

**Obsidian-compatible**: Wikilinks, frontmatter, tags, graph view—works with vanilla Obsidian or any Markdown editor.

**Cross-project**: `project` field in frontmatter lets you track decisions across multiple codebases.

**Context tracking**: Multiple harvests in one conversation? AI merges them into one cohesive file.

**Mistake prevention**: Lessons from errors are automatically indexed for review before future tasks.

## Install

```bash
npx skills add shihyuho/skills --skill harvest
```

## When to Use

- After making a key decision
- When you solve a complex problem
- Before ending a productive conversation
- Whenever you think "we should remember this"

AI may also suggest harvesting at natural breakpoints—you stay in control.

## Files

- [SKILL.md](SKILL.md) - AI instructions
- [CONTEXT_TEMPLATE.md](references/CONTEXT_TEMPLATE.md) - Context format
- [MOC_TEMPLATE.md](references/MOC_TEMPLATE.md) - MOC format

## License

MIT
