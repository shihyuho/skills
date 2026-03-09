---
id: db-schema-before-worker-restart
date: 2026-03-10
scope: module
tags: [db-schema, worker, deployment-order, cache, migration]
source: user-correction
confidence: 0.7
related: []
---

# Apply DB schema changes before worker restart

## Context

When redesigning a system with both DB schema and cache layer changes, the initial approach was to modify the cache layer first.

## Mistake

Touching the cache layer before the DB schema change lands causes the worker to crash. The worker reads an old column set from the DB while the cache expects new data, causing a mismatch.

## Lesson

- Apply DB schema changes first and ensure they land before worker restart
- Only after DB schema is updated and workers have restarted should cache layer changes be deployed
- This ensures workers read the correct column set from the DB first

## When to Apply

When deploying changes that involve both DB schema modifications and worker/cache layer updates. Always prioritize DB schema changes and worker restarts before cache invalidation or changes.
