# Planning artifacts

Read when accepting planning material, classifying producer outputs, checking content approval, or recovering interrupted publication. Keep working revisions, approvals, and operation results in the session or controlled temporary storage; the published Map carries agreed delivery content and links.

## Existing artifacts

Reuse an existing artifact without invoking its producer when it has:

- a durable pointer and revision or equivalent identity when available;
- the fields required by its artifact role;
- recoverable approval evidence for the consumed revision, or a content review still to obtain;
- unresolved decisions and contradictions separated from approved content; and
- readback matching the artifact identity and content being consumed.

Record available evidence and missing reviews internally; the artifact needs no public approval/state or source-mode field. Producer availability, mutation-free drafting, resumability, and write preview are irrelevant because production has already happened. Verify the owning workflow's required content approvals before advancing; ask for any missing evidence or review. A material change to the artifact's content invalidates prior content approval until the new revision is reviewed.

Record accepted pointers on the draft Map now and attach them to the canonical planning post during final publication. Keep full content in its owning artifact; acceptance does not rehome or duplicate it, including artifacts in an older combined layout.

Record the exact body, comment, or document section that owns each role. When Scope shares a post with the managed Map block, compare its own content to the approved revision: a Map-only edit or post timestamp change does not invalidate Scope approval. Material Scope changes still do.

## Drafts and temporary staging

A source-owned draft can satisfy a discussion step before publication. Keep its exact content, revision identity, proposed destination, and approval evidence internally. A conversation checkpoint can identify the revision; a published URL is not required for handoff to the next source. Distinguish drafts from actual published artifacts, and use proposed ticket references instead of invented tracker identities.

Default to the session. When a source needs a file or a resumable snapshot helps, use a fresh controlled task-local temporary location and retain drafts, the proposed Map, approvals, remaining writes, and publication bindings together. Share the recovery location and its access/retention arrangements if the session pauses. Temporary staging does not authorize tracker writes, canonical spec updates, commits, or preference changes, and is not automatically Carry. If draft content or approval evidence cannot be recovered, ask only for the missing material rather than claiming it was approved.

## Roles

Keep artifact roles separate:

- **Scope:** what, why, boundaries, and success evidence.
- **Delivery ticket:** an end-to-end outcome with acceptance evidence and blockers, addressable by a proposed reference during planning and a tracker identity after publication.
- **Execution plan:** how, including files, interfaces, coding steps, commands, or commit sequence.
- **Supporting map:** evidence that informs scope or slicing without becoming a ticket graph.

A checklist item, plan task, module, file, or dependency list becomes a ticket proposal only after it independently satisfies the delivery-ticket role. If one production run returns several roles, record each artifact separately.

## Compact scope

For one clear delivery unit, a conversation checkpoint or existing tracker item may satisfy the scope role when it records the observable result, boundaries, and acceptance evidence, with content approval recoverable separately. Read back existing published material when accepting it. The same tracker item can serve as Map home and delivery ticket identity; new ticket content still goes in its own comment, separate from Scope/Map. Reuse already accepted ticket content without republishing it solely to change its layout. This compact path creates no extra spec document, execution plan, or tracker item merely to complete a phase.

## Approval gates

Content approval belongs to the artifact-owning workflow and may require more than one review. Preserve those gates using the exact draft or staged revision when the source permits it. If a required review can only happen after external publication, report the incompatibility before writes and ask for a compatible source or completed artifact.

Planning advances when the current revision satisfies its role and required content approvals. Continue directly to the next frontier; publication and readback of new artifacts are not prerequisites. Unresolved decisions remain pending.

A changed content revision invalidates its approval and any downstream conclusions affected by that change. Preserve unaffected work, revise the dependent drafts, and refresh the final bundle approval if its approved content or writes change. At publication, bind the returned artifact revision to its confirmed draft by matching the reviewed content in readback. New storage revision IDs and substituting returned tracker identities for approved proposed references are not themselves content changes; substantive changes require fresh approval.

The final publication checkpoint binds the confirmed draft revisions to all exact writes. An earlier confirmation of scope or ticket content does not authorize publication. The final content confirmation may also authorize publication when both are explicitly presented together.

## Recovery record

Retain the exact confirmed drafts or revision-pinned references, the final write list, scoped approval evidence, and proposed-to-actual operation bindings in the session or controlled temporary storage. Keep successful and uncertain results as they happen, including returned item identities and comment permalinks. This internal record is not a required tracker artifact or part of the final Map. Any separately requested external storage is an exact write needing approval; do not upload full worktree snapshots or unrelated Preserve content implicitly.

For an interrupted publication, recover that record and read actual tracker results before performing only the missing approved writes. A Map, artifact link, or historical progress label does not establish approval for unknown work. If a comment creation times out, inspect the target's comments and reconcile the operation with its exact approved content before retrying; an ambiguous match requires recovery, not another comment. Keep full ticket drafts in this recovery context or their owning artifacts, not in the combined Scope/Map post.

Read back each published artifact before consuming it in dependent writes. A mismatch pauses affected work for content review and a revised write checkpoint. Preserve successful results; never rewrite them merely to make them match an old draft without approval. If exact drafts, approval, or uncertain operation bindings cannot be recovered from the session, controlled storage, and readback, ask for the missing evidence before further writes. Reuse known artifacts without restarting their analysis or inventing the missing approved content.

## Final publication verification

Per-operation readback protects dependent writes; completion also requires a fresh consolidated pass after all approved operations. Re-read the current state rather than relying on earlier successes:

- artifact content/revisions, approved placement and attachments, and source-required metadata/readiness;
- native containment and native blockers independently, or each approved unavailable-axis fallback with its provenance and degraded evidence;
- applicable Planning Carrier, exact path, complete pointers, baseline ancestry and cleanup invariants, plus enabled lane contracts and publication-time evidence; and
- affected source-preference values covered by approved writes, preserving unrelated preferences.

Compare this pass to the approved bundle and the Map's actual bindings. Earlier artifact, edge, or preference readback does not excuse later drift. On mismatch, preserve results, report the affected work incomplete in the session, and reconcile only that part; changed content or writes require an updated checkpoint. Once the pass matches, read back the complete final Map and its combined Scope content. Confirm actual artifact links and delivery contracts match the agreement, surrounding content remains intact, and no orchestration fields or draft placeholders were added. This is current-state verification, not a claim that the tracker transaction was atomic.

Publication is complete only when:

1. every final artifact revision has its required content approvals;
2. each write is covered by the approved bundle; and
3. the fresh consolidated pass and final Map readback match the approved bundle.

Otherwise retain actual partial results in the recovery record and report the missing verification or write without stamping a workflow status onto the Map. Reconcile before retrying; reuse matching items rather than duplicating them. Publication or readback alone is never content approval.

Finish this workflow after verified publication. Persist the Planning and lane contracts and link their evidence from the Map, but do not wait for implementation, landing, or tracker closure. A later explicit delivery-verification request checks those lifecycle gates through [delivery.md](delivery.md#requested-delivery-verification); a failed delivery gate does not erase successful publication. Further discussion or handoff retrieval creates no progress update on the Map; content amendments and exact repairs need their own approval.
