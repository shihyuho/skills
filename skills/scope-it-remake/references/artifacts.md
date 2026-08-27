# Planning artifacts

Read when accepting completed planning material, classifying producer outputs, or deciding whether a frontier can advance.

## Existing artifacts

Accept an existing artifact without invoking its producer when it has:

- a durable pointer and revision or equivalent identity when available;
- the fields required by its artifact role;
- content-approval state with durable evidence, or an explicit `pending` state;
- unresolved decisions and contradictions separated from approved content; and
- readback matching the Map entry.

Record mode `supplied-artifact`. Producer availability, mutation-free drafting, resumability, and write preview are irrelevant because production has already happened. A material change to the artifact's content invalidates prior content approval until the new revision is reviewed.

Record accepted pointers on the draft Map now and attach them to the canonical planning post during final publication. Keep full content in its owning artifact; acceptance does not rehome or duplicate it, including artifacts in an older combined layout.

Record the exact body, comment, or document section that owns each role. When Scope shares a post with the managed Map block, compare its own content to the approved revision: a Map-only edit or post timestamp change does not invalidate Scope approval. Material Scope changes still do.

## Drafts and temporary staging

A source-owned draft can satisfy a planning frontier before publication. Record its exact content, revision identity, proposed destination, and the user's approval evidence. A conversation checkpoint can identify the revision; a published URL is not required for handoff to the next source. Keep draft and published states distinct, and use proposed ticket references instead of invented tracker identities.

Default to conversation state. When a source needs a file or a resumable snapshot helps, use a fresh task-local temporary location and retain the drafts, Map, approvals, pending writes, and any publication bindings together. Temporary staging is permitted during planning; it does not authorize tracker writes, canonical spec updates, commits, or preference changes, and it is not automatically Carry. Share its path if the session pauses. If draft content or approval evidence cannot be recovered, ask only for the missing material rather than claiming it was approved.

## Roles

Keep artifact roles separate:

- **Scope:** what, why, boundaries, and success evidence.
- **Delivery ticket:** an end-to-end outcome with acceptance evidence and blockers, addressable by a proposed reference during planning and a tracker identity after publication.
- **Execution plan:** how, including files, interfaces, coding steps, commands, or commit sequence.
- **Supporting map:** evidence that informs scope or slicing without becoming a ticket graph.

A checklist item, plan task, module, file, or dependency list becomes a ticket proposal only after it independently satisfies the delivery-ticket role. If one production run returns several roles, record each artifact separately.

## Compact scope

For one clear delivery unit, an approved conversation checkpoint or existing tracker item may satisfy the scope role when it records the observable result, boundaries, acceptance evidence, and approval reference. Read back existing published material when accepting it. The same tracker item can serve as Map home and delivery ticket identity; new ticket content still goes in its own comment, separate from Scope/Map. Reuse already accepted ticket content without republishing it solely to change its layout. This compact path creates no extra spec document, execution plan, or tracker item merely to complete a phase.

## Approval gates

Content approval belongs to the artifact-owning workflow and may require more than one review. Preserve those gates using the exact draft or staged revision when the source permits it. If a required review can only happen after external publication, report the incompatibility before writes and ask for a compatible source or completed artifact.

Planning advances when the current revision satisfies its role and required content approvals. Continue directly to the next frontier; publication and readback of new artifacts are not prerequisites. Unresolved decisions remain pending.

A changed content revision invalidates its approval and any downstream conclusions affected by that change. Preserve unaffected work, revise the dependent drafts, and refresh the final bundle approval if its approved content or writes change. At publication, bind the returned artifact revision to its confirmed draft by matching the reviewed content in readback. New storage revision IDs and substituting returned tracker identities for approved proposed references are not themselves content changes; substantive changes require fresh approval.

The final publication checkpoint binds the confirmed draft revisions to all exact writes. An earlier confirmation of scope or ticket content does not authorize publication. The final content confirmation may also authorize publication when both are explicitly presented together.

## Publication record

Include a resumable record in the final write preview. At publication, place it on the Map home or link a durable artifact from **Publication**: retain exact confirmed draft content or revision-pinned durable references, the final write list, scoped approval evidence, and proposed-to-actual identity bindings. Keep already-owned content at its existing home rather than duplicating it. Record each successful or uncertain operation as it happens. A conversation-only or temporary-file reference is sufficient while drafting, but the published Map must let a later session recover the approved remaining work without that conversation.

Keep the planning post's record compact, using durable references for ticket payloads instead of embedding their full drafts there. Include any separate durable draft storage in the approved write list. Bind both item identities and comment permalinks to their operations. If a comment creation times out, inspect the target's comments and reconcile the operation with its exact approved content before retrying; an ambiguous match requires recovery, not another comment.

Read back each published artifact before consuming it in dependent writes. A mismatch pauses affected work for content review and a revised write checkpoint. Preserve successful results; never rewrite them merely to make them match an old draft without approval. If the publication record cannot be recovered, ask for the missing bundle or approval evidence instead of regenerating content under an old `approved` status.

Publication is complete only when:

1. every final artifact revision has its required content approvals;
2. each write is covered by the approved bundle; and
3. readback of artifacts, attachments, relationships, conditional delivery evidence, and any queued preference changes matches the approved bundle and Map.

Otherwise keep `publish` current and record actual partial results. Reconcile them before retrying; reuse matching items rather than duplicating them. Publication or readback alone is never content approval.
