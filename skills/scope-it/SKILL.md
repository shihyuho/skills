---
name: scope-it
description: "Coordinate scope and ticket workflows into one Delivery Map and a verified AFK handoff."
license: MIT
disable-model-invocation: true
---

# scope-it

Coordinate scope and delivery planning. The selected planning skills own their complete outputs, reviews and publication; this coordinator prepares the Delivery Map and delegates its publication, Planning Carry and readiness to `to-afk-agent`. Finish with verified AFK-ready Issues and one canonical Map whose continuation protocol lets another session start from the parent. Implementation and dispatch belong to the receiving workflow.

## Workflow

1. **Orient.** Read repository guidance, artifacts and approvals. Resolve the planning roles, GitHub placement and `to-afk-agent` before dependent writes; reuse confirmed work. Read the handoff skill's current contract and applicable references. Find repository facts, recommend answers and ask unresolved questions in dependency order.
2. **Scope.** Give the Scope skill the settled context and agreed placement. Let it complete its native content checks and reviews, then publish under the authority below. Keep the complete output and read back its actual location before Tickets.
3. **Tickets.** Pass the complete published Scope and real reference to the Tickets skill. Resolve choices affecting shape or responsibilities and arrange deferred new ready markers before publication. Let the source propose, review and publish complete tickets in the agreed placement; retain their verified identities and relationships.
4. **Assemble.** Reconcile this planning session's artifacts, changes and created worktrees, including work from invoked skills, against ownership evidence and delivery obligations. Prepare the complete Map from published artifacts and verified relationships, identifying positions for Carry results. Retain each agreed delivery obligation with its owner, trigger and required evidence. Requirements and acceptance stay in the source artifacts; return gaps or conflicts to their source for approved revision.
5. **Hand off.** Under the publication contract, give `to-afk-agent` the bounded handoff below: complete Map, permitted substitutions, selected Issues, Carry inputs and source/worktree disposition. It owns preservation, Map publication and readback, necessary Ticket pointers, cleanup and final readiness. Retain its verified publication identity and results. Save only separately approved preference changes.
6. **Verify and finish.** Compare the returned Map with the prepared content and permitted substitutions; verify links, metadata, attachments, unchanged Scope/Ticket content, both native relationship axes and completion of the required handoff. Reuse valid readback evidence and refresh missing or changed evidence. Report the parent, canonical Map, ready Issues, Carry and disposition results, plus unresolved work. Successful planning publication alone does not complete an unfinished AFK handoff.

## Conditional references

Read the applicable reference before the affected work, including when reusing completed artifacts:

- **Preferences:** when a role needs saved defaults or the user requests a preference change or migration, read [preferences.md](references/preferences.md) before using or writing the configuration.
- **Recovery:** for interrupted publication, uncertain creations, retrieval or amendment of an existing Map, legacy Map markers, or a delivery audit, read [recovery.md](references/recovery.md) before continuing or retrying.
- **Delivery options:** for repository planning files, planning worktree creation or transfer, a shared lane, or special verification/closure duties, read [delivery-options.md](references/delivery-options.md) before shaping or accepting the delivery contract or preparing its handoff.

## Planning skills

Choose two roles independently:

- **Scope:** what and why, boundaries, constraints, success criteria and testing seams.
- **Tickets:** independently deliverable outcomes, acceptance evidence and real prerequisites.

An explicit role choice by name or `--scope-skill <skill>` / `--ticket-skill <skill>` wins. Otherwise use the current task's choice/lineage, a compatible skill explicitly invoked for the task, the saved choice, then compatible repository guidance. Accept `--scope-source` and `--ticket-source` as legacy input aliases. One-run choices and artifact reuse leave defaults unchanged.

Resolve exact identities through host discovery before declaring them unavailable. Follow host invocation rules: lineage or recommendations do not grant delegation authority. Clarify unavailable, ambiguous or incompatible choices instead of substituting silently.

For source work still needed, read the selected workflow before invoking it or accepting its new output. The source owns analysis, templates, slicing, required reviews, publication, metadata and attachments. Pass settled decisions, repository evidence, complete upstream artifacts, agreed placement and the current scope and workflow authority. Preserve its full content and checks. If its workflow requires Git or implementation beyond that scope, resolve the boundary or use a compatible skill or completed artifact.

Reuse complete artifacts with recoverable evidence of the selected source's contract and reviews, even when the producer is unavailable, or when the user explicitly accepts a complete substitute. Otherwise let the source assess existing material and fill its gaps. One artifact can satisfy both roles when it meets both contracts. Coding steps still need ticket shaping by the Tickets source.

## Publication contract

`--publish` from the user or an authorized caller authorizes this skill's full workflow within the agreed scope, including the delegated AFK handoff and ready markers. Complete and verify it without routine confirmation between steps. Ask only about unresolved decisions or changes beyond that scope.

Otherwise, each phase uses its native confirmations and approval for the concrete content, destinations, attachments, metadata and relationships. Reuse that approval while those writes still match; ask only about missing decisions or changed writes, preserving the source's required content checks and reviews.

Scope and Tickets become visible before the Map. Arrange for their sources to defer new ready markers to `to-afk-agent`; ready authorizes autonomous pickup after preparation. Preserve existing markers and coordinate any existing automatic-pickup race with the receiving workflow before changing executor inputs. Read fresh targets before writes and compare results with the approved payload before dependent work. Preserve unrelated content and the starting item's lifecycle.

Verify native containment and blockers separately. An unavailable capability needs an approved concrete fallback with its limitation recorded; failed readback of a supported capability remains unresolved. Preview-only requests stop before writes; a source that cannot provide bounded drafting needs a compatible alternative or clarification.

## AFK handoff

The fixed handoff delegation is `to-afk-agent`, within this invocation's approved scope and host rules. Resolve its exact installed identity; a missing or incompatible handoff skill leaves delivery unresolved rather than moving its operations back into this coordinator. Planning-role preferences do not select or authorize additional handoff skills.

Explicitly request publication of the complete Map as one authoritative comment. Supply:

- the parent Issue, complete Map, identity markers, existing comment ID/URL when known, and authorized editing boundary;
- the exact positions allowed to receive verified branch names, full SHAs and immutable links; all delivery decisions and other content remain settled upstream;
- complete Scope/Ticket references, selected Issue identities and order, native relationships, Carrier bindings and landing obligations;
- required files or patches with ownership evidence, earlier source-disposition decisions, and any planning worktrees explicitly entrusted for cleanup with their creation/transfer evidence and current path/ref/HEAD identities.

Keep the Map draft and recovery evidence available through verified publication. Follow `to-afk-agent` for preservation, publication recovery and cleanup: **Clean up local source** is the default after remote preservation and required publication; explicit retention takes precedence. Transfer cleanup responsibility for eligible planning worktrees even when Carry is empty. The handoff checks changed or uncertain sources and worktree safety before cleanup.

Readiness requires the Map, required remote artifacts and applicable source/worktree disposition to be verified first. Request a canonical Map link on a selected Ticket only where needed to make its execution context discoverable; keep the full Map on the parent. Preserve blockers, claims and existing Ticket content. An incomplete handoff retains successful outputs and resumes through the same delegate and publication identity.

An approved local or unsupported-tracker fallback can retain planning drafts, but cannot be reported as a completed AFK handoff. Resolve GitHub placement before live handoff; keep preview and requested read-only retrieval/audit paths bounded. Dispatch, claims, implementation, merging, deployment, ticket closure and default-branch commits/pushes require their own workflow authority.

## Delivery Map

The Map is a low-resolution delivery index. Requirements, acceptance and product boundaries remain in Scope and Tickets. Native tracker membership and dependencies remain authoritative; project them into the topology rather than repeating Ticket or blocker lists. Keep runtime progress, frontier snapshots and claim state out of the durable Map.

Agree placement before source publication:

- Reuse the starting tracker item as parent; otherwise agree one from repository guidance or use local Markdown. Publish or link complete Scope while preserving an existing report.
- With one Ticket, the parent is its tracker identity and a separate `## Ticket — <Title>` comment holds its content; create no child or self-relationship.
- With multiple Tickets, use native children with real blockers.
- Preserve existing layouts unless migration is approved. Without a commentable parent, use the approved local/unsupported fallback: local Scope/Map may share a file and link separate Ticket files. An independent fallback Map needs only a compact Scope pointer.

After Scope and Tickets exist, have `to-afk-agent` publish the full Map once as a standalone parent comment. Its read-back comment ID/URL is canonical; later comments do not change that identity. Tickets may receive a link to that comment when context is missing, while the full Map stays on the parent. Use `<!-- scope-it:delivery-map:start -->` and `<!-- scope-it:delivery-map:end -->` to delimit the editable block.

Use linked Ticket titles as diagram nodes. Ticket-to-Ticket edges project verified native blockers (`A → B` means B is blocked by A); Ticket-to-target edges show branch/PR landing and converge on each shared endpoint once. Independent landing is the default. Omit the diagram for one Ticket.

Use this outline. Insert `## Continue` between Planning Carry and Start the Next Ticket only when a task-specific selection override exists. Use Planning Carry `None` only when that reconciliation confirms no planning content needs carrying; it creates no baseline work.

```markdown
## Delivery Topology
<Linked Ticket topology: verified native blocker edges plus branch/PR landing endpoints.>
## Planning Carry
<Durable location/baseline, Carrier Ticket and landing path; or None.>
## Start the Next Ticket
- If the user names a Ticket, select it and report its live readiness and blockers before work. Otherwise use an eligible `Continue` override, then the first open Ticket in tracker order with the repository's ready marker, completed blockers and, when reliable claim state exists, no claim.
- Re-read live readiness and parent relations before work. For one Ticket, use the parent and its `## Ticket — <Title>` comment; for many, use the selected child. If none qualifies, report why; unreliable claim state makes the choice provisional. Autonomous pickup requires readiness; starting a named unready Ticket needs separate execution authority.
- Load only the selected Ticket and closed Tickets needed for context. Follow the receiving workflow's execution authority and the repository's claim process, then the recorded branch, PR target and Planning Carry.
```

Publish **Start the Next Ticket** in every Map, adapting tracker terms while keeping the instructions in the Map. The parent, Scope, native relations and canonical Map let later sessions select one Ticket before loading its body. The selected Ticket carries complete prerequisites and acceptance; the Map carries cross-Ticket delivery facts. Keep planner write limits and operation receipts in the approval context.

Preserve unrelated entry changes and resolve uncertain planning-file ownership before including content. Prepare applicable Carry and worktree transfers under [delivery-options.md](references/delivery-options.md); their verified handoff results determine completion.

$ARGUMENTS
