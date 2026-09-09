# Planning Carry and delivery options

Read this for repository planning files, a shared lane or special verification/closure duties, including when accepting existing Tickets. The Tickets source owns ticket content; repository and executor workflows own Git, CI and implementation mechanics.

## Planning Carry

For ADRs, `CONTEXT.md` changes or other repository content the executor needs, agree exact scope-owned files/patches, retrievable version/location, landing target and one responsible Carrier Ticket. Preserve unrelated bytes and keep uncertain ownership unresolved; similarity or a clean worktree does not establish ownership.

Carry each confirmed planning patch still needed for delivery, even when Ticket acceptance quotes its content or assigns later recreation. Acceptance defines the requirement; Carry preserves the existing patch for the executor. This includes one-line edits and single-Ticket plans; direct delivery uses the final branch below.

Present the exact patch, Carrier, final branch/baseline plan and source cleanup together. Approval covers preservation and cleanup of those same selected changes; reuse it through cleanup without reconfirming unchanged scope. Respect an explicit request to retain source copies. When authority or preservation evidence is missing, expose only the gap and keep the delivery obligation unresolved.

Use repository workflows/tools for preservation, publication and cleanup. An unknown executor needs access beyond a local path.

For direct delivery, the immutable Planning Baseline starts the Carrier Ticket's final branch. Follow repository naming for its final delivery type and Carrier identity—for example, `fix/1049-terminal-payload-lifecycle` rather than a planning-only branch named from the Carry.

When supported, create the native linked branch from the Carrier's Issue—the Scope Issue when one Ticket is a comment—before a local worktree tracks it. A push alone does not establish native linkage. Unavailable linking uses the repository workflow's approved fallback and degraded evidence.

Record one compact Planning Carry pointer:

- Carrier Ticket and linked branch;
- repository/path, base and baseline full SHAs, plus patch bounds when needed;
- landing target and approved-content obligation.

Before cleanup or reporting Carry complete, verify pointer consistency, selected content, executor access and native linkage (on GitHub, the Carrier Issue's `linkedBranches`). Retain an existing delivery-path binding. The executor resumes that branch for implementation, tests, required ADR and the PR to target under separate authority.

After those checks, finish the move by removing only the delivered pending changes from the source worktree, even on `main`. Re-read selected sources against the agreed patch and recorded pre-move state: delete unchanged untracked files wholly included in Carry; for tracked or mixed files, remove only Carry from the worktree and index, preserving other bytes and their staged/unstaged state. Preserve branch history. Changed or uncertain sources stay intact.

Verify the resulting source state before declaring Carry complete. Failed checks or cleanup leave that work unresolved while preserving successful publication. If the user requested source retention, verify and report that state instead.

## Shared lane and special responsibilities

For an agreed shared delivery lane, have the Tickets source supply a final integration/verification Ticket with dependencies on all terminal Tickets. Record the lane, target, aggregate verification and closure responsibility in the Map, linking the applicable repository workflow.

Preserve agreed conditional duties, including when independent delivery assigns aggregate evidence or parent closure to whichever Ticket finishes last. Record each obligation once with its owner, trigger and required evidence; execution order alone creates no blocker or shared lane.

Git setup, CI rules and implementation belong to the repository/executor workflow. A change to file ownership, delivery path or shared responsibility needs an approved Map amendment.
