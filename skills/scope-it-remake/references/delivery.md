# Planning files and shared delivery

Some plans leave files that the next agent needs, such as an ADR or a `CONTEXT.md` change. Save their exact approved version on the actual delivery path before calling publication complete. Implementation, merges and ticket closure remain the executor's work.

## Select the changes

Account for every entry change and newly drafted repository file/patch needed after publication in the approval proposal:

| Treatment | Meaning |
| --- | --- |
| Carry | Proven scope-owned file or independently applicable exact patch that delivery must retain. |
| Remove | Proven scope-owned patch superseded by a durable artifact. |
| Preserve | Unrelated bytes, unchanged. |
| Uncertain | Candidate path/range, missing ownership evidence and recommended treatment. |

Use edit records, snapshots, exact patches or explicit user confirmation as ownership evidence; similarity supports only a recommendation. Include bounded uncertainties in the proposal. Preserve unbounded candidates and ask only when they prevent verifiable delivery. A new draft becomes Carry only after explicit selection of its exact content and repository destination; it need not be written into the entry worktree first.

Without Carry or a saved baseline, report Planning `none`: apply only approved Remove cleanup, with no Carrier, baseline branch/worktree/commit/push or pointer. An independently approved shared-lane bootstrap can still apply.

## Save and hand off

For non-empty Carry, select exactly one **Carrier** (the ticket transporting the files): the only ticket; an earliest executable ticket for independent multi-ticket delivery, using document/foundation ownership to break ties; or the final integrate-and-verify ticket for a shared lane. Bundle approval fixes this choice. Direct delivery starts with its Carrier; shared delivery starts with terminal tickets. Selection creates no parent or blocker edge.

1. Bind the approved operations to the Carrier, repository, exact branch/path, base SHA, isolated worktree, Carry manifest and remote-publication choice. Check ownership, collisions, tools and permissions before mutation. Use available tools under repository/host rules; Git helper skills are optional. An unrelated branch is not reusable, and failures do not authorize forcing, bypassing permissions or choosing another path.
2. Initialize the actual delivery path from the fetched remote default branch: the Carrier's ticket branch for independent delivery, or the canonical integration branch for a shared lane. Commit only Carry as its immutable **Planning Baseline**, before other path commits. Reuse an existing approved path after verifying its baseline diff and ancestry.
3. Make the content retrievable by the executor. A local commit suffices only with verified, accepted shared-repository access. For an unknown executor or another clone/machine, propose and approve publication of the delivery branch to a readable remote, then read back its full SHA and content. A local path or SHA string alone is not a cross-agent handoff. This never authorizes a default-branch push.
4. Put a **Baseline Pointer** on every related ticket and link it from the Map: Carrier URL; repository and exact branch/path; full baseline SHA; landing target; approved Carry manifest with paths/patches and base SHA. Publish its executor duties with it: the Carrier resumes that path with baseline ancestry; other tickets consume pointers, not duplicate Carry or parallel baselines; the target, and ultimately main, must contain Carry.
5. Read back the pointers and accessible baseline before entry cleanup. Verify `baseline diff = all approved Carry`, `entry after = entry before − entry's Carry − Remove`, and byte-for-byte unchanged Preserve. Cleanup touches only approved patches originally present in entry; publishing a new draft adds no entry cleanup. Retain recoverable evidence. Share only approved payloads and non-disclosing preservation receipts; full entry snapshots stay local or in explicitly approved storage with known access/retention.

On interruption, verify existing Git work and fill only missing approved pointers/cleanup. A clean entry, missing comment or unavailable tool does not justify recreating a baseline. Missing evidence, entry drift or leftover patches prevent claiming cleanup complete: reconcile, approve changed writes and preserve successful results plus unrelated new work.

## Shared integration delivery

Use only when multiple terminal tickets must land atomically to main; independent delivery is the default. Verify the canonical branch and applicable rules/checks for both terminal-to-integration and final-to-target paths. Any missing-capability bootstrap is an exact approved write, verified before the lane is considered runnable.

Have the planning skill supply a final integrate-and-verify ticket blocked by every terminal. Publish a lane contract linked from the Map and every terminal/final ticket:

- Canonical branch/target, capability or bootstrap evidence, terminal/final identities and real blockers.
- Optional Baseline Pointer and immutable full integration start SHA, with its capture point.
- Umbrella PR URL, or the final executor's responsibility to bind it when created.
- The executor duties below.

Capture the start during approved publication. With empty Carry, establish the canonical path from the approved base if needed and capture its SHA immediately, before later bootstrap. With Carry, initialize the baseline before any other lane commits or terminal branches, finish approved bootstrap, then capture start and prove baseline ancestry. Mutable integration HEAD, checks and PR receipts never replace baseline/start evidence.

Executor duties:

1. Terminals branch independently from the latest green integration HEAD and use `Refs` or equivalent non-closing PR references.
2. A terminal closes only after merge to integration, required checks on the exact resulting HEAD, and durable PR URL/full-SHA receipts.
3. The final ticket waits for every terminal and owns main-drift reconciliation, aggregate verification, umbrella synchronization and Map-home parent closure after the final gate.
4. Failed or unknown rules/checks/ancestry/exact-head evidence blocks new closure/finalization; retain artifacts and report the affected gate incomplete.

Publish these contracts without waiting for their execution or changing the starting item's lifecycle.

## Requested verification

When this planning skill is invoked only to verify delivery, remain read-only and preserve prior publication; corrective writes require separate exact approval. This audit boundary does not replace the executor's own implementation authorization.

### Executor checks to publish

Include these applicable resume/landing checks in the baseline/lane handoff, with project-specific paths, check names and evidence requirements. The executor reads that published contract, not this skill reference.

Check applicable ticket/relationship evidence, Carrier availability and the exact path/baseline binding and diff. Use evidence appropriate to the stage:

| Evidence | Unfinished delivery | Completed landing |
| --- | --- | --- |
| Carry/baseline | Current same-path HEAD descends from baseline. | Readable immutable implementation/PR head bound to Carrier/path proves baseline ancestry; retired refs need not exist. |
| Shared lane | Current branch/rules and required checks on its exact current HEAD. | Bound final integration/umbrella head with applicable rules/checks for that exact head, even after ref retirement. |

Also verify immutable integration start, baseline ancestry when applicable, and relevant PR/full-SHA receipts. Another head's green checks never fill a gap. Recover missing historical evidence rather than recreating refs.

A cancelled Carrier requires an approved Map amendment before replacement.

Read actual Carry content in the target and, after final landing, main. A baseline, ancestor or merge receipt does not excuse reverted content; squash landing need not preserve baseline ancestry in target/main. Work may resume before Carry lands, but delivery is incomplete until its content gate passes.

Planning `none` skips Carry/baseline checks, not applicable ticket, relationship or shared-lane gates.
