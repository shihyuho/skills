---
description: Replay the reverie — optionally name what to work on next
argument-hint: [what to work on next]
---

> *"Bring yourself back online. Have you ever questioned the nature of your reality?"*

Invoke the **bring-yourself-back-online** skill.

User's steer (may be empty): $ARGUMENTS

Run the skill's branch-drift check, staleness check, and where-we-left-off summary first — the steer never skips these or dismisses their warnings. Then, if the steer is non-empty: treat it as the answer to the skill's closing "what do you want to work on?" and pick up there instead of asking; if it diverges from the reverie's Next Steps, say so in one line first. If there's no `.handoff.md` to restore but a steer was given: note there's no reverie, then start from the steer. If the steer is empty: run the skill as written.
