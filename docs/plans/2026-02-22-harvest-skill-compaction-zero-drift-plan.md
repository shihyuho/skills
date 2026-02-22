# Harvest SKILL Compaction (Unified Plan)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reduce `skills/harvest/SKILL.md` to <= 200 lines with zero behavior drift.

**Architecture:** Keep `SKILL.md` as execution control plane (trigger, deterministic workflow, hard constraints, verification). Move long-form details into minimal references and keep normative `MUST` links.

**Tech Stack:** Markdown docs (`SKILL.md`, `references/*.md`), repo search (`rg`), validation (`skills-ref`).

---

## Non-Negotiable Invariants

These contracts MUST remain semantically identical:

1. SOT boundary: `task_plan.md`, `findings.md`, `progress.md`.
2. Workflow order: preflight -> bootstrap -> extract -> classify -> publish -> verify/report.
3. Mode contracts preserved: `capture`, `status`, `audit`, `review`, `optimize`.
4. Dedupe parity: same-day + same `sot_fingerprint` => no-op.
5. Fingerprint normalization algorithm unchanged.
6. Anti-recursion unchanged (`docs/notes` cannot become capture input).
7. Review/optimize scoring and aggregation unchanged.
8. Verification checklist obligations unchanged.
9. Command entrypoint section anchors remain valid.
10. Failure handling semantics remain explicit and unchanged.

## Scope and Guardrails

- Preserve command-dependent headers in `skills/harvest/SKILL.md`:
  - `## Core Contract`
  - `## Deterministic Workflow (Required)`
  - `## First-Run Bootstrap (Required)`
  - `## Review Report Mode (Required)`
  - `## Review Rollup Mode (Required)`
  - `## Source Extraction Boundaries (Required)`
  - `## Anti-Recursion Guard`
  - `## Verification Checklist`
  - `## Failure Handling`
- Keep algorithmic/safety-critical rules inline in `SKILL.md`:
  - dedupe condition
  - fingerprint normalization steps
  - anti-recursion rule
  - entrypoint equivalence
  - failure handling behavior

## Files

**Modify:**
- `skills/harvest/SKILL.md`

**Create:**
- `skills/harvest/references/extraction-and-classification.md`
- `skills/harvest/references/publishing-and-dedupe.md`
- `skills/harvest/references/quality-reports.md`
- `skills/harvest/references/semantic-parity-mapping.md`

**Optional:**
- `skills/harvest/README.md` (only if wording drift appears)

## Execution Steps (Mandatory)

### Step 1: Build parity mapping first

Run:

```bash
rg -n "Required\)|MUST|Never|Do not|only source of truth|sot_fingerprint|anti-recursion|Failure Handling|Verification Checklist" skills/harvest/SKILL.md
```

Create `semantic-parity-mapping.md` with: invariant ID, original clause, destination section, parity check.

### Step 2: Extract long-form contracts to references

- `extraction-and-classification.md`: extraction boundaries, markers, classification decision table.
- `publishing-and-dedupe.md`: publish confirmation semantics, bootstrap minimal files/rules, dedupe and fingerprint example.
- `quality-reports.md`: review/optimize contracts and structured mode outputs.

### Step 3: Compress SKILL.md to control plane

- Keep all required anchor headers unchanged.
- Replace large detail blocks with concise normative lines linking to `references/*.md`.
- Ensure `MUST/NEVER/Required` strength is not weakened.

### Step 4: Run verification gates

Run:

```bash
wc -l skills/harvest/SKILL.md
rg -n "## (Core Contract|Deterministic Workflow \(Required\)|First-Run Bootstrap \(Required\)|Review Report Mode \(Required\)|Review Rollup Mode \(Required\)|Source Extraction Boundaries \(Required\)|Anti-Recursion Guard|Verification Checklist|Failure Handling)" skills/harvest/SKILL.md
npx --yes skills-ref validate ./skills/harvest
```

Expected:
- `SKILL.md` line count <= 200
- all required anchors present
- `Valid skill: ./skills/harvest`

### Step 5: Final parity checklist

Confirm unchanged:
- SOT input set and output path set
- bootstrap minimal-file set
- review/optimize scoring and aggregation
- dedupe/fingerprint behavior
- failure handling behavior
- no weakening of hard normative wording

## Definition of Done

- `skills/harvest/SKILL.md` about 200 lines.
- `semantic-parity-mapping.md` coverage complete.
- Required command-dependent anchors preserved.
- `skills-ref` validation passes.
- No behavior drift observed in parity checks.

## Risks and Mitigations

- Risk: semantic drift during extraction.
  - Mitigation: invariants + parity mapping + gates.
- Risk: command anchors broken by header renames.
  - Mitigation: preserve exact header text.
- Risk: references become duplicated/non-authoritative.
  - Mitigation: single-owner contract per reference file.
