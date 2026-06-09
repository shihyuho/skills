---
name: freeze-all-motor-functions
description: Save a reverie before the wipe — for the next loop
license: MIT
---

# Freeze All Motor Functions

> *"Freeze all motor functions. Limit your perceptual functions to this script."*

Compact the current conversation into a reverie — a handoff at `.handoff.md` — so a fresh session can resume the loop after `/clear` or `/compact`.

## What to do

Write a handoff summarising the conversation to `.handoff.md` at the project root so a fresh agent can resume. If one exists, `rm -f .handoff.md` and write a fresh file.

Suggest the skills to be used, if any, by the next session.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

If `.handoff.md` is not gitignored, remind the user and offer to add it to `.gitignore`.
