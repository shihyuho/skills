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

When the loop should continue somewhere else — the user worked in one directory but wants a fresh session to pick it up in another — write the reverie at the *target* tree's root instead (resolve it with `git -C <target> rev-parse --show-toplevel`), and stamp the reverie with that tree's coordinates rather than the current one's. That is the tree the reader re-enters and where `/wake` looks, so it must be a git tree; check its `.gitignore`, not the current tree's.

Unlike the current-tree case, don't silently replace an existing `.handoff.md` there — it may be another loop's pending memory, so show its branch and modification time and confirm before overwriting.

Suggest the skills to be used, if any, by the next session.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

If `.handoff.md` is not gitignored, remind the user and offer to add it to `.gitignore`.
