# Lesson Capture Result

## Summary

Captured 1 new lesson card from user correction.

## Created Cards

| ID | Scope | Source | Confidence |
|---|---|---|---|
| `db-schema-before-worker-restart` | project | user-correction | 0.7 |

## Card Details

### db-schema-before-worker-restart

**Title**: Apply DB schema changes before worker restart

**Tags**: db-schema, worker, restart-order, migration, cache

**Lesson**: DB schema changes must be applied BEFORE worker restart. If you restart the worker first, it will read the old column set from the cache and crash due to schema mismatch.

## Files Created

- `db-schema-before-worker-restart.md` (lesson card in docs/lessons/)

## Notes

This lesson applies to any scenario where:
- A worker process caches DB schema/column information
- Schema changes are being deployed
- The fix requires both DB migration AND worker restart

The critical ordering constraint: schema migration must complete and land BEFORE the worker restarts.
