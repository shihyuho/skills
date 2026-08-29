---
name: scope-it-remake
description: "Coordinate interchangeable scope and ticket workflows into one Delivery Map with a self-contained continuation protocol."
license: MIT
disable-model-invocation: true
---

# scope-it-remake

Orchestrate scope and delivery planning. The selected skills create, review and publish their outputs through their own workflows; this skill coordinates the discussion and connects those artifacts in a Delivery Map whose continuation protocol travels with it. Finish after publication and readback. Implementation belongs to the executor's workflow.

## Planning skills

Choose two roles independently:

- **Scope:** what and why, boundaries, constraints, success criteria and testing seams.
- **Tickets:** independently deliverable outcomes, acceptance evidence and real prerequisites.

Read each selected skill's workflow before invoking it or accepting its output. It owns analysis, templates, slicing, required reviews, publication, metadata and attachments. Pass settled decisions, repository evidence, complete upstream artifacts, the placement preferences below and the current authorized scope. Follow its native planning steps, preserving the full content and checks while applying the agreed placement. If it requires Git or implementation beyond the approved scope, pause to resolve that boundary; choose a compatible skill or completed artifact when necessary.

Reuse complete artifacts with recoverable evidence of the selected skill's contract and reviews, even when the producer is unavailable, or when the user explicitly accepts an artifact as the complete substitute. Otherwise send existing material to the selected skill to assess and fill its gaps; clarify missing evidence rather than infer completeness. One artifact can satisfy both roles when it meets both contracts. A plan of coding steps needs ticket shaping by the ticket skill, not a relabeling by the coordinator.

## Process

1. **Orient.** Read repository guidance, existing artifacts and approvals. Resolve the planning skills and destinations; reuse confirmed work. Find repository facts, recommend answers and ask unresolved questions in dependency order.
2. **Scope.** Give settled context to the scope skill. Let it complete its own content checks, confirmations and publication. Keep the complete output and read back its actual location before proceeding.
3. **Tickets.** Pass the complete published Scope and its real reference to the ticket skill. Resolve delivery choices affecting ticket shape, responsibilities or readiness before publication. Let that skill propose, review and publish its complete tickets in the agreed placement. Retain the real identities and verify the outputs before assembling the Map.
4. **Assemble.** Build the Map below from those published artifacts. Check identities and relationships; retain every agreed delivery obligation with its owner, trigger and required evidence, including while shortening the handoff. Source content stays complete in its own artifacts; return content gaps or conflicts to the responsible skill for approved revision.
5. **Publish the Map.** Show the Map and remaining planning-file and preference writes. After approval, publish only those changes. Preserve Scope and Ticket bytes; the Map never replaces source artifacts.
6. **Verify and finish.** Freshly compare complete source artifacts, the Map and remaining writes with their approvals, including links, metadata, attachments and relationships. Report the parent, Map and applicable delivery evidence, then stop. This does not wait for implementation or close tickets; planning approval does not authorize implementation, merging or default-branch Git writes.

At each phase, use its native confirmations and current approval covering the concrete content, destinations, attachments, metadata and relationships to write. Explain that Scope and tickets become visible before the Map; resolve any execution-triggering metadata before publication. Read fresh targets before writes and compare each result with its approved payload before dependent work. Preserve unrelated content and the starting item's lifecycle. Verify native containment and blockers separately. An unavailable capability needs an approved concrete fallback with its limitation recorded; a failed readback of a supported capability remains unresolved. Preview-only requests stop before writes, without inventing a draft mode for a skill that cannot provide one.

On interruption, recover exact drafts, approvals and successful writes; look up uncertain creations before retrying. Repair only missing approved operations, asking about ambiguity or changed writes. Keep operation records outside the formal Map. On a later retrieval, return the parent and published Map without restarting planning. The Map's embedded **Work through the Map** protocol lets another session continue without this skill or the planning chat. Discuss and publish only approved amendments. A requested delivery audit uses the published agreement and repository workflow, read-only until corrective writes are approved.

## Delivery Map

The Map is a low-resolution delivery index attached to its parent, not another Scope source of truth. Requirements, acceptance and product boundaries stay in the parent Scope and Ticket artifacts. Use linked Ticket titles as diagram nodes and native tracker membership/dependencies as their source of truth; do not repeat a Ticket or blocker list. Show branches, PR targets and direct/integration landing paths as labels or edges. Independent landing is the default. Omit the diagram for one Ticket; keep runtime progress and frontier snapshots out of the Map.

Reuse the starting tracker item as parent; otherwise agree one from repository guidance or use local Markdown. Publish or link the complete Scope without replacing an existing report. After Scope and Tickets exist, publish the full Map once as a standalone, then-current final comment on a commentable parent. Its read-back comment ID/URL is canonical; markers delimit its editable block. Later comments do not change that identity, and approved amendments edit it in place. After a creation timeout without an ID, bind only a unique marker-and-content match.

With one Ticket, the parent is its tracker identity and a separate `## Ticket — <Title>` comment holds its content; create no child item or self-relationship. With multiple Tickets, use native child items with real blockers. Ticket artifacts do not link back to or copy the Map. Read back the canonical ID/content, unchanged Scope/Ticket bytes and no duplicate Map. Pass these placements to the source skills and preserve existing layouts unless migration is approved. Without a commentable parent, retain the approved local/unsupported fallback; local Scope/Map may share one file and link separate Ticket files. If a fallback makes the Map independent, add only a compact Scope pointer.

Use this outline inside `<!-- scope-it-remake:delivery-map:start -->` and `<!-- scope-it-remake:delivery-map:end -->`:

```markdown
## Delivery Path
<Ticket topology with branch, PR target and direct/integration landing path.>
## Planning Carry
<Durable location/baseline, Carrier Ticket and landing path; or None.>
## Continue
<Only an effort-specific selection override; omit when none.>
## Work through the Map
- Start from this parent, this Map and fresh native child, dependency and linked-branch relations. Keep the low-resolution view until one Ticket is selected.
- If the user names a Ticket, use it and surface whether it is currently eligible. Otherwise use an eligible `Continue` override; absent one, take the first Ticket in tracker order that is open, has all blockers complete and has no active claim when the repository exposes reliable claim state.
- For one Ticket, select the parent and its `## Ticket — <Title>` comment; for many, select one child item. Re-read live relations immediately before proceeding. If claim state is unreliable, mark the choice provisional; if nothing qualifies, report the live reason.
- Load only the selected Ticket and related closed Tickets needed to understand it. Before implementation, the executor revalidates the selection and performs the repository-defined claim, then follows the recorded branch, PR target and relevant Planning Carry.
```

Always publish **Work through the Map** as a compact, self-contained operating protocol, adapting tracker terms without moving the rules into Ticket bodies. `Continue` stores only an effort-specific override; live eligibility and current/following frontier never become Map snapshots. The parent is the entry for later sessions. Its Scope, native relations and marker-bound Map provide the low-resolution view; Ticket bodies stay unloaded until selection. The selected Ticket's source-owned content carries its complete prerequisites and acceptance evidence, while the Map owns cross-Ticket delivery facts. Keep planner write limits and operation receipts in the approval context.

### Planning files and delivery choices

For ADRs, `CONTEXT.md` changes or other repository content the executor needs, agree the exact scope-owned files/patches, retrievable version/location, landing target and one responsible delivery ticket. Preserve unrelated entry changes; resolve uncertain ownership before including content. Use repository workflows/tools for approved preservation or publication, verifying access for the intended executor. An unknown executor needs access beyond a local path. Verify durable content before any approved entry cleanup; missing content or access leaves publication incomplete.

For direct delivery, the Planning Baseline starts the Carrier ticket's final branch, never a planning-only branch. Follow repository naming while reflecting final delivery type and Carrier identity—for example, `fix/1049-terminal-payload-lifecycle`, not `docs/` inferred from the Carry. When supported, create the native linked branch from the Carrier's Issue—the Scope Issue when one Ticket is a comment—before a local worktree tracks it; push alone is insufficient. Repository/executor workflow owns Git mechanics; unavailable native linking uses its approved fallback and degraded evidence.

Planning Carry records one compact pointer: Carrier Ticket, linked branch, repository/path, base and baseline full SHAs with patch bounds when needed, landing target and approved-content obligation. Before cleanup, verify pointer consistency, content/access and native linkage (on GitHub, the Carrier's Issue `linkedBranches`). The executor resumes that branch for implementation, tests, required ADR and the PR to target under separate authority. Retain an existing delivery-path binding. With no planning files, report `None` and create no baseline work.

For an agreed shared delivery lane, have the ticket skill supply its final integration/verification ticket with dependencies on all terminal tickets. Record the approved lane, target and responsibility for aggregate verification and closure, linking the applicable repository workflow. Git setup, CI rules and implementation procedures belong to that workflow. A change to file ownership, delivery path or shared responsibilities needs an approved Map amendment.

## Choosing and remembering skills

An explicit role choice by name or `--scope-skill <skill>` / `--ticket-skill <skill>` wins. Otherwise use the effort's choice/lineage, a compatible skill explicitly invoked for the task, the saved choice, then compatible repository guidance. Resolve exact identities through host discovery before declaring them unavailable. Follow host invocation rules: lineage or recommendations do not grant delegation authority. Clarify unavailable, ambiguous or incompatible choices instead of substituting silently. Accept `--scope-source` and `--ticket-source` as legacy input aliases.

Save confirmed cross-repository defaults at `~/.config/softleader/agent-skills/scope-it-remake/sources.json`:

```json
{"schema_version":3,"scope":"<skill identity>","tickets":"<skill identity>"}
```

V3 records explicit user selection and consent to future planning delegation on explicit invocations of this coordinator; it grants no publication, Git or implementation authority. Explain that consent when selecting/saving. Internal chaining still follows host invocation rules.

Include preference writes in final approval; one-run choices and artifact reuse leave defaults unchanged. Preserve unrelated fields and omit unresolved roles. V2 choices need delegation consent before v3 migration. For v1, resolve explicit choice > `global` > unanimous legacy `repositories`; clarify conflicts, and approve conversion/removal of legacy containers with consent for every retained role. Unknown versions or unusable files need clarification. Before saving, reread the file, preserve unrelated concurrent changes and renew approval for changed affected values; verify the save without republishing artifacts.

$ARGUMENTS
