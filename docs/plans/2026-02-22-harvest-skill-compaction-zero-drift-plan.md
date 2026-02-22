# Harvest SKILL Compaction (Unified Plan)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reduce `skills/harvest/SKILL.md` to around 200 lines while preserving behavior exactly.

**Architecture:** Keep `SKILL.md` as the control plane (triggering, workflow order, hard constraints, verification obligations). Move long-form operational detail into focused reference files and link with explicit normative wording.

**Tech Stack:** Markdown docs (`SKILL.md`, `references/*.md`), repository search (`rg`), validation (`skills-ref`).

---

## Non-Negotiable Invariants

These contracts MUST remain semantically identical:

1. SOT boundary stays `task_plan.md`, `findings.md`, `progress.md`.
2. Workflow order stays `preflight -> bootstrap -> extract -> classify -> publish -> verify/report`.
3. Mode contracts stay intact for `capture`, `status`, `audit`, `review`, `optimize`.
4. Dedupe parity stays `same-day + same sot_fingerprint => no-op`.
5. Fingerprint normalization algorithm stays unchanged.
6. Anti-recursion remains enforced (`docs/notes` cannot become capture input).
7. Review/optimize scoring and aggregation contracts stay unchanged.
8. Verification checklist obligations stay unchanged.
9. Command entrypoint section anchors remain valid.
10. Failure handling semantics remain explicit and unchanged.

## Scope and Guardrails

### Required section anchors in `skills/harvest/SKILL.md`

Do not rename these headers:

- `## Core Contract`
- `## Deterministic Workflow (Required)`
- `## First-Run Bootstrap (Required)`
- `## Review Report Mode (Required)`
- `## Review Rollup Mode (Required)`
- `## Source Extraction Boundaries (Required)`
- `## Anti-Recursion Guard`
- `## Verification Checklist`
- `## Failure Handling`

### Rules that must remain inline in `SKILL.md`

- dedupe condition
- fingerprint normalization steps
- anti-recursion rule
- entrypoint equivalence rule
- failure handling behavior

### Rules that can be externalized to references

- long decision tables
- long bootstrap file lists
- review/optimize mode detail contracts
- structured output schemas
- long examples

## Files

**Modify:**

- `skills/harvest/SKILL.md`

**Create/maintain:**

- `skills/harvest/references/extraction-and-classification.md`
- `skills/harvest/references/publishing-and-dedupe.md`
- `skills/harvest/references/quality-reports.md`
- `skills/harvest/references/semantic-parity-mapping.md`

**Optional alignment:**

- `skills/harvest/README.md` (only if wording drift appears)

## Execution Steps (Mandatory)

### Step 1: Build semantic parity map first

Run:

```bash
rg -n "Required\)|MUST|Never|Do not|only source of truth|sot_fingerprint|anti-recursion|Failure Handling|Verification Checklist" skills/harvest/SKILL.md
```

Create `skills/harvest/references/semantic-parity-mapping.md` with columns:

- invariant ID
- original contract snippet
- destination section/file
- parity check method

Fail fast rule: if any hard clause has no destination, stop and fix mapping before edits.

### Step 2: Externalize long-form detail to references

Populate:

- `extraction-and-classification.md`
  - extraction boundaries
  - exclusion markers
  - classification decision table
- `publishing-and-dedupe.md`
  - publish confirmation semantics
  - bootstrap minimal files and bootstrap rules
  - dedupe contract and fingerprint example
- `quality-reports.md`
  - review mode contract
  - optimize mode contract
  - structured mode outputs

### Step 3: Rewrite `SKILL.md` as control plane

- Keep required anchors unchanged.
- Replace long detail blocks with concise normative statements and links to `references/*.md`.
- Keep hard constraints in imperative language (`MUST`/`NEVER`/`Required`).
- Preserve all behavior-critical rules listed in guardrails.

### Step 4: Run verification gates

Run:

```bash
wc -l skills/harvest/SKILL.md
rg -n "## (Core Contract|Deterministic Workflow \(Required\)|First-Run Bootstrap \(Required\)|Review Report Mode \(Required\)|Review Rollup Mode \(Required\)|Source Extraction Boundaries \(Required\)|Anti-Recursion Guard|Verification Checklist|Failure Handling)" skills/harvest/SKILL.md
npx --yes skills-ref validate ./skills/harvest
```

Expected:

- `SKILL.md` line count is near 200 (target range: ~180-210)
- all required anchors present
- `Valid skill: ./skills/harvest`

### Step 5: Run parity checklist

Confirm unchanged:

- SOT input set and output path set
- bootstrap minimal-file set
- review/optimize scoring and aggregation
- dedupe/fingerprint behavior
- failure handling behavior
- no weakening of hard normative wording

## Definition of Done

- `skills/harvest/SKILL.md` is around 200 lines with no semantic drift.
- `semantic-parity-mapping.md` has full coverage for hard clauses.
- required command-dependent anchors are preserved.
- `skills-ref` validation passes.
- parity checklist passes.

## Risks and Mitigations

- Risk: semantic drift during extraction.
  - Mitigation: map invariants before edits, then run parity gate.
- Risk: command anchors broken by heading rename.
  - Mitigation: keep exact heading text and run anchor regex gate.
- Risk: references become duplicated/non-authoritative.
  - Mitigation: one canonical contract owner per reference file.
- Risk: over-compression reduces readability.
  - Mitigation: target "around 200" and prefer clarity over aggressive trimming.

## Mandatory vs Optional Work

### Mandatory

- keep command-dependent anchor headers unchanged
- keep behavior-critical rules inline
- keep parity mapping up to date
- run all verification gates
- keep normative wording strength (`MUST/NEVER/Required`)

### Optional

- align `skills/harvest/README.md` wording if references changed
- add brief examples in references to improve onboarding
- annotate parity mapping with owner/review date metadata

## Verification Evidence Template

Capture this evidence block in the execution log:

- `wc -l skills/harvest/SKILL.md` output
- anchor regex output
- `npx --yes skills-ref validate ./skills/harvest` output
- parity checklist outcomes for SOT/modes/dedupe/failure handling
- list of files created/modified in this refactor

## Execution Notes

- This plan intentionally balances two goals: preserve behavior and keep documentation maintainable.
- If tradeoff appears between strict brevity and clarity, prefer clarity while staying near 200 lines.
- Do not change implementation behavior while improving document structure.
