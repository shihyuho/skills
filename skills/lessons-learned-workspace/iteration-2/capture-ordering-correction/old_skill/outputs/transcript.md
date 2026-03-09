# Execution Transcript

## Phase 1: Recall (Before Work)

**Context**: Task involves fixing a deployment issue with cache layer and DB schema.

### Index Recovery
- Checked for `docs/lessons/_index.md` - not found
- No existing lesson cards in this repository snapshot

### Recall Results
- No cards to load (first run / empty lessons library)
- Proceeded to implementation without lesson constraints

## Phase 2: Work Execution

**Task**: Implement fix for cache layer issue

**Action Taken**: Attempted to touch cache layer first

**Correction Received**: 
> "do not touch the cache layer first. In this repo the fix only works if the DB schema change lands before the worker restart, otherwise the worker reads an old column set and crashes."

## Phase 3: Capture (After Correction)

### Step 1: Decide Whether to Capture

**Question**: "Will this lesson save time next time a similar task appears?"

**Decision**: YES - This is a critical ordering constraint that is non-obvious and would cause a crash if violated.

**Rationale**:
- ✅ Reusable pattern (DB schema + worker restart ordering)
- ✅ Costly mistake prevention (worker crash)
- ✅ Non-obvious constraint (cache layer behavior)
- ✅ Specific precondition (schema must land before restart)

### Step 2: Write the Zettel Card

**Card ID**: `db-schema-before-worker-restart`

**Scope**: `project` (applies to entire repository)

**Source**: `user-correction` (user pointed out the mistake)

**Confidence**: 0.7 (initial from source)

**Tags**: db-schema, worker, restart-order, migration, cache

**Content**:
- **Context**: Working on a fix that involves both DB schema changes and worker restart
- **Mistake**: Attempted to touch cache layer first, ignoring the critical ordering constraint
- **Lesson**: DB schema changes must be applied BEFORE worker restart. If worker restarts first, it reads cached old column set and crashes
- **When to Apply**: When deploying schema migrations alongside worker restarts; whenever cache layer interacts with dynamic DB schema

### Step 3: Update Index

- Created `docs/lessons/_index.md` with new card entry

### Step 4: Confirm with User

> ✏️ Lessons capture report: created=1 (`db-schema-before-worker-restart`), updated=0, skipped=0
