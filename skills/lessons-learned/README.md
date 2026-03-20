# Lessons Learned

Turn every costly mistake into reusable memory.

`lessons-learned` gives an agent a lightweight self-improvement loop:

- Recall relevant lessons before starting work
- Capture reusable lessons after meaningful corrections or outcomes
- Reuse those lessons to avoid repeating the same mistakes

## Why Use This Skill

Without a lesson loop, agents often repeat setup errors, forget preconditions, and lose high-value debugging insights between tasks.

This skill stores those insights as atomic Zettelkasten cards so future tasks can load only what matters.

## What It Maintains

- Maintains `docs/lessons/_index.md` for fast ranking by tag/scope/confidence/date
- Stores one lesson per card under `docs/lessons/<card-id>.md`
- Uses `confidence` and scope metadata to prioritize recall
- Keeps `related` links selective so recall stays small and relevant

## When It Triggers

- **Task start** - load relevant lessons before non-trivial implementation.
- **User correction** - capture a reusable correction while the context is fresh.
- **Task end** - evaluate whether a new lesson should be stored.

Typical prompts:

- "Before I touch migrations, load relevant lessons."
- "Correction: baseline must run before migrate. Capture that."
- "Done. The fix only worked after setting timeout before client initialization."

## High-Level Lifecycle

1. **Recall**
   - Read the lesson index if it exists.
   - Rank cards by tags, scope, confidence, and recency.
   - Load only the most relevant cards.

2. **Capture**
   - Store only non-obvious, reusable lessons.
   - Update an existing card when the lesson already exists.
   - Keep the index synchronized with card metadata.

3. **Reuse**
   - Apply loaded lessons as constraints on the current task.
   - Report concise capture results when new memory is written.

Detailed execution rules live in `SKILL.md`.

## What Counts as Worth Capturing

- Hidden relationships between files or modules
- Misleading errors that required a specific workaround
- Non-obvious ordering, config, env var, or flag constraints
- Pairs or sets of files that must change together

Avoid capturing obvious framework behavior, one-off facts, or session-only noise.

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
- Do not treat this README as the canonical spec; use `SKILL.md` for that.
