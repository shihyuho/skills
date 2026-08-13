# Delivery Skills

This context names the durable artifacts that connect scoping with implementation across skills, sessions, and agents.

## Language

**Planning Baseline**:
An immutable commit containing the scope-related documents settled before implementation and shared as the starting point for delivery work.
_Avoid_: Handoff commit, orphan-file commit

**Planning Owner Ticket**:
The single delivery ticket that owns the Planning Baseline when a scope produces more than one ticket.
_Avoid_: Suitable ticket, arbitrary ticket

**Baseline Pointer**:
A durable tracker reference that identifies a Planning Baseline by its owner ticket, branch, and full commit SHA.
_Avoid_: Conversation handoff, branch-only reference

**Scope-related Change**:
A whole-file change or independently applicable exact patch whose ownership is evidenced as part of the settled scope and may therefore enter its Planning Baseline.
_Avoid_: Dirty file, nearby change
