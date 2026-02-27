---
name: skill-design
description: Design and refactor Agent Skills with concise, high-signal instructions and explicit trigger metadata. Use when creating a new skill, revising SKILL.md/README.md structure, or improving skill discoverability and portability.
license: MIT
metadata:
  author: shihyuho
  version: "1.4.0"
---

# Skill Design

Design skills as reusable behavior systems that are easy to discover and execute.

## Trigger Contract

Use this skill when users ask to:

- create a new skill
- refactor an existing skill
- improve trigger quality or discoverability
- align `SKILL.md`, `README.md`, and `references/`
- remove ambiguity or conflicting guidance

Typical trigger phrases:

- "create a skill for X"
- "design a new skill"
- "refactor this skill"
- "make this skill reusable"
- "align README and SKILL behavior"

## Core Principles

- Optimize for reliable agent behavior, not document aesthetics.
- Make trigger conditions explicit and searchable.
- Keep instructions executable and verifiable.
- Avoid implicit project context unless explicitly required.
- Default to secure-by-construction wording for any instructions that may trigger execution.

## Writing Style Rules

- Use imperative voice.
- Keep sections short and high-signal.
- Prefer concrete constraints over abstract advice.
- Use `MUST`/`NEVER` for true invariants (safety, correctness, irreversible failure).
- For normal guidance, use direct action verbs and clear defaults.
- Avoid weak modal wording for hard rules (`should`, `could`, `may`, `consider`, `usually`).
- Remove narrative text that does not change execution.

## Metadata and Discovery

- Write frontmatter `description` in third person.
- Include both what the skill does and when to use it.
- Keep trigger terms concrete (`file type`, `task type`, `user phrasing`).
- Do not put workflow details in `description`; keep those in the body.

## Workflow

### Phase 1 - Define Contract

1. Define who uses the skill and when it triggers.
2. Define non-negotiable behavior and failure boundaries.
3. Define deterministic vs heuristic decisions.

### Phase 2 - Structure Content

1. Write trigger and constraints first.
2. Keep `SKILL.md` as execution logic and decision constraints.
3. Move bulky detail to `references/` and keep one source of truth per schema.
4. Add `scripts/` only for repeatable deterministic operations.
5. When composing with other skills, invoke them by name and never copy their instruction bodies.

### Phase 2.5 - Outer/Inner Boundary

1. Treat `SKILL.md` as outer governance: trigger contract, conservative boundaries, workflow, verification gates, and escalation path.
2. Treat `references/` as inner detail: practical conventions, preferred patterns, examples, and extended rationale.
3. Do not place decision gates only in `references/`; keep governing decisions in `SKILL.md`.
4. If `references/` and `SKILL.md` conflict, align `references/` to `SKILL.md`.

### Phase 3 - Author/Refactor SKILL

1. Tighten description and trigger wording.
2. Convert soft guidance into explicit, executable instructions.
3. Provide one default path first; add alternatives only when necessary.
4. Remove duplicate or contradictory instructions.

### Phase 3.5 - Security Hardening Pass (When Skill Includes Commands/Automation)

1. Replace direct execution language with review-gated flow (`fetch -> review/validate -> explicit approval`).
2. Add trust-boundary disclosure when external services or remote content are involved.
3. Add forbidden command patterns and safer alternatives.
4. Add persistence checkpoints for changes that mutate shell/profile/system state.
5. Add provenance requirements for external artifacts (source rationale, version pin, integrity verification, rollback).
6. Document residual risk explicitly rather than implying risk elimination.

### Phase 4 - Align README (Human-Facing)

1. Keep README value-first: problem -> value -> example -> activation.
2. Treat `README.md` as style charter for future AI output quality.
3. Keep implementation internals out of README.
4. Keep claims behavior-accurate.

### Phase 5 - Validate

1. Run available validator for your environment.
2. If no validator exists, run manual consistency checks.
3. Confirm no repository-specific assumptions remain unless explicitly intended.

## Progressive Disclosure Rules

- Keep `SKILL.md` body compact (target under 500 lines).
- Put advanced or domain-specific detail in `references/`.
- Link reference files directly from `SKILL.md` (avoid deep nested references).
- For long reference files (100+ lines), add a short table of contents.

## README Rules

- In this skill, `README.md` means the skill-level README (for example `skills/<skill-name>/README.md`), not the repository root README.
- `README.md` is not required by Agent Skills Specification.
- `README.md` is recommended for faster human understanding and adoption.
- Keep README focused on outcomes, style expectations, and activation cues.

## Anti-Patterns

- Hardcoded local paths as universal defaults.
- Tool lock-in with no fallback path.
- Copying external skill instruction bodies instead of invoking the source skill.
- Workflow summary inside frontmatter `description`.
- Duplicated schema definitions across files.
- Long narrative prose with no executable instruction.
- Repeating `MUST`/`NEVER` for non-critical guidance.
- Offering too many equivalent options without a default recommendation.
- Fetch-and-follow phrasing that implies autonomous execution of remote content.
- Unsafe install examples (`curl|bash`, `wget|bash`) without review and verification gates.
- Persistent environment mutation guidance without explicit confirmation checkpoint.
- Security logic split across multiple docs with no single source of truth.
- Keeping conservative boundaries, workflow gates, or escalation rules only in `references/`.
- Letting `references/` override governing decisions defined in `SKILL.md`.

## Security Patterns (Execution-Sensitive Skills)

Apply these when skills can produce or run commands:

1. **Review Gate Pattern**
   - Use: fetch -> review/validate -> explicit approval -> execute.
   - Never imply direct execution from raw URLs.

2. **Trust Boundary Pattern**
   - Explicitly state outbound data flow to external APIs/services.
   - Require redaction/sanitization guidance for sensitive content.

3. **Command Safety Pattern**
   - Define forbidden command patterns.
   - Provide safer alternatives (pinned versions, checksum/signature, least privilege).

4. **Persistence Checkpoint Pattern**
   - Prefer session-scoped behavior by default.
   - Require explicit confirmation before persistent shell/profile mutation.

5. **Provenance Pattern**
   - Require source rationale, version pin, integrity verification command, rollback/uninstall path.

### Required Output Contract for Security Patterns

When applying security patterns, the resulting skill text MUST include explicit, auditable wording:

1. **Review gate text**
   - MUST include all four steps in order: `fetch -> review/validate -> explicit approval -> execute`.
   - MUST include a prohibition sentence equivalent to: "Do not execute remote content directly from URL."

2. **Trust boundary text**
   - MUST name the external destination (domain/service) when data leaves local context.
   - MUST include redaction/sanitization instruction before transmission.

3. **Command safety text**
   - MUST include a forbidden list with concrete examples.
   - MUST include at least one safer alternative for each high-risk pattern class.

4. **Persistence checkpoint text**
   - MUST include session-scoped default first.
   - MUST include explicit confirmation checkpoint before persistent shell/profile change.

5. **Provenance text**
   - MUST require source rationale, version pin, integrity verification command, and rollback/uninstall path.

### Rewrite Templates (Use Verbatim Structure)

- Replace risky phrase:
  - from: `Fetch and follow instructions from [URL]`
  - to: `Fetch [URL], review and validate steps, ask for explicit approval, then execute.`

- Add prohibition:
  - `Never execute remote raw content directly from URL.`

- Add persistence checkpoint:
  - `Use session-scoped change by default; require explicit confirmation before persistent shell rc updates.`

### Security Verification Checklist (MANDATORY)

Before finalizing an execution-sensitive skill, verify all checks pass:

1. No fetch-and-follow wording remains.
2. Forbidden patterns and safer alternatives are both present.
3. Trust boundary disclosure includes explicit external destination.
4. Persistent mutation requires explicit confirmation language.
5. Provenance requirements include all four fields.
6. Residual risk statement exists and does not claim full elimination.

## Consolidation Pattern (Multi-Plan Work)

When multiple plan docs overlap:

1. Create one consolidated execution plan as single source of truth.
2. Keep a "Sources Consolidated" section with explicit source paths.
3. Preserve all unique requirements via phased plan + detailed task matrix.
4. Prefer deleting superseded plan docs after consolidation to prevent drift.

## Done Checklist

- `SKILL.md` has explicit trigger contract and executable workflow.
- `SKILL.md` defines outer governance boundaries (conservative rules, gates, escalation).
- Frontmatter `description` clearly states what + when.
- `README.md` defines style expectations for future contributions.
- `references/` contains heavy details only when needed.
- `references/` extends details without conflicting with `SKILL.md` governance.
- No stale terms, duplicated schema ownership, or contradictory rules.
- Validation evidence is recorded (tool-based or manual).
- Example validation command: `npx --yes skills-ref validate ./skills/<skill-name>`.

## See Also

- [Agent Skills Specification](https://agentskills.io/specification)
- [Claude Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
