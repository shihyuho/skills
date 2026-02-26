---
name: workflow-orchestration
description: Use when coordinating non-trivial implementation work, executing implementation plans, or modifying AGENTS.md/CLAUDE.md.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Workflow Orchestration

## Prerequisites

**MUST** read `references/bootstrap.md` when the task modifies `AGENTS.md` or `CLAUDE.md`.

## Workflow

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update `docs/tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project
- This lessons update is NON-REPLACEABLE, even when other process skills are active

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Create a task tracker with checkable items before implementation.
2. **Cross-Skill Compatibility (Task Tracker)**: If another active skill defines its own task-tracking artifact, respect that artifact as the primary tracker (this may replace `docs/tasks/todo.md`).
3. **Verify Plan**: Check in before starting implementation.
4. **Track Progress**: Mark items complete as you go.
5. **Explain Changes**: Provide a high-level summary at each step.
6. **Document Results**: Record a final review in the active task-tracking artifact.
7. **Capture Lessons (Hard Requirement)**: Update `docs/tasks/lessons.md` after corrections. This cannot be replaced by `todo`, `progress`, `findings`, or any other skill artifact.

## Cross-Skill Priority

- **Task tracking**: Follow the active skill's tracker format when multiple process skills are loaded.
- **Lessons**: `docs/tasks/lessons.md` is always required for user corrections while this skill is active.

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
