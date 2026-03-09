# User Notes - Lessons Learned Setup

## What Was Done

I've initialized the lessons-learned reminder for this project by:

1. **Analyzed existing AGENTS.md** - Found a minimal lessons-learned section with just "MUST use the lessons-learned skill before any execution"

2. **Created canonical reminder block** - A more comprehensive reminder that adds value without duplicating the existing wording. The canonical block includes:
   - Workflow explanation (before/during/after)
   - Explicit trigger conditions  
   - Storage location reference
   - Clear non-trigger list

3. **Captured a lesson** - Created a lesson card (`lessons-learned-initial-setup`) because setting up lessons-learned infrastructure is a reusable pattern that will save time on future projects

## The Canonical Reminder Block

You can add this to your AGENTS.md (or keep as reference):

```markdown
## Lessons Learned

This project uses the [lessons-learned](skills/lessons-learned/SKILL.md) skill for continuous improvement.

**Workflow**:
- **Before starting work**: Run recall to load relevant lessons
- **During work**: Capture lessons when you make mistakes or discover insights
- **After completing work**: Evaluate if captured lessons meet capture criteria

**Trigger Conditions**:
- Task start → invoke recall phase
- User correction → capture lesson
- Bug fix with reusable pattern → capture lesson
- Task end → evaluate capture criteria

**Storage**: All lessons are stored in `docs/lessons/` as Zettelkasten cards.

**Do not trigger for**:
- One-off factual Q&A
- Pure concept explanations
- Formatting-only edits
- Non-reproducible context
```

## Notes

- The existing AGENTS.md wording was preserved - no duplicates
- The canonical reminder adds substantial guidance beyond the minimal existing text
- A lesson card was created for this setup process (scope: project)
- All outputs are saved to the specified directory as requested

## Files Created

| File | Description |
|------|-------------|
| `result.md` | Main result summary |
| `transcript.md` | Detailed execution transcript |
| `user_notes.md` | This file |
| `metrics.json` | Execution metrics |
