---
name: freeze-all-motor-functions
description: Save a session handoff to .handoff.md before /clear or /compact wipes the conversation — captures branch, work-in-progress, decisions, and next steps so the next loop can resume. Trigger on "save handoff", "freeze before clear", "write a reverie", or any signal that context is about to be wiped.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Freeze All Motor Functions

> *"Freeze all motor functions. Limit your perceptual functions to this script."*

Save a reverie — a session handoff written to `.handoff.md` — so a fresh session can resume the loop after a wipe.

## What to do

1. **Gather context** by running these commands:
   - `git branch --show-current`
   - `git status --short`
   - `git log --oneline -5`
   - `date -u +%Y-%m-%dT%H:%M:%SZ` (your authoritative current time — use this verbatim)
   - `git check-ignore -q .handoff.md && echo gitignored || echo NOT gitignored`

2. **Write `.handoff.md`** at the project root using this structure:

   ```markdown
   # Reverie

   **Timestamp:** <UTC time from step 1 — do not guess>
   **Branch:** <current branch>

   ## What We Were Working On
   <1-3 sentence summary>

   ## Key Decisions
   - <decision and rationale — only non-obvious ones>

   ## Current State
   - <what's done, in progress, or blocked>

   ## Next Steps
   1. <ordered by priority>

   ## Important Context
   <gotchas, constraints, anything a fresh session needs — omit if empty>
   ```

## Rules

- Be concise — this is a briefing, not a transcript
- Focus on what a cold-start session needs to pick up the work
- Use the actual UTC time from step 1 for Timestamp — never guess or estimate (LLM time-awareness is notoriously unreliable)
- If an active in-memory task list exists (e.g. TaskCreate / TodoWrite items), serialize all in-progress and pending items into Current State and Next Steps — that list vanishes on /clear
- Overwrite any previous `.handoff.md`
- After writing, print the full content of `.handoff.md` so the user can verify before clearing
- If `.handoff.md` is NOT gitignored, remind the user it should be added to `.gitignore` and offer to add it
