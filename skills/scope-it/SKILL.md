---
name: scope-it
description: "Coordinate interchangeable scope and ticket workflows into one Delivery Map with a self-contained continuation protocol."
license: MIT
disable-model-invocation: true
---

# scope-it

Coordinate scope and delivery planning. The selected skills own their complete outputs, reviews and publication; this coordinator connects the published artifacts in a Delivery Map. Finish with verified publication so another session can continue from the parent alone. Implementation belongs to the executor's workflow.

## Workflow

1. **Orient.** Read repository guidance, artifacts and approvals. Resolve the roles and placement below; reuse confirmed work. Find repository facts, recommend answers and ask unresolved questions in dependency order.
2. **Scope.** Give the Scope skill the settled context and agreed placement. Let it complete its native content checks, confirmations and publication. Keep the complete output and read back its actual location before Tickets.
3. **Tickets.** Pass the complete published Scope and real reference to the Tickets skill. Resolve choices affecting shape, responsibilities or readiness before publication. Let the source propose, review and publish complete tickets in the agreed placement; retain their verified identities.
4. **Assemble.** Build the Map from those published artifacts and verified relationships. Retain every agreed delivery obligation with its owner, trigger and required evidence. Requirements and acceptance stay complete in the source artifacts; return gaps or conflicts to the responsible source for approved revision.
5. **Publish.** Show the Map and remaining planning-file and preference writes. Use approval covering those concrete changes, then publish only them. Preserve the source artifacts and record the canonical Map identity.
6. **Verify and finish.** Freshly compare the complete sources, Map and remaining writes with their approvals, including links, metadata, attachments and both relationship axes. Check unchanged Scope/Ticket bytes and one canonical Map. Report the parent, Map and applicable delivery evidence, then stop. Planning approval does not authorize implementation, merging, ticket closure or default-branch Git writes.

## Conditional references

Read the applicable reference before the affected work, including when reusing completed artifacts:

- **Preferences:** when a role needs saved defaults or the user requests a preference change or migration, read [preferences.md](references/preferences.md) before using or writing the configuration.
- **Recovery:** for interrupted publication, uncertain creations, retrieval or amendment of an existing Map, legacy Map markers, or a delivery audit, read [recovery.md](references/recovery.md) before continuing or retrying.
- **Delivery options:** for repository planning files, a shared lane, or special verification/closure duties, read [delivery-options.md](references/delivery-options.md) before shaping or accepting the delivery contract, assembling its Map, or proposing related writes.

## Planning skills

Choose two roles independently:

- **Scope:** what and why, boundaries, constraints, success criteria and testing seams.
- **Tickets:** independently deliverable outcomes, acceptance evidence and real prerequisites.

An explicit role choice by name or `--scope-skill <skill>` / `--ticket-skill <skill>` wins. Otherwise use the current task's choice/lineage, a compatible skill explicitly invoked for the task, the saved choice, then compatible repository guidance. Accept `--scope-source` and `--ticket-source` as legacy input aliases. One-run choices and artifact reuse leave defaults unchanged.

Resolve exact identities through host discovery before declaring them unavailable. Follow host invocation rules: lineage or recommendations do not grant delegation authority. Clarify unavailable, ambiguous or incompatible choices instead of substituting silently.

For source work still needed, read the selected workflow before invoking it or accepting its new output. The source owns analysis, templates, slicing, required reviews, publication, metadata and attachments. Pass settled decisions, repository evidence, complete upstream artifacts, agreed placement and the current authorized scope. Preserve its full content and checks. If its workflow requires Git or implementation beyond that scope, resolve the boundary or use a compatible skill or completed artifact.

Reuse complete artifacts with recoverable evidence of the selected source's contract and reviews, even when the producer is unavailable, or when the user explicitly accepts a complete substitute. Otherwise let the source assess existing material and fill its gaps. One artifact can satisfy both roles when it meets both contracts. Coding steps still need ticket shaping by the Tickets source.

## Publication contract

Each phase uses its native confirmations and approval for the concrete content, destinations, attachments, metadata and relationships. Reuse that approval while those writes still match; ask only about missing decisions or changed writes, preserving the source's required content checks and reviews.

Explain that Scope and Tickets become visible before the Map, and resolve execution-triggering metadata before publication. Read fresh targets before writes and compare each result with its approved payload before dependent work. Look up uncertain creations before retrying. Preserve unrelated content and the starting item's lifecycle.

Verify native containment and blockers separately. An unavailable capability needs an approved concrete fallback with its limitation recorded; failed readback of a supported capability remains unresolved. Preview-only requests stop before writes; a source that cannot provide bounded drafting needs a compatible alternative or clarification.

## Delivery Map

The Map is a low-resolution delivery index. Requirements, acceptance and product boundaries remain in Scope and Tickets. Native tracker membership and dependencies remain authoritative; project them into the topology rather than repeating Ticket or blocker lists. Keep runtime progress, frontier snapshots and claim state out of the durable Map.

Agree placement before source publication:

- Reuse the starting tracker item as parent; otherwise agree one from repository guidance or use local Markdown. Publish or link complete Scope while preserving an existing report.
- With one Ticket, the parent is its tracker identity and a separate `## Ticket — <Title>` comment holds its content; create no child or self-relationship.
- With multiple Tickets, use native children with real blockers.
- Preserve existing layouts unless migration is approved. Without a commentable parent, use the approved local/unsupported fallback: local Scope/Map may share a file and link separate Ticket files. An independent fallback Map needs only a compact Scope pointer.

Ticket artifacts neither link back to nor copy the Map. After Scope and Tickets exist, publish the full Map once as a standalone, then-current final comment on a commentable parent. Its read-back comment ID/URL is canonical; later comments do not change that identity. Use `<!-- scope-it:delivery-map:start -->` and `<!-- scope-it:delivery-map:end -->` to delimit the editable block.

Use linked Ticket titles as diagram nodes. Ticket-to-Ticket edges project verified native blockers (`A → B` means B is blocked by A); Ticket-to-target edges show branch/PR landing and converge on each shared endpoint once. Independent landing is the default. Omit the diagram for one Ticket.

Use this outline. Insert `## Continue` between Planning Carry and Start the Next Ticket only when a task-specific selection override exists. With no planning files, Planning Carry is `None` and creates no baseline work.

```markdown
## Delivery Topology
<Linked Ticket topology: verified native blocker edges plus branch/PR landing endpoints.>
## Planning Carry
<Durable location/baseline, Carrier Ticket and landing path; or None.>
## Start the Next Ticket
- If the user names a Ticket, select it and report any live blocker before work. Otherwise use an eligible `Continue` override, then the first open Ticket in tracker order whose blockers are complete and, when reliable claim state exists, is unclaimed.
- Re-read live parent relations before work. For one Ticket, use the parent and its `## Ticket — <Title>` comment; for many, use the selected child. If none qualifies, report why; unreliable claim state makes the choice provisional.
- Load only the selected Ticket and closed Tickets needed for context. Follow the repository's claim process, then the recorded branch, PR target and Planning Carry.
```

Publish **Start the Next Ticket** in every Map, adapting tracker terms while keeping the instructions in the Map. The parent, Scope, native relations and canonical Map let later sessions select one Ticket before loading its body. The selected Ticket carries complete prerequisites and acceptance; the Map carries cross-Ticket delivery facts. Keep planner write limits and operation receipts in the approval context.

Preserve unrelated entry changes and resolve uncertain planning-file ownership before including content. Verify durable content and executor access before approved cleanup; missing content or access leaves publication incomplete.

$ARGUMENTS
