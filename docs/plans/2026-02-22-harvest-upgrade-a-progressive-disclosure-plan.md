# Harvest Upgrade A Implementation Plan

## Scope

Implement only Upgrade A: progressive disclosure reading strategy for `harvest` notes consumption.

In scope:

- Add a deterministic read workflow for large `docs/notes` sets.
- Keep current capture/publish/dedupe contracts unchanged.
- Keep command files thin and non-authoritative.

Out of scope:

- Hook automation changes (Upgrade B).
- Citation ID system changes (Upgrade C).
- Any plugin runtime behavior changes.

## Objective

Reduce token usage and retrieval drift when an agent needs historical context from `docs/notes` by enforcing a fixed read order.

## Current Baseline

Existing harvest contract already defines deterministic capture, extraction boundaries, anti-recursion, and fingerprint dedupe:

- `skills/harvest/SKILL.md`
- `commands/harvest*.md`

This plan adds a retrieval/read layer only.

## Proposed Design

### A1. Add "Progressive Disclosure Read Workflow" to SKILL contract

Add one new section in `skills/harvest/SKILL.md`:

- Name: `## Progressive Disclosure Read Workflow (Required)`
- Purpose: define default reading order when querying existing second-brain notes.

Required sequence:

1. Read `docs/notes/index.md` first.
2. Read hub pages second (`docs/notes/projects.md`, `docs/notes/decisions.md`, `docs/notes/knowledge.md`) based on query intent.
3. Read only targeted leaf notes third (timeline day file, decision note, or knowledge note).

Hard constraints:

- Never start from deep leaf files unless user gives exact path.
- Never treat `docs/notes` as source-of-truth input for new capture.
- Preserve anti-recursion guard.

### A2. Add trigger wording for read scenarios

Extend trigger guidance in `skills/harvest/SKILL.md` with read-intent cues:

- "find prior decision"
- "look up past context"
- "trace project timeline"
- "retrieve existing second-brain note"

This clarifies when the new read workflow applies.

### A3. Keep commands unchanged unless reference pointers are needed

Command files in `commands/harvest*.md` remain thin entrypoints.

Only update if needed to reference the new SKILL section title; do not duplicate workflow details in commands.

### A4. Add one reference example file

Create a concise reference doc under `skills/harvest/references/`:

- Suggested file: `progressive-disclosure-read-example.md`

Content:

- one "decision lookup" example
- one "timeline investigation" example
- one "knowledge pattern retrieval" example

Each example must show: query intent -> file read order -> stop condition.

## Implementation Steps

1. Update `skills/harvest/SKILL.md` with new read workflow section and trigger cues.
2. Add reference example file under `skills/harvest/references/`.
3. Verify command files still follow thin-entrypoint design.
4. Run skill validation:

```bash
npx --yes skills-ref validate ./skills/harvest
```

5. Manual consistency check:
   - Ensure no conflict with `Source Extraction Boundaries`.
   - Ensure no conflict with `Anti-Recursion Guard`.
   - Ensure no capture contract drift.

## Acceptance Criteria

- `SKILL.md` contains explicit progressive-disclosure read order.
- Read workflow is deterministic and uses fixed default sequence.
- Source-of-truth contract remains unchanged (`task_plan.md`, `findings.md`, `progress.md`).
- Command files do not duplicate workflow logic.
- `skills-ref validate` passes for `skills/harvest`.

## Risks and Mitigations

- Risk: read workflow accidentally encourages using notes as SOT input.
  - Mitigation: explicitly restate SOT-only rule in new section.

- Risk: section bloat in `SKILL.md` reduces clarity.
  - Mitigation: keep section short; move examples to `references/`.

- Risk: ambiguous stop condition causes over-reading.
  - Mitigation: define stop condition as "stop when target note or two consecutive non-novel reads".

## Rollout

Phase 1 (docs only): add section + examples.

Phase 2 (verification): run validator + manual retrieval walkthrough using existing notes.

No runtime/plugin changes in this upgrade.
