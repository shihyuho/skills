# Planning Carry and delivery options

Read this for repository planning files, planning worktree creation or cleanup, a shared lane or special verification/closure duties, including when accepting existing Tickets. The Tickets source owns ticket content; repository and executor workflows own Git, CI and implementation mechanics.

Source and worktree cleanup must leave required planning content retrievable through the handoff's recorded locations. Retain any required local parent, Scope, Ticket or Map path until an approved replacement and its updated binding are verified.

## Planning Carry

For ADRs, `CONTEXT.md` changes or other repository content the executor needs, agree exact scope-owned files/patches, retrievable version/location, landing target and one responsible Carrier Ticket. Preserve unrelated bytes and keep uncertain ownership unresolved; similarity or a clean worktree does not establish ownership.

Record the pre-move source state and Carry ownership separately in the index and worktree, including differing staged and unstaged versions.

Carry each confirmed planning patch still needed for delivery, even when Ticket acceptance quotes its content or assigns later recreation. Acceptance defines the requirement; Carry preserves the existing patch for the executor. This includes one-line edits and single-Ticket plans; direct delivery uses the final branch below.

Present the exact patch, Carrier, final branch/baseline plan, source cleanup and temporary worktree removal together. Approval covers that move and cleanup; reuse it without reconfirming unchanged scope. Respect an explicit request to retain source copies or a worktree. When authority or preservation evidence is missing, expose only the gap and keep the delivery obligation unresolved.

Use repository workflows/tools for preservation, publication and cleanup. An unknown executor needs access beyond a local path.

For direct delivery, the immutable Planning Baseline starts the Carrier Ticket's final branch. Follow repository naming for its final delivery type and Carrier identity—for example, `fix/1049-terminal-payload-lifecycle` rather than a planning-only branch named from the Carry.

When supported, create the native linked branch from the Carrier's Issue—the Scope Issue when one Ticket is a comment—before a local worktree tracks it. A push alone does not establish native linkage. Unavailable linking uses the repository workflow's approved fallback and degraded evidence.

Record one compact Planning Carry pointer:

- Carrier Ticket and linked branch;
- repository/path, base and baseline full SHAs, plus patch bounds when needed;
- landing target and approved-content obligation.

Before cleanup or reporting Carry complete, verify pointer consistency, selected content, executor access and native linkage (on GitHub, the Carrier Issue's `linkedBranches`). Retain an existing delivery-path binding. The executor resumes that branch for implementation, tests, required ADR and the PR to target under separate authority.

After those checks, finish the approved move in the source worktree, even on `main`. Re-read selected sources against the agreed patch and each layer's recorded pre-move state: delete unchanged untracked files wholly included in Carry; for tracked or mixed files, remove only that layer's recorded Carry changes, preserving other bytes and their staged/unstaged state. Preserve branch history. Changed or uncertain sources stay intact.

Verify the resulting source state and applicable [worktree cleanup](#worktree-cleanup) before declaring Carry complete. Failed checks or cleanup leave that work unresolved while preserving successful publication. If the user requested retention, verify and report the agreed retained state instead.

## Worktree cleanup

Account for worktrees created by this planning run, including invoked workflows, whether or not Carry exists. Keep creation evidence and repository/path/ref/HEAD identities in the approval context to distinguish them from pre-existing worktrees. Include temporary worktree removal in the creation or Carry proposal and reuse matching approval.

Once their planning or publication purpose is complete, remove those owned worktrees after required content and executor access are verified. Future execution on the same branch does not require retaining its current worktree. Keep worktrees explicitly retained or handed over for continued work, along with pre-existing or ownership-uncertain worktrees.

Before removal, confirm the registered identity, required commits and output still match the approved cleanup state. Verify that required commits will remain reachable through retained refs or durable publication accessible to the executor after removal. Inspect staged, unstaged, untracked and ignored content. Preserve worktrees with unpreserved work, locks, ongoing use or unresolved identity changes. Leave the directory before ordinary non-force removal; preserve local/remote branches and Carry pointers. Verify both deregistration and directory removal.

Report removed and retained worktrees with reasons. A failed or uncertain required removal leaves cleanup incomplete while preserving successful publication; agreed retention satisfies that worktree's planning obligation. Reuse verified removal receipts on resume without recreating the worktree.

## Shared lane and special responsibilities

For an agreed shared delivery lane, have the Tickets source supply a final integration/verification Ticket with dependencies on all terminal Tickets. Record the lane, target, aggregate verification and closure responsibility in the Map, linking the applicable repository workflow.

Preserve agreed conditional duties, including when independent delivery assigns aggregate evidence or parent closure to whichever Ticket finishes last. Record each obligation once with its owner, trigger and required evidence; execution order alone creates no blocker or shared lane.

Git setup, CI rules and implementation belong to the repository/executor workflow. A change to file ownership, delivery path or shared responsibility needs an approved Map amendment.
