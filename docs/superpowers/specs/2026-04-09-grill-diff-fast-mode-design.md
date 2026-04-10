# grill-diff — Design Spec

## Objective

Specialist-filtered code review. The agent reviews every file and interrogates every aspect. When a potential issue is found, 3 fixed specialists (detective, attacker, gatekeeper) evaluate it internally. Only high-value findings reach the user for discussion. Deep interactive grilling is handled by the separate `grill-me` skill.

## Diff Scope

Two independent dimensions that combine freely (e.g. "against develop src/auth.ts"):

- **File scope:** user-specified files if listed, otherwise all changed files.
- **Diff baseline** (priority cascade): staged > unstaged > user-specified branch > PR URL > current branch vs default branch.

## Spec/Plan Context

Ask the user once if there is a related spec or plan file. If provided, used as background knowledge during review. The `gatekeeper` specialist uses it for bidirectional coverage/overreach/alignment analysis.

## Specialists

Three fixed specialists, all consulted for every finding. Sequential consultation — later specialists see earlier opinions.

**detective** — Correctness & Edge Cases
- Does this code do what it intends to do?
- Are edge cases handled — null, empty, boundary values, error paths?
- Are there race conditions, off-by-one errors, or state inconsistencies?

**attacker** — Security
- Is user input validated and sanitized at system boundaries?
- Are secrets kept out of code, logs, and version control?
- Is authentication/authorization checked where needed?
- Are there injection risks — SQL, command, template, or otherwise?
- Are new dependencies introduced? Are they from trusted sources?

**gatekeeper** — Necessity & Scope
- Is this change needed? What breaks if we revert it?
- With spec/plan: Is every spec requirement addressed? Is every change traceable to a spec requirement? Does the implementation match the spec's described behavior?
- Without spec/plan: Is this change doing too much — should it be split?

## Review Flow

```
0. Ask for spec/plan file
1. Read all changed files
2. Go through files one at a time, interrogate every aspect
3. When a finding is spotted:
   → consult detective, attacker, gatekeeper sequentially
   → each gives opinion + confidence (high / medium / low)
   → classify: high → present, medium/disagree → present as uncertain, all low → drop
4. Aggregate file's findings: merge duplicates, link related
5. Present surviving findings to user one at a time, discuss until shared understanding
6. Files with no surviving findings advance silently
```

### Classification

| Conclusion | Rule | Action |
|------------|------|--------|
| **Needs change** | Any specialist rated high confidence | Present to user |
| **Uncertain** | Highest confidence is medium, or specialists disagree | Present to user, marked as "uncertain" |
| **No issue** | All specialists rated low confidence | Silently drop |

### Self-Explore

If a question can be answered by exploring the codebase, specs, or tests, explore instead of asking the user. This applies during both the review phase and the user discussion phase.

## Non-Goals

- No mode selection — this skill is specialist-filtered only. Deep interactive grilling is `grill-me`.
- No subagent architecture — all specialist consultation happens within the primary agent context.
- No dynamic specialist selection — 3 fixed specialists, always all 3.
- No summary report — findings are addressed inline per file.

## Success Criteria

- Every finding that reaches the user is worth discussing (low false positive rate).
- Real issues are not silently dropped (low false negative rate — uncertain findings surface to user).
- Specialist opinions add genuine signal — not 3 copies of the same judgment.
- When a spec/plan is provided, gatekeeper performs bidirectional coverage analysis.
- Self-explore is used to avoid unnecessary user interruption.
