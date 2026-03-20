---
name: lessons-learned
description: Use when starting, executing, or finishing non-trivial implementation tasks where reusable constraints may matter. Recall relevant lessons before work, capture reusable corrections or discoveries during and after work, and keep project memory in `docs/lessons/`.
license: MIT
metadata:
  author: shihyuho
  version: "2.1.1"
---

# Lessons Learned

Use this skill to maintain a lightweight project memory loop.

Treat this file as the **single source of truth** for lesson-memory behavior:
trigger rules, recall flow, capture flow, limits, and validation.
`README.md`, `references/`, and phase-entry commands must not override those
rules.

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

Store all lesson artifacts under `docs/lessons/` at the project root:

```text
docs/lessons/
├── _index.md
├── api-timeout-retry-pattern.md
├── db-migration-run-order.md
└── null-check-before-save.md
```

Each lesson card is one atomic Zettelkasten note. Keep one reusable lesson per
card.

## Canonical Limits

Apply these limits everywhere in the skill package:

- Load **1-3** primary cards during recall.
- Load up to **2** related cards.
- Load at most **5** cards total.
- Use **0-2** `related` links per card.
- Use **3-6** tags per card.
- Keep `confidence` in the inclusive range `0.0-0.9`.

Use these canonical `confidence` values for new and edited cards:

- `0.0`
- `0.3`
- `0.5`
- `0.7`
- `0.9`

If another file conflicts with these limits, this file wins.

## Confidence Scoring

`confidence` represents application strength, not objective truth.

- A low-confidence lesson may still be valid, but should be applied cautiously.
- A high-confidence lesson should be treated as a stronger default unless the current context conflicts.
- `confidence` must not decay solely because a lesson was not used recently.

Use these canonical levels:

| Score | Meaning | Behavior |
|---|---|---|
| `0.0` | Inactive | Excluded from normal recall |
| `0.3` | Tentative | Suggested but not enforced |
| `0.5` | Moderate | Applied when relevant |
| `0.7` | Strong | Preferred unless context conflicts |
| `0.9` | Core | Treat as default project behavior |

For compatibility during transition work:

- Existing non-canonical values may remain temporarily.
- If an existing non-canonical value is edited, normalize it to the nearest canonical value.
- If a value is exactly between two canonical levels, normalize downward to the more conservative level.
- Do not perform a one-time bulk migration of untouched cards.

## Recall Phase

Run this phase before writing code.

1. Extract task keywords (technology, failure mode, domain terms).
2. Determine whether lesson storage exists:
   - If `docs/lessons/` does not exist, treat this as first-run state and skip recall.
   - If `docs/lessons/` exists but `_index.md` does not, rebuild `_index.md` from existing card frontmatter before recall.
3. Determine working scope from the task context:
   - `project` for cross-cutting or repo-wide concerns
   - `module` for package/directory-level concerns
   - `feature` for a specific flow or component
4. Read `docs/lessons/_index.md`.
5. Exclude cards with `confidence: 0.0` from normal recall.
   - They remain available only when the user explicitly asks to inspect inactive lessons.
6. Rank remaining candidates with this order:
   `tag match -> scope match -> confidence (desc) -> date (desc)`.
   - Legacy fallback: if a card has no `confidence`, derive it from `source`
      (`user-correction=0.7`, `bug-fix=0.5`, `retrospective=0.3`). If both
      are missing, use `0.3`.
7. Load **1-3** primary cards.
8. Expand with `related` links from primary cards, loading up to **2**
   additional cards.
9. Enforce the hard cap: primary plus related cards must not exceed **5**
   total.
10. Apply loaded lessons as constraints for current work and mention loaded card IDs briefly.

If no cards match, continue work without lesson constraints.

### Recall Warnings

Treat these as non-blocking and continue:

- `docs/lessons/` is missing on first run.
- `_index.md` had to be rebuilt.
- A loaded card is missing `confidence` and needs legacy fallback.
- A `related` target is missing.

## Capture Phase

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

Before writing a new card, check for a semantically similar existing card and
make the decision explicit:

- `decision=create` when no similar card exists.
- `decision=update` when a similar card already covers the same lesson.

Surface this decision in the capture output. Do not jump straight to card
content without stating whether you are creating or updating.

Assign a `scope` before writing the card:
- `project` for repo-wide constraints
- `module` for package/directory-level constraints
- `feature` for one flow/component

Assign initial `confidence` by `source`:
- `user-correction`: `0.7`
- `bug-fix`: `0.5`
- `retrospective`: `0.3`

When updating an existing card, choose the canonical `confidence` value that
best matches the new evidence.

- Small strengthening or weakening usually moves one canonical level.
- Strong validating or contradictory evidence may justify moving multiple levels.
- If a lesson should no longer participate in normal recall, move it directly to `0.0`.

Write the card to `docs/lessons/<id>.md` using the template in
`references/card-template.md`.

Before creating a new card, check semantic duplication:

- If an existing card is semantically similar, update that card instead of creating a duplicate.
- Preserve existing card ID when updating.

Minimal correction-capture example:

> Lessons capture report: decision=update, updated=1 (`db-migration-run-order`), confidence=0.7->0.5 (weaker applicability in current config)

Card fields:

| Field | Purpose |
|---|---|
| `id` | Semantic kebab-case slug, also the filename |
| `date` | ISO date when the lesson was captured |
| `scope` | `project` / `module` / `feature` applicability |
| `tags` | 3–6 lowercase tags for recall matching |
| `source` | `user-correction` / `bug-fix` / `retrospective` |
| `confidence` | Application strength for recall and default lesson use |
| `related` | 0–2 high-relevance lesson references using `[[card-id]]` |
| Title | One-line summary of the lesson |
| Context | What was happening when the mistake occurred |
| Mistake | What went wrong |
| Lesson | Extracted rule or best practice |
| When to Apply | Future situations where this lesson matters |

Task-end behavior:

- If capture criteria are met, auto-capture without asking for permission first.
- After capture, report what was created or updated.
- For normal user-facing output, prefer a short capture summary.
- Do not reproduce the full card body unless the user asks to inspect it.

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

> Lessons capture report: decision=create, created=1 (`api-timeout-retry-pattern`), confidence=none->0.5 (new reusable pattern)

If capture occurred, include the create-vs-update decision in the report when it
helps explain the outcome, for example `decision=create` or `decision=update`.

If `confidence` changed, include:

- the previous value
- the new value
- a brief reason

If `confidence` becomes `0.0`, explicitly state that the card is excluded from
normal recall.

Keep this confirmation short. Prefer the decision, the affected card ID, and a
one-line rule summary. Avoid dumping the full markdown card or index contents in
normal output.

## Linking Rule

Use `related` links for high-value cards only.

Create `related` links when at least **2 of 4** conditions are true:

1. Reusable across different tasks.
2. Represents a high-cost mistake (multiple attempts or significant time loss).
3. Depends on critical parameter/config/decision details.
4. Connects naturally to at least two existing lesson cards.

Linking constraints:

- Add 0–2 related links per card, only when relevance is strong.
- Use deterministic ranking from `references/linking-heuristics.md`.
- Do not add weak or speculative links.

Broken related targets are non-blocking:

- If a related target is missing, ignore it and warn.
- Continue recall/capture flow.

## Anti-patterns

- Capturing obvious language/framework behavior with no hidden constraint.
- Capturing session-only notes (temporary logs, ad-hoc local paths, one-off environment noise).
- Writing verbose narrative cards without actionable prevention rules.
- Creating near-duplicate cards when an update to an existing card is enough.
- Recording broad advice without a concrete trigger in `When to Apply`.

## Validation

Apply these checks during capture or update. These are blocking failures unless
explicitly listed as warnings elsewhere.

- Card filename equals `id` slug.
- `date` format is ISO `YYYY-MM-DD`.
- `scope` is one of `project`, `module`, `feature`.
- `tags` count is 3–6.
- `source` is valid enum.
- `confidence` is numeric and in range `0.0-0.9`.
- New and edited cards use canonical confidence values only: `0.0`, `0.3`, `0.5`, `0.7`, `0.9`.
- `related` count is 0–2 and every target resolves to an existing card.
- Index row exists and matches card metadata, including `scope`.
- `_index.md` rows are ordered by `Date` descending (newest first).
- Cards with `confidence: 0.0` are excluded from normal recall unless the user explicitly requests inactive lesson lookup.
- Recall limits are respected: 1–3 primary + up to 2 related, max 5 total.
- Capture reports include confidence transitions when confidence changed.

## Integration Guide

When used with other skills in the same session, follow the Trigger Contract as
the single source of truth:

- task start -> recall
- user correction during work -> capture
- task end -> capture evaluation

This is a **non-replaceable** step — lesson capture cannot be substituted by
todo trackers, progress files, or other skill artifacts.
