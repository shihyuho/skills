# Transcript: Capture - DB Schema Before Worker Restart

## Invocation Context

- **Skill invoked**: `lessons-learned` 
- **Phase**: Capture (correction-driven capture)
- **Trigger**: User provided a correction about deployment ordering

## User Input

The user provided the following correction:
- Task: "Correction: do not touch the cache layer first. In this repo the fix only works if the DB schema change lands before the worker restart, otherwise the worker reads an old column set and crashes."
- This is a reusable lesson about deployment ordering constraints

## Execution Steps

1. **Read skill files**: Loaded SKILL.md, card-template.md, and recall-and-index.md
2. **Check for duplicates**: Searched for existing lesson cards in docs/lessons/
3. **No existing cards found**: This is the first lesson card in this repository
4. **Created lesson card**: Used the card template to capture the reusable rule
5. **Created index**: Created docs/lessons/_index.md with the new card entry

## Card Created

- **ID**: `db-schema-before-worker-restart`
- **Location**: `/docs/lessons/db-schema-before-worker-restart.md`
- **Scope**: module
- **Tags**: db-schema, worker, deployment-order, cache, migration
- **Source**: user-correction
- **Confidence**: 0.7 (derived from source)

## Result

- **Outcome**: created
- **Files modified**: 
  - Created: docs/lessons/db-schema-before-worker-restart.md
  - Created: docs/lessons/_index.md
