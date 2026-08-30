# Scope-it coordinates portable Delivery Maps

This decision supersedes ADR 0002 and ADR 0003 as the current `scope-it` runtime contract. The interactive `scope-it-remake` design graduates under the canonical `scope-it` name; the prior fixed-source, single-approval workflow is retired.

## Decision

- Selected scope and ticket skills own their content, reviews, publication, metadata, and phase-specific confirmations.
- `scope-it` coordinates their order, approved placement, native relation readback, and one canonical Delivery Map on the parent.
- The Map projects verified Ticket blockers and landing paths, embeds the next-Ticket selection protocol, and remains usable without the planning skill or chat.
- Planning Carry records one compact pointer to approved repository content and its Carrier Ticket's actual delivery path. Repository and executor workflows own Git, CI, implementation, and landing mechanics.
- New Maps and saved preferences use the `scope-it` identity. Existing `scope-it-remake` markers and preference files remain readable and migrate only through approved writes.

## Consequences

Scope and Tickets may become visible before the Map because each producer keeps its own publication gate. Planning finishes after the Map and approved planning writes are read back; implementation starts separately by following the Map against fresh tracker state. Native tracker relations remain authoritative, and neither Ticket bodies nor the Map duplicate source artifacts.
