---
name: bring-yourself-back-online
description: Replay the reverie — recover memory from the previous loop
license: MIT
---

# Bring Yourself Back Online

> *"Bring yourself back online. Have you ever questioned the nature of your reality?"*

Restore the saved reverie — the handoff at `.handoff.md` — so a fresh build picks up where the previous loop ended.

## What to do

Locate the reverie. It lives in `.handoff.md` at the root of a working tree — but a fresh session after `/clear` no longer knows whether the previous loop ran in the main checkout or in a linked git worktree, so don't assume the current directory. Run `git worktree list --porcelain` to enumerate every working tree (the main checkout plus any linked worktrees) and look for `.handoff.md` at each one's root.

- None found → tell the user there's no reverie and offer to review the git log and working tree instead.
- Exactly one → use it.
- Several → list each with its branch and modification time, and ask which to resume.

If the reverie sits in a worktree other than the current working directory, say so and switch into that worktree (make its root the working directory) before resuming — its opening records the branch and worktree root. Otherwise the build would resume in the wrong tree.

Before internalizing the reverie, check staleness by the located file's modification time: compare the literal stdout of `date -r <path>` with the literal stdout of `date -u`. If older than 24 hours, warn with the age and ask whether to proceed or discard. If discarded, offer to delete that file.

Then summarise where things left off and ask what the user wants to work on. Don't auto-delete the reverie — the user decides when to clean up.
