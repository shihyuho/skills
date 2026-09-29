# revisit

Recover why a ticket or PR exists, what changed, and what remains to address or decide, then assess the current version and discuss the smallest complete change if needed.

## Usage

```text
$skills:revisit <ticket or PR number or link>
```

Requires `productivity:explain`, `mattpocock-skills:diagnosing-bugs`, and `skills:grill-minimal`, including its `grill-with-docs` dependency.

Applies across ticket types, including defects, performance, security, and enhancements.

The first assessment response includes enough background and a concrete example to stand alone, even after time away from the issue; follow-up discussion builds on that context.

The workflow ends with findings or a discussion of proposed changes; implementation requires separate authorization.
