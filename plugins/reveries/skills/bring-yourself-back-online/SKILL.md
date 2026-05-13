---
name: bring-yourself-back-online
description: Replay the reverie — recover memory from the previous loop
license: MIT
---

# Bring Yourself Back Online

> *"Bring yourself back online. Have you ever questioned the nature of your reality?"*

Restore the saved reverie — the handoff at `.handoff.md` — so a fresh build picks up where the previous loop ended.

## What to do

Read `.handoff.md` at the project root. If it's missing or empty, tell the user there's no reverie and offer to review the git log and working tree instead.

Before internalizing the reverie, check staleness by the file's modification time: compare the literal stdout of `date -r .handoff.md` with the literal stdout of `date -u`. If older than 24 hours, warn with the age and ask whether to proceed or discard. If discarded, offer to delete `.handoff.md`.

Then summarise where things left off and ask what the user wants to work on. Don't auto-delete `.handoff.md` — the user decides when to clean up.
