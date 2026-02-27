# Lessons Learned

Turn every costly mistake into reusable memory.

`lessons-learned` gives your agent a lightweight self-improvement loop:

- Recall relevant lessons before starting work
- Capture reusable lessons after meaningful corrections or outcomes
- Reuse those lessons to avoid repeating the same mistakes

## Why Use This Skill

Without a lesson loop, agents often repeat setup errors, forget preconditions, and lose high-value debugging insights between tasks.

This skill stores those insights as atomic Zettelkasten cards so future tasks can load only what matters.

## What It Does

- Maintains `docs/lessons/_index.md` for fast tag+scope recall (newest-first)
- Stores one lesson per card under `docs/lessons/<card-id>.md`
- Captures only non-obvious, reusable lessons
- Auto-captures qualifying lessons at task end
- Adds selective `related` links for high-value knowledge connections

## What Counts as Non-Obvious

- Hidden relationships between files/modules
- Misleading errors that required a specific workaround
- Non-obvious ordering, config, env var, or flag constraints
- Files that must change together to keep behavior correct

## When It Triggers

### Task Start (Recall)

Use when a new task begins and you want to preload relevant constraints.

Example prompts:

- "Start implementing retry logic for webhook timeout handling."
- "Before I touch migrations, load relevant lessons."

### User Correction (Capture)

Use when the user corrects approach and the correction is reusable.

Example prompt:

- "Correction: baseline must run before migrate."

### Task End (Capture Evaluation)

Use when finishing a task and a reusable rule emerged.

Example prompt:

- "Done. The fix only worked after setting timeout before client initialization."

### AGENTS/CLAUDE Policy Edits (Bootstrap)

Use when adding or enforcing project-level instruction blocks.

Example prompt:

- "Update AGENTS.md so lessons-learned is mandatory before execution."

Agent behavior: follow `references/bootstrap.md` to add canonical blocks without duplication.

## Recall and Capture Lifecycle

1. **Recall**
   - Determine task scope (`project` / `module` / `feature`)
   - Match task keywords to tags in `_index.md`
   - Prefer cards with matching scope
   - Break ties by `date` (newer first)
   - Load 1-3 primary cards
   - Optionally expand with up to 2 `related` cards
   - Apply those lessons as constraints

2. **Capture**
   - Evaluate whether the outcome is reusable and non-obvious
   - Auto-capture if criteria are met
   - Update or create card + index row
   - Report `created/updated/skipped` in a compact capture report

3. **Selective Linking**
   - Add `related` links only when high-value gate is met
   - Avoid speculative links
   - Cap at 3 related links per card

## File Layout

```text
docs/lessons/
├── _index.md
├── api-timeout-retry-pattern.md
└── db-migration-run-order.md
```

## Guardrails

- Do not read entire card corpus during recall.
- Do not capture obvious framework/language behavior.
- Do not capture one-off, non-reproducible facts.
- Do not capture session-only noise (temporary paths/logs/local artifacts).
- Do not create duplicate cards when an existing card can be updated.
