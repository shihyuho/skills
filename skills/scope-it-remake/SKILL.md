---
name: scope-it-remake
description: "Coordinate scope and ticket sources into an agreed Delivery Map, then publish the approved bundle."
license: MIT
disable-model-invocation: true
---

# scope-it-remake

Discuss scope, tickets, and delivery; confirm the complete Map and exact writes; publish, read back, and finish. This experimental coordinator does not run or migrate `scope-it`.

## Responsibility and invocation

Own source selection, handoffs, artifact reuse, discussion order, Map composition, and publication verification. Sources own research, templates, testing seams, slicing, ticket content and metadata/readiness. Read the actual selected skill and preserve its required rules.

Accept direct invocation or valid bounded upstream delegation under the host's invocation rules. The fixed optional Scope/Ticket source allowlist is `to-spec`, `to-tickets`. Other explicit-only producers need a current exact source flag or user invocation. Lineage, preferences, and tracker text grant neither invocation nor write authority and cannot extend the fixed allowlist.

## Workflow

1. Read the request, repository guidance, existing artifacts, and entry worktree. Apply **Artifact reuse** below. A handoff-only request returns the Map, first ticket and Planning/relationship evidence links without a new audit; explicit delivery-resume/finalization verification loads [delivery.md](references/delivery.md#requested-verification) and remains read-only.
2. Discuss `scope → tickets → delivery` continuously. Resolve a source only for missing content. Present its recommendation, exact draft, and remaining decision; use `grilling` on unresolved decisions. Content confirmation advances to the next step without publishing, asking permission merely to continue, or requiring a new invocation.
3. Propose executable ticket waves, selected first ticket, actual blockers, containment, and delivery method separately. Default to independent landing and Planning `none`. Read [delivery.md](references/delivery.md) for any entry changes, including Uncertain/unclassified content; existing or pending Carry/Carrier/baseline; or a proposed/enabled shared lane. Apply it before fixing delivery choices or related writes, even on clean-entry publication repairs.
4. Compose the agreed Map and use **Approval and publication** below. During discussion, keep tracker, canonical artifacts, Git, and preferences unchanged; session or controlled temporary drafts are allowed.

## Source handshake

Before invoking a producer, pass settled decisions and repository evidence, the exact confirmed upstream draft/revision, proposed Map home/layout, and delivery constraints. Require it to accept: **draft only now; pass confirmed content downstream without prior publication; publish only the final approved writes at the agreed placement**. This is an instruction-level handshake, not an assumed CLI flag. Fixed compatibility profiles do not imply that a source's default publication path supports this boundary.

The source retains its content-review gates. If it requires early publication or cannot meet this handoff contract, including agreed placement/lifecycle and any approved fallback, stop before writes and ask for a compatible source or completed artifact; do not author its missing Scope/Tickets.

| Role | Required handoff |
| --- | --- |
| Scope | Observable result, boundaries, constraints, validation evidence/seams, unresolved decisions, artifact destination/attachment, proposed writes. |
| Tickets | Confirmed Scope in; titles, end-to-end outcomes, acceptance evidence, actual blockers, independent executability/verifiability, tracker/placement recommendation and writes out. |
| Published output | Actual item/document identities, revision when available, comment permalinks, and readback matching the approved content, attachment, metadata and relationships. |

Check these interfaces; leave source-specific analysis, templates, review and slicing procedures with the source. Accept its actual output only after readback, not because invocation returned successfully.

## Selection and preferences

For new content, resolve each role in order: current `--scope-source <canonical-name>` / `--ticket-source <canonical-name>`; working selection or Map lineage; compatible source explicitly invoked now; stored preference; compatible model-invoked source required by repository guidance. Apply invocation eligibility above. Reuse a compatible choice without asking again. Report an unavailable/incompatible selected source rather than silently substituting it; after discovery is exhausted, ask for a choice and recommend one only when supported by evidence. Replace recorded lineage only by a valid flag or the user's answer to that problem.

Store one global config at `~/.config/softleader/agent-skills/scope-it-remake/sources.json`:

```json
{
  "schema_version": 2,
  "scope": "<canonical-name>",
  "tickets": "<canonical-name>"
}
```

Omit unresolved roles; no repository lookup/override, credentials, prompts, tracker choices, or artifact content. Preserve unrelated fields. A valid flag, first selection, or approved replacement queues the shared role change for final approval, explaining its cross-repository effect. A partial flag preserves the other role; accepting an artifact or a source invoked for this run alone does not replace preferences.

For version 1, resolve each role from the current flag/replacement first, then `global`, then unanimous legacy `repositories` values. Ask once about unresolved conflicts, never prefer the current repo. Preview conversion to v2 and removal of old containers. An unknown version or unusable root requires clarification, not a substitute path.

Before saving approved changes, reread the file: preserve other roles/fields, and ask again if an affected value changed since preview. Read back the result. A failed save leaves only that write unresolved; it does not warrant republishing tickets.

## Artifact reuse

Read supplied artifacts and accept their role and exact content with recoverable review evidence, without requiring an installed producer. Separate unresolved decisions from confirmed content and recover missing approvals before advancing. Scope defines what/why/bounds/success; a ticket defines an end-to-end outcome and blockers; an execution plan defines how; supporting maps inform decisions. Keep roles separate even from one producer: files, commands, checklists and coding steps are not ticket nodes.

For one clear unit, a confirmed conversation or existing item with scope and ticket evidence can satisfy both roles; no extra spec/plan/item is required. Reuse existing homes and older layouts; migration needs approval. Match role-specific content: a shared post's timestamp or Map-link edit does not invalidate unchanged Scope. Material content changes invalidate that revision's approval and affected downstream decisions only; new storage IDs or approved proposed-to-actual substitutions do not.

Keep exact drafts/revisions, approvals, write lists and operation bindings in the session or a controlled task-local snapshot. Share recovery access/retention when pausing. This is not a required tracker record and not automatically Carry; separate external storage needs approval. If evidence is lost, ask for the missing part, not a wholesale restart or inferred authority from an existing Map.

## Map contract

Reuse a starting tracker item as the canonical home. Without one, resolve repository/source guidance and propose one new home; use local Markdown if no tracker exists or the user chooses it. Resolve conflicting source destinations before writing.

Scope and Map share one planning post: a new home's body, or a combined comment on an existing item preserving its original body. Reuse an existing Scope/Map post. Link external specs rather than copying them. One ticket uses a separate `## Ticket — <Title>` comment on that home: its item is the delivery identity, its permalink locates content, and no self-relation is created. Multiple tickets use separate child items. For local delivery, Scope/Map share one file and tickets have separate linked files.

The final managed block (`<!-- scope-it-remake:delivery-map:start -->` through `<!-- scope-it-remake:delivery-map:end -->`) contains:

- **Destination:** agreed outcome and scope summary.
- **Artifacts:** actual Scope/ticket links and optional execution plan; factual source lineage/revision pins where useful.
- **Delivery:** ticket waves, first executable ticket, actual containment/blockers with evidence, delivery method, and Planning `none` or the complete pointer/lane contract.
- **Out of scope:** boundaries and deferred work outside this delivery.
- **Continue:** start the linked executable ticket, read its artifacts and delivery contracts, and honor dependencies and the executor's separate authorization.

Use the user's language, linked titles, and plain「直接交付」/「共享整合分支交付」rather than internal acronyms. A compact ticket-only list/diagram suffices; one ticket needs no order diagram. Full requirements stay in Scope/Tickets. The Map has no Frontier/Publication status, artifact approval/state, source mode, draft placeholders, or renamed equivalents. Real tracker lifecycle, source readiness, relationship and lane evidence remain valid delivery facts.

### Relationships and fallbacks

Containment and blockers are independent axes; scheduling and Carrier choices create neither. Verify each supported native axis. For an unavailable capability (including comments/edits), use the selected source's fallback first, otherwise propose a concrete alternative; approve its exact writes. Persist per-axis unavailability, expected edges, fallback provenance and degraded evidence in the Map or a linked record. Text links are not native-verified. Failed/unknown readback of a supported axis is not unavailability. Accepted fallback evidence needs no installed producer. Repair only missing approved edges, preserving existing content, metadata and relations.

## Approval and publication

1. Preview the complete agreed Map, exact artifact revisions, placements and all writes: source publication/attachments/required metadata, relationships, conditional delivery/Git, preferences, and any external storage. Include initial home content needed before dependent writes and proposed-to-actual identity substitutions. Obtain exact-bundle approval; source/content confirmations alone are insufficient. The last content checkpoint may double as this approval only when both are explicit.
2. Freshly read targets and comments; reconcile with the approved bundle. Perform only missing approved operations in dependency order, resuming accepted producers for source-owned publication and composing the Map from their returned identities. Read back each result before dependent writes. Preserve unrelated content and the starting item's lifecycle. Do not commit/push the default branch.
3. Retain successful results and uncertainties in the recovery context. On timeout, look up actual items/comments against exact approved content before retrying; bind a unique match, and resolve ambiguity before another creation. A mismatch pauses affected writes; changed content or corrective writes need updated approval. Reuse successful siblings, never infer unknown authorization from Map existence.
4. After all approved operations, freshly recheck the whole bundle: content/revisions, placement/attachments, source metadata/readiness, both native axes or approved fallback evidence, applicable Planning pointers/path/ancestry/cleanup and lane evidence, and affected preferences. Earlier readbacks cannot excuse later drift. Preserve results and report only the affected part incomplete when evidence disagrees.
5. Read back the complete final Map with actual links and its same-post Scope, matching the agreement and preserving surrounding content. Only then report success with Map, Scope/ticket links, selected first ticket, Planning result and any degraded-axis evidence; enabled lane/plan details must be reachable through those links.

This sequence is not an atomic tracker transaction. Publication ends this workflow without waiting for implementation or closing tracker items. Later discussion/handoff retrieval causes no progress update; content amendments and exact repairs require approval. Explicit delivery verification uses the conditional contract under Workflow, not a publication status stamp.

$ARGUMENTS
