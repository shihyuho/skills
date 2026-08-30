# Scope owns conditional planning baselines

> Superseded by [ADR 0004](0004-scope-it-coordinates-portable-delivery-maps.md).

When settled scoping leaves Scope-related Changes, `scope-it` creates one Planning Baseline from the latest remote `main` and assigns exactly one Planning Carrier to transport it into delivery. The only ticket is its own Carrier; without an Integration Delivery Lane (IDL), the approved Delivery Map recommends one first-to-land ticket; with IDL, the final integrate-and-verify ticket carries it on the canonical integration path. Every related ticket receives a Baseline Pointer, while scopes without related file changes retain the tracker-only flow.

## Considered Options

- **Wait for the delivery workflow to move uncommitted files into its worktree** — rejected because dirty worktree state is not a durable cross-session or cross-agent handoff.
- **Require the user to split mixed files or operate Git manually** — rejected because `scope-it` can propose and transport independently verifiable patches while keeping Git mechanics inside the workflow.
- **Create a separate planning ticket and branch for every multi-ticket scope** — rejected because it adds a delivery unit that exists only to carry shared documents.
- **Repeat the same planning changes on every ticket branch** — rejected because it creates duplicate commits instead of one verifiable shared starting point.
- **Keep the baseline as a durable archive only** — rejected because the purpose is to land settled ADR and context changes with delivery, not merely preserve a remote receipt.

## Consequences

Before mutation, `scope-it` proposes how every entry-worktree change will be carried, removed as superseded, preserved, or resolved. Whole files and independently applicable exact patches may enter the baseline when session evidence or a bounded user confirmation establishes ownership; semantic similarity alone supports only a recommendation. An unbounded candidate remains untouched while `scope-it` asks for the smallest content decision, never for Git mechanics.

The baseline is built in an isolated worktree from the latest remote `main`, pushed, and SHA-verified as the immutable start of the Carrier's actual delivery path. Direct delivery reuses the Carrier ticket's issue-linked branch and returns that Carrier as the selected first delivery ticket. IDL places the baseline on the canonical integration path before terminal branches start and records an integration start SHA that descends from it. Carrier selection transports content and creates no blocker edge; other tickets reference the pointer without copying the changes. Each pointer records the Carrier, branch, full SHA, landing target, and the gate that requires the target and final `main` to contain Carry.

Only after publication does `scope-it` subtract the published and superseded scope changes from the entry worktree and verify that every unrelated byte remains unchanged. Planning publication completes at that durable handoff, while delivery completes only when the approved target contains the carried changes and final landing proves `main` contains them. Conflicts, dependent patches, failed ancestry, failed landing, or failed cleanup preserve completed artifacts and leave the affected checkpoint incomplete. A cancelled Carrier requires an updated Delivery Map rather than silent reassignment.
