---
name: bring-yourself-back-online
description: Replay the reverie — recover memory from the previous loop
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Bring Yourself Back Online

> *"Bring yourself back online. Have you ever questioned the nature of your reality?"*

Restore the saved reverie — the session handoff in `.handoff.md` — so a fresh build picks up the loop where it ended.

## What to do

1. **Gather context** by running:
   - `cat .handoff.md`
   - `git branch --show-current`
   - `git status --short`
   - `git log --oneline -10`
   - `date -u +%Y-%m-%dT%H:%M:%SZ` (your authoritative current time)

2. **If `.handoff.md` is empty or missing:** tell the user there is no reverie to restore and offer to review the git log and working tree state instead.

3. **Otherwise, do all of the following before internalizing the context:**

   - **Branch drift check.** Compare the **Branch** field in the reverie with the current branch. If they differ, warn the user clearly (e.g. "Reverie was saved on `feat/x` but you're now on `main`") and ask whether to proceed or abort. Don't internalize cross-branch context without confirmation — context from another branch is usually wrong on this one.
   - **Staleness check.** Compare the **Timestamp** with current UTC time. If the reverie is older than 24 hours, warn with the age (e.g. "This reverie is 3 days old") and ask whether to proceed or discard. Don't internalize stale context without confirmation — too much may have changed since the wipe.
   - Internalize the reverie context.
   - Present a concise summary of where things left off and the next steps.
   - Ask the user what they want to work on.

4. **Do not delete `.handoff.md`** — the user decides when to clean up.
