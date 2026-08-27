# Conditional delivery planning

Read only the branch activated by the current `delivery` frontier. This frontier plans the work; queue every tracker, repository, and Git mutation for the final publication checkpoint. Content confirmation alone does not execute this reference's writes.

## Scope-owned worktree changes

Account for every entry-worktree change before moving any planning content:

- **Carry:** a proven scope-owned whole file or independently applicable exact patch that delivery must retain.
- **Remove:** a proven scope-owned patch superseded by a durable artifact.
- **Preserve:** unrelated content kept byte-for-byte.
- **Uncertain:** a bounded candidate with its evidence and recommended treatment.

Session records, snapshots, exact patches, or user confirmation establish ownership. Semantic similarity supports a recommendation, not ownership. Preserve unbounded candidates and ask only for the smallest content decision that can bound them.

If Carry is empty, propose Planning `none` and queue any exact Remove patches for final publication, then verify Preserve after applying them. If Carry is non-empty, recommend exactly one **Planning Carrier** in the delivery proposal:

- the only ticket for one-ticket delivery;
- a foundation ticket from the earliest executable frontier for independent multi-ticket landing; or
- the final integrate-and-verify ticket for shared integration branch delivery.

After final bundle approval, create or resume the Carrier's actual delivery path from the fetched default branch in an isolated worktree. Commit only Carry as its immutable Planning Baseline, verify the full SHA and ancestry, publish the pointer on every related ticket, then remove only approved Carry and Remove from the entry worktree. Publication completion requires baseline diff equal to Carry and every Preserve byte unchanged. Temporary drafting snapshots are not Carry unless the user separately selects exact content for delivery.

The Carrier transports planning content; it adds no containment or blocker edge. A cancelled Carrier requires an updated delivery proposal and fresh approval of affected publication writes.

## Shared integration branch delivery

Keep independent ticket landing unless multiple terminal tickets must land atomically through a shared integration branch and repository evidence proves that required checks can run on its exact HEAD.

When that condition holds, include the lane in the delivery proposal and final publication checkpoint with:

- canonical integration branch and target;
- capability or bootstrap evidence;
- terminal tickets and final integrate-and-verify ticket;
- immutable integration start SHA timing; and
- final aggregate verification and main-drift gate.

With Carry, put the Planning Baseline on the canonical integration path first and prove it is an ancestor of the subsequently recorded integration start SHA. Terminal tickets branch from the latest green integration HEAD. Close a terminal ticket only after its PR merges to integration, required checks pass on the exact resulting HEAD, and durable PR URL plus full-SHA evidence exists. The final ticket owns aggregate verification, main-drift reconciliation, umbrella synchronization, and Delivery Map closure.

Failed or contradictory planning evidence leaves delivery unresolved. Failures during publication preserve completed artifacts and leave `publish` incomplete with its actual results recorded.
