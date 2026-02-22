# Harvest Strengthening Plan (Proposal)

Status: draft proposal (not executed)
Date: 2026-02-22
Owner: shihyuho/skills maintainers

## Goal

Strengthen `skills/harvest` so capture behavior is more deterministic, less ambiguous, and easier to automate consistently across entrypoints (`/harvest`, `/harvest-start`, `/harvest-capture`, `/harvest-status`, `/harvest-audit`).

## Scope

In scope:
- Clarify contracts in `skills/harvest/SKILL.md`.
- Improve reproducibility of extraction and dedupe behavior.
- Add machine-checkable output conventions for status/audit/review/optimize flows.
- Preserve current command-entrypoint pattern (thin command, skill as source of truth).

Out of scope:
- Implementing runtime plugins or external services.
- Migrating existing notes automatically.
- Changing repository-wide conventions unrelated to harvest.

## Proposed Workstreams

### 1) Deterministic Fingerprint Spec

Problem:
- `sot_fingerprint` formula is conceptually defined but not operationally specified.

Plan:
- Define canonical normalization in `skills/harvest/SKILL.md`:
  - Trim leading/trailing whitespace.
  - Collapse internal whitespace to single spaces.
  - Lowercase.
  - Canonical join format: `<source_ref>||<change>||<why>`.
- Define hash algorithm: SHA-256 hex lowercase.
- Add one concrete example input/output pair.

Acceptance criteria:
- Two agents processing same source produce identical `sot_fingerprint`.
- Dedupe no-op decisions are stable across trigger entrypoints.

### 2) Source Pointer and Path Canonicalization

Problem:
- Relative `source_files` in templates can become inconsistent when notes are nested.

Plan:
- Standardize source references as workspace-root relative paths (e.g. `task_plan.md`, `findings.md`, `progress.md`).
- Keep `source_ref` as `<path>#<section-or-keyword>` using the same canonical path style.
- Update references templates accordingly.

Acceptance criteria:
- No template emits deep relative traversal (`../../..`) for source-of-truth pointers.
- All generated notes use one path style.

### 3) Extraction Thresholds for "Record-worthy" Content

Problem:
- "significant update" and "reusable finding" are still subjective.

Plan:
- Add explicit threshold rules in `skills/harvest/SKILL.md`:
  - Timeline candidate if any phase status changes OR any decision line is finalized OR any validated fix is recorded.
  - Decision candidate requires a clear conclusion + rationale pair.
  - Knowledge candidate requires reusable pattern + at least one caveat/constraint.
- Add "skip" criteria for noise-only changes (format churn, empty placeholders, operational chatter).

Acceptance criteria:
- Different agents classify the same source slice into same note type in most cases.
- Reduced over-capture of low-value updates.

### 4) Structured Mode Outputs (status/audit/review/optimize)

Problem:
- Mode outputs are readable but not fully machine-checkable.

Plan:
- Define minimal output schema per mode:
  - `status`: `{mode, passed, missing_files[], notes_count}`
  - `audit`: `{mode, passed, issues:[{path, rule, severity}]}`
  - `review`: include dimension scores + weighted total + evidence paths
  - `optimize`: include input roots, included/skipped reports, score aggregates, prioritized roadmap
- Keep human-readable summary plus structured block.

Acceptance criteria:
- Outputs can be consumed by automation without regex-heavy parsing.
- Existing manual readability remains intact.

### 5) Guardrails and Anti-Recursion Hardening

Problem:
- Current anti-recursion is strong, but edge cases can still leak process noise.

Plan:
- Expand denylist examples for tool chatter patterns.
- Add explicit "never harvest docs/notes into docs/notes" examples with path-based checks.
- Add verification checklist item for recursion leak detection.

Acceptance criteria:
- Audit mode catches recursion leakage with concrete file paths.
- Reduced false positives in harvested notes.

## Rollout Plan

Phase A (spec-only, no behavior break):
- Update `skills/harvest/SKILL.md` contracts and examples.
- Update `skills/harvest/references/*/.templates/*.md` path conventions.

Phase B (entrypoint alignment):
- Ensure `commands/harvest*.md` references updated SKILL sections only.
- Keep commands thin and non-authoritative.

Phase C (verification dry-run):
- Perform one manual dry run for each mode (`capture/status/audit/review/optimize`) on sample SOT files.
- Record mismatches and adjust wording only (no scope expansion).

## Risks and Mitigations

- Risk: Over-constraining rules reduces flexibility.
  - Mitigation: Keep criteria explicit but minimal; allow `draft` fallback.
- Risk: Backward mismatch with existing notes.
  - Mitigation: New rules apply forward; no forced migration.
- Risk: Increased spec length hurts usability.
  - Mitigation: Keep SKILL concise and move dense examples to `references/`.

## Decision Gate (for later)

Before execution, decide:
1. Adopt all five workstreams, or prioritize subset (1, 2, 3 first).
2. Whether to enforce structured output blocks as mandatory or recommended.
3. Whether to run a one-time compatibility audit on existing `docs/notes` artifacts.
