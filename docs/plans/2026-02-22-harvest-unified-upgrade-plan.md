# Harvest Unified Upgrade Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Consolidate the three 2026-02-22 harvest proposals into one execution-ready plan that improves determinism, retrieval quality, and anti-noise behavior without changing the source-of-truth contract.

**Architecture:** Keep `skills/harvest/SKILL.md` as the single behavior authority, keep `commands/harvest*.md` as thin entrypoints, and move detailed examples into `skills/harvest/references/`. Roll out in phased docs-first changes: retrieval workflow first (Upgrade A), then deterministic capture hardening, then structured outputs and guardrail hardening.

**Tech Stack:** Markdown skill specs (`SKILL.md`), command entrypoints (`commands/harvest*.md`), `skills-ref` validator, Obsidian-compatible notes templates.

---

## Intent and Consolidation Scope

This plan unifies:

- `docs/plans/2026-02-22-harvest-strengthening-plan.md`
- `docs/plans/2026-02-22-harvest-capture-heuristics-from-claude-mem.md`
- `docs/plans/2026-02-22-harvest-upgrade-a-progressive-disclosure-plan.md`

into one sequence that can be executed with minimal ambiguity.

In scope:

- Progressive-disclosure retrieval order for reading existing `docs/notes`.
- Deterministic capture hardening (`sot_fingerprint`, canonical source pointers, extraction thresholds).
- Structured mode outputs (`status/audit/review/optimize`) that remain human-readable.
- Anti-recursion and denylist hardening.
- References/examples updates needed to keep `SKILL.md` concise.

Out of scope:

- Plugin runtime or external service implementation.
- Forced migration of existing `docs/notes` artifacts.
- Repository-wide conventions unrelated to `harvest`.

## Current Baseline (Verified)

Current `skills/harvest/SKILL.md` already defines:

- Source-of-truth boundary (`task_plan.md`, `findings.md`, `progress.md`).
- Deterministic workflow: preflight -> bootstrap -> extract -> classify -> publish -> verify.
- Dedupe rule using `sot_fingerprint`.
- Source extraction boundaries and anti-recursion guard.

Current `commands/harvest*.md` are thin entrypoints and mostly compliant with non-authoritative design.

## Unified Design Decisions

### Decision 1: Keep Upgrade A as Phase 1 (Recommended)

Add required progressive-disclosure retrieval sequence before any deeper hardening:

1. Read `docs/notes/index.md`.
2. Read intent-specific hub page(s):
   - `docs/notes/projects.md`
   - `docs/notes/decisions.md`
   - `docs/notes/knowledge.md`
3. Read only targeted leaf note(s).

Stop condition:

- Stop when target note is found, or after two consecutive non-novel reads.

Hard constraints:

- Never begin from deep leaves unless user provides exact path.
- Never treat `docs/notes` as source input for new capture.
- Preserve anti-recursion guard.

### Decision 2: Adopt claude-mem-inspired heuristics as deterministic rules

Apply these rules in extraction/publish contracts:

- Persist-first, curate-second mental model: candidate staging before publish confirmation.
- Explicit skip policy for tool chatter, placeholders, and harvest self-logs.
- Schema-first candidate normalization with deterministic fallback to `draft`.
- Confirmation semantics: mark committed only after publish succeeds.

### Decision 3: Prioritize workstreams 1, 2, 3 first; defer strictness of 4

Adopt strengthening workstreams in this order:

- Priority P1: deterministic fingerprint spec.
- Priority P1: source pointer/path canonicalization.
- Priority P1: extraction thresholds and skip criteria.
- Priority P2: structured mode outputs (start as recommended block).
- Priority P2: anti-recursion guardrail hardening.

Rationale:

- P1 directly improves reproducibility and capture quality.
- P2 improves automation and safety without blocking core capture flow.

### Decision 4: Structured outputs rollout policy

- Phase 2: `status/audit/review/optimize` structured blocks are **recommended**.
- Phase 3 gate: raise to **required** only after one dry-run compatibility audit.

## Canonical Contract Additions to Implement

Add/clarify the following in `skills/harvest/SKILL.md`:

1. `## Progressive Disclosure Read Workflow (Required)`
   - fixed read order
   - stop condition
   - anti-recursion and SOT-only restatement

2. Trigger cues for read intent:
   - "find prior decision"
   - "look up past context"
   - "trace project timeline"
   - "retrieve existing second-brain note"

3. Deterministic fingerprint normalization:
   - trim edges
   - collapse internal whitespace to single spaces
   - lowercase
   - canonical join `<source_ref>||<change>||<why>`
   - SHA-256 hex lowercase
   - one deterministic input/output example

4. Candidate schema-first extraction block:
   - `source_ref`, `change`, `why`, `candidate_type`, `confidence`, `exclusion_reason?`
   - unresolved pointer fallback to `draft` with `unresolved_source_ref`

5. Extraction threshold rules:
   - timeline: phase status change OR finalized decision line OR validated fix
   - decision: clear conclusion + rationale
   - knowledge: reusable pattern + at least one caveat/constraint
   - skip: format churn, placeholders, operational chatter, harvest self-logs

6. Publish confirmation semantics:
   - extract candidate
   - validate candidate
   - publish note
   - mark committed

7. Structured mode outputs (initially recommended):
   - `status`: `{mode, passed, missing_files[], notes_count}`
   - `audit`: `{mode, passed, issues:[{path, rule, severity}]}`
   - `review`: dimension scores + weighted total + evidence paths
   - `optimize`: input roots, included/skipped reports, aggregates, prioritized roadmap

8. Guardrail hardening examples:
   - explicit denylist examples for tool chatter patterns
   - explicit path-based "never harvest docs/notes into docs/notes" checks

## File-by-File Execution Plan

### Task 1: Add progressive-disclosure retrieval contract

**Files:**
- Modify: `skills/harvest/SKILL.md`
- Create: `skills/harvest/references/progressive-disclosure-read-example.md`

**Step 1: Add required retrieval workflow section**

Add section title exactly:

- `## Progressive Disclosure Read Workflow (Required)`

Include required order and stop condition.

**Step 2: Add read-intent trigger cues in trigger contract**

Add four phrases listed in "Canonical Contract Additions".

**Step 3: Add reference examples**

Create one concise file with three scenarios:

- decision lookup
- timeline investigation
- knowledge pattern retrieval

Each scenario must include: intent -> read order -> stop condition.

**Step 4: Validate no SOT contract drift**

Ensure section explicitly states `docs/notes` is retrieval-only, not capture input.

### Task 2: Formalize deterministic capture and schema rules

**Files:**
- Modify: `skills/harvest/SKILL.md`

**Step 1: Add deterministic fingerprint normalization and hash details**

Include exact normalization algorithm and SHA-256 requirement.

**Step 2: Add one concrete fingerprint example**

Use fixed sample input/output to reduce interpretation variance.

**Step 3: Add candidate schema block and draft fallback**

Define required fields and unresolved pointer handling.

**Step 4: Add extraction thresholds and skip criteria**

Add timeline/decision/knowledge thresholds and explicit noise skip rules.

### Task 3: Add structured output schemas with staged enforcement

**Files:**
- Modify: `skills/harvest/SKILL.md`

**Step 1: Add per-mode structured output schema section**

Keep human-readable summary + structured block together.

**Step 2: Mark enforcement level as recommended (phase-gated)**

Document that mandatory enforcement is delayed until compatibility dry run passes.

### Task 4: Align references and preserve thin command pattern

**Files:**
- Check/Modify as needed: `commands/harvest.md`
- Check/Modify as needed: `commands/harvest-start.md`
- Check/Modify as needed: `commands/harvest-capture.md`
- Check/Modify as needed: `commands/harvest-status.md`
- Check/Modify as needed: `commands/harvest-audit.md`
- Modify templates if needed:
  - `skills/harvest/references/projects/.templates/timeline-template.md`
  - `skills/harvest/references/decisions/.templates/decision-template.md`
  - `skills/harvest/references/knowledge/.templates/knowledge-template.md`

**Step 1: Keep command files thin and non-authoritative**

Only reference SKILL sections; do not duplicate logic/rules.

**Step 2: Canonicalize source path style in templates**

Use workspace-root relative references (for example `task_plan.md#...`).

### Task 5: Validation and rollout gate

**Files:**
- Verify skill package: `skills/harvest/`

**Step 1: Run validator**

Run:

```bash
npx --yes skills-ref validate ./skills/harvest
```

Expected: validation passes.

**Step 2: Manual consistency checks**

Confirm no conflict with:

- `## Source Extraction Boundaries (Required)`
- `## Anti-Recursion Guard`
- existing capture/publish/dedupe contract

**Step 3: Dry-run checklist for phase-gate**

Execute one manual walkthrough each for `capture`, `status`, `audit`, `review`, `optimize` against sample SOT files and record mismatches.

## Acceptance Criteria

- `skills/harvest/SKILL.md` contains required progressive-disclosure read workflow and stop condition.
- Read workflow explicitly preserves SOT-only input contract.
- Deterministic fingerprint algorithm is operationally specified (normalization + hash + example).
- Candidate schema, extraction thresholds, and skip rules are explicit and testable.
- Structured mode outputs are defined and clearly marked recommended/required by phase.
- Commands remain thin and non-authoritative.
- `npx --yes skills-ref validate ./skills/harvest` passes.

## Risks and Mitigations

- Risk: Retrieval workflow is misused as capture input path.
  - Mitigation: Repeat SOT-only rule in retrieval section and anti-recursion section.

- Risk: Over-constrained rules reduce practical usefulness.
  - Mitigation: Keep `draft` fallback for ambiguous pointers and avoid forced migration.

- Risk: Longer `SKILL.md` reduces usability.
  - Mitigation: Keep examples in `references/` and keep SKILL normative.

- Risk: Structured output change breaks existing consumers.
  - Mitigation: phase-gated rollout (recommended first, mandatory later).

## Decision Gates (Must Resolve Before Execution)

1. Scope gate: execute all workstreams now, or execute P1 only (recommended: P1 first).
2. Structured output gate: keep as recommended until compatibility audit passes (recommended).
3. Compatibility gate: run one-time audit on existing `docs/notes` before mandatory structured blocks (recommended).

## Suggested Rollout Timeline

- Phase 1 (docs-only core): Task 1 + Task 2.
- Phase 2 (reporting clarity): Task 3.
- Phase 3 (alignment + verification): Task 4 + Task 5.

No runtime/plugin behavior changes in this plan.
