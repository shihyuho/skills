---
name: freeze-all-motor-functions
description: Save a reverie before the wipe — for the next loop
license: MIT
---

# Freeze All Motor Functions

> *"Freeze all motor functions. Limit your perceptual functions to this script."*

Save a reverie — a session handoff written to `.handoff.md` — so a fresh session can resume the loop after a wipe.

## What to do

1. **Survey what's about to be lost.** `/clear` wipes RAM, not disk — a useful reverie captures what only lives in RAM right now. Pull from all three sources:

   **Repository ground truth** (run these — cheap baseline):
   - `git branch --show-current`
   - `git status --short`
   - `git stash list`
   - `git worktree list`
   - `git log --oneline -5`
   - `date -u +%Y-%m-%dT%H:%M:%SZ` (your authoritative timestamp — use verbatim)
   - `git check-ignore -q .handoff.md && echo gitignored || echo NOT gitignored`

   **Volatile in-memory state** (reflect — these vanish on `/clear`):
   - Active task list (TaskCreate / TodoWrite — every in-progress and pending item)
   - Background or scheduled work you spawned (Agent runs, Crons, Monitors, ScheduleWakeups)
   - Decisions made in conversation, with rationale — including approaches you rejected
   - Failures and dead-ends — what you tried that didn't work, so the next loop doesn't repeat them
   - User constraints / preferences expressed verbally ("don't touch schema", "skip prod")
   - Findings from tool output (Read, Grep, WebFetch, build/test results) that informed your current direction but aren't yet written to any file

   **External coupling** (skip if none):
   - Open PRs / issues / deployments / CI runs tied to this work

   The commands are a floor, not a ceiling — if something matters and falls outside them, capture it.

2. **Write `.handoff.md`** at the project root using this structure:

   ```markdown
   # Reverie

   **Timestamp:** <UTC time from step 1 — do not guess>
   **Branch:** <current branch>

   ## What We Were Working On
   <1-3 sentence summary>

   ## Key Decisions
   - <decision and rationale — only non-obvious ones>

   ## What We Tried That Didn't Work
   - <failed approach + why — omit if empty>

   ## Current State
   - <what's done, in progress, or blocked>

   ## Next Steps
   1. <ordered by priority>

   ## Important Context
   <constraints, gotchas, user preferences, anything a fresh session needs — omit if empty>
   ```

3. **Self-check before printing.** Can a fresh session answer all five from your `.handoff.md` alone?
   - Where am I? (branch + current state)
   - Where am I going? (next steps)
   - What's the goal? (what we were working on)
   - What have I learned? (key decisions + important context)
   - What have I already tried that failed? (don't repeat — saves the next loop's tokens)

   If any answer would require re-doing work, expand the relevant section.

## Rules

- Be concise — this is a briefing, not a transcript
- Focus on what a cold-start session needs to pick up the work
- Use the actual UTC time from step 1 for Timestamp — never guess or estimate (LLM time-awareness is notoriously unreliable)
- Overwrite any previous `.handoff.md`
- After writing, print the full content of `.handoff.md` so the user can verify before clearing
- If `.handoff.md` is NOT gitignored, remind the user it should be added to `.gitignore` and offer to add it
