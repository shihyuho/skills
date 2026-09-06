# Planning Carry and delivery options

Read this for repository planning files, a shared lane or special verification/closure duties, including when accepting existing Tickets. The Tickets source owns ticket content; repository and executor workflows own Git, CI and implementation mechanics.

## Planning Carry

For ADRs, `CONTEXT.md` changes or other repository content the executor needs, agree exact scope-owned files/patches, retrievable version/location, landing target and one responsible Carrier Ticket. Similarity or a clean worktree does not establish ownership.

Use repository workflows/tools for approved preservation or publication. An unknown executor needs access beyond a local path; verify content and access as required by the main workflow before cleanup.

For direct delivery, the immutable Planning Baseline starts the Carrier Ticket's final branch. Follow repository naming for its final delivery type and Carrier identity—for example, `fix/1049-terminal-payload-lifecycle` rather than a planning-only branch named from the Carry.

When supported, create the native linked branch from the Carrier's Issue—the Scope Issue when one Ticket is a comment—before a local worktree tracks it. A push alone does not establish native linkage. Unavailable linking uses the repository workflow's approved fallback and degraded evidence.

Record one compact Planning Carry pointer:

- Carrier Ticket and linked branch;
- repository/path, base and baseline full SHAs, plus patch bounds when needed;
- landing target and approved-content obligation.

Before cleanup, verify pointer consistency, content/access and native linkage (on GitHub, the Carrier Issue's `linkedBranches`). Retain an existing delivery-path binding. The executor resumes that branch for implementation, tests, required ADR and the PR to target under separate authority.

## Shared lane and special responsibilities

For an agreed shared delivery lane, have the Tickets source supply a final integration/verification Ticket with dependencies on all terminal Tickets. Record the lane, target, aggregate verification and closure responsibility in the Map, linking the applicable repository workflow.

Preserve agreed conditional duties, including when independent delivery assigns aggregate evidence or parent closure to whichever Ticket finishes last. Record each obligation once with its owner, trigger and required evidence; execution order alone creates no blocker or shared lane.

Git setup, CI rules and implementation belong to the repository/executor workflow. A change to file ownership, delivery path or shared responsibility needs an approved Map amendment.
