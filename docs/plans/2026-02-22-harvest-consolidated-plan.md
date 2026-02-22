# Harvest Consolidated Strengthening Plan

Status: draft proposal (consolidated)
Date: 2026-02-22
Owner: shihyuho/skills maintainers

## Sources Consolidated

- `docs/plans/2026-02-22-harvest-strengthening-plan.md`
- `docs/plans/2026-02-22-harvest-capture-heuristics-from-claude-mem.md`
- `docs/plans/2026-02-22-harvest-upgrade-a-progressive-disclosure-plan.md`
- `docs/plans/2026-02-22-harvest-unified-upgrade-plan.md`

This document is the single execution plan and replaces cross-reading the four source plans.

## Goal

Strengthen `skills/harvest` to make retrieval and capture more deterministic, less noisy, and easier to automate across all entrypoints, while preserving source-of-truth boundaries.

## Scope

In scope:

- Progressive-disclosure retrieval workflow for reading existing `docs/notes`.
- Deterministic capture hardening (`sot_fingerprint`, schema rules, extraction thresholds).
- Source pointer/path canonicalization in templates.
- Structured mode outputs for `status`, `audit`, `review`, `optimize`.
- Anti-recursion and denylist hardening.
- Keep command files thin and non-authoritative.

Out of scope:

- Runtime plugin or external service implementation.
- Forced migration of existing note artifacts.
- Repository-wide conventions unrelated to `harvest`.

## Baseline Constraints (Must Preserve)

- `skills/harvest/SKILL.md` remains the behavior source of truth.
- `commands/harvest*.md` remain entrypoints that reference SKILL sections only.
- Capture input remains SOT-only: `task_plan.md`, `findings.md`, `progress.md`.
- `docs/notes` is output and retrieval surface, never capture input.
- Anti-recursion guard remains mandatory.

## Design Decisions

### D1. Phase priority

Adopt a phased rollout to reduce risk:

- Phase 1 (P1): retrieval workflow + deterministic capture core.
- Phase 2 (P2): structured mode outputs.
- Phase 3 (P3): guardrail hardening + compatibility gate.

### D2. Retrieval first (Upgrade A)

Add required progressive-disclosure reading order:

1. Read `docs/notes/index.md`.
2. Read one or more intent hubs:
   - `docs/notes/projects.md`
   - `docs/notes/decisions.md`
   - `docs/notes/knowledge.md`
3. Read targeted leaf note(s) only.

Stop condition:

- Stop when target note is found, or after two consecutive non-novel reads.

Hard constraints:

- Never start at deep leaf unless user gives exact path.
- Never use `docs/notes` as capture input.

### D3. claude-mem-inspired capture heuristics (normalized)

Adopt the following capture model:

- Persist-first, curate-second: candidate staging and publish confirmation are distinct.
- Strict skip policy: filter tool chatter, placeholders, and self-log noise.
- Schema-first extraction: normalize to a canonical candidate shape before classification.
- Confirmation semantics: mark committed only after publish succeeds.

Reference implementation pointers (relative to `claude-mem` repository root):

- `src/services/worker/SessionManager.ts`
- `src/services/sqlite/PendingMessageStore.ts`
- `src/services/worker/agents/ResponseProcessor.ts`
- `src/services/worker/http/routes/SessionRoutes.ts`
- `src/services/worker/validation/PrivacyCheckValidator.ts`
- `src/sdk/prompts.ts`
- `src/sdk/parser.ts`
- `src/services/worker/SearchManager.ts`
- `src/services/worker/http/routes/SearchRoutes.ts`

## Canonical Contract Additions

Update `skills/harvest/SKILL.md` with these explicit rules:

1. `## Progressive Disclosure Read Workflow (Required)`
   - fixed read order
   - stop condition
   - SOT-only and anti-recursion restatement

2. Trigger cues for read intent:
   - find prior decision
   - look up past context
   - trace project timeline
   - retrieve existing second-brain note

3. Deterministic fingerprint spec:
   - trim edges
   - collapse internal whitespace
   - lowercase
   - canonical join `<source_ref>||<change>||<why>`
   - SHA-256 hex lowercase
   - one concrete example

4. Candidate schema and fallback:
   - `source_ref`, `change`, `why`, `candidate_type`, `confidence`, `exclusion_reason?`
   - unresolved pointer -> `draft` with `unresolved_source_ref`

5. Extraction thresholds:
   - timeline: phase status change OR finalized decision OR validated fix
   - decision: conclusion + rationale
   - knowledge: reusable pattern + caveat/constraint

6. Skip criteria:
   - operational chatter
   - placeholders
   - format-only churn
   - harvest self-publishing logs

7. Publish confirmation semantics:
   - extract -> validate -> publish -> mark committed

8. Structured mode outputs (phase-gated):
   - `status`: `{mode, passed, missing_files[], notes_count}`
   - `audit`: `{mode, passed, issues:[{path, rule, severity}]}`
   - `review`: dimension scores + weighted total + evidence paths
   - `optimize`: input roots, included/skipped reports, aggregates, roadmap

9. Guardrail hardening:
   - explicit path-based recursion checks
   - expanded denylist examples for tool chatter patterns

## Implementation Tasks

### Task 1: Retrieval workflow and read examples

Files:

- Modify `skills/harvest/SKILL.md`
- Add `skills/harvest/references/progressive-disclosure-read-example.md`

Deliverables:

- Required retrieval workflow section and trigger cues.
- Three examples: decision lookup, timeline investigation, knowledge retrieval.

### Task 2: Deterministic capture core

Files:

- Modify `skills/harvest/SKILL.md`

Deliverables:

- Fingerprint normalization + hash algorithm + deterministic example.
- Candidate schema and extraction threshold rules.
- Publish confirmation semantics.

### Task 3: Template/source path canonicalization

Files:

- `skills/harvest/references/projects/.templates/timeline-template.md`
- `skills/harvest/references/decisions/.templates/decision-template.md`
- `skills/harvest/references/knowledge/.templates/knowledge-template.md`

Deliverables:

- Workspace-root relative source pointer style.
- No deep relative traversal in template defaults.

### Task 4: Structured outputs and command alignment

Files:

- Modify `skills/harvest/SKILL.md`
- Check `commands/harvest*.md` (keep thin, no duplicated behavior)

Deliverables:

- Structured output contract by mode.
- Commands remain section-pointer entrypoints only.

## Acceptance Criteria

- One deterministic retrieval read order exists in SKILL contract.
- Capture contract remains SOT-only and anti-recursive.
- Fingerprint and dedupe behavior is operationally specified.
- Candidate classification and skip behavior is explicit and testable.
- Templates use canonical relative source pointer style.
- Structured mode outputs are defined with rollout level.
- `skills-ref` validation passes.

## Verification and Gate

Tool validation:

```bash
npx --yes skills-ref validate ./skills/harvest
```

Manual checks:

- No conflict with `Source Extraction Boundaries`.
- No conflict with `Anti-Recursion Guard`.
- No drift in capture/publish/dedupe contract.

Compatibility gate before making structured output mandatory:

- Run one dry run each for `capture`, `status`, `audit`, `review`, `optimize`.
- Record mismatches and adjust wording only.

## Risks and Mitigations

- Risk: retrieval flow accidentally treated as capture input.
  - Mitigation: repeat SOT-only rule in retrieval and guardrail sections.

- Risk: over-constrained rules reduce flexibility.
  - Mitigation: keep explicit `draft` fallback.

- Risk: structured output breaks existing consumers.
  - Mitigation: start as recommended, promote to required after compatibility gate.

## Decision Gates

Before execution, confirm:

1. Scope: execute full plan vs P1 first (recommended: P1 first).
2. Structured output strictness: recommended vs required (recommended first).
3. Compatibility audit: run one-time audit on existing `docs/notes` artifacts.
