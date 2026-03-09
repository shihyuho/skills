---
id: db-schema-before-worker-restart
date: 2026-03-10
scope: project
tags: [database, migration, deployment, worker, ordering]
source: user-correction
confidence: 0.7
related: []
---

# DB schema changes must land before worker restart

## Context

In a system with a database layer and worker layer, attempting to fix a schema-related issue by updating the cache/query layer first causes the worker to crash. The worker reads an old column set from the database but the new query layer expects different columns, creating a mismatch.

## Mistake

Attempted to fix the cache/query layer first without ensuring the DB schema change had already been applied and the worker had restarted with the new schema expectations.

## Lesson

- **Always apply DB schema changes before restarting workers that depend on those schemas**
- The worker reads column definitions from the database at startup or refreshes them periodically
- If the worker restarts before the schema change lands, it reads the old column set and crashes when the code expects new columns
- Deployment order: database migration → verify complete → then restart workers
- Do not touch the cache layer first - the root cause is the DB schema not matching worker expectations

## When to Apply

- When fixing schema-related bugs in systems with separate database and worker components
- When deployment involves cache layer updates and database schema changes
- Any scenario where worker restart could read stale schema definitions
