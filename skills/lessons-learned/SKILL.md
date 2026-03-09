---
name: lessons-learned
description: Recall relevant lessons before non-trivial work and capture reusable corrections after meaningful outcomes. Use this whenever starting implementation, debugging, refactoring, or planning work that could benefit from prior constraints, when the user corrects the approach, or when task completion reveals a reusable prevention rule.
license: MIT
metadata:
  author: shihyuho
  version: "3.0.0"
---

# Lessons Learned

Use this skill as a lightweight memory system for reusable prevention rules.
Store only lessons that will likely save time on future tasks.

## Trigger Contract

Invoke this skill in these situations:

- **Task-start recall** - before non-trivial implementation, debugging,
  refactoring, migration, or planning work.
- **Correction-driven capture** - when the user corrects the approach and the
  correction is reusable beyond the current task.
- **Task-end capture review** - when finishing work reveals a non-obvious rule,
  dependency, ordering constraint, or recovery pattern worth keeping.
- **Explicit setup requests** - when asked to initialize or repair the project
  instruction-file reminder for `AGENTS.md` or `CLAUDE.md`.

Repository policy that requires using this skill before execution should invoke
the recall gate. It does not imply setup or mandatory capture.

Do not trigger for:

- one-off factual answers with no reusable process
- pure concept explanation with no execution consequence
- formatting-only or administrative edits
- context that cannot produce a stable future rule
- generic note-taking or journaling requests

## Operating Model

- Treat lessons as reusable memory, not session logs.
- Store one lesson per card under `docs/lessons/`.
- Load only the most relevant cards for the current task.
- Prefer compact, actionable rules over narrative summaries.
- If no lesson qualifies for recall or capture, continue without forcing one.

All lesson storage and index details live in:

- [references/card-template.md](references/card-template.md)
- [references/recall-and-index.md](references/recall-and-index.md)

## Recall Workflow

Run recall before starting work when this skill is invoked for task-start recall
or when repository policy requires consulting lessons before execution.

1. Identify task keywords and the likely working scope.
2. Read and apply the index rules in
   [references/recall-and-index.md](references/recall-and-index.md).
3. Load only the selected lesson cards.
4. Convert loaded lessons into explicit working constraints for the current
   task.
5. Mention the loaded card IDs briefly when lessons were applied.

If no relevant lessons exist, continue without inventing constraints.

Repository policies such as "use `lessons-learned` before execution" are
satisfied by running this recall gate. They do not imply that a new lesson must
be captured.

## Capture Workflow

Run capture only when invoked for correction-driven capture or task-end capture
review.

First ask: will this lesson save time next time a similar task appears?

Capture when the outcome yields a reusable rule such as:

- a hidden file or module relationship
- a misleading error with a reliable recovery pattern
- a non-obvious config, flag, ordering, or environment constraint
- a set of files that must change together for correctness
- a repeated failure mode with a clear prevention rule

Skip capture when the result is:

- obvious framework or language behavior
- a one-off context-specific note
- temporary local noise such as ad-hoc paths or logs
- generic advice without a clear future trigger

When capture qualifies:

1. Write or update a card using
   [references/card-template.md](references/card-template.md).
2. Apply duplicate-handling and index-update rules from
   [references/recall-and-index.md](references/recall-and-index.md).
3. Report a compact result such as `created`, `updated`, or `skipped`.

Do not create a new card when an existing card can be updated without losing a
stable semantic ID.

## Integration Rules

### Phase Isolation

Execute only the requested phase for a given invocation:

- recall invocation -> recall only
- capture invocation -> capture only
- setup invocation -> setup only

Do not assume that every invocation runs the full lifecycle.

### Setup Entry Point

When the user explicitly asks to initialize or repair project instructions,
run this setup flow:

1. Check `AGENTS.md` and `CLAUDE.md` at the project root.
2. Treat each existing file as a target file.
3. If neither file exists, ask which file to create at project root and use it
   as the target.
4. Ensure each target contains exactly one canonical lessons block:

   ```markdown
   ## Lessons Learned

   **MUST** use the `lessons-learned` skill before any execution
   ```

5. If equivalent mandatory wording already exists, keep one canonical block and
   remove duplicates.

This setup path is explicit-only. Do not run it just because repository policy
requires consulting lessons before execution.

### Composition with Other Skills

This skill may provide prior constraints to other process skills, but it does
not replace their main responsibilities.

- brainstorming owns design
- writing-plans owns implementation planning
- debugging skills own root-cause analysis
- implementation skills own code and file changes

`lessons-learned` only contributes reusable memory before work and captures new
reusable rules after meaningful outcomes.

### Minimal Guardrails

When this skill is the primary process skill in a session:

- create a task tracker for non-trivial work
- verify relevant commands before claiming success
- do not substitute assumptions for verification evidence

## Validation

Before considering recall or capture complete, confirm:

- `SKILL.md` governs trigger, phase, integration, and validation rules
- `references/card-template.md` owns card structure and card-local validation
- `references/recall-and-index.md` owns index, ranking, recovery, dedupe, and
  related-expansion behavior
- broken related links are treated as non-blocking and cleaned up according to
  reference rules
- recall limits are respected and capture reports stay compact

If the references and `SKILL.md` disagree, treat `SKILL.md` as the governing
contract.
