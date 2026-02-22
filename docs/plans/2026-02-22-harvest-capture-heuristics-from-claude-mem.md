# Harvest Capture Heuristics Inspired by claude-mem

## Purpose

This document captures what `skills/harvest` can learn from `claude-mem` about selecting what to record and what to skip.

This is a planning proposal only.

## Why claude-mem is relevant

`claude-mem` and `harvest` solve similar problems:

- Convert noisy execution traces into durable memory.
- Preserve traceability to source context.
- Keep capture deterministic enough for automation.

## Key lessons harvest can adopt

### 1) Persist-first, curate-second

Observation from `claude-mem`:

- Events are first persisted into a durable queue before deeper processing.
- Processing and deletion are separated by explicit confirmation.

Relevant files:

- `/Users/matt/tmp/claude-mem/src/services/worker/SessionManager.ts`
- `/Users/matt/tmp/claude-mem/src/services/sqlite/PendingMessageStore.ts`
- `/Users/matt/tmp/claude-mem/src/services/worker/agents/ResponseProcessor.ts`

Harvest implication:

- Keep extraction and publishing as two distinct phases.
- In capture logic, treat candidate generation as "durable staging" and publish as "confirmed commit".

### 2) Strict skip policy prevents memory pollution

Observation from `claude-mem`:

- Skips private prompts, low-value tools, and meta-observations.
- Applies explicit privacy checks before queueing content.

Relevant files:

- `/Users/matt/tmp/claude-mem/src/services/worker/http/routes/SessionRoutes.ts`
- `/Users/matt/tmp/claude-mem/src/services/worker/validation/PrivacyCheckValidator.ts`

Harvest implication:

- Strengthen denylist with concrete, testable rules.
- Add explicit "never-capture" examples for tool chatter and harvest self-logs.

### 3) Schema-first capture improves consistency

Observation from `claude-mem`:

- Agent output follows a structured schema (observation/summary XML).
- Parser then normalizes missing fields and applies fallbacks deterministically.

Relevant files:

- `/Users/matt/tmp/claude-mem/src/sdk/prompts.ts`
- `/Users/matt/tmp/claude-mem/src/sdk/parser.ts`

Harvest implication:

- Define a canonical candidate schema before classification:
  - `source_ref`
  - `change`
  - `why`
  - `candidate_type`
  - `confidence`
  - `exclusion_reason?`
- Keep draft fallback when required fields are missing.

### 4) Confirmation semantics reduce accidental data loss

Observation from `claude-mem`:

- Data is marked complete only after storage succeeds.
- Failures are retriable without losing original messages.

Relevant files:

- `/Users/matt/tmp/claude-mem/src/services/sqlite/PendingMessageStore.ts`
- `/Users/matt/tmp/claude-mem/src/services/worker/agents/ResponseProcessor.ts`

Harvest implication:

- Apply the same mental model to note publishing:
  - extract candidate
  - validate candidate
  - publish note
  - mark candidate as committed

### 5) Hybrid retrieval model is better than semantic-only

Observation from `claude-mem`:

- Query pipeline combines semantic retrieval with SQLite hydration/filtering.
- Keeps both recall quality and traceable fields.

Relevant files:

- `/Users/matt/tmp/claude-mem/src/services/worker/SearchManager.ts`
- `/Users/matt/tmp/claude-mem/src/services/worker/http/routes/SearchRoutes.ts`

Harvest implication:

- If harvest later adds note retrieval or quality audits, use hybrid scoring:
  - semantic similarity for discovery
  - path/source-field checks for precision and trust

## Concrete heuristics proposal for harvest

Adopt the following selection rules in `skills/harvest/SKILL.md`:

1. Capture if a phase moved state or a decision became final.
2. Capture if a finding is reusable and includes at least one caveat.
3. Skip if content is operational chatter or placeholder text.
4. Skip if content only describes harvest publishing activity.
5. Mark as `draft` when source pointer cannot be resolved.

## Suggested SKILL.md updates (non-executed)

- Add a "Candidate Schema" section under extraction.
- Add a "Skip Rules" section with explicit examples.
- Add a "Publish Confirmation" section to make commit semantics explicit.
- Add a small deterministic example from source slice -> candidate -> note output.

## Validation checklist for future implementation

- Same input produces same candidate set.
- Same candidate set produces same timeline dedupe outcome.
- Noise-only updates do not create notes.
- Missing source pointers always degrade to `draft`, never silent drop.
