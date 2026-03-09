# Capture Result

**Result**: created

A new lesson card was created for the DB schema/worker ordering lesson.

## Details

- **Card ID**: db-schema-before-worker-restart
- **Source**: user-correction
- **Confidence**: 0.7
- **Scope**: module

## Summary

The lesson captures the constraint that DB schema changes must land before worker restart, otherwise the worker reads stale column metadata and crashes.
