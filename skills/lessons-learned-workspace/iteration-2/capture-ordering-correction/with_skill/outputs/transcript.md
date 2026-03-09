# Transcript: Lesson Capture

## Task
Capture a reusable lesson about DB schema changes and worker restart ordering.

## Input
- Correction: do not touch the cache layer first. In this repo the fix only works if the DB schema change lands before the worker restart, otherwise the worker reads an old column set and crashes.

## Recall Phase
- Checked for existing lesson cards in docs/lessons/
- No existing cards found

## Capture Phase
1. Created lesson card: db-schema-before-worker-restart.md
2. Created _index.md with card entry
3. Output files generated

## Files Created
- docs/lessons/db-schema-before-worker-restart.md
- docs/lessons/_index.md

## Output Location
/Users/matt/code/github.com/shihyuho/skills/.worktrees/lessons-learned-contract-redesign/skills/lessons-learned-workspace/iteration-2/capture-ordering-correction/with_skill/outputs/
