# Delivery Skills

This context names the durable artifacts that connect scoping with implementation across skills, sessions, and agents.

## Language

**Ticket Map**:
The parent comment that shows people, at a glance, how a plan's Tickets depend on each other, drawn from native relations, which stay authoritative.
_Avoid_: Delivery Map, duplicate spec, progress tracker

**Planning Carry**:
The landing obligation `scope-it` hands to `to-afk-agent`: approved scope-related repository content, its ownership evidence and landing target. How it lands, including its Carrier and branch, is the handoff's decision.
_Avoid_: Shared handoff contract, copied ticket pointers

**Planning Baseline**:
An immutable commit containing approved scope-related repository content at the start of a delivery branch; `to-afk-agent` calls it the Carry baseline.
_Avoid_: Handoff commit, orphan-file commit

**Baseline Pointer**:
The legacy or narrow worktree input comprising a delivery branch and the full Planning Baseline SHA.
_Avoid_: Conversation handoff, branch-only reference

**Scope-related Change**:
A whole-file change or independently applicable exact patch whose ownership is evidenced as part of the settled scope and may therefore enter Planning Carry.
_Avoid_: Dirty file, nearby change
