---
name: scope-it-remake
description: "Coordinate interchangeable scope and ticket workflows, then connect their published outputs in one Delivery Map."
license: MIT
disable-model-invocation: true
---

# scope-it-remake

Orchestrate scope and delivery planning. The selected skills create, review and publish their outputs through their own workflows; this skill coordinates the discussion and connects those artifacts in a Delivery Map. Finish after publication and readback. Implementation belongs to the executor's workflow.

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
5. **Publish the Map.** Show the Map and any remaining writes: handoff links, planning-file operations and preference changes. Obtain approval, then publish only those changes using repository/tracker tools. Preserve the existing Scope and ticket content; a Map summary never replaces them.
6. **Verify and finish.** Freshly compare complete source artifacts, the Map and remaining writes with their approvals, including links, metadata, attachments and relationships. Check every ticket's reachable handoff. Report the Map, first executable ticket and applicable delivery evidence, then stop. This does not wait for implementation or close tickets; planning approval does not authorize implementation, merging or default-branch Git writes.

At each phase, use its native confirmations and current approval covering the concrete content, destinations, attachments, metadata and relationships to write. Explain that Scope and tickets become visible before the Map; resolve any execution-triggering metadata before publication. Read fresh targets before writes and compare each result with its approved payload before dependent work. Preserve unrelated content and the starting item's lifecycle. Verify native containment and blockers separately. An unavailable capability needs an approved concrete fallback with its limitation recorded; a failed readback of a supported capability remains unresolved. Preview-only requests stop before writes, without inventing a draft mode for a skill that cannot provide one.

On interruption, recover exact drafts, approvals and successful writes; look up uncertain creations before retrying. Repair only missing approved operations, asking about ambiguity or changed writes. Keep operation records outside the formal Map. On a later invocation, return the published Map and handoffs without restarting planning; discuss and publish only approved amendments. A requested delivery audit uses the published agreement and repository workflow, read-only until corrective writes are approved.

## Delivery Map

The Map contains links and coordination decisions. Requirements, acceptance and execution instructions stay in the linked Scope, tickets and repository guidance. Use the user's language and linked titles. Only delivery tickets become diagram nodes; describe the home and branches in prose. Show waves, blockers and delivery lanes as labels or edges; scheduling and document ownership alone create no blocker. Independent landing is the default. Omit the diagram for one ticket; keep runtime progress statuses out of the Map.

Reuse the starting tracker item as home; otherwise agree one from repository guidance or use local Markdown. Publish the full Scope in a new home's body or a comment preserving an existing report; an existing complete artifact may be linked. Add the approved Map to that planning post without changing Scope content. One ticket gets a separate `## Ticket — <Title>` comment on the same home, whose item is the delivery identity; create no extra issue or self-relationship. Multiple tickets get child items with real blockers. Local Scope/Map share one file and link separate ticket files. Pass these placement preferences before each skill publishes, and preserve existing layouts unless migration is approved. An unsupported placement needs an approved fallback before creating anything elsewhere.

Use this outline inside `<!-- scope-it-remake:delivery-map:start -->` and `<!-- scope-it-remake:delivery-map:end -->`:

```markdown
## Destination
<Agreed outcome and scope summary.>
## Artifacts
<Links to the complete Scope and tickets.>
## Delivery
<Waves, first executable ticket, containment, real blockers and landing method.>
<One compact handoff: planning-file pointer and cross-ticket delivery responsibilities.>
## Out of scope
<Product exclusions and deferred deliverables from Scope.>
## Continue
<First ticket link, with its handoff in Delivery.>
```

Each ticket must be usable by an executor with its own workflow and authorization, without this skill or the planning chat. Include or durably link its complete Scope, prerequisites, acceptance evidence, repository/target and assigned delivery responsibilities. The common handoff belongs only in Delivery and adds only delivery facts missing from those linked artifacts; every affected ticket links it. Reuse an existing handoff when available. Keep the planner's write limits and operation receipts in the approval context.

### Planning files and delivery choices

For ADRs, `CONTEXT.md` changes or other repository content the executor needs, agree the exact scope-owned files/patches, retrievable version/location, landing target and one responsible delivery ticket. Preserve unrelated entry changes; resolve uncertain ownership before including content. Use repository workflows/tools for approved preservation or publication, verifying access for the intended executor. An unknown executor needs access beyond a local path. Verify durable content before any approved entry cleanup; missing content or access leaves publication incomplete.

In Delivery, publish one compact pointer with the owner ticket, repository/path, immutable revision (including base and patch bounds where needed), target and obligation to deliver the approved content there. A full-SHA commit/diff link can identify a Planning Baseline without extra file hashes. Other tickets link to it rather than duplicate the files or pointer. If a planning baseline already exists, retain its actual delivery-path binding. With no planning files, report none and create no baseline work.

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
