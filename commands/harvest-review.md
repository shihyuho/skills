---
description: "Review relevant Harvest lessons before work using existing index and lessons MOC."
---

Read lesson sources and return a concise pre-work brief.

## Read Sources

1. `docs/notes/00-INDEX.md` (if exists)
2. `docs/notes/mocs/lessons-learned.md` (if exists)
3. Recent context files referenced by index/lessons links (if needed)

## Selection Heuristic

Select lessons most relevant to the current task by:
- matching stable lesson IDs/anchors first (`LL-*`)
- same technology/framework
- same operation type (async/state/API/integration)
- similar error pattern
- source-note evidence relevance when lessons originated from planning snapshots

## Output

- 3 to 7 bullets max
- each bullet includes: `LL-*` (if available) + lesson title + why relevant + context link
- if no lessons match, state that clearly and suggest running `/harvest-capture` after the task

Do not write or modify files in this command.
