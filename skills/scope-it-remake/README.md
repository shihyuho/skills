# scope-it-remake

Discuss scope, tickets, and delivery through a lightweight Delivery Map, then publish the confirmed bundle together.

This user-invoked prototype lives beside `scope-it`; it does not replace or migrate the existing workflow. `to-spec`, `to-tickets`, other compatible skills, and completed artifacts can supply planning content through capability-based contracts. Scope confirmation leads straight into ticket drafting, and ticket confirmation into delivery planning; tracker writes wait until the final publication approval. Drafts may stay in the conversation or temporary local files.

It remembers one shared pair of source preferences across repositories, accepts `--scope-source` or `--ticket-source` to replace those defaults, and asks when no compatible producer can be resolved. Repository guidance or the selected source defines the tracker. One top-level Delivery Map connects scope and tickets; execution plans remain separate from the ticket graph.

Scope and Delivery Map share one planning post: a new item's body or a combined comment on an existing item, reusing an existing planning post when present. A single Ticket gets its own comment on that item; multiple Tickets get separate child items with native containment and actual blocking links. Unsupported tracker capabilities require an agreed alternative. Existing external specs remain linked rather than copied.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it-remake -g
```
