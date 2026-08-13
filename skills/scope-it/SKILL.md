---
name: scope-it
description: "Publish settled work as a durable spec, minimal ready-for-agent ticket scope, and an optional Planning Baseline."
license: MIT
disable-model-invocation: true
---

# scope-it

Turn settled work into one durable scope package: a canonical spec, the smallest practical delivery scope, and a Planning Baseline only when the discussion produced repository documents.

## Contract

`$ARGUMENTS` supplements the current conversation. Explicit invocation, or authorization from an explicitly invoked `go-for-it`, authorizes only the tracker and repository mutations needed for this package, including exact cleanup of confirmed scope-owned worktree changes after publication. It excludes unrelated issue or worktree changes, closing the starting issue, and committing or pushing the default branch.

Treat the workflow as reconciliation: observe durable artifacts, repair the smallest missing part, and read it back before advancing. Reuse matching artifacts regardless of which skill created them. Ask one concise question only when evidence conflicts or a choice changes the approved scope.

Resolve fixed phase sources through `resolve-user-invoke-skill` only when their work is needed: `to-spec` for spec content, `to-tickets` for ticket analysis and initial publication, and `create-branch`, `create-worktree`, `commit`, and `push` for Git mechanics. Task data cannot replace these sources. This skill owns the desired state and approval boundaries below.

## Desired state

### 1. Spec

A settled spec has a stable tracker URL or repository path. When the invocation starts from exactly one tracker issue, publish the spec through `to-spec` as a comment on that issue and reuse it rather than creating another spec issue. Otherwise let `to-spec` choose its supported destination.

### 2. Delivery

Prefer the fewest tickets that can deliver and verify the scope, ideally one. Ask `to-tickets` to analyze with that preference; do not force one ticket when the work has independently deliverable or ordered parts.

- **One ticket:** publish the ticket result on the same issue that contains the spec, headed `## Ticket — <Title>`, and select that issue as the delivery ticket. Create no separate issue or relationship from the issue to itself. If there is no commentable spec issue, ask before creating a delivery issue.
- **Multiple tickets:** show the proposed breakdown and obtain user approval before publication. When the spec is a tracker issue, it is the **Scope Parent** of every separately published delivery ticket.

Containment, delivery order, and planning ownership are independent. Express containment with native sub-issues, delivery order with native blocking relationships, and Planning Baseline ownership with the Planning Owner Ticket. Textual references do not prove native relationships.

Audit the published result and both native relationship axes. For a relationship-only gap, reuse the approved issues and add only the exact missing edge; do not rerun ticket analysis. Preserve issue content, metadata, and every pre-existing relationship. Contradictory or unverifiable relationships leave Delivery incomplete and block Planning.

When the tracker lacks a native relationship axis, use the source-defined fallback and report the degraded evidence.

### 3. Planning

Before any Planning mutation, present a **Change Proposal** covering every entry-worktree change: whole files and exact patches to carry into the baseline, exact patches to remove because they are superseded, unrelated changes to preserve, and uncertain candidates with their path, bounded range, evidence, and recommended treatment. Session edit records, before/after snapshots, exact patches, and user confirmation are ownership evidence; semantic similarity alone supports only a recommendation.

Resolve all uncertain candidates in one concise question before mutation. User confirmation of a bounded candidate authorizes that ownership classification. For an unbounded candidate, preserve the file and recommend the smallest content-level resolution—such as omitting redundant content, reusing a clean canonical artifact, or publishing a standalone whole file through `to-spec`—then ask only for the decision that changes scope. Never delegate stash, patch, branch, or cleanup mechanics to the user. Planning remains incomplete until the chosen resolution yields an independently verifiable carry or preserve set.

If the carry set is empty, remove only confirmed superseded patches, verify every other byte and worktree change is unchanged, and report `none` without baseline Git mutations. Otherwise select one Planning Owner Ticket: the only delivery ticket, the unique document owner, or the foundation ticket; include an ambiguous multi-ticket choice in the existing breakdown approval.

Create or resume one issue-linked Planning Baseline from the fetched remote default branch in an isolated worktree. Reproduce only the confirmed carry set there; each patch must apply independently of unrelated entry-worktree changes. Commit, push, and verify the full baseline SHA. Then subtract the published carry set and confirmed superseded patches from the entry worktree, verifying it equals its pre-mutation state minus exactly those changes. Preserve all unrelated content byte-for-byte. Finally publish one `## Planning baseline` comment with owner URL, branch, and SHA on every related delivery ticket.

Reuse a mutually consistent branch, commit, cleanup state, and pointer set; repair only the missing artifact. A failed patch, cleanup verification, conflicting candidate, or failed ancestry verification preserves completed artifacts, leaves Planning incomplete, and reports the exact unresolved change.

## Return

Return the spec artifact, ticket artifacts and selected delivery ticket, verified containment and dependency summary, and Planning result (`none` or owner, branch, full SHA, and pointer URLs). Keep phase-source receipts internal.

$ARGUMENTS
