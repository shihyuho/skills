---
name: freeze-all-motor-functions
description: Save a reverie before the wipe — for the next loop
license: MIT
---

# Freeze All Motor Functions

> *"Freeze all motor functions. Limit your perceptual functions to this script."*

Compact the current conversation into a reverie — a handoff at `.handoff.md` — so a fresh session can resume the loop after `/clear` or `/compact`.

## What to do

Write a handoff summarising the conversation to `.handoff.md` at the root of the current working tree (`git rev-parse --show-toplevel`) so a fresh agent can resume. If one exists, `rm -f .handoff.md` and write a fresh file.

The current working tree may be a linked git worktree rather than the main checkout. Writing the reverie there is deliberate — it keeps each worktree's handoff isolated so parallel tasks don't clobber each other's. But a fresh session after `/clear` loses all knowledge of which worktree it was in, so stamp the reverie's opening with its coordinates — the branch (`git branch --show-current`) and the absolute worktree root — so the reader can re-enter the right tree before resuming.

Suggest the skills to be used, if any, by the next session.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

If `.handoff.md` is not gitignored, remind the user and offer to add it to `.gitignore`.
