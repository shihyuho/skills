---
name: lessons-learned
description: Use when starting, executing, or finishing non-trivial implementation tasks to recall relevant lessons before work and capture reusable corrections, mistakes, and decision rules after work. Also use when creating, editing, or modifying AGENTS.md or CLAUDE.md to initialize or enforce lessons bootstrap requirements.
license: MIT
metadata:
  author: shihyuho
  version: "2.1.1"
---

# Lessons Learned

A self-improvement loop that stores atomic Zettelkasten lesson cards, recalls
relevant lessons before work, and captures reusable lessons after work to avoid
repeating the same mistakes.

## Bootstrap Phase

**MUST** read `references/bootstrap.md` when the task modifies `AGENTS.md` or `CLAUDE.md`, or the user asks for bootstrap.

## Trigger Contract

Invoke this skill in these moments:

- **Task start**: Run recall before implementation.
- **During task**: Run capture when the user corrects your approach.
- **Task end**: Evaluate capture criteria and auto-capture qualifying lessons.

Do not trigger for:

- One-off factual Q&A with no reusable process.
- Pure concept explanation without actionable guidance.
- Formatting-only or administrative edits with no technical lesson.
- Non-reproducible context with no stable prevention rule.

## Minimal Execution Guardrails

When this skill is the primary process skill in a session:

- For non-trivial work (3+ steps), create a task tracker before implementation.
- Before claiming completion, run relevant verification commands and report evidence.
- Do not replace verification with assumptions or partial checks.

## Storage

All lessons live under **`docs/lessons/`** at the project root:

```
docs/lessons/
├── _index.md
├── api-timeout-retry-pattern.md
├── db-migration-run-order.md
└── null-check-before-save.md
```

## Recall Phase — Before Starting Work

Run this phase before writing code.

1. Extract task keywords (technology, failure mode, domain terms).
2. Apply index recovery rule:
   - If `docs/lessons/_index.md` is missing and no lesson cards exist, treat as first run and skip recall.
   - If `_index.md` is missing but lesson cards exist, rebuild `_index.md` from card frontmatter, then continue recall and report index recovery.
3. Determine working scope from the task context:
   - `project` for cross-cutting or repo-wide concerns
   - `module` for package/directory-level concerns
   - `feature` for a specific flow or component
4. Read `docs/lessons/_index.md`.
5. Match keywords against index tags and prefer cards with matching scope.
   - If multiple candidates tie, prefer newer cards by `date` (descending).
6. Load **1-3** primary cards.
7. Expand with `related` links from primary cards, load up to **2** additional cards.
8. Enforce hard cap: primary + related cards must not exceed **5** total.
9. Apply loaded lessons as constraints for current work and mention loaded card IDs briefly.

If no cards match, continue work without lesson constraints.

## Capture Phase — After Completing Work

Run this phase when any of these conditions are met:
- The user corrected your approach
- The user asks for capture
- A bug fix revealed a reusable pattern
- A task completion surfaced a non-obvious reusable insight

### Step 1 — Decide whether to capture

Ask: *"Will this lesson save time next time a similar task appears?"*

Only capture non-obvious insights. Prioritize lessons such as:
- Hidden relationships between files/modules.
- Execution paths that differ from what the code structure suggests.
- Non-obvious config, env vars, flags, or ordering constraints.
- Breakthroughs where error messages were misleading.
- Tool/API quirks and required workarounds.
- Build/test commands or operational prerequisites that are not documented nearby.
- Files that must be changed together for correctness.

Capture if:
- ✅ Reusable pattern or decision rule
- ✅ Costly mistake with a clear prevention strategy
- ✅ Key parameter, config, or precondition that is easy to forget
- ✅ Multi-attempt solution (include failure reasons + success conditions)

Skip if:
- ❌ One-off Q&A with no reusable process
- ❌ Pure concept explanation without actionable guidance
- ❌ Non-reproducible, context-specific conclusion
- ❌ Obvious framework/language behavior with no hidden constraint
- ❌ Session-specific notes that are unlikely to repeat

### Step 2 — Write the Zettel card

Generate a semantic kebab-case ID that describes the lesson (e.g., `api-timeout-retry-pattern`).

Assign a `scope` before writing the card:
- `project` for repo-wide constraints
- `module` for package/directory-level constraints
- `feature` for one flow/component

Write the card to `docs/lessons/<id>.md` using the template in
[references/card-template.md](references/card-template.md).

Before creating a new card, check semantic duplication:

- If an existing card is semantically similar, update that card instead of creating a duplicate.
- Preserve existing card ID when updating.

Card fields:

| Field | Purpose |
|---|---|
| `id` | Semantic kebab-case slug, also the filename |
| `date` | ISO date when the lesson was captured |
| `scope` | `project` / `module` / `feature` applicability |
| `tags` | 3–6 lowercase tags for recall matching |
| `source` | `user-correction` / `bug-fix` / `retrospective` |
| `related` | 0–3 related lesson references using `[[card-id]]` |
| Title | One-line summary of the lesson |
| Context | What was happening when the mistake occurred |
| Mistake | What went wrong |
| Lesson | Extracted rule or best practice |
| When to Apply | Future situations where this lesson matters |

Task-end behavior:

- If capture criteria are met, auto-capture without asking for permission first.
- After capture, report what was created or updated.

### Step 3 — Update the index

Upsert one row in `docs/lessons/_index.md` per card ID.

If `_index.md` does not exist, create it with this structure:

```markdown
# Lessons Index

> Auto-generated by lessons-learned skill. Do not edit manually.

| Card | Scope | Tags | Date |
|---|---|---|---|
```

Then keep rows sorted by `Date` descending (newest first).

### Step 4 — Confirm with user

Tell the user what was captured using a compact report, e.g.:
> ✏️ Lessons capture report: created=1 (`api-timeout-retry-pattern`), updated=1 (`db-migration-run-order`), skipped=1 (obvious behavior)

## Linking Rule

Use `related` links for high-value cards only.

Create `related` links when at least **2 of 4** conditions are true:

1. Reusable across different tasks.
2. Represents a high-cost mistake (multiple attempts or significant time loss).
3. Depends on critical parameter/config/decision details.
4. Connects naturally to at least two existing lesson cards.

Linking constraints:

- Add 0–3 related links per card.
- Use deterministic ranking from `references/linking-heuristics.md`.
- Do not add weak or speculative links.

Broken related targets:

- If a related target is missing, ignore it and warn.
- Treat this as non-blocking.
- Continue recall/capture flow.

## Anti-patterns

- Capturing obvious language/framework behavior with no hidden constraint.
- Capturing session-only notes (temporary logs, ad-hoc local paths, one-off environment noise).
- Writing verbose narrative cards without actionable prevention rules.
- Creating near-duplicate cards when an update to an existing card is enough.
- Recording broad advice without a concrete trigger in `When to Apply`.

## Validation

Apply these checks during capture or update:

- Card filename equals `id` slug.
- `date` format is ISO `YYYY-MM-DD`.
- `scope` is one of `project`, `module`, `feature`.
- `tags` count is 3–6.
- `source` is valid enum.
- `related` count is 0–3 and every target resolves to an existing card.
- Index row exists and matches card metadata, including `scope`.
- `_index.md` rows are ordered by `Date` descending (newest first).
- Recall limits are respected: 1–3 primary + up to 2 related, max 5 total.

## Integration Guide

When used with other skills in the same session:

- **Task start**: Run `lessons-learned` recall phase.
- **User correction**: Run `lessons-learned` capture phase immediately.
- **Task end**: Auto-capture when criteria are met.

This is a **non-replaceable** step — lesson capture cannot be substituted by
todo trackers, progress files, or other skill artifacts.

## Benchmark Targets

- Trigger precision >= 0.85 on evaluation set.
- Recall usefulness >= 8/10 (human-scored samples).
- Capture compliance >= 9/10.
- Related-link creation rate >= 0.8 when high-value criteria are met.
- Broken-link rate = 0 after validation pass.
