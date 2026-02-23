# Skills Security Remediation Roadmap (fanfuaji + agent-install-guide)

## Scope

- Skill A: `skills/fanfuaji`
- Skill B: `skills/agent-install-guide`
- Input audits: Agent Trust Hub, Snyk, Socket

## Unified Risk Themes

1. **Untrusted external content controls agent behavior**
2. **Unsafe command patterns in examples can be copied into execution flows**
3. **Insufficient guardrails for sensitive files and persistent environment mutation**

## Execution Order

### Phase 0 - Baseline snapshot (Day 0)

- Export current audit findings and keep as baseline.
- Run validation:

```bash
npx --yes skills-ref validate ./skills/fanfuaji
npx --yes skills-ref validate ./skills/agent-install-guide
```

### Phase 1 - Policy hardening (Day 0-1)

- Apply plan in `docs/plans/2026-02-23-fanfuaji-security-remediation.md` Task 1-2, 4.
- Apply plan in `docs/plans/2026-02-23-agent-install-guide-security-remediation.md` Task 1-4.
- Outcome: immediate reduction in prompt-injection and unsafe execution pathways.

### Phase 2 - Runtime hardening (Day 1-2)

- Implement `fanfuaji.py` input path and size guardrails (fanfuaji Task 3).
- Add/execute script-level tests for blocked secret files and unsafe input patterns.

### Phase 3 - Validation and audit loop (Day 2)

- Re-run `skills-ref validate` for both skills.
- Re-run all three external audits.
- Diff against baseline and capture risk delta.

### Phase 4 - Governance and maintenance (Day 3+)

- Add recurring checklist in PR workflow:
  - no fetch-and-follow language,
  - no `curl|bash` style examples,
  - explicit trust boundary and human approval checkpoints.
- Review every new/changed template against this checklist.

## Definition of Done

- Both skills still validate with `skills-ref`.
- Explicit trust boundaries documented in `SKILL.md` and `README.md`.
- `fanfuaji` has code-level input guards + tests passing.
- Audit status improves (or same severity with materially reduced exploitability and explicit controls).
