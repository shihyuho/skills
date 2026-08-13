# Scope owns conditional planning baselines

When settled scoping leaves Scope-related Changes, `scope-it` creates one Planning Baseline from the latest remote `main`, pushes it on an issue-linked branch owned by a Planning Owner Ticket, and publishes a Baseline Pointer to every related delivery ticket. This conditional checkpoint is owned by `scope-it` whether invoked directly or delegated by another skill; scopes without related file changes retain the existing tracker-only flow.

## Considered Options

- **Wait for the delivery workflow to move uncommitted files into its worktree** — rejected because dirty worktree state is not a durable cross-session or cross-agent handoff.
- **Require the user to split mixed files or operate Git manually** — rejected because `scope-it` can propose and transport independently verifiable patches while keeping Git mechanics inside the workflow.
- **Create a separate planning ticket and branch for every multi-ticket scope** — rejected because it adds a delivery unit that exists only to carry shared documents.
- **Repeat the same planning changes on every ticket branch** — rejected because it creates duplicate commits instead of one verifiable shared starting point.

## Consequences

Before mutation, `scope-it` proposes how every entry-worktree change will be carried, removed as superseded, preserved, or resolved. Whole files and independently applicable exact patches may enter the baseline when session evidence or a bounded user confirmation establishes ownership; semantic similarity alone supports only a recommendation. An unbounded candidate remains untouched while `scope-it` asks for the smallest content decision, never for Git mechanics.

The baseline is built in an isolated worktree from the latest remote `main`, pushed, and SHA-verified. Only after publication does `scope-it` subtract the published and superseded scope changes from the entry worktree and verify that every unrelated byte remains unchanged. Conflicts, dependent patches, or failed cleanup preserve completed artifacts and leave the checkpoint incomplete. `create-worktree` must be able to attach or track the existing branch, while a delegating skill must treat a matching baseline as part of Scope completion and resume partial baseline work instead of duplicating it.
