# Planning artifacts

Read when accepting completed planning material, classifying producer outputs, or deciding whether a frontier can advance.

## Acceptance

Accept an existing artifact without invoking its producer when it has:

- a durable pointer and revision or equivalent identity when available;
- the fields required by its artifact role;
- content-approval state with durable evidence, or an explicit `pending` state;
- unresolved decisions and contradictions separated from approved content; and
- readback matching the Map entry.

Record mode `supplied-artifact`. Producer availability, mutation-free drafting, resumability, and write preview are irrelevant because production has already happened. A revision change invalidates prior content approval until the new revision is reviewed.

Attach an accepted artifact by recording its pointer on the Map home. Keep its full content in its owning artifact unless the approved artifact is already a section of the Map home; acceptance does not rehome or duplicate it.

## Roles

Keep artifact roles separate:

- **Scope:** what, why, boundaries, and success evidence.
- **Delivery ticket:** a tracker-addressable, end-to-end outcome with acceptance evidence and blockers.
- **Execution plan:** how, including files, interfaces, coding steps, commands, or commit sequence.
- **Supporting map:** evidence that informs scope or slicing without becoming a ticket graph.

A checklist item, plan task, module, file, or dependency list becomes a ticket proposal only after it independently satisfies the delivery-ticket role. If one production run returns several roles, record each artifact separately.

## Compact scope

For one clear delivery unit, an approved conversation checkpoint or existing tracker issue may satisfy the scope role when it records the observable result, boundaries, acceptance evidence, approval pointer, and readback. The Delivery Map home may also satisfy the scope and single delivery-ticket roles. This compact path creates no separate spec or execution plan merely to complete a phase.

## Approval gates

Content approval belongs to the artifact-owning workflow and may require more than one review. Mutation approval applies only to the exact writes shown by `scope-it-remake`. Publication alone is not content approval.

Advance the frontier only when all three conditions have durable evidence:

1. the current artifact revision has every required content approval;
2. every performed write has mutation approval; and
3. readback matches the Map entry.

Otherwise record the current state and leave the frontier unchanged.
