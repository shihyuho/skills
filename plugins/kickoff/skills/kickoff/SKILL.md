---
name: kickoff
description: Re-read the approved SPEC or PLAN, then build it while silently maintaining a running implementation-notes file that records every design decision, deviation, tradeoff, and open question where the build diverges from or interprets the spec. Use when the user says "start work", "begin implementation", "let's build this", or "kick it off" to start implementing a plan or spec they have just reviewed, even when they do not name the spec file. This is the handoff from plan review to coding.
license: MIT
---

# Kickoff

The user just reviewed a SPEC or PLAN and handed it to you to build. Build from the *approved* document — not a half-remembered one — and leave its author a record of where the build diverged from it.

## On kickoff

**1. Re-read the spec.** Read the SPEC/PLAN in full from disk before touching code — the user likely edited it during review, so your context is stale. If you can't tell which document, or there are several, ask. If none exists, say so — kickoff assumes a reviewed plan.

**2. Open the notes file.** Unless the user already picked a format, ask: Markdown or HTML. Create `implementation-notes.md` (or `.html`) beside the spec — repo root if the spec lives there. Structure it however reads best; no fixed template — just keep the four kinds of note below distinct. If it already exists for this work, append rather than overwrite.

**3. Build, logging divergences as they happen.** Implement with whatever workflow fits. The moment the build departs from or interprets the spec, log an entry — then and there, not batched for the end, when the alternatives you weighed are forgotten.

## What to log

Four kinds of note, each answering a question the spec's author would ask:

- **Design decisions** — the spec was ambiguous or silent; this is what you chose.
- **Deviations** — you knowingly did other than what the spec says, because [reason].
- **Tradeoffs** — you weighed alternatives; you picked this one because [reason].
- **Open questions** — something for the user to confirm or revise.

The test: would the spec's author be surprised, or want a say? If yes, log it. If the spec determined the choice, or it's a routine detail, skip it — a notes file padded with the obvious goes unread.

## The log changes nothing

The notes file is an extra record alongside your work, never a driver of it. Build exactly as you would if it did not exist.

Don't pause to walk the user through it, and don't announce entries — they open it when they choose. Don't let it suppress anything either: whatever you would normally stop and raise — a blocking question, a decision you would surface anyway — you still raise, log or no log. Logging an open question is no substitute for asking one that genuinely blocks you.
