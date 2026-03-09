# User Notes: Migration Runner Refactor Recall

## Original Request

"Before I refactor our migration runner, recall any relevant lessons. We had a bad incident last month where the baseline and migrate order mattered, and I do not want to repeat that."

## Context Extracted

- **Task**: Refactor migration runner
- **Past incident**: Bad incident last month involving baseline and migrate order
- **User concern**: The order of baseline vs migrate operations matters
- **User goal**: Avoid repeating the past incident

## User's Manual Insight

The user explicitly mentioned:
- **"baseline and migrate order mattered"**
- Known constraint: **baseline must run before migrate**

## Observations

1. **No stored lessons**: The lessons-learned system has no cards stored in `docs/lessons/`
2. **First run scenario**: No previous lessons have been captured
3. **Example reference exists but not actual file**: The skill's README references `db-migration-run-order.md` but this file doesn't exist
4. **Previous iteration confirmed**: Iteration-1 recall for the same task also found no stored lessons

## Recommendations for User

1. **Before refactoring**: Verify the correct order (baseline → migrate) is maintained in any new implementation
2. **During refactoring**: Document any specific ordering constraints discovered
3. **After refactoring**: If the refactor reveals a specific prevention rule, capture it using the lessons-learned skill

## Next Steps

Proceed with the migration runner refactoring. Since no stored lessons exist, rely on the user's manual insight: **baseline must run before migrate**. Consider capturing a lesson card after the refactor if specific code patterns or configurations emerge as reusable prevention rules.
