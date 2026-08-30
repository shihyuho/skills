# Delivery Skills

This context names the durable artifacts that connect scoping with implementation across skills, sessions, and agents.

## Language

**Delivery Map**:
The canonical parent artifact that connects published Scope and Tickets to native relations, landing paths, optional Planning Carry, and the protocol for selecting the next live Ticket.
_Avoid_: Duplicate spec, progress tracker

**Planning Baseline**:
An immutable commit containing approved scope-related repository content at the start of its Carrier Ticket's delivery path.
_Avoid_: Handoff commit, orphan-file commit

**Planning Carry**:
The compact Delivery Map pointer that records approved scope-related content, its Carrier Ticket, linked branch, base and baseline SHAs, landing target, access, and delivery obligation.
_Avoid_: Shared handoff contract, copied ticket pointers

**Carrier Ticket**:
The delivery ticket whose recorded final path transports Planning Carry; this ownership creates no blocker relationship.
_Avoid_: Planning-only ticket, arbitrary owner

**Baseline Pointer**:
The legacy or narrow worktree input comprising the branch and full baseline SHA extracted from Planning Carry.
_Avoid_: Conversation handoff, branch-only reference

**Scope-related Change**:
A whole-file change or independently applicable exact patch whose ownership is evidenced as part of the settled scope and may therefore enter Planning Carry.
_Avoid_: Dirty file, nearby change
