# scope-it-remake

Discuss scope, tickets, and delivery, confirm the complete Delivery Map and exact writes, then publish, read back, and finish.

This user-invoked prototype lives beside `scope-it`; it does not replace or migrate the existing workflow. `to-spec`, `to-tickets`, other compatible skills, and completed artifacts can supply planning content through capability-based contracts. Scope confirmation leads straight into ticket drafting, and ticket confirmation into delivery planning; tracker writes wait until the final publication approval. Drafts, approvals, and interrupted-publication evidence stay in the session or controlled temporary storage. Retries recover exact approved writes and read actual results before filling gaps.

It remembers one shared pair of source preferences across repositories, accepts `--scope-source` or `--ticket-source` to replace those defaults, and asks when no compatible producer can be resolved. Repository guidance or the selected source defines the tracker. One top-level Delivery Map connects scope and tickets; execution plans remain separate from the ticket graph.

Scope and Delivery Map share one planning post: a new item's body or a combined comment on an existing item, reusing an existing planning post when present. A single Ticket gets its own comment on that item; multiple Tickets get separate child items with native containment and actual blocking links. Unsupported tracker capabilities require an agreed alternative. Existing external specs remain linked rather than copied.

The published Map holds the agreed destination, artifact links, ticket graph and first executable ticket, delivery contracts, boundaries, and handoff. Discussion and publication statuses stay out of it. After verification the workflow ends; later discussion alone does not update the Map, while content amendments and exact repairs require approval.

Planning carries approved discussion artifacts through one delivery ticket, with exact cleanup and a durable baseline handoff when needed. Publication finishes after a fresh verification pass; it does not mean implementation has landed. Later delivery verification follows the saved baseline or shared-lane gates, and relationship fallbacks remain visibly degraded.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it-remake -g
```
