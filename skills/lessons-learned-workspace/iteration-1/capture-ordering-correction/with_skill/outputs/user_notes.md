# User Notes

## Original Task Input

**Task**: Correction: do not touch the cache layer first. In this repo the fix only works if the DB schema change lands before the worker restart, otherwise the worker reads an old column set and crashes. Capture that as a reusable lesson.

**Input files**: none

**Save outputs to**: /Users/matt/code/github.com/shihyuho/skills/.worktrees/lessons-learned-contract-redesign/skills/lessons-learned-workspace/iteration-1/capture-ordering-correction/with_skill/outputs/

**Required files to save**: result.md, transcript.md, user_notes.md, metrics.json

## Interpretation

This is a **correction-driven capture** scenario where the user corrected the approach. The correction reveals a reusable rule about deployment ordering:

- DB schema changes must land before worker restart
- Cache layer changes should come after
- Otherwise the worker crashes due to reading old column set

## Lesson Extracted

When deploying changes involving both DB schema and worker/cache updates:
1. Apply DB schema changes first
2. Ensure workers restart and read new schema
3. Only then deploy cache layer changes
