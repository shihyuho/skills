---
name: scope-it-remake
description: "Chart settled work into a Delivery Map and advance one planning frontier at a time through interchangeable scope and ticket sources."
license: MIT
disable-model-invocation: true
---

# scope-it-remake

Turn settled work into a durable Delivery Map without trying to finish the whole planning pipeline in one interaction. Advance one visible **frontier** at a time, load only what that frontier needs, and leave the next step obvious.

This is an experimental parallel experience. It does not replace or migrate `scope-it` artifacts.

## Contract

`$ARGUMENTS` supplements the conversation. It may set `--scope-source <canonical-name>` and `--ticket-source <canonical-name>`; source resolution and persistence follow [references/sources.md](references/sources.md). An invocation authorizes read-only orientation; mutate only the current frontier after the user approves its exact proposed writes. Track that mutation approval separately from the owning workflow's content approval as defined in [references/artifacts.md](references/artifacts.md). Preserve unrelated tracker content, the starting item's lifecycle state, repository bytes, and Git state. Do not commit or push the default branch.

Scope and ticket production use interchangeable sources rather than required skill names; read [references/sources.md](references/sources.md) when selecting or invoking a source.

## The Delivery Map

The Delivery Map is the top-level planning artifact. Keep one managed low-resolution status block in its canonical home and update that block in place while preserving all surrounding content:

1. When a starting tracker item exists, reuse that item as the Delivery Map home.
2. Otherwise resolve the publication environment from repository guidance and the selected sources, then propose one new Delivery Map item in that tracker. When neither defines a tracker, include one bounded tracker recommendation or question in the first checkpoint. Use local Markdown as the Map home when no tracker is available or the user chooses a local artifact.
3. Attach the approved Scope to the Map home: keep it as a section there when the Scope source produces tracker content, or link its owning artifact when the full spec lives elsewhere.
4. For one delivery ticket, keep its `## Ticket — <Title>` section on the Map home. For multiple tickets, publish each delivery ticket as a child item of the Map home when native containment is available.

Use exactly one Map home: reuse the starting tracker item or create a new Delivery Map item, never both. Update its block rather than adding a new map comment per frontier. The checkpoint must identify the tracker chosen by repository guidance or a source contract, the canonical block, and the exact section replacement it proposes. Do not assume a tracker vendor.

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
- Scope: <pointer or pending>; revision: <identity or unavailable>; approval: <approved | pending>
- Tickets: <pointers or pending>; revision: <identity or unavailable>; approval: <approved | pending>
- Execution plan: <pointer or none>; revision: <identity or unavailable>; approval: <approved | pending>

## Frontier
<scope | tickets | delivery | done>: <one-line current objective; when done, start the linked first executable delivery ticket>

## Later
- <known work that is not current yet>

## Out of scope
- <explicit boundary and reason>

## Continue
Resume from **Frontier** and follow **Artifacts** pointers only for material that frontier needs. Reuse approved revisions instead of restarting completed work.

Before any write, show the exact current-frontier mutations and wait for approval. After writing, read the result back, replace this same Delivery Map block, and stop.

When no compatible Scope or Ticket source can be resolved, stop and ask the user which skill should produce it. When **Frontier** is `done`, hand implementation to its linked delivery ticket instead of restarting planning.
<!-- scope-it-remake:delivery-map:end -->
```

Render map headings and continuation instructions in the user's language. Refer to tracker artifacts by linked title in user-facing text. Keep detailed content in its owning artifact and only a gist on the map. Keep **Continue** stable across frontier updates unless the protocol itself changes.

## Interaction

### Chart

Use this mode when no Delivery Map exists.

1. Orient from the conversation, supplied tracker item or document, repository guidance, and current worktree status. Avoid loading ticket, Git, or delivery-lane detail before its frontier.
2. Name the Destination and Map home, following any publication environment defined by the selected source. When completed planning material exists, read [references/artifacts.md](references/artifacts.md) and accept it when it satisfies the artifact contract.
3. If the input is not settled, bound the unresolved branch to the decisions blocking the current frontier and invoke `grilling`. Let it reach shared understanding and user confirmation, then stop; charting resumes in the next interaction.
4. For the first incomplete frontier, resolve an active Source through [references/sources.md](references/sources.md) only when new content is required. When no compatible source can be resolved, stop and ask the user which skill should produce it.
5. Draft the low-resolution map with the first incomplete frontier in `scope → tickets → delivery`; use `done` when all three are complete. Show one compact checkpoint:
   - **Now:** the current frontier and proposed outcome.
   - **Recommendation:** the source, destination, and material choice being recommended.
   - **Content:** the artifact revision and content-approval state.
   - **Writes:** the exact tracker or repository mutations approval would authorize.
   - **Later:** the next known frontier, without doing its analysis.
6. Wait for approval. The first interaction remains read-only.

### Advance

Use this mode with an existing map or a previously approved checkpoint.

1. Load the map and the artifacts referenced by its current frontier. Zoom into other material only when the frontier depends on it.
2. Read [references/artifacts.md](references/artifacts.md) when accepting, classifying, or approving artifacts. Reconcile durable evidence: reuse matching artifacts, propose the smallest missing delta, and surface contradictions without restarting completed frontiers. A changed artifact revision requires fresh content-approval evidence.
3. Work exactly one frontier:
   - **scope:** accept a completed artifact that satisfies the scope role, including the compact one-unit path, or ask the selected scope source for a mutation-free draft attached to the Map home. Present its artifact form, Map attachment, observable behavior, boundaries, validation seams, unresolved decisions, and proposed writes.
   - **tickets:** accept completed artifacts that satisfy the delivery-ticket role, or give the approved scope artifact to the selected ticket source. Present each proposed ticket by title, end-to-end outcome, acceptance evidence, and blockers. Use ticket nodes—not files, modules, coding steps, or tests—for any diagram.
   - **delivery:** publish or repair native containment and blockers as separate axes, choose the first executable ticket, and finish delivery-only planning. Read [references/delivery.md](references/delivery.md) only when scope-owned worktree changes or atomic multi-ticket landing activates those branches.
4. Before writes, show the compact checkpoint and wait for mutation approval unless durable evidence proves those exact writes were already approved. Preserve every content-approval gate owned by the artifact-producing workflow.
5. After mutation approval, perform only that frontier's writes, update the canonical map block in place, and read them back. Advance the map only when the current artifact revision has content approval, the performed writes have mutation approval, and readback matches; otherwise leave the frontier current. Report the verified result and stop.

Independent ticket landing is the default delivery path. Describe the choice in the user's language with plain terms such as「直接交付」and「共享整合分支交付」instead of internal acronyms. The map reaches `done` when the scope artifact, delivery tickets, native relationships, and any activated delivery-only planning have all been read back with their required approvals. Set its Frontier to the linked first executable delivery ticket, then return that ticket with the linked scope and ticket titles plus any execution-plan pointer. Leave workspace, agent, and commit-cycle policy to the execution workflow unless conditional planning already created a durable path.

$ARGUMENTS
