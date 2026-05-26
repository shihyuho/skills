# ADR Format

ADRs live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Create the `docs/adr/` directory lazily — only when the first ADR is needed.

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one. Zero-pad to four digits. The slug is a short kebab-case summary of the decision (`0007-event-sourced-orders.md`).

## Template

```md
# {Short title of the decision}

{1–3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The point is to record *that* a decision was made and *why* — not to fill out sections. If you find yourself padding it to look "complete", stop: the reasoning is the deliverable.

## Optional sections

Include these only when they add genuine value. Most ADRs won't need any of them.

- **`status` frontmatter** — `proposed | accepted | deprecated | superseded by ADR-NNNN`. Useful once decisions in the repo start getting revisited; pointless before that.
- **Considered Options** — only when the rejected alternatives are worth remembering (e.g. someone will otherwise re-suggest them).
- **Consequences** — only when non-obvious downstream effects need to be called out.

## Examples

### Minimal — the common case

```md
# Manual SQL instead of an ORM

We write queries by hand against the `orders` schema rather than using an ORM.
The hot paths need index hints and window functions the ORM can't express cleanly,
and the team reads SQL fluently. The cost is more boilerplate for simple CRUD,
which we accept.
```

One paragraph. Reversing it is expensive (queries everywhere), it's surprising (most teams reach for an ORM), and it's a real trade-off (boilerplate vs. control). All three gates pass.

### With optional sections — when revisiting is likely

```md
---
status: accepted
---

# REST over GraphQL for the public API

We expose the public API as REST, not GraphQL.

## Considered Options

- **GraphQL** — flexible client queries, but our consumers are a small set of
  known partners on fixed contracts, so the flexibility buys little and the
  caching story is worse for our CDN-heavy traffic.
- **REST** — chosen. Maps cleanly to CDN caching and the partners already
  integrate against REST elsewhere.

## Consequences

Clients that later want field-level selection will have to over-fetch. Revisit
if a consumer's payload sizes become a real problem.
```

The `Considered Options` section earns its place because GraphQL is the obvious thing someone will re-suggest — recording why it was rejected stops that conversation from recurring.

### Superseding a decision

Leave the original ADR untouched and mark its status. Write a new ADR that explains what changed:

```md
---
status: superseded by ADR-0012
---

# ADR-0007: Event-sourced orders

(original content unchanged)
```

```md
# Projected orders into Postgres, dropping event sourcing

Supersedes ADR-0007. Projection lag grew past the 200ms read SLA as event
volume climbed, and the audit requirement that justified event sourcing is now
met by the append-only `order_audit` table. We keep a relational orders table
as the source of truth.
```
