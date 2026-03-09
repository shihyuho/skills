# User Notes

## Original User Request

"Before I refactor our migration runner, recall any relevant lessons. We had a bad incident last month where the baseline and migrate order mattered, and I do not want to repeat that."

## Key Information Provided by User

- **Task**: Refactor migration runner
- **Past incident**: Bad incident last month involving baseline and migrate order
- **Concern**: Order of baseline vs migrate operations

## Manual Insight (from user)

The user explicitly mentioned: **baseline and migrate order mattered**

This suggests:
- There is a specific order requirement: baseline must run before migrate
- This caused a "bad incident" meaning it led to failures or data issues

## Recommendations

1. **Before refactoring**: Verify the correct order (baseline → migrate) is maintained in any new implementation
2. **After refactoring**: If a reusable pattern or constraint is discovered, capture it as a lesson card
3. **Validation**: Test the migration runner with the known order dependency to ensure the refactor doesn't break it

---

*User notes captured during recall phase*
