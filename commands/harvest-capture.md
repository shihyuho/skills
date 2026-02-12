---
description: "Capture the current conversation into Harvest second brain with smart merge and index updates."
---

Invoke the `harvest` skill and follow it exactly.

Run the full capture flow for the current conversation:
- detect `context_id`
- create or smart-merge context note
- update `docs/notes/00-INDEX.md`
- update lesson/topic MOCs when relevant
- enforce merge-stable entries (`D-*`, `Q-*`, `LL-*`) with preserved anchors
- when planning files are used as sources, store medium-density snapshots (`conclusion + evidence + source note`) instead of full copies
- avoid wikilinks to files outside `docs/notes/` vault scope

Follow confirmation rules from the skill before writing files.

Finish with a compact result summary listing created, updated, and skipped files.
