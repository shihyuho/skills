# adr

Record and consult **Architecture Decision Records** — short Markdown notes in `docs/adr/` that capture *that* a hard-to-reverse decision was made and *why*.

Covers the full lifecycle:

- **Read first** — consult ADRs in an area before changing its code; don't re-litigate settled decisions, surface conflicts explicitly.
- **Whether to write one** — a three-gate test (hard to reverse, surprising without context, the result of a real trade-off). Most decisions don't qualify.
- **How to write one** — a minimal title-plus-a-paragraph format, sequential numbering, optional sections only when they pull their weight. See [references/format.md](skills/adr/references/format.md).
- **Maintaining** — supersede rather than rewrite; track `status` once decisions start getting revisited.

The aim is a decision log future engineers and agents can trust, without ADR ceremony for decisions that don't deserve it.
