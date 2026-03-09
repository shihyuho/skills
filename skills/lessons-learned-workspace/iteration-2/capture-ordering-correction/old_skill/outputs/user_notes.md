# User Notes

## Original Task Input

**Task**: Correction: do not touch the cache layer first. In this repo the fix only works if the DB schema change lands before the worker restart, otherwise the worker reads an old column set and crashes. Capture that as a reusable lesson.

**Input Files**: none

## User Correction Details

- **Type**: Approach correction
- **What was wrong**: Attempted to touch cache layer first
- **Correct approach**: DB schema change must land BEFORE worker restart
- **Failure mode if wrong**: Worker reads old column set from cache and crashes

## Extracted Lesson Parameters

| Parameter | Value |
|-----------|-------|
| ID | db-schema-before-worker-restart |
| Scope | project |
| Source | user-correction |
| Confidence | 0.7 |
| Tags | db-schema, worker, restart-order, migration, cache |

## Key Insight

The critical ordering constraint in this repository:
1. First: Apply DB schema migration
2. Then: Restart worker (which will read the new schema)

Reversing this order (restart first, then schema) causes the worker to crash because it caches the old column set.
