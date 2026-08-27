---
name: scope-it-remake
description: "Shape scope, tickets, and delivery into one Delivery Map through interchangeable sources, then publish the confirmed bundle."
license: MIT
disable-model-invocation: true
---

# scope-it-remake

Shape work into a Delivery Map through a continuous planning conversation. Focus on one **frontier** at a time, then continue directly to the next after its content is confirmed. Publish only after the whole bundle is ready and the user approves its exact writes.

This is an experimental parallel experience. It does not replace or migrate `scope-it` artifacts.

## Contract

`$ARGUMENTS` supplements the conversation. It may set `--scope-source <canonical-name>` and `--ticket-source <canonical-name>`; source resolution and persistence follow [references/sources.md](references/sources.md). Scope and ticket production use interchangeable sources rather than required skill names.

During planning, keep tracker items, published artifacts, preferences, and Git state unchanged. Keep drafts in the conversation or optional task-local temporary files. Content confirmation permits the next planning frontier, not publication. The final checkpoint authorizes the complete publication bundle; track that approval separately from each source's content gates through [references/artifacts.md](references/artifacts.md). Preserve unrelated content and the starting item's lifecycle state. Do not commit or push the default branch.

## The Delivery Map

The Delivery Map is the top-level planning artifact. During discussion, maintain a draft of its managed low-resolution status block. Propose its canonical home now, but create or update that home only during final publication:

1. When a starting tracker item exists, reuse that item as the Delivery Map home.
2. Otherwise resolve the publication environment from repository guidance and the selected sources, then propose one new Delivery Map item in that tracker. A source may resolve this choice while drafting tickets; settle it before the final checkpoint. If still unresolved, recommend a home and ask the user. Use local Markdown as the Map home when no tracker is available or the user chooses a local artifact.
3. Publish Scope and the Delivery Map together in one **planning post**. For a new tracker item, use its body. For an existing item without a planning post, add one combined comment and preserve the original body. If an accepted Scope or Map already has a post on that home, reuse it with only the approved changes. When the full spec belongs to an external artifact, keep a Scope link in the planning post rather than copying that artifact.
4. Keep delivery tickets separate from the planning post. For one ticket, publish `## Ticket — <Title>` as its own comment on the Map home; use the home item's identity for delivery and its comment permalink for ticket content, with no extra item or self-relationship. For multiple tickets, create separate child items with native containment and native blockers only for actual dependencies. If the selected layout needs unsupported comments, post edits, or native relations, propose a supported alternative and obtain approval before publication. For local Markdown, keep Scope and Map in one file and each ticket in a separate linked file.

Use exactly one Map home and one canonical planning post. After publication, update the managed Map block in that post while preserving Scope and surrounding content. Identify the tracker item, body or comment permalink, and exact changes in the final checkpoint. A new frontier does not need a new comment; a temporary draft is not a second Map home. Reuse accepted artifacts in older layouts without moving or duplicating them unless the user approves a layout migration.

```markdown
<!-- scope-it-remake:delivery-map:start -->
## Destination
<the observable result this delivery should reach>

## Sources
- Scope: <identity or pending>; mode: <invoked | supplied-artifact | pending>
- Tickets: <identity or pending>; mode: <invoked | supplied-artifact | pending>

## Settled
- <decision gist and pointer when one exists>

## Artifacts
- Scope: <draft reference, published pointer, or pending>; revision: <identity or unavailable>; approval: <approved | pending>; state: <pending | draft | published>
- Tickets: <draft reference, published pointer, or pending>; revision: <identity or unavailable>; approval: <approved | pending>; state: <pending | draft | published>
- Execution plan, when present: <draft reference or published pointer>; revision: <identity or unavailable>; approval: <approved | pending>; state: <draft | published>

## Frontier
<scope | tickets | delivery | publish | done>: <one-line current objective; when done, start the linked first executable delivery ticket>

## Publication
<not-approved | approved | partial | verified>; bundle: <draft reference or durable approved publication record>; results: <published bindings or none>

## Later
- <known work that is not current yet>

## Out of scope
- <explicit boundary and reason>

## Continue
Resume from **Frontier** and follow **Artifacts** references only for material that frontier needs. Reuse approved draft revisions and existing published artifacts instead of restarting completed work.

After content confirmation, continue directly to the next planning frontier. Keep tracker and publication writes queued until scope, tickets, and delivery are settled and the user approves the complete bundle's exact writes.

If publication is partial, recover the exact bundle and approval evidence from **Publication**, read back existing results, and resume only the missing approved writes. If that record is missing, recover it with the user before further writes; the status alone is not authorization. When new content is needed but no compatible Scope or Ticket source can be resolved, stop and ask which skill should produce it. Set **Frontier** to `done` only after publication readback, then hand implementation to its linked delivery ticket.
<!-- scope-it-remake:delivery-map:end -->
```

Render map headings and continuation instructions in the user's language. Repeat artifact entries per ticket when there are several, keeping each revision, approval, and publication state separate. Refer to tracker artifacts by linked title in user-facing text. Keep full requirements, acceptance criteria, and product decisions in Scope or Tickets; the Map carries brief pointers, ticket relationships, delivery choices, and continuation state. Keep **Continue** stable across frontier updates unless the protocol itself changes.

## Interaction

### Orient or resume

1. Read the conversation, supplied tracker item or document, repository guidance, and current worktree status. Load an existing Map or saved draft when present; otherwise name the Destination and propose a Map home. Avoid loading later-frontier detail early.
2. Read [references/artifacts.md](references/artifacts.md) to classify existing material and recover exact revisions and approvals. Start from the first unresolved planning frontier, or `publish` when all planning is confirmed. If an existing Map is verified `done` and no amendment is requested, return its handoff instead of publishing again. Existing published Maps remain unchanged while drafting amendments.
3. If decisions block the current frontier, use `grilling` on that branch. Wait for substantive answers, then continue planning once shared understanding is confirmed; no separate restart invocation is needed.

### Discuss continuously

Work through `scope → tickets → delivery` in order. Resolve a source through [references/sources.md](references/sources.md) when new scope or ticket content is needed. Pass **draft-only now; publication deferred until final bundle approval** to every source.

- **scope:** accept suitable existing material, including the compact one-unit path, or obtain a source-owned draft. Present observable behavior, boundaries, validation seams, unresolved decisions, and proposed attachment to the Map home. Once that revision is confirmed, continue directly to the ticket frontier; a published spec URL is not a prerequisite.
- **tickets:** reuse accepted ticket material when it already satisfies the role, including the compact single-ticket path; otherwise give the confirmed scope revision to the ticket source for drafting. Present each ticket by title, end-to-end outcome, acceptance evidence, and blockers. Use proposed ticket references until publication assigns real identities. Once the breakdown is confirmed, continue directly to delivery planning.
- **delivery:** propose containment and blockers as separate axes, select the first executable ticket, and settle any delivery-only choices. Independent ticket landing is the default. Read [references/delivery.md](references/delivery.md) only for scope-owned worktree changes or atomic multi-ticket landing; queue its writes for final publication.

At each content checkpoint, show the recommendation, exact draft revision, and remaining decision. After confirmation, update the draft Map and proceed until the next substantive question or the final checkpoint. A phase boundary is not a reason to publish, stop, ask permission merely to continue, or require a new skill invocation. If a source is missing or cannot defer publication, stop and ask the user for a compatible source or completed artifact; do not generate its missing content yourself.

Use [references/artifacts.md](references/artifacts.md) for optional temporary staging and revision changes. If confirmed content changes, revisit only affected downstream decisions before proceeding.

### Confirm and publish

1. Assemble one final checkpoint after planning is ready. Show the Map home and planning post, exact scope and ticket revisions, ticket graph and first executable ticket, delivery choice, and all proposed writes: combined Scope/Map publication or section updates, separate ticket comments or child items, publication record, external artifact publication or attachment, relationships, source preferences, and any activated repository or Git changes. Use proposed identities and explicit bindings for items or comments that do not exist yet.
2. Wait for approval of this complete bundle. The last content checkpoint may double as publication approval when it shows all exact writes and clearly asks to publish them. Earlier scope or ticket confirmation alone is not publication approval.
3. Freshly read the targets, including relevant comments, and reconcile existing artifacts. Establish the single Map home and combined planning post with `publish` status and the approved publication record defined in [references/artifacts.md](references/artifacts.md). Publish or reuse artifacts through their sources, bind returned item and comment identities, and apply approved relationships and delivery-only changes in dependency order. Read back each result before dependent writes, preserving unrelated target content. If reviewed content or placement no longer matches, stop affected writes and obtain a revised checkpoint.
4. Save queued source preferences through [references/sources.md](references/sources.md), read them back, and update the Map with actual results. If any operation fails or is uncertain, record partial progress; look up existing results before retrying and resume only missing approved writes. Batch publication is not an atomic tracker transaction.
5. Set `done` only when all approved artifact, relationship, conditional delivery, and preference writes have matching readback, then verify the final Map block itself. Return the linked first executable ticket, scope and ticket titles, and any execution-plan pointer, then stop. Leave implementation and its workspace, agent, and commit-cycle policy to the execution workflow.

Render delivery choices in the user's language with plain terms such as「直接交付」and「共享整合分支交付」instead of internal acronyms.

$ARGUMENTS
