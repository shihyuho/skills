# Preflight Gate Policy

Use this file as the canonical policy for gate execution order and decision logic.

## Execution Order

Evaluate rows top-to-bottom.

| id | skip_if | blocks_on_fail | detail_file |
| --- | --- | --- | --- |
| G.1 | not a git repository | true | `references/gates/g1-branch-context.md` |
| G.2 | not a git repository | true | `references/gates/g2-worktree-clean.md` |
| G.3 | not a git repository OR no tracking remote | true | `references/gates/g3-remote-sync.md` |

### Allowed gate outcomes

- `PASS`: gate conditions satisfied.
- `BLOCK`: gate conditions failed; execution halts only when `blocks_on_fail: true`.
- `SKIP`: gate intentionally skipped due to policy condition.

## Decision Semantics

- Every gate is evaluated in listed order unless its `skip_if` condition is met.
- `skip_if` defines when a gate is intentionally skipped.
- `blocks_on_fail: true` means outcome `BLOCK` halts plan execution.
- Use `git rev-parse --is-inside-work-tree` to check whether preflight is inside a git repository.
- If the check fails, treat the context as non-git and apply policy `skip_if` rules.

## Preflight Pass Criteria

Preflight passes only when:

1. No evaluated gate returns `BLOCK` with `blocks_on_fail: true`.
2. Every listed gate must be evaluated or explicitly skipped by policy.

## Reporting Contract

For each gate, report:

- gate id
- gate outcome
- evidence summary
- next required action (if gate outcome is `BLOCK` and `blocks_on_fail: true`)

When any gate returns `BLOCK` with `blocks_on_fail: true`:

- include at least one concrete suggested remediation action
- include exact command or workflow step the user can approve
- do not continue to plan execution until user confirms the selected next step
