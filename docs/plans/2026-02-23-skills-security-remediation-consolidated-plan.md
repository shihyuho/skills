# Skills Security Remediation Consolidated Plan (fanfuaji + agent-install-guide)

Status: consolidated execution plan
Date: 2026-02-23
Owner: shihyuho/skills maintainers

## Sources Consolidated

- `docs/plans/2026-02-23-fanfuaji-security-remediation.md`
- `docs/plans/2026-02-23-agent-install-guide-security-remediation.md`
- `docs/plans/2026-02-23-skills-security-remediation-roadmap.md`

This document is the single execution plan and replaces cross-reading the three source plans.

## Goal

Reduce command-injection, remote-code-execution, prompt-injection, and data-exfiltration risk across:

- `skills/fanfuaji`
- `skills/agent-install-guide`

while preserving deterministic and practical skill behavior.

## Scope

In scope:

- Policy hardening in skill docs (`SKILL.md`, `README.md`, template references).
- Runtime hardening for `skills/fanfuaji/scripts/fanfuaji.py`.
- Security-focused test coverage for fanfuaji runtime input constraints.
- Validation and external re-audit loop (Agent Trust Hub, Snyk, Socket).

Out of scope:

- Changes unrelated to `fanfuaji` and `agent-install-guide`.
- Infrastructure/runtime changes outside documented skill templates and fanfuaji script runtime.

## Unified Risk Themes

1. Untrusted external content controls agent behavior.
2. Unsafe command patterns in examples can be copied into execution flows.
3. Insufficient guardrails for sensitive files and persistent environment mutation.

## Architecture Strategy

### A. fanfuaji

- Harden policy layer (`skills/fanfuaji/SKILL.md`, `skills/fanfuaji/README.md`) with trust boundaries.
- Harden runtime layer (`skills/fanfuaji/scripts/fanfuaji.py`) with path/content guards.
- Add script-level security tests to lock expected behavior.

### B. agent-install-guide

- Replace risky fetch-and-follow guidance with fetch-review-approval flow.
- Add explicit forbidden command patterns and safer alternatives.
- Add PATH persistence checkpoint and external artifact provenance requirements.

## Execution Plan (Phased)

### Phase 0 - Baseline Snapshot (Day 0)

1. Export current audit findings and keep as baseline.
2. Validate current skill format:

```bash
npx --yes skills-ref validate ./skills/fanfuaji
npx --yes skills-ref validate ./skills/agent-install-guide
```

### Phase 1 - Policy Hardening (Day 0-1)

Apply all policy-only changes first for immediate risk reduction.

#### fanfuaji policy tasks

1. Add threat model and trust boundary in docs.
2. Add sensitive-file guardrails and denylist workflow in SKILL instructions.
3. Add non-execution boundary for converted output (untrusted text).

#### agent-install-guide policy tasks

1. Remove direct fetch-and-follow instruction patterns.
2. Add command safety policy (forbidden patterns + safer alternatives).
3. Harden PATH modification guidance with mandatory confirmation.
4. Add trust-source and provenance requirements.

Outcome target:

- Immediate reduction in prompt-injection and unsafe execution pathways.

### Phase 2 - Runtime Hardening (Day 1-2)

Apply fanfuaji runtime controls and tests.

1. Add centralized file input validator before reads.
2. Enforce blocked secret path patterns and suspicious binary extensions.
3. Enforce max input size with explicit override flag.
4. Add optional safe-directory allowlist mode.
5. Add tests and run fail-first then pass verification:

```bash
python -m pytest skills/fanfuaji/scripts/test_fanfuaji_security.py -q
```

### Phase 3 - Validation and Audit Loop (Day 2)

1. Re-run format validation for both skills:

```bash
npx --yes skills-ref validate ./skills/fanfuaji
npx --yes skills-ref validate ./skills/agent-install-guide
```

2. Re-run external audits and compare with baseline:

- Agent Trust Hub
- Snyk (W011/W012)
- Socket

3. Capture risk delta and residual risks.

### Phase 4 - Governance and Maintenance (Day 3+)

Add recurring PR checklist items for any future skill/template changes:

- no fetch-and-follow language
- no `curl|bash` style examples
- explicit trust boundary and human approval checkpoints
- provenance requirements for external artifacts

Review every new/changed template against this checklist.

## Detailed Task Matrix

### fanfuaji Work Items

1. **Docs boundary + secrets policy**
   - Files:
     - `skills/fanfuaji/SKILL.md`
     - `skills/fanfuaji/README.md`
   - Must include:
     - outbound disclosure to `https://api.zhconvert.org`
     - never process secret files by default (`.env`, `id_rsa`, cloud credentials)
     - redact secrets before conversion

2. **Sensitive-file workflow controls**
   - File: `skills/fanfuaji/SKILL.md`
   - Must include:
     - preflight classify/block/confirm flow
     - denylist examples (`~/.ssh/id_rsa`, `.env`, `*credentials*`, cloud key files)

3. **Runtime hardening + tests**
   - Files:
     - `skills/fanfuaji/scripts/fanfuaji.py`
     - `skills/fanfuaji/scripts/test_fanfuaji_security.py` (new)
   - Must include:
     - centralized validator
     - deterministic blocked-reason errors
     - default max input size (example: 1 MB) + explicit override flag
     - tests for blocked secrets, size threshold, binary extension reject, allowlist mode

4. **Output trust boundary**
   - Files:
     - `skills/fanfuaji/SKILL.md`
     - `skills/fanfuaji/README.md`
   - Must include:
     - output is untrusted data
     - never execute / do not chain into commands

5. **Residual risk documentation**
   - File: `skills/fanfuaji/README.md`
   - Must include:
     - unavoidable external API visibility risk
     - operator guidance: use sanitized text

### agent-install-guide Work Items

1. **Remove fetch-and-follow patterns**
   - Files:
     - `skills/agent-install-guide/references/readme-integration-template.md`
     - `skills/agent-install-guide/README.md`
     - `skills/agent-install-guide/SKILL.md`
   - Must include:
     - fetch -> review/validate -> explicit approval flow
     - no autonomous remote raw URL execution wording

2. **Command safety policy**
   - Files:
     - `skills/agent-install-guide/SKILL.md`
     - `skills/agent-install-guide/references/install-template.md`
   - Must include:
     - forbidden patterns (`curl|bash`, `wget|bash`, unverified scripts)
     - safer alternatives (checksum/signature, version pinning, immutable URL, least privilege)

3. **PATH mutation hardening**
   - Files:
     - `skills/agent-install-guide/SKILL.md`
     - `skills/agent-install-guide/README.md`
   - Must include:
     - persistence impact explanation
     - exact shell rc line
     - explicit user confirmation for persistent change
     - session-scoped default path export first

4. **Provenance requirements**
   - Files:
     - `skills/agent-install-guide/SKILL.md`
     - `skills/agent-install-guide/references/install-template.md`
   - Must include:
     - host allowlist rationale
     - version pin
     - checksum/signature verification command
     - rollback/uninstall command

5. **Residual risk documentation + audits**
   - File: `skills/agent-install-guide/README.md`
   - Must include:
     - concise residual risk note for third-party software dependency
     - external re-audit comparison note

## Verification Checklist

### Required checks during implementation

- fanfuaji docs gap checks:

```bash
grep -n "api.zhconvert.org\|sensitive\|secret\|id_rsa\|.env" skills/fanfuaji/SKILL.md skills/fanfuaji/README.md
grep -n "preflight\|denylist\|id_rsa\|credentials" skills/fanfuaji/SKILL.md
grep -n "untrusted\|never execute\|do not chain" skills/fanfuaji/SKILL.md skills/fanfuaji/README.md
```

- fanfuaji runtime test:

```bash
python -m pytest skills/fanfuaji/scripts/test_fanfuaji_security.py -q
```

- agent-install-guide policy checks:

```bash
grep -n "Fetch and follow\|raw.githubusercontent.com" skills/agent-install-guide/references/readme-integration-template.md skills/agent-install-guide/README.md skills/agent-install-guide/SKILL.md
grep -n "Forbidden command patterns\|curl | sh\|checksum\|signature\|least-privilege" skills/agent-install-guide/SKILL.md skills/agent-install-guide/references/install-template.md
grep -n "session-scoped\|persistent\|confirmation\|shell rc" skills/agent-install-guide/SKILL.md skills/agent-install-guide/README.md
grep -n "allowlist\|version pin\|checksum\|rollback\|uninstall" skills/agent-install-guide/SKILL.md skills/agent-install-guide/references/install-template.md
```

- final skill validation:

```bash
npx --yes skills-ref validate ./skills/fanfuaji
npx --yes skills-ref validate ./skills/agent-install-guide
```

## Definition of Done

- Both skills validate with `skills-ref`.
- Explicit trust boundaries documented in both `SKILL.md` and `README.md` for both skills.
- `fanfuaji` has code-level input guards and passing security tests.
- `agent-install-guide` templates no longer promote direct remote execution flows.
- External audit status improves, or severity remains but exploitability is materially reduced with explicit controls.
