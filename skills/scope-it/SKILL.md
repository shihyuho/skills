---
name: scope-it
description: "Coordinate scope and ticket workflows into a Ticket Map and a verified AFK handoff."
license: MIT
disable-model-invocation: true
---

# scope-it

Coordinate scope and ticket planning. The selected planning skills own their complete outputs, reviews and publication. This coordinator settles what must land, publishes a Ticket Map for people, and hands the work to `to-afk-agent`, which owns how it lands, including the Carrier, branches, preservation, Carry records, cleanup, readiness and dispatch. Finish with verified AFK-ready Issues, so another session can start from the parent. Implementation belongs to the receiving workflow.

## Workflow

1. **Orient.** Read repository guidance, artifacts and approvals. Resolve the planning roles, GitHub placement and `to-afk-agent` before dependent writes; reuse confirmed work. Read the handoff skill's current contract and applicable references. Find repository facts, recommend answers and ask unresolved planning questions in dependency order; how the work lands is the handoff's question.
2. **Scope.** Give the Scope skill the settled context and agreed placement. Let it complete its native content checks and reviews, then publish under the authority below. Keep the complete output and read back its actual location before Tickets.
3. **Tickets.** Pass the complete published Scope and real reference to the Tickets skill. Resolve choices affecting shape or responsibilities and arrange deferred new ready markers before publication. Let the source propose, review and publish complete tickets in the agreed placement; retain their verified identities and relationships.
4. **Assemble.** Reconcile this planning session's artifacts, changes and created worktrees, including work from invoked skills, against ownership evidence and landing obligations. Requirements and acceptance stay in the source artifacts. Agreed delivery duties, such as aggregate verification or parent closure, belong in Ticket acceptance with their owner, trigger and required evidence; keep a conditional owner, such as whichever Ticket finishes last, conditional rather than fixing one Ticket. Return gaps or conflicts to their source for approved revision. With two or more Tickets, publish the [Ticket Map](#ticket-map) and read it back; no executor reads it, so a failed publication or readback is reported as unresolved without holding back the handoff.
5. **Hand off.** Under the publication contract, give `to-afk-agent` the bounded handoff below. Retain its verified results. Save only separately approved preference changes.
6. **Verify and finish.** Verify links, metadata, attachments, the Ticket Map, unchanged Scope/Ticket content, both native relationship axes and completion of the required handoff. Reuse valid readback evidence and refresh missing or changed evidence. Report the parent, Ticket Map, ready Issues, the handoff's results for how the work lands, Carry, disposition and dispatch, plus unresolved work. Successful planning publication alone does not complete an unfinished AFK handoff.

## Conditional references

Read the applicable reference before the affected work, including when reusing completed artifacts:

- **Preferences:** when a role needs saved defaults or the user requests a preference change or migration, read [preferences.md](references/preferences.md) before using or writing the configuration.
- **Recovery:** for interrupted publication, uncertain creations, retrieval of a published plan, changes to published Tickets or blockers, amendment of an existing Map, legacy Map markers, or a delivery audit, read [recovery.md](references/recovery.md) before continuing or retrying.
- **Handoff inputs:** for repository planning files or planning worktree creation or transfer, read [handoff-inputs.md](references/handoff-inputs.md) before shaping or accepting their landing obligations or preparing the handoff.

## Planning skills

Choose two roles independently:

- **Scope:** what and why, boundaries, constraints, success criteria and testing seams.
- **Tickets:** independently deliverable outcomes, acceptance evidence and real prerequisites.

An explicit role choice by name or `--scope-skill <skill>` / `--ticket-skill <skill>` wins. Otherwise use the current task's choice/lineage, a compatible skill explicitly invoked for the task, the saved choice, then compatible repository guidance. Accept `--scope-source` and `--ticket-source` as legacy input aliases. One-run choices and artifact reuse leave defaults unchanged.

Resolve exact identities through host discovery before declaring them unavailable. Follow host invocation rules: lineage or recommendations do not grant delegation authority. Clarify unavailable, ambiguous or incompatible choices instead of substituting silently.

For source work still needed, read the selected workflow before invoking it or accepting its new output. The source owns analysis, templates, slicing, required reviews, publication, metadata and attachments. Pass settled decisions, repository evidence, complete upstream artifacts, agreed placement and the current scope and workflow authority. Preserve its full content and checks. If its workflow requires Git or implementation beyond that scope, resolve the boundary or use a compatible skill or completed artifact.

Reuse complete artifacts with recoverable evidence of the selected source's contract and reviews, even when the producer is unavailable, or when the user explicitly accepts a complete substitute. Otherwise let the source assess existing material and fill its gaps. One artifact can satisfy both roles when it meets both contracts. Coding steps still need ticket shaping by the Tickets source.

## Publication contract

`--publish` from the user or an authorized caller authorizes this skill's full workflow within the agreed scope, including the Ticket Map, the delegated AFK handoff and ready markers. Complete and verify it without routine confirmation between steps. Ask only about unresolved decisions or changes beyond that scope.

Otherwise, each phase uses its native confirmations and approval for the concrete content, destinations, attachments, metadata and relationships. Reuse that approval while those writes still match; ask only about missing decisions or changed writes, preserving the source's required content checks and reviews.

Scope, Tickets and the Ticket Map become visible before the handoff. Arrange for the sources to defer new ready markers to `to-afk-agent`; ready authorizes autonomous pickup after preparation. Preserve existing markers and coordinate any existing automatic-pickup race with the receiving workflow before changing executor inputs. Read fresh targets before writes and compare results with the approved payload before dependent work. Preserve unrelated content and the starting item's lifecycle.

Verify native containment and blockers separately. An unavailable capability needs an approved concrete fallback with its limitation recorded; failed readback of a supported capability remains unresolved. Preview-only requests stop before writes; a source that cannot provide bounded drafting needs a compatible alternative or clarification.

## AFK handoff

The fixed handoff delegation is `to-afk-agent`, within this invocation's approved scope and host rules. Resolve its exact installed identity; a missing or incompatible handoff skill leaves delivery unresolved rather than moving its operations back into this coordinator. Planning-role preferences do not select or authorize additional handoff skills.

Supply:

- the parent Issue, complete Scope/Ticket references, selected Issue identities and order, and native relationships;
- landing obligations under [handoff-inputs.md](references/handoff-inputs.md): exact files or patches with ownership evidence, repository and landing target;
- decisions already settled in this planning conversation and verified existing Carrier or delivery-path bindings, passed as given; open delivery questions, such as how the Tickets land, are for `to-afk-agent` to ask under its own contract;
- earlier source-disposition decisions, and any planning worktrees explicitly entrusted for cleanup with their creation/transfer evidence and current path/ref/HEAD identities.

Follow `to-afk-agent` for preservation and cleanup: **Clean up local source** is the default after remote preservation and required publication; explicit retention takes precedence. Transfer cleanup responsibility for eligible planning worktrees even when nothing needs carrying. The handoff checks changed or uncertain sources and worktree safety before cleanup.

The handoff owns readiness: it adds missing ready markers once its own preparation is verified. Preserve blockers, claims and existing Ticket content. An incomplete handoff retains successful outputs and resumes through the same delegate.

An approved local or unsupported-tracker fallback can retain planning drafts, but cannot be reported as a completed AFK handoff. Resolve GitHub placement before live handoff; keep preview and requested read-only retrieval/audit paths bounded. Dispatch follows the handoff's own agreement rules; claims, implementation, merging, deployment, ticket closure and default-branch commits/pushes require their own workflow authority.

## Placement

Agree placement before source publication:

- Reuse the starting tracker item as parent; otherwise agree one from repository guidance or use local Markdown. Publish or link complete Scope while preserving an existing report.
- With one Ticket, the parent is its tracker identity and a separate `## Ticket — <Title>` comment holds its content; create no child, self-relationship or Ticket Map.
- With multiple Tickets, use native children with real blockers.
- Preserve existing layouts unless migration is approved. Without a commentable parent, use the approved local/unsupported fallback: a local Scope and Ticket Map may share a file and link separate Ticket files.

## Ticket Map

The Ticket Map shows people, at a glance, how a plan's Tickets depend on each other. Agents read the native relationships, which stay authoritative, and selection and execution order belong to the receiving workflow. Requirements and acceptance stay in Scope and Tickets, and delivery and Carry records stay with the handoff; keep runtime progress, claim state and operation receipts out of the Map.

With two or more Tickets, publish the Map once their relationships are verified, as one parent comment delimited by `<!-- scope-it:ticket-map:start -->` and `<!-- scope-it:ticket-map:end -->`. Head it `## Ticket Map` and write it in the Issue's language. Its read-back comment ID/URL is the Map's identity. When the parent already carries a Map, including one under legacy markers, amend it under [recovery.md](references/recovery.md) instead of adding another.

Draw the verified blockers (native, or the approved fallback with its limitation) in the smallest view that makes their shape clear: a numbered list for a chain, a nested list for branches, a short "waits for A, B" note where one Ticket has several blockers, and one line when all Tickets can run in parallel. Reach for Mermaid only when a list would hide the shape. Lead with one short sentence naming the overall shape, such as where work starts, and let the view carry the rest. Reference each Ticket as `[#n short label](url)` with a two-to-four-word label; GitHub expands a bare `#n` into its full title. The Map should read at a glance at phone width.

$ARGUMENTS
