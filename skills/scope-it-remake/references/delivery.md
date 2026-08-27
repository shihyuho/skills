# Conditional delivery planning

Read the relevant branch for entry changes (including unclassified or Uncertain content), existing or pending Carry/Carrier/baseline evidence, or a proposed or enabled shared integration lane. This applies at delivery planning, before conditional publication or repair even with a clean entry worktree, and when the user asks to verify delivery resume or finalization. Queue mutations for final bundle approval; a delivery-verification request alone authorizes readback, not implementation, merges, closure, or repairs.

## Scope-owned worktree changes

Record the entry state and account for every change in the Change Proposal before moving any planning content:

- **Carry:** a proven scope-owned whole file or independently applicable exact patch that delivery must retain.
- **Remove:** a proven scope-owned patch superseded by a durable artifact.
- **Preserve:** unrelated content kept byte-for-byte.
- **Uncertain:** candidate, path, bounded range, ownership evidence, and recommended treatment.

Session records, snapshots, exact patches, or user confirmation establish ownership. Semantic similarity supports a recommendation, not ownership. Bring bounded uncertainties into the current proposal with a recommendation. Preserve unbounded candidates; ask for the smallest content decision only when they prevent an independently verifiable proposal. Temporary drafting snapshots are not Carry unless the user separately selects exact content for delivery.

If no Carry or existing baseline needs delivery, record Planning `none`. Queue only exact Remove patches and verify the cleanup gate below; select no Carrier and perform no baseline branch, worktree, commit, push, or pointer writes. Independently approved lane bootstrap is a separate operation. A clean entry worktree does not erase previously approved Carry or baseline evidence.

For non-empty Carry, recommend exactly one **Planning Carrier**:

- the only ticket for one-ticket delivery;
- one ticket from the earliest executable frontier for independent multi-ticket landing, using document or foundation ownership to break ties; a foundation ticket is not required; or
- the final integrate-and-verify ticket for shared integration branch delivery.

For independent landing with Carry, set the selected first delivery ticket to the Carrier, replacing any earlier provisional choice. For a shared integration lane, keep the approved executable terminal-ticket frontier; the final Carrier is not the first implementation ticket. Carrier selection transports content and creates no containment or blocking edge. Approval of the final bundle fixes the choice without another confirmation.

## Publish or reconcile a Planning Baseline

Resolve the Git mechanics through [sources.md](sources.md#git-mechanics) only for required Git writes. After final approval, create the baseline from the fetched remote default branch in an isolated worktree on the Carrier's actual delivery path. For independent landing, use the Carrier-linked delivery branch; for a shared lane, initialize its canonical integration path as described below. Commit only Carry and publish the approved branch/baseline, retaining its full SHA and approved base.

On resume, recover the approved Change Proposal, Carrier, branch, baseline SHA, target, and existing pointers before planning new writes. Verify that the branch and commit exist, the baseline diff matches Carry, and the recorded baseline is an ancestor of the current delivery-path HEAD. Reuse matching evidence and fill only missing approved pointers or cleanup. Missing or contradictory evidence requires recovery; a clean entry or missing comment is not a reason to recreate a branch, baseline commit, or Carrier.

Publish and read back the following durable pointer on every related ticket before cleaning the entry worktree, and link it from the Map's Planning result:

```markdown
## Planning baseline

- Carrier: <linked delivery ticket>
- Branch: <repository and exact delivery branch/path>
- Commit: <full baseline SHA>
- Landing target: <target branch>
- Carry: <durable approved Change Proposal with exact paths/patches and base SHA>
- Landing gate: Carry must be present in the target and, after final landing, main.
- Continue: Resume this exact delivery path with the baseline SHA as an ancestor of its HEAD. Other tickets consume this pointer; they do not duplicate Carry or create parallel baseline commits.
```

Then apply only the approved Carry and Remove cleanup. Verify all three conditions, including on partial retries:

1. Baseline diff equals approved Carry, when a baseline exists.
2. Entry state after cleanup equals entry state before cleanup minus approved Carry and Remove.
3. Every Preserve byte is unchanged.

Keep recoverable verification evidence without publishing unrelated worktree content. Shared records may retain approved Carry/Remove payloads and exact patch boundaries, plus non-disclosing Preserve hashes or verification receipts. A full entry snapshot, when needed, stays local or in explicitly approved controlled storage with its access and retention recorded; it is not implicitly authorized for tracker upload. If that evidence becomes unavailable, recover it before claiming the affected cleanup invariant verified. If entry state has drifted, reconcile it before cleanup and obtain approval for changed writes; never overwrite new unrelated work. A failed patch, leftover Remove hunk, or invariant mismatch leaves the affected publication checkpoint incomplete while preserving successful artifacts.

Persist the exact-path, ancestor, pointer-only, and landing requirements as the executor's contract. Initial publication can finish once the baseline, pointers, cleanup, and other approved writes verify; implementation and landing may still be pending.

## Shared integration branch delivery

Keep independent ticket landing unless multiple terminal tickets must land atomically to `main` through a shared integration branch. Verify that the canonical branch path, applicable repository rules, and required checks can support terminal-to-integration and final-to-target delivery. If prerequisites need bootstrap, include its exact writes in the final bundle and verify them before treating the lane as runnable; checks alone do not prove the rules permit the lane.

When that condition holds, persist a lane record linked from the Map and the final ticket, containing:

- canonical integration branch and target;
- capability or bootstrap evidence;
- optional full Planning Baseline pointer;
- terminal tickets and the final integrate-and-verify ticket, blocked by every terminal ticket;
- immutable full integration start SHA and its capture point;
- umbrella PR pointer, or `pending` with the final executor responsible for binding it when created; and
- the executor gates below, including final aggregate verification and main-drift reconciliation.

Have the ticket source supply or amend the final ticket and terminal blocking edges before final approval; this reference does not author a missing delivery ticket. Native containment remains separate from these blockers.

Record the start SHA during approved publication, never by an early tracker write during discussion:

- **Empty Carry:** capture the canonical integration path's current full SHA immediately when the lane is established, before subsequent bootstrap or implementation commits. If the path must be created, create it from the approved base first. Keep that start immutable.
- **Non-empty Carry:** initialize the canonical integration path from the fetched base with the baseline before other lane commits or terminal branches. Complete approved capability bootstrap, then capture the immutable integration start SHA and prove the baseline SHA is its ancestor.

Keep mutable integration HEAD, checks, PR progress, and receipts in lane state, separate from immutable baseline and start evidence. Lane movement never rewrites those recorded identities.

Persist these execution obligations in the lane record and relevant tickets:

- Terminal tickets use independent branches from the latest green integration HEAD. Their PRs reference scoped tickets (`Refs` or the tracker's equivalent), without automatic closing keywords.
- A terminal ticket may close only after its PR merges to integration, required checks pass on the exact resulting integration HEAD, and a durable PR URL plus full-SHA receipt exists.
- The final ticket waits for all terminals and owns main-drift reconciliation, aggregate verification, umbrella synchronization, and closure of the Map home itself as the parent tracker item after the final gate. Parent lifecycle closure is separate from publishing the agreed Map.
- Failed, unknown, or contradictory branch/rule, check, ancestry, or exact-HEAD evidence blocks new child closure and finalization. Preserve completed artifacts and report the affected delivery checkpoint incomplete.

The executor performs implementation, merges, and lifecycle changes under its own authorization. This skill publishes their contract and verifies requested evidence; initial publication preserves the starting item's lifecycle.

## Requested delivery verification

When the user asks whether delivery can resume or be finalized, read the saved contracts and fresh evidence even after the agreed Map has been published. A pure request for the existing handoff can return its links without running this lifecycle audit. Neither request alone authorizes progress updates on the Map.

- **With non-empty Carry or an existing baseline:** check Carrier availability, the recorded path/baseline binding, and baseline diff. Before unfinished implementation resumes, require the exact live path and baseline ancestry of its current HEAD. For already completed landing, recover an immutable implementation or PR-head SHA bound to that Carrier and path, and verify baseline ancestry there; a retired branch need not still exist. Missing historical evidence leaves that verification incomplete and calls for recovery, not recreating refs. A cancelled Carrier leaves delivery incomplete until an approved Map amendment selects another; do not reassign it silently.
- **For that Carry's landing gate:** read its actual content from the approved landing target and report whether the gate has been met. Work may resume before landing, but delivery cannot be declared complete until the target contains Carry. After final landing, also verify Carry content in `main`. A squash landing may preserve the content without preserving the original baseline SHA in target/main ancestry; that is valid. Ancestry checks on the original implementation path do not impose a baseline-ancestor requirement on squash landing targets, and ancestry alone cannot detect reverted Carry.
- **With an enabled lane:** before unfinished delivery resumes or finalizes, recheck applicable current branch/rule evidence and required checks on the current exact integration HEAD. For already completed landing, recover the immutable final integration or umbrella PR-head SHA bound to that lane and approved landing; verify the applicable rule evidence and required checks for that exact final head without requiring a retired integration ref. In either case, verify immutable start identity, baseline ancestry when a baseline exists, and relevant PR/SHA receipts. Missing historical evidence leaves verification incomplete; a green result for a different head is insufficient.

For Planning `none`, skip Carrier, baseline, and Carry-landing checks. Verify only the published ticket/relationship and any enabled lane evidence relevant to the request; an empty-Carry lane still has its recorded integration start and executor gates. Missing inapplicable baseline fields are not failures and do not authorize creating them.

Report the scoped result without redoing successful publication, starting implementation, or changing tracker lifecycle. Preserve earlier publication success while reporting an affected delivery checkpoint incomplete; any corrective Map, tracker, or Git writes need their own exact approved amendment.
