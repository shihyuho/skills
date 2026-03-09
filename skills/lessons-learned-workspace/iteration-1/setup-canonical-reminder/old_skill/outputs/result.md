# Lessons Learned Setup - Canonical Reminder

## Task Summary
Initialize the lessons-learned reminder for the project. The project already has an AGENTS.md with a brief lessons-learned section, but requires the canonical reminder block without duplicate wording.

## Recall Phase
- **Status**: Executed
- **Result**: No existing lesson cards found in `docs/lessons/`. No cards to recall.
- **Cards Loaded**: 0 (expected - first-time setup)

## Execution

### Analysis of Existing AGENTS.md
The existing AGENTS.md contains:
```
## Lessons Learned
**MUST** use the `lessons-learned` skill before any execution
```

This is a minimal trigger statement. The canonical reminder block should provide more context without duplicating this wording.

### Canonical Reminder Block Created

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

### Key Differences from Existing Wording
- Adds workflow explanation (before/during/after)
- Lists trigger conditions explicitly
- Explains storage location
- Clarifies what NOT to trigger for

## Capture Phase Decision
- **Capture Needed**: Yes
- **Reason**: Setting up lessons-learned infrastructure is a reusable pattern that will save time on future projects
- **Scope**: `project` (repo-wide concern)

## Lesson Card Created
A lesson card was generated for this setup process:

- **ID**: `lessons-learned-initial-setup`
- **Location**: `docs/lessons/lessons-learned-initial-setup.md`
- **Scope**: project
- **Tags**: setup, lessons-learned, workflow, initialization
- **Confidence**: 0.7 (user-correction source)

## Output Location
All files saved to:
`skills/lessons-learned-workspace/iteration-1/setup-canonical-reminder/old_skill/outputs/`

## Files Produced
1. `result.md` - This file
2. `transcript.md` - Execution transcript
3. `user_notes.md` - User-facing notes
4. `metrics.json` - Execution metrics
