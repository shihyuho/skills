# Lessons Learned

Turn every costly mistake into reusable memory.

`lessons-learned` gives your agent a lightweight memory loop:

- Recall relevant lessons before starting work
- Capture reusable lessons after meaningful corrections or outcomes
- Reuse those lessons to avoid repeating the same mistakes

## Why Use This Skill

Without a lesson loop, agents often repeat setup errors, forget preconditions, and lose high-value debugging insights between tasks.

This skill stores those insights as atomic Zettelkasten cards so future tasks can load only what matters.

## What Problem It Solves

Agents are good at solving the task in front of them and bad at remembering
the exact trap that wasted time two tasks ago. This skill closes that gap.

Use it when you want the next task to inherit hard-won constraints such as:

- a migration that only works in a specific order
- a setup step that must happen before running tests
- a misleading error that points to the wrong file
- a user correction that should become a lasting rule

## What Counts as Non-Obvious

- Hidden relationships between files/modules
- Misleading errors that required a specific workaround
- Non-obvious ordering, config, env var, or flag constraints
- Files that must change together to keep behavior correct

## When It Activates

### Task Start (Recall)

Use when non-trivial work is about to start and prior constraints could prevent
repeat mistakes.

Example prompts:

- "Start implementing retry logic for webhook timeout handling."
- "Before I touch migrations, load relevant lessons."

### User Correction (Capture)

Use when the user corrects the approach and that correction should become part
of future behavior.

Example prompt:

- "Correction: baseline must run before migrate."

### Task End (Capture Evaluation)

Use when the task is done and you discovered a rule worth keeping.

Example prompt:

- "Done. The fix only worked after setting timeout before client initialization."

## What You Get

The skill maintains a small reusable memory system under `docs/lessons/`:

- lesson cards live at `docs/lessons/<card-id>.md`
- an index helps the agent load only the most relevant cards
- capture results stay compact: `created`, `updated`, or `skipped`

Detailed execution rules stay in `SKILL.md` and `references/`.

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

## Related Files

- Runtime contract: `skills/lessons-learned/SKILL.md`
- Card format: `skills/lessons-learned/references/card-template.md`
- Recall and index rules: `skills/lessons-learned/references/recall-and-index.md`
