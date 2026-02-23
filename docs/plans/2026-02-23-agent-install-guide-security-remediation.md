# Agent Install Guide Security Remediation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reduce command-injection, remote-code-execution, and third-party prompt-injection risk in `agent-install-guide` without losing usefulness for deterministic install documentation.

**Architecture:** Convert risky "fetch-and-follow" guidance into "fetch-review-execute" with explicit human checkpoints. Tighten templates so examples are safe-by-default, and move risky patterns into clearly marked anti-patterns with verification requirements.

**Tech Stack:** Markdown policy and templates (`SKILL.md`, `README.md`, `references/*.md`).

---

### Task 1: Remove direct "fetch and follow" instruction patterns

**Files:**
- Modify: `skills/agent-install-guide/references/readme-integration-template.md`
- Modify: `skills/agent-install-guide/README.md`
- Modify: `skills/agent-install-guide/SKILL.md`

**Step 1: Write failing policy check**

- Define prohibited phrase set:
  - `Fetch and follow instructions`
  - any phrase implying direct execution of remote raw URL content.

**Step 2: Verify current violations**

Run:

```bash
grep -n "Fetch and follow\|raw.githubusercontent.com" skills/agent-install-guide/references/readme-integration-template.md skills/agent-install-guide/README.md skills/agent-install-guide/SKILL.md
```

Expected: Existing template demonstrates direct fetch-and-follow flow.

**Step 3: Implement safer wording**

- Replace with mandatory 3-phase workflow:
  1. fetch,
  2. summarize + validate,
  3. require explicit human approval before execution.
- Keep URL examples but never as autonomous execution source.

**Step 4: Verify**

Run:

```bash
grep -n "fetch\|review\|approval\|must not execute" skills/agent-install-guide/references/readme-integration-template.md
```

Expected: New review gate language present; prohibited phrase removed.

### Task 2: Add command safety policy for high-risk install snippets

**Files:**
- Modify: `skills/agent-install-guide/SKILL.md`
- Modify: `skills/agent-install-guide/references/install-template.md`

**Step 1: Define fail condition**

- No explicit ban on dangerous command patterns (`curl | sh`, unverified setup scripts, blind shell rc mutation).

**Step 2: Implement policy controls**

- Add "Forbidden command patterns" section:
  - forbid `curl|bash` / `wget|bash` style examples,
  - forbid backticks for dynamic command substitution in generated instructions,
  - forbid credential-file access in install docs unless strictly necessary and user-approved.
- Add "Safer alternatives" section:
  - checksum/signature verification,
  - pinned version + immutable release artifact URL,
  - explicit least-privilege install paths.

**Step 3: Verify**

Run:

```bash
grep -n "Forbidden command patterns\|curl | sh\|checksum\|signature\|least-privilege" skills/agent-install-guide/SKILL.md skills/agent-install-guide/references/install-template.md
```

Expected: Clear hard policy and alternatives present.

### Task 3: Harden PATH modification guidance

**Files:**
- Modify: `skills/agent-install-guide/SKILL.md`
- Modify: `skills/agent-install-guide/README.md`

**Step 1: Define fail condition**

- PATH mutation currently presented without risk-tiering/human confirmation.

**Step 2: Implement control flow**

- Add mandatory prompt checkpoint before shell rc modification:
  - explain persistence impact,
  - show exact line to append,
  - require user confirmation.
- Add safer default: session-scoped PATH export for immediate use, persistent change only after approval.

**Step 3: Verify**

Run:

```bash
grep -n "session-scoped\|persistent\|confirmation\|shell rc" skills/agent-install-guide/SKILL.md skills/agent-install-guide/README.md
```

Expected: Explicit two-step PATH policy exists.

### Task 4: Add trust-source and provenance requirements for external artifacts

**Files:**
- Modify: `skills/agent-install-guide/SKILL.md`
- Modify: `skills/agent-install-guide/references/install-template.md`

**Step 1: Define fail condition**

- External URLs and scripts can be referenced without provenance standard.

**Step 2: Implement provenance rules**

- Require documenting all external sources with:
  - host allowlist rationale,
  - version pin,
  - checksum/signature verification command,
  - rollback/uninstall command.

**Step 3: Verify**

Run:

```bash
grep -n "allowlist\|version pin\|checksum\|rollback\|uninstall" skills/agent-install-guide/SKILL.md skills/agent-install-guide/references/install-template.md
```

Expected: Provenance checklist present.

### Task 5: Re-validate and re-audit

**Files:**
- Modify: `skills/agent-install-guide/README.md`

**Step 1: Validate skill format**

Run:

```bash
npx --yes skills-ref validate ./skills/agent-install-guide
```

Expected: Validation passes.

**Step 2: Document residual risk**

- Add concise note: install docs inherently reference external software; risk is reduced by review gates and provenance checks, not eliminated.

**Step 3: Re-run external audits**

- Re-run and compare against baseline:
  - Agent Trust Hub: MEDIUM warn -> target LOW or lower-confidence MEDIUM.
  - Socket: Fail -> target Warn/Pass after removal of high-risk phrase patterns.
  - Snyk W011/W012: retain detection possibility but with explicit non-execution constraints.

---

## Priority and Sequencing

1. Task 1 (remove fetch-and-follow) - highest impact for Snyk W011/W012 and prompt-injection path.
2. Task 2 (forbidden patterns + safer examples) - addresses Socket critical/high command findings.
3. Task 3 (PATH mutation gating) - mitigates persistence abuse.
4. Task 4 (provenance policy) - lowers RCE and external-download risk.
5. Task 5 (validate + re-audit) - evidence of remediation.
