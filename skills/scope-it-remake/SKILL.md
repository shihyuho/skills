---
name: scope-it-remake
description: "Shape scope, tickets, and delivery into one Delivery Map through interchangeable sources, then publish the confirmed bundle."
license: MIT
disable-model-invocation: true
---

# scope-it-remake

Shape work into a Delivery Map through a continuous planning conversation. Discuss scope, tickets, and delivery, confirm the complete Map and its exact writes, then publish, read back, and finish.

This is an experimental parallel experience. It does not replace or migrate `scope-it` artifacts.

## Contract

`$ARGUMENTS` supplements the conversation. It may set `--scope-source <canonical-name>` and `--ticket-source <canonical-name>`; source resolution and persistence follow [references/sources.md](references/sources.md). Scope and ticket production use interchangeable sources rather than required skill names.

Accept direct invocation or valid delegation from any upstream skill under the host's explicit-invocation rules, including a caller's fixed allowlist. Both remain bounded to the user's approved scope package. An upstream invocation or saved lineage alone does not authorize arbitrary writes or bypass this skill's final checkpoint.

The fixed allowlist for conditional Git mechanics is `create-branch`, `create-worktree`, `commit`, and `push`; follow [their source contract](references/sources.md#git-mechanics) only for approved operations that remain incomplete.

During planning, keep tracker items, published artifacts, preferences, and Git state unchanged. Keep drafts and recovery evidence in the session or controlled task-local temporary storage. Content confirmation permits the next discussion step, not publication. The final checkpoint authorizes the complete publication bundle; track that approval separately from each source's content gates through [references/artifacts.md](references/artifacts.md). Preserve unrelated content and the starting item's lifecycle state. Do not commit or push the default branch.

## The Delivery Map

The Delivery Map is the agreed delivery content: destination, artifact links, ticket graph, delivery contracts, boundaries, and handoff. Draft it during discussion and propose its canonical home, then publish only the confirmed content:

1. When a starting tracker item exists, reuse that item as the Delivery Map home.
2. Otherwise resolve the publication environment from repository guidance and the selected sources, then propose one new Delivery Map item in that tracker. A source may resolve this choice while drafting tickets; settle it before the final checkpoint. If still unresolved, recommend a home and ask the user. Use local Markdown as the Map home when no tracker is available or the user chooses a local artifact.
3. Publish Scope and the Delivery Map together in one **planning post**. For a new tracker item, use its body. For an existing item without a planning post, add one combined comment and preserve the original body. If an accepted Scope or Map already has a post on that home, reuse it with only the approved changes. When the full spec belongs to an external artifact, keep a Scope link in the planning post rather than copying that artifact.
4. Keep delivery tickets separate from the planning post. For one ticket, publish `## Ticket — <Title>` as its own comment on the Map home; use the home item's identity for delivery and its comment permalink for ticket content, with no extra item or self-relationship. For multiple tickets, create separate child items with native containment and native blockers only for actual dependencies. If the selected layout needs unsupported comments, post edits, or native relations, use [the source's fallback contract](references/sources.md#tracker-capability-fallback) and obtain approval before publication. For local Markdown, keep Scope and Map in one file and each ticket in a separate linked file.

Use exactly one Map home and one canonical planning post. Identify the tracker item, body or comment permalink, and exact changes in the final checkpoint. After publication, update its managed Map block only for an approved content amendment or exact repair, preserving Scope and surrounding content. Discussion progress creates no tracker updates. Reuse accepted artifacts in older layouts without moving or duplicating them unless the user approves a layout migration.

```markdown
<!-- scope-it-remake:delivery-map:start -->
## Destination
<the confirmed observable result and scope summary>

## Artifacts
- Scope: <linked title or section in this planning post>
- Tickets: <linked titles; single-ticket comment permalink when applicable>
- Execution plan, when present: <linked title>

## Delivery

- Order: <ticket waves or executable frontier; selected first ticket>
- Relationships: <containment and blockers; evidence pointer with any degraded axis identified>
- Lane: <independent landing, or shared integration lane record>
- Planning: <none, or complete Planning Baseline pointer>

## Out of scope
- <explicit boundary and reason, including deferred work outside this delivery>

## Continue
Start the linked first executable ticket and follow its actual blockers. Read its Scope, execution plan when present, and applicable Planning/lane contracts before implementation. Reuse the recorded delivery path and shared Planning pointers rather than duplicating Carry.

Implementation, merges, and tracker closure belong to the execution workflow under its own authorization. For requested delivery-resume or landing verification, follow the saved contracts for that stage: unfinished implementation needs its current path; completed landing may use recoverable immutable implementation or PR-head evidence after branch retirement. Verify ancestry, landing content, and applicable exact-HEAD gates before reporting delivery complete.
<!-- scope-it-remake:delivery-map:end -->
```

Render headings and handoff instructions in the user's language and refer to tracker artifacts by linked title. Use actual published identities in the final Map; omit absent optional artifacts. Include factual source names/links or revision pins only when needed for lineage or delivery. Keep full requirements, acceptance criteria, and product decisions in Scope or Tickets.

The published Map contains no discussion Frontier, Publication status, artifact approval/state fields, source modes, or draft/pending artifact placeholders. Keep orchestration evidence in [session or controlled temporary recovery records](references/artifacts.md#recovery-record), not renamed progress fields on the Map. Actual tracker lifecycle, source-required readiness metadata, relationship evidence, and Planning/lane execution contracts remain authoritative.

Keep recommended ticket waves/frontiers, native containment, actual blockers, the delivery lane, and Planning transport distinct. An ordering preference or Carrier choice creates no blocker. Use a compact list or diagram for multiple tickets; a single ticket needs no order diagram. Keep code files, modules, and execution steps inside their owning artifacts, not as ticket-graph nodes.

## Interaction

### Orient or resume

1. Read the conversation, supplied tracker item or document, repository guidance, and current worktree status. Load an existing Map and any recoverable working drafts when present; otherwise name the Destination and propose a Map home. Load only evidence needed for the current decision.
2. Read [references/artifacts.md](references/artifacts.md) to classify material and recover exact content, approvals, and remaining writes. Continue from the first unresolved discussion step, or reconcile an interrupted publication when exact write approval is recoverable. A Map's existence is not approval for missing writes. A request only to retrieve an existing handoff returns its links without restarting planning; explicit delivery verification follows the conditional routing below. Leave published Maps unchanged while drafting amendments.
3. If decisions block the current step, use `grilling` on that branch. Wait for substantive answers, then continue planning once shared understanding is confirmed; no separate restart invocation is needed.

Read [references/delivery.md](references/delivery.md) at delivery planning, or before conditional publication/repair, when there are entry changes (including unclassified or Uncertain changes), existing/pending Carry, Carrier or baseline evidence, or a proposed/enabled shared integration lane. Apply this routing even when only publication repairs remain and the entry worktree is clean. For requested delivery verification, read its relevant branch rather than returning only the handoff; keep verification read-only unless exact corrective writes are separately approved.

### Discuss continuously

Work through `scope → tickets → delivery` in order. Resolve a source through [references/sources.md](references/sources.md) when new scope or ticket content is needed. Pass **draft-only now; publication deferred until final bundle approval** to every source.

- **scope:** accept suitable existing material, including the compact one-unit path, or obtain a source-owned draft. Present observable behavior, boundaries, validation seams, unresolved decisions, and proposed attachment to the Map home. Once that revision is confirmed, continue directly to the ticket frontier; a published spec URL is not a prerequisite.
- **tickets:** reuse accepted ticket material when it already satisfies the role, including the compact single-ticket path; otherwise give the confirmed scope revision to the ticket source for drafting. Present each ticket by title, end-to-end outcome, acceptance evidence, and blockers. Use proposed ticket references until publication assigns real identities. Once the breakdown is confirmed, continue directly to delivery planning.
- **delivery:** propose ticket waves/frontiers, containment, actual blockers, and delivery lane as distinct choices. Independent ticket landing is the default. Apply any triggered conditional delivery rules before fixing the selected first ticket: independent landing with Carry selects its sole Carrier; a shared lane retains its executable terminal frontier. Record Planning `none` when no Carry or saved baseline requires delivery. Queue all writes for final publication.

At each content checkpoint, show the recommendation, exact draft revision, and remaining decision. After confirmation, update the draft Map and proceed until the next substantive question or the final checkpoint. A phase boundary is not a reason to publish, stop, ask permission merely to continue, or require a new skill invocation. If a source is missing or cannot defer publication, stop and ask the user for a compatible source or completed artifact; do not generate its missing content yourself.

Use [references/artifacts.md](references/artifacts.md) for optional temporary staging and revision changes. If confirmed content changes, revisit only affected downstream decisions before proceeding.

### Confirm and publish

1. Assemble one final checkpoint after planning is ready. Show the complete agreed Map, its home and planning post, exact scope and ticket revisions, ticket graph and selected first executable ticket, delivery choice, Planning result, and all proposed writes: combined Scope/Map publication or section updates, separate ticket comments or child items, source-required metadata/readiness, external artifact publication or attachment, relationships and fallback evidence, source preferences, and any activated repository or Git changes. Preview any initial content needed to establish a home before dependent writes, plus its final Map bindings. Use proposed identities and explicit substitutions for items or comments that do not exist yet; retain this approval through [the recovery contract](references/artifacts.md#recovery-record).
2. Wait for approval of this complete bundle. The last content checkpoint may double as publication approval when it shows all exact writes and clearly asks to publish them. Earlier scope or ticket confirmation alone is not publication approval.
3. Freshly read the targets, including relevant comments, and reconcile existing artifacts. Publish or reuse artifacts through their sources and apply approved relationships and delivery-only changes in dependency order. Where a home must exist before its dependents, establish it using the previewed confirmed content, then finish the same planning post's Map with actual returned identities. Read back each result before dependent writes, preserving unrelated target content. If reviewed content or placement no longer matches, stop affected writes and obtain a revised checkpoint.
4. Save queued source preferences through [references/sources.md](references/sources.md) and read them back. Keep successful and uncertain operation bindings in the recovery record. On interruption, look up existing results before retrying and resume only missing approved writes. Batch publication is not an atomic tracker transaction.
5. Finish the approved Map with actual artifact links, then run the fresh consolidated verification in [references/artifacts.md](references/artifacts.md#final-publication-verification), retaining per-operation readback as well. Read back the complete final Map and its Scope content before reporting success. Return the Map link, selected first executable ticket, linked scope/ticket titles, and compact Planning result (`none` or pointer); identify any degraded relationship axis and link its evidence. The Map must expose enabled lane records and any execution plan without expanding low-level receipts in the reply. End this workflow after verification; implementation, landing, and tracker closure proceed under the execution contract. Further discussion or a handoff request alone causes no Map update or ongoing progress tracking.

Render delivery choices in the user's language with plain terms such as「直接交付」and「共享整合分支交付」instead of internal acronyms.

$ARGUMENTS
