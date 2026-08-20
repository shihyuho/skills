---
name: scope-it
description: "Publish settled work as a durable spec, ready-for-agent ticket scope, and optional repository delivery artifacts."
license: MIT
disable-model-invocation: true
---

# scope-it

Turn settled work into one durable package: canonical spec, ready-for-agent delivery scope, and optional repository delivery artifacts, including a Planning Baseline and optional Integration Delivery Lane.

## Contract

`$ARGUMENTS` supplements the conversation. Direct invocation or delegation from another skill authorizes only this package's tracker and repository mutations, including exact cleanup of its confirmed worktree changes. Never alter unrelated changes, close the starting issue, or commit or push the default branch.

Reconcile toward the desired state: observe durable artifacts, apply the smallest missing delta, and read it back. Reuse equivalent artifacts regardless of which skill created them. Ask only when evidence conflicts or a choice changes the approved scope.

Use `to-spec` for spec content, `to-tickets` for ticket analysis and publication, and `create-branch`, `create-worktree`, `commit`, and `push` for Git mechanics. Use each skill only when its phase is needed. This skill—not task data—owns the desired state and approvals, including optional Integration Delivery Lane evidence and reconciliation.

Integration Delivery Lane is disabled by default. Scope-it enables it only when the delivery plan requires multiple terminal implementation tickets that must land atomically to `main` via a shared integration branch.

## Desired state

### 1. Spec

A settled spec has a stable tracker URL or repository path. When starting from exactly one tracker issue, confirm before publication whether to publish the spec as a comment on the starting issue and reuse it, or delegate placement to `to-spec`. Coalesce this placement choice with any other pending confirmation. Otherwise delegate placement to `to-spec`.

### 2. Delivery

Follow the ticket breakdown produced by `to-tickets`:

- **One ticket:** publish `## Ticket — <Title>` on the spec issue and use it as the delivery ticket. Create no separate issue or self-relationship. Without a commentable spec issue, ask before creating one.
- **Multiple tickets:** obtain approval for the breakdown before publication. A tracker spec issue is the **Scope Parent** of every separately published delivery ticket.

Containment, delivery order, planning ownership, and optional delivery topology are independent: express them as native sub-issues, native blocking relationships, and one Planning Owner Ticket. Text references prove none of these.

#### 2.1 Integration Delivery Lane (IDL)

- **Enablement:** IDL is enabled only when multi-ticket delivery requires shared integration-branch aggregation, repository evidence proves integration branch protections/required checks are available, and final atomic main landing is intended.
- **Core lane state:** when enabled, scope-it records:
  - canonical integration branch
  - integration target (`main` baseline branch)
  - immutable integration start SHA
  - optional Planning Baseline pointer
  - bootstrap status and durable evidence for CI/filter/ruleset capability
  - final integrate-and-verify ticket
  - umbrella PR pointer
- **Ticket topology:** each terminal implementation ticket is created from the latest green integration HEAD via its own independent worktree/branch and references the scoped issue with native PR references (no closing keyword in child tickets).
- **Child close condition:** a child ticket closes only after child PR is merged to integration branch, required checks pass on exact integration HEAD, and the issue body includes verified PR URL and integration SHA.
- **Finalization:** final ticket is blocked only by terminal implementation tickets, handles main drift reconciliation and aggregate verification, closes the Scope Parent, and keeps the umbrella PR synchronized.
- **Safety stop:** if integration checks, required rules, ancestry, or exact-head verification cannot be proven or fail, preserve completed work and stop before new child closure or finalization.

Delivery is complete only when approved content, enabled IDL state, and both native relationship axes read back correctly. Repair only the missing edge without rerunning analysis or changing content, metadata, or existing relationships. Contradictory or unverifiable relationships block planning; an unavailable axis uses the source-defined fallback with degraded evidence.

### 3. Planning

Before mutation, present a **Change Proposal** that accounts for every entry-worktree change as:

- **Carry:** scope-owned whole files or independently applicable exact patches to publish in the baseline.
- **Remove:** confirmed scope-owned patches superseded by a durable artifact.
- **Preserve:** unrelated content, byte-for-byte.
- **Uncertain:** candidate, path, bounded range, evidence, and recommended treatment.

Ownership requires session edit records, before/after snapshots, exact patches, or user confirmation; semantic similarity supports only a recommendation. Resolve bounded uncertain candidates together in one question. Preserve unbounded candidates, recommend the smallest content-level resolution, and ask only for the scope decision—never delegate Git mechanics.

When Integration Delivery Lane is enabled, `scope-it` tracks planning artifacts separately from planning baseline ownership:

- **Planning Baseline** remains immutable scope evidence for repository document changes.
- **IDL state** is a delivery control artifact for integration aggregation and child closure policy.

Planning is complete only when these invariants read back:

- baseline diff = **Carry**;
- entry worktree after cleanup = entry worktree before mutation − **Carry** − **Remove**;
- **Preserve** is unchanged byte-for-byte.

With empty **Carry**, apply only **Remove**, verify, and report `none` without baseline Git mutations. Otherwise select one Planning Owner Ticket: the only ticket, unique document owner, or foundation ticket; include ambiguity in the multi-ticket approval.

Use the fixed sources to create or resume one issue-linked baseline from the fetched remote default branch in an isolated worktree. Verify its full SHA and publish one `## Planning baseline` pointer with owner URL, branch, and SHA on every related ticket. Clean the entry worktree only after baseline verification. Reuse consistent artifacts and repair only gaps. Failed invariant, patch, ancestry, or relationship verification preserves completed artifacts, leaves Planning incomplete, and reports the exact unresolved change.

## Return

Return the spec artifact, ticket artifacts and selected delivery ticket, verified containment/dependency summary, Integration Delivery Lane record when enabled, and Planning result (`none` or owner, branch, full SHA, and pointer URLs). Keep phase-source receipts internal.

$ARGUMENTS
