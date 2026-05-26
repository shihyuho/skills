---
name: adr
description: Record and consult Architecture Decision Records (ADRs) — short Markdown notes in `docs/adr/` capturing *that* a hard-to-reverse decision was made and *why*. Use whenever a real architectural trade-off is being made or has just been settled (tech choice with lock-in, context boundaries, integration patterns, a deliberate deviation from the obvious path, a constraint invisible in the code), when a decision is being reversed or superseded, when the user mentions ADR / architecture decision record / decision log, or before changing code in an area so you read and respect prior decisions rather than re-litigating them. Trigger even when the user doesn't say "ADR" but describes locking in a decision they'll want future engineers to understand.
license: MIT
---

# ADR — Architecture Decision Records

An ADR records *that* a decision was made and *why*, so a future reader (human or agent) doesn't undo it by accident or burn a week rediscovering the reasoning. It is **not** a spec, a design doc, or a task list. The value is in the reasoning, not in filling out sections.

This skill covers the full lifecycle: deciding **whether** a decision deserves an ADR, **writing** it, **reading** existing ones before you touch code, and **maintaining** them as decisions get revisited.

## Where ADRs live

- Default: `docs/adr/` at the repo root.
- Multi-context repos (e.g. a monorepo with separate bounded contexts) may also keep context-scoped decisions in `src/<context>/docs/adr/`. Root `docs/adr/` holds system-wide decisions; per-context dirs hold local ones.
- Create the directory **lazily** — only when the first ADR is actually needed. Don't scaffold empty folders.

## Before you change code: read first

When you're about to work in an area, read the ADRs that touch it before writing anything. They tell you which decisions are settled. Two rules follow:

1. **Don't re-litigate.** If an ADR already settled something, build on it — don't re-propose the alternative it rejected.
2. **Surface conflicts, don't silently override.** If your plan contradicts an existing ADR, say so explicitly and let the human decide:

   > _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because the projection lag now breaks the 200ms SLA._

   Only raise it when the friction is real enough to justify reopening the decision. Don't list every theoretical change an ADR forbids.

## Whether to write one: all three must be true

Most decisions don't need an ADR. Write one only when **all three** hold:

1. **Hard to reverse** — changing your mind later carries real cost. (Easy to reverse? Skip it — you'll just reverse it.)
2. **Surprising without context** — a future reader looks at the code and asks "why on earth did they do it this way?" (Not surprising? Nobody will wonder.)
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons. (No real alternative? There's nothing to record beyond "we did the obvious thing.")

### What qualifies

- **Architectural shape** — "monorepo", "write model is event-sourced, read model projected into Postgres".
- **Integration patterns between contexts** — "Ordering and Billing talk via domain events, not synchronous HTTP".
- **Technology choices that carry lock-in** — database, message bus, auth provider, deployment target. Not every library — only the ones that'd take a quarter to swap.
- **Boundary and scope decisions** — "Customer data is owned by the Customer context; others reference it by ID only". The explicit *no*s are as valuable as the *yes*es.
- **Deliberate deviations from the obvious path** — "manual SQL instead of an ORM because X". Anything where a reasonable reader would assume the opposite — this stops the next engineer from "fixing" something that was intentional.
- **Constraints not visible in the code** — "can't use AWS due to compliance", "responses must be under 200ms per the partner contract".
- **Rejected alternatives where the rejection is non-obvious** — picked REST over GraphQL for subtle reasons? Record it, or someone re-suggests GraphQL in six months.

## How to write one

Keep it to the minimum that carries the reasoning. The template, numbering rules, optional sections, and worked examples live in [references/format.md](references/format.md) — read it when you're about to create or revise an ADR.

The short version: a title line plus 1–3 sentences (context, decision, why) is a complete ADR. Add optional sections only when they pull their weight.

## Maintaining ADRs

Decisions get revisited. Rather than editing history into something that never happened, record the change:

- **Don't delete or rewrite** a superseded ADR. Leave it; it's the record of what was once true and why.
- **Supersede** by writing a new ADR and marking the old one `superseded by ADR-NNNN` (a `status` frontmatter field — see format reference). The new one should say what changed and why the original reasoning no longer holds.
- A `status` of `proposed | accepted | deprecated | superseded` is only worth adding once decisions in the repo actually start getting revisited. Don't add ceremony before it earns its keep.
