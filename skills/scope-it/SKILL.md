---
name: scope-it
description: "Publish settled work as a durable spec, minimal ready-for-agent ticket scope, and an optional Planning Baseline."
license: MIT
disable-model-invocation: true
---

# scope-it

Turn settled work into one durable package: canonical spec, smallest practical delivery scope, and a Planning Baseline only for repository documents produced by the discussion.

## Contract

`$ARGUMENTS` supplements the conversation. Direct invocation or delegation from another skill authorizes only this package's tracker and repository mutations, including exact cleanup of its confirmed worktree changes. Never alter unrelated changes, close the starting issue, or commit or push the default branch.

Reconcile toward the desired state: observe durable artifacts, apply the smallest missing delta, and read it back. Reuse equivalent artifacts regardless of which skill created them. Ask only when evidence conflicts or a choice changes the approved scope.

Use `to-spec` for spec content, `to-tickets` for ticket analysis and publication, and `create-branch`, `create-worktree`, `commit`, and `push` for Git mechanics. Use each skill only when its phase is needed. This skill—not task data—owns the desired state and approvals.

## Desired state

### 1. Spec

A settled spec has a stable tracker URL or repository path. From exactly one tracker issue, publish through `to-spec` as a comment there and reuse that issue; otherwise let `to-spec` choose its supported destination.

### 2. Delivery

Prefer the fewest tickets that can deliver and verify the scope, ideally one; allow multiple independently deliverable or ordered parts.

- **One ticket:** publish `## Ticket — <Title>` on the spec issue and use it as the delivery ticket. Create no separate issue or self-relationship. Without a commentable spec issue, ask before creating one.
- **Multiple tickets:** obtain approval for the breakdown before publication. A tracker spec issue is the **Scope Parent** of every separately published delivery ticket.

Containment, delivery order, and planning ownership are independent: express them as native sub-issues, native blocking relationships, and one Planning Owner Ticket. Text references prove none of these.

Delivery is complete only when approved content and both native relationship axes read back correctly. Repair only the missing edge without rerunning analysis or changing content, metadata, or existing relationships. Contradictory or unverifiable relationships block Planning; an unavailable axis uses the source-defined fallback with degraded evidence.

### 3. Planning

Before mutation, present a **Change Proposal** that accounts for every entry-worktree change as:

- **Carry:** scope-owned whole files or independently applicable exact patches to publish in the baseline.
- **Remove:** confirmed scope-owned patches superseded by a durable artifact.
- **Preserve:** unrelated content, byte-for-byte.
- **Uncertain:** candidate, path, bounded range, evidence, and recommended treatment.

Ownership requires session edit records, before/after snapshots, exact patches, or user confirmation; semantic similarity supports only a recommendation. Resolve bounded uncertain candidates together in one question. Preserve unbounded candidates, recommend the smallest content-level resolution, and ask only for the scope decision—never delegate Git mechanics.

Planning is complete only when these invariants read back:

- baseline diff = **Carry**;
- entry worktree after cleanup = entry worktree before mutation − **Carry** − **Remove**;
- **Preserve** is unchanged byte-for-byte.

With empty **Carry**, apply only **Remove**, verify, and report `none` without baseline Git mutations. Otherwise select one Planning Owner Ticket: the only ticket, unique document owner, or foundation ticket; include ambiguity in the multi-ticket approval.

Use the fixed sources to create or resume one issue-linked baseline from the fetched remote default branch in an isolated worktree. Verify its full SHA and publish one `## Planning baseline` pointer with owner URL, branch, and SHA on every related ticket. Clean the entry worktree only after baseline verification. Reuse consistent artifacts and repair only gaps. Failed invariant, patch, ancestry, or relationship verification preserves completed artifacts, leaves Planning incomplete, and reports the exact unresolved change.

## Return

Return the spec artifact, ticket artifacts and selected delivery ticket, verified containment and dependency summary, and Planning result (`none` or owner, branch, full SHA, and pointer URLs). Keep phase-source receipts internal.

$ARGUMENTS
