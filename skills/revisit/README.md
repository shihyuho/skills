# revisit

Recover why a ticket or PR exists and what changed, reassess it against the current version, and discuss the smallest complete change if one is still needed. Unlike diagnosing a ticket directly, which reports findings against background the reader no longer remembers, it writes for a returning reader: it restores why the ticket was opened before reassessing, and makes the first assessment's response stand alone.

## When to use

- You come back to a ticket or PR after time away and no longer remember why it was opened.
- You need to know whether an old ticket still applies to the current version or was overtaken by later changes.
- You pick up a ticket whose history you never followed.

This skill must be invoked explicitly. For a fresh failure you are already in the middle of, use `diagnosing-bugs` directly, because revisit spends its first phase restoring history you still have.

## Before you start

- `productivity:explain`, `mattpocock-skills:diagnosing-bugs`, and `skills:grill-minimal` with its `grill-with-docs` dependency are installed.
- The agent can read the ticket or PR, such as through a logged-in `gh` for GitHub.

## Getting started

```text
$skills:revisit <ticket or PR number or link>
```

## Restore, reassess, decide

Each run takes the ticket through three phases, each handled by an existing skill:

| Phase | Skill | What you get |
|---|---|---|
| Restore | `explain` | Why the ticket or PR exists, through one concrete situation |
| Reassess | `diagnosing-bugs` for a defect, performance, or security concern; a current-version check for an enhancement | Findings against a named version |
| Decide | `grill-minimal`, when a change is still needed | A discussion of the smallest complete change; otherwise why no action is needed, or what remains unverified |

The first assessment response is written for a returning reader who may read nothing else: it leads with why the ticket was opened, then the current-version findings, then the next decision, keeping the original report, current evidence, and proposed changes apart. Follow-ups build on that context and add only the background the question needs.

## It's working if

- The first response tells you why the ticket was opened, through a concrete situation, before any current-version finding.
- You could retell the ticket's story from the final response alone, without scrolling back through progress messages.
- Findings name the version they were checked against.
- An example the ticket's history does not back is marked as illustrative.
- An enhancement gets a capability check rather than a bug hunt.

## Limitations

- It stops at findings or a discussion; implementation needs your separate go-ahead.
- Missing history or evidence is reported as a limit rather than reconstructed, and a concern without confirming evidence stays unverified rather than resolved.
