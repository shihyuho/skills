# Lessons Learned Capture Transcript

## Session Information

- **Date**: 2026-03-10
- **Skill**: lessons-learned (baseline snapshot v2.1.1)
- **Task Type**: Capture (correction)
- **Working Directory**: /Users/matt/code/github.com/shihyuho/skills/.worktrees/lessons-learned-contract-redesign

## Trigger

User provided a correction about deployment ordering:
> "Correction: do not touch the cache layer first. In this repo the fix only works if the DB schema change lands before the worker restart, otherwise the worker reads an old column set and crashes. Capture that as a reusable lesson."

## Execution Steps

### Step 1: Recall Phase
- **Status**: Skipped
- **Reason**: This is a capture task (correction from user), not a recall task

### Step 2: Capture Decision
- **Question**: "Will this lesson save time next time a similar task appears?"
- **Answer**: Yes
- **Rationale**:
  - This is a reusable pattern about deployment ordering
  - The mistake (touching cache first) is non-obvious
  - The prevention rule (schema before restart) is actionable
  - This applies to any system with DB + worker architecture

### Step 3: Write Zettel Card
- **Card ID**: `db-schema-before-worker-restart`
- **Scope**: `project` (applies to entire deployment process)
- **Source**: `user-correction` (user explicitly corrected the approach)
- **Confidence**: `0.7` (initial value for user-correction)
- **Tags**: database, migration, deployment, worker, ordering

### Step 4: Update Index
- **Status**: Deferred
- **Note**: Per task requirements, outputs saved to iteration-specific directory

## Output Files

1. **result.md**: Lesson card in Zettel format
2. **transcript.md**: This file - documentation of capture process
3. **user_notes.md**: Session-specific notes
4. **metrics.json**: Capture metrics

## Validation Checks

- ✅ Card filename equals `id` slug: `db-schema-before-worker-restart.md`
- ✅ `date` format is ISO: `2026-03-10`
- ✅ `scope` is valid: `project`
- ✅ `tags` count is 3-6: 5 tags
- ✅ `source` is valid enum: `user-correction`
- ✅ `confidence` is numeric in range: `0.7`
- ✅ `related` count is 0-2: 0 (no strong related cards found)
