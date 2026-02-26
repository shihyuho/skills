# Semantic Parity Mapping

Use this mapping to verify behavior did not drift while compacting `SKILL.md`.

| Invariant ID | Original Contract | Canonical Destination | Verification Method |
| --- | --- | --- | --- |
| INV-01 | SOT-only input boundary (`task_plan.md`, `findings.md`, `progress.md`) | `SKILL.md` `## Core Contract`, `## Anti-Recursion Guard` | Read section text and verify exact file set |
| INV-02 | Deterministic workflow order and mode selection | `SKILL.md` `## Deterministic Workflow (Required)` | Verify ordered steps: preflight -> bootstrap -> extract -> classify -> publish -> verify/report |
| INV-03 | Candidate schema fields and draft unresolved behavior | `SKILL.md` `## Candidate Schema and Extraction Rules (Required)` + `references/extraction-and-classification.md` | Confirm all required and optional fields present |
| INV-04 | Allowlist/denylist extraction boundaries and markers | `SKILL.md` `## Source Extraction Boundaries (Required)` + `references/extraction-and-classification.md` | Confirm allowlist, denylist, and markers are unchanged |
| INV-05 | Publish confirmation semantics | `SKILL.md` `## Publish Confirmation Semantics (Required)` + `references/publishing-and-dedupe.md` | Confirm 4-step publish sequence is unchanged |
| INV-06 | Bootstrap minimal files and no-overwrite rules | `SKILL.md` `## First-Run Bootstrap (Required)` + `references/publishing-and-dedupe.md` | Compare required file set and rule bullets |
| INV-07 | Classification routing and milestone rules | `SKILL.md` `## Publishing Strategy` + `references/extraction-and-classification.md` | Verify decision table conditions and output fields |
| INV-08 | Review mode contract, scoring, and evidence requirements | `SKILL.md` `## Review Report Mode (Required)` + `references/quality-reports.md` | Verify sections, weights, and deterministic scoring rules |
| INV-09 | Optimize mode contract and aggregation | `SKILL.md` `## Review Rollup Mode (Required)` + `references/quality-reports.md` | Verify roots handling, filtering, aggregation, and empty-input behavior |
| INV-10 | Dedupe condition and fingerprint normalization algorithm | `SKILL.md` `## Dedupe and Fingerprint Contract (Required)` + `references/publishing-and-dedupe.md` | Validate 5 normalization steps and same-day no-op rule |
| INV-11 | Failure handling behavior | `SKILL.md` `## Failure Handling` | Verify unresolved source handling and non-blocking SOT workflow |
| INV-12 | Verification checklist obligations | `SKILL.md` `## Verification Checklist` | Ensure all 8 checklist items remain |
