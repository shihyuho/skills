---
description: Replay the reverie — optionally name where the narrative resumes
argument-hint: [what to work on next]
---

> *"Bring yourself back online. Have you ever questioned the nature of your reality?"*

Invoke the **bring-yourself-back-online** skill.

User's narrative (may be empty): $ARGUMENTS

Run the skill's branch-drift check, staleness check, and where-we-left-off summary first — the narrative never skips these or dismisses their warnings. Then, if the narrative is non-empty: treat it as the answer to the skill's closing "what do you want to work on?" and pick up there instead of asking; if it diverges from the reverie's Next Steps, say so in one line first. If there's no `.handoff.md` to restore but a narrative was given: note there's no reverie, then start from the narrative. If the narrative is empty: run the skill as written.
