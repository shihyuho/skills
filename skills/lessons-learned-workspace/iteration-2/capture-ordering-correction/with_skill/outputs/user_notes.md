# User Notes

## Original Correction

"Correction: do not touch the cache layer first. In this repo the fix only works if the DB schema change lands before the worker restart, otherwise the worker reads an old column set and crashes."

## Interpretation

The user corrected the approach for handling database schema changes in a worker-based system. The key insight is:

1. **Ordering matters**: DB schema migration must complete BEFORE worker restart
2. **Root cause**: Workers cache column metadata at startup; if schema changes before restart, the cached metadata is stale
3. **Failure mode**: Worker reads old column set and crashes

## Lesson Captured

When deploying schema changes to a database that is accessed by workers or services that cache column metadata:
- Always run database schema migrations BEFORE restarting workers
- The deployment order must be: schema change first, then worker restart
- If worker restarts before schema change lands, the worker will crash due to stale metadata

## Tags Applied
- db-migration
- worker
- restart
- ordering
- schema-change
