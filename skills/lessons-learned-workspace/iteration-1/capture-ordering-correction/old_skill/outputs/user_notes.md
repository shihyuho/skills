# User Notes

## Original Task Input

> Correction: do not touch the cache layer first. In this repo the fix only works if the DB schema change lands before the worker restart, otherwise the worker reads an old column set and crashes. Capture that as a reusable lesson.

## Key Points Captured

1. **The core insight**: DB schema changes must be applied BEFORE worker restart
2. **The mistake**: Touching the cache/query layer first, before the schema change lands
3. **The failure mode**: Worker reads old column set and crashes when code expects new columns

## Lesson Summary

This is a deployment ordering lesson. In systems with:
- Database layer (with schema)
- Worker layer (reads schema at startup)
- Cache/query layer (updated code)

The correct order is:
1. Apply DB schema migration
2. Wait for migration to complete
3. Restart worker (so it reads new schema)
4. Then update cache/query layer if needed

The user's correction emphasizes that in this specific repo, the cache layer fix only works if the DB schema change has already landed AND the worker has been restarted.

## Files Created

- `/outputs/result.md` - The lesson card
- `/outputs/transcript.md` - Capture process documentation
- `/outputs/user_notes.md` - This file
- `/outputs/metrics.json` - Capture metrics
