# Preflight Gate Policy

Use this file as the canonical policy for gate execution order and decision logic.

## Execution Order

Evaluate rows top-to-bottom.

| id | required | run_if | skip_if | blocks_on_fail | detail_file |
| --- | --- | --- | --- | --- | --- |
| G.1 | true | always | none | true | `references/gates/g1-branch-context.md` |
| G.2 | true | always | none | true | `references/gates/g2-worktree-clean.md` |
| G.3 | false | tracking remote exists | no tracking remote | true | `references/gates/g3-remote-sync.md` |

## Decision Semantics

- `required: true` means the gate must be evaluated unless an explicit `skip_if` condition is met.
- `run_if` defines when to evaluate a gate.
- `skip_if` defines when a gate is intentionally skipped.
- `blocks_on_fail: true` means a failing gate blocks plan execution.

Allowed gate outcomes:

- `PASS`: gate conditions satisfied.
- `BLOCK`: gate conditions failed and execution must stop.
- `SKIP`: gate intentionally skipped due to policy condition.

## Preflight Pass Criteria

Preflight passes only when:

1. No evaluated gate returns `BLOCK` with `blocks_on_fail: true`.
2. All required gates were evaluated or explicitly skipped by policy.

## Reporting Contract

For each gate, report:

- gate id
- outcome (`PASS`/`BLOCK`/`SKIP`)
- evidence summary
- next required action (if blocked)

When any gate returns `BLOCK`:

- include at least one concrete suggested remediation action
- include exact command or workflow step the user can approve
- do not continue to plan execution until user confirms the selected next step
