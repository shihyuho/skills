# Scope-it publishes Ticket Maps and leaves landing to the handoff

This decision supersedes ADR 0004 as the current `scope-it` runtime contract. Decided in [shihyuho/skills#44](https://github.com/shihyuho/skills/issues/44).

## Context

- `to-afk-agent` now settles a delivery mode (`integration` or `independent`) that selects the Carrier and the dispatch target. A coordinator that settles the mode upstream has to track every delivery decision the handoff adds later.
- The Delivery Map served two readers at once: a human overview and a machine handoff record (Carrier, SHAs, positions for the handoff to fill). On a phone, the published Map was hard to read.
- Agents already read native relations, and no workflow parses the Map.

## Decision

- `scope-it` owns content and landing obligations: which files or patches must land, their ownership evidence, repository and landing target. `to-afk-agent` owns how the work lands: delivery mode, Carrier, branches, preservation, Carry records, readiness and dispatch.
- `scope-it` settles no delivery mode and drafts no handoff record. It passes decisions already settled in the planning conversation, and existing bindings, as given.
- The Delivery Map becomes the Ticket Map: a human-only parent comment showing how two or more Tickets depend on each other, in the smallest view that makes the shape clear. `scope-it` publishes it itself after Tickets and before the handoff; it carries no Carry, SHAs, mode or branches. One Ticket gets no Map.
- Agreed delivery duties such as aggregate verification or parent closure belong in Ticket acceptance.

## Consequences

`to-afk-agent` changes no longer require `scope-it` changes, and the handoff's dispatch stays its final write. Carry details now appear only in the handoff's own Issue comments, whose format `to-afk-agent` owns. Existing `scope-it:delivery-map` Maps stay unchanged until an approved amendment rewrites them.
