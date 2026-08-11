# Scope owns conditional planning baselines

When settled scoping leaves Scope-related Changes, `scope-it` creates one Planning Baseline from the latest remote `main`, pushes it on an issue-linked branch owned by a Planning Owner Ticket, and publishes a Baseline Pointer to every related delivery ticket. This conditional checkpoint is owned by `scope-it` whether invoked directly or through `go-for-it`; scopes without related file changes retain the existing tracker-only flow.

## Considered Options

- **Move uncommitted files when `go-for-it` creates a worktree** — rejected because dirty worktree state is not a durable cross-session or cross-agent handoff.
- **Create a separate planning ticket and branch for every multi-ticket scope** — rejected because it adds a delivery unit that exists only to carry shared documents.
- **Repeat the same planning changes on every ticket branch** — rejected because it creates duplicate commits instead of one verifiable shared starting point.

## Consequences

Only whole files that unambiguously belong to the scope may enter the baseline; ambiguity or conflicts stop the checkpoint. The baseline branch starts from the latest remote `main`, is pushed and SHA-verified, and is released from the originating worktree before handoff. `create-worktree` must be able to attach or track the existing branch, while `go-for-it` must treat a matching baseline as part of Scope completion and resume partial baseline work instead of duplicating it.
