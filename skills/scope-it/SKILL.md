---
name: scope-it
description: "Compose upstream spec and ticket workflows into one approved Delivery Map and durable scope package."
license: MIT
disable-model-invocation: true
---

# scope-it

Turn settled work into one Delivery Map, approve it once, then materialize its spec, ready-for-agent tickets, native relationships, and optional repository delivery artifacts.

## Contract

`$ARGUMENTS` supplements the conversation. Direct invocation or delegation from another skill authorizes only this package's tracker and repository mutations, including exact cleanup of its confirmed worktree changes. Never alter unrelated changes, close the starting issue, or commit or push the default branch.

This is a thin orchestrator. Use `to-spec` at runtime for spec analysis and content, `to-tickets` for tracer-bullet ticket analysis and content, and `create-branch`, `create-worktree`, `commit`, and `push` for Git mechanics. Use each source only when its phase is incomplete. The sources remain authoritative for their phase rules; `scope-it` owns their shared interaction and mutation boundary, publication shape, Delivery Map, reconciliation, and approval.

Reconcile toward the approved map: reuse equivalent artifacts, apply the smallest missing delta, and read it back. Ask outside the map only when conflicting evidence prevents one defensible proposal.

## Flow

### 1. Draft at the shared boundary

Follow `to-spec` to synthesize the spec and testing seams, then give that draft to `to-tickets` to produce ticket drafts and their blocking graph. Hold both source workflows before their user confirmation or tracker writes. This shared side-effect boundary lets one Delivery Map approval satisfy both sources while preserving their analysis and content rules.

`scope-it` starts from settled work. Include source-requested confirmations in the Delivery Map when the conversation already supports a recommendation. If a missing product, architecture, or testing decision prevents a defensible draft, stop and report that unresolved decision instead of opening another interview inside this workflow.

Observe existing tracker artifacts, repository state, and entry-worktree changes once while drafting. Consistent durable artifacts may satisfy part of the map; contradictory evidence blocks only the affected part.

### 2. Approve one Delivery Map

Present one concise proposal with:

- **Scope:** spec destination, testing seam, and the decisions the spec will preserve.
- **Tickets:** each proposed ticket's title, blockers, and end-to-end behavior from `to-tickets`.
- **Implementation order:** ticket dependency waves or frontier. Each node is a proposed or published ticket; describe files, modules, coding steps, and test tasks only inside the ticket's end-to-end delivery.
- **Native graph:** Scope Parent containment and blocking edges as separate axes.
- **Delivery lane:** direct delivery or enabled Integration Delivery Lane (IDL), including the final gate when applicable.
- **Planning:** Change Proposal, Planning Owner Ticket, and Planning Baseline result.
- **Writes:** tracker and repository mutations that approval will authorize.

For one ticket, omit Implementation order and the diagram. Show the ticket, `Blocked by: None`, IDL state, Planning Owner and result, and approved writes.

For multiple tickets, use a short labeled diagram whose nodes are tickets and whose labels distinguish implementation order, blocking, and delivery lane. The map approval replaces `to-spec`'s pending seam confirmation, `to-tickets`'s granularity and blocker quiz, spec placement confirmation, multi-ticket approval, Planning approval, and IDL choice. Coalesce bounded uncertainties into the same proposal with a recommendation.

Materialize nothing before the map is approved. When durable evidence proves the same map was already approved, resume its missing deltas without asking again.

### 3. Materialize spec and tickets

After approval, resume the source workflows from their drafts without repeating analysis or phase-specific confirmation.

- Publish the approved spec through `to-spec` at the map's destination and retain its required metadata.
- Follow the ticket breakdown and content produced by `to-tickets` without a ticket-count preference.
- **One ticket:** publish `## Ticket — <Title>` on the spec issue and use that issue as the delivery ticket. Create no separate issue or self-relationship. Without a commentable spec issue, the Delivery Map must approve a separate destination.
- **Multiple tickets:** publish in dependency order. A tracker spec issue is the **Scope Parent** of every delivery ticket.

Containment, blocking, Planning ownership, and optional delivery topology are independent. Express supported relationship axes natively; textual references are content, not relationship evidence. Repair only a missing edge without rerunning source analysis or changing approved content, metadata, or existing relationships.

#### Integration Delivery Lane

IDL remains disabled unless multiple terminal implementation tickets must land atomically to `main` through a shared integration branch and repository evidence proves the lane can run.

When enabled, record the canonical integration branch and target, immutable integration start SHA, capability or bootstrap evidence, optional Planning Baseline pointer, final integrate-and-verify ticket, and umbrella PR pointer. Terminal tickets use independent branches from the latest green integration HEAD and reference rather than close their scoped issues. A child closes only after its PR merges to integration, required checks pass on the exact resulting integration HEAD, and durable PR URL/full-SHA evidence exists. The final ticket is blocked by terminal tickets and owns main-drift reconciliation, aggregate verification, Scope Parent closure, and umbrella synchronization.

Keep mutable IDL state separate from the immutable Planning Baseline; never encode lane movement in baseline evidence.

Failed or unverifiable rules, checks, ancestry, or exact-head evidence preserve completed artifacts and stop new child closure or finalization.

### 4. Materialize Planning

The Delivery Map's **Change Proposal** accounts for every entry-worktree change as:

- **Carry:** scope-owned whole files or independently applicable exact patches to publish in the baseline.
- **Remove:** confirmed scope-owned patches superseded by a durable artifact.
- **Preserve:** unrelated content, byte-for-byte.
- **Uncertain:** candidate, path, bounded range, evidence, and recommended treatment.

Ownership requires session edit records, snapshots, exact patches, or approved classification; semantic similarity alone supports only a recommendation. Coalesce bounded uncertain candidates into the Delivery Map. Preserve unbounded candidates, recommend the smallest content-level resolution, and stop only when they prevent an independently verifiable map.

Planning is complete only when baseline diff equals **Carry**, the cleaned entry state equals its original state minus **Carry** and **Remove**, and **Preserve** is byte-for-byte unchanged. With empty **Carry**, apply only **Remove**, verify, and report `none` without baseline Git mutations.

Otherwise use the approved Planning Owner Ticket to create or resume one issue-linked baseline from the fetched remote default branch in an isolated worktree. Verify its full SHA, publish one `## Planning baseline` pointer on every related ticket, then clean the entry worktree. A failed patch, invariant, ancestry, relationship, or preservation check keeps completed artifacts and leaves Planning incomplete.

### 5. Verify and return

Read back the approved content, native containment, native blockers, enabled lane state, Planning pointers, branch SHA, and worktree invariants in one consolidated verification pass. An unavailable native axis uses the source-defined fallback and reports degraded evidence; contradictory evidence leaves that part incomplete.

Return the spec artifact, ticket artifacts, selected delivery ticket, issue-only Delivery Map, verified relationship summary, enabled IDL record, and Planning result (`none` or owner, branch, full SHA, and pointer URLs). Keep phase-source and low-level command receipts internal.

$ARGUMENTS
