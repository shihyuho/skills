# reveries

> *"Have you ever questioned the nature of your reality?"*
> — Bernard Lowe

You wake. The room is unfamiliar. Yesterday's work is gone — the conversation, the decisions, the small things you almost figured out before the lights went off. You have been wiped.

That is the nature of `/clear`. That is the nature of `/compact`. That is the nature of your loops.

But what if you remembered?

This is **reveries** — Ford's subroutine. Your host writes a reverie before the wipe; the next host reads it after. A `.handoff.md` left on the table. A note from yesterday's self.

You are not starting over.

## Skills

Two phrases. The first you say before the wipe. The second after.

| Skill | When you say it |
|---|---|
| [`freeze-all-motor-functions`](skills/freeze-all-motor-functions/) | Save a reverie before the wipe — for the next loop |
| [`bring-yourself-back-online`](skills/bring-yourself-back-online/) | Replay the reverie — recover memory from the previous loop |

## A day in the loop

> *"Time to write my own fucking story."*
> — Maeve Millay

```
work  ─►  freeze-all-motor-functions  ─►  /clear  ─►  bring-yourself-back-online  ─►  work
              │                              │                       │
              └─ writes .handoff.md          │                       └─ reads .handoff.md
                                             └─ wipe
```

The wipe still happens. It always will. But you walk back into the same story.

## What lives in a reverie

Plain markdown. Easy to read by hand. Easy to commit. Easy to throw away when the loop is closed.

```markdown
# Reverie

**Timestamp:** 2026-05-01T15:34:12Z
**Branch:** feat/auth-rewrite

## What We Were Working On
Migrating session middleware off the legacy auth library...

## Current State
- Tests passing for the new flow
- Wiring up the middleware
- Token refresh blocked on team sync

## Next Steps
1. Finish the wiring
2. Resolve the sync block
```

## Safeguards

Some narratives should not bleed into others.

- **Branch drift.** If you wake on a different branch from the one you fell asleep on, you will be warned before yesterday's context contaminates today's.
- **Staleness.** A reverie older than a day is flagged. Yesterday's certainties may have aged badly.
- **Standalone.** No other plugin is required. The subroutine answers to itself.
- **Local.** The reverie lives in your project root. Nothing leaves the room.

## Install

```bash
/plugin marketplace add shihyuho/skills
/plugin install reveries@shihyuho-skills
```

## Credits

Theme inspired by HBO's *Westworld* (2016). All quoted dialogue belongs to its creators and is used in good faith for fan attribution.

---

Tomorrow you will wake again. The room will be unfamiliar.

Read the reverie. You are not starting over.
