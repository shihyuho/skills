# revisit

Recover why a ticket or PR exists and what changed, reassess it against the current version, and discuss the smallest complete change if one is still needed.

Unlike diagnosing a ticket directly, which reports findings against background the reader no longer remembers, it writes for a returning reader: it restores why the ticket was opened before reassessing, and makes the first assessment's response stand alone.

## Usage

```text
$skills:revisit <ticket or PR number or link>
```

Requires `productivity:explain`, `mattpocock-skills:diagnosing-bugs`, and `skills:grill-minimal`, including its `grill-with-docs` dependency.

Defect, performance, and security concerns are reassessed with `diagnosing-bugs`; enhancements are checked for whether the current version already delivers them.

Follow-up discussion builds on the context the returning reader already has. The workflow ends with findings or a discussion of proposed changes; implementation requires separate authorization.
