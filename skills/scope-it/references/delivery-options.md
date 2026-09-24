# Planning Carry and delivery options

Read this for repository planning files, planning worktree creation or transfer, a shared lane or special verification/closure duties, including when accepting existing Tickets. This coordinator settles the delivery contract and prepares its inputs; `to-afk-agent` owns preservation, publication and source/worktree disposition under its current workflow.

## Prepare Planning Carry

Reconcile all planning artifacts against the settled scope and current repository state. Distinguish repository content with a landing obligation from content supplied only for Issue-comment publication. For ADRs, `CONTEXT.md` changes or other required repository content, establish exact scope-owned files/patches, their index/worktree versions, ownership evidence, repository and landing target. Preserve unrelated bytes and keep uncertain ownership unresolved.

Carry confirmed planning patches still needed for delivery even when Ticket acceptance quotes them or assigns later recreation. An Issue comment can preserve a supplied document, but does not discharge a repository patch's landing obligation. A clean worktree or semantic similarity does not establish ownership or eliminate an existing delivery obligation.

Retain verified Carrier and delivery-path bindings. Resolve a missing Carrier under the handoff workflow using the established Ticket order and repository ownership; settle conflicts before publication. Carry ownership creates no blocker. For direct delivery, the Planning Baseline starts the Carrier's final delivery branch; repository naming, native Issue linkage, preservation and access checks belong to `to-afk-agent`.

Prepare the Map's compact Carry entry with the Carrier, repository/paths or exact patch bounds, landing target and approved-content obligation. Identify only the branch, base/baseline full SHA and immutable-link positions that the delegate may fill from verified results. A change to the Carrier, target or delivery obligation returns to this coordinator for an approved Map revision.

Pass existing remote artifacts and preservation evidence for reuse, together with explicit retention/cleanup choices or unresolved legacy source-choice questions. Let the handoff workflow resolve what still needs preservation; reuse verified publication rather than creating a second baseline. Keep required drafts and continuation paths available until their replacements and bindings are verified.

## Transfer planning worktrees

Account for temporary worktrees created by this planning run and its invoked workflows, including when Carry is empty. Record creation or transfer evidence and current repository/path/ref/HEAD identities. Explicitly entrust the eligible worktrees to `to-afk-agent` within the handoff's cleanup scope, carrying forward retention choices and any continuing use or required local paths.

The delegate verifies preservation, source disposition, worktree eligibility and removal under its own cleanup rules. Existing, unrelated or ownership-uncertain worktrees stay outside the transfer. Retaining a source at an agreed worktree path can require retaining that worktree too. Keep successful publication and removal evidence on interruption; unresolved required disposition leaves the handoff incomplete.

## Shared lane and special responsibilities

For an agreed shared delivery lane, have the Tickets source supply a final integration/verification Ticket with dependencies on all terminal Tickets. Record the lane, target, aggregate verification and closure responsibility in the Map, linking the applicable repository workflow.

Preserve agreed conditional duties, including when independent delivery assigns aggregate evidence or parent closure to whichever Ticket finishes last. Record each obligation once with its owner, trigger and required evidence; execution order alone creates no blocker or shared lane.

Integration setup, CI rules and implementation remain with the repository/executor workflow. A change to file ownership, delivery path or shared responsibility needs an approved Map amendment; verified handoff values alone do not authorize such a change.
