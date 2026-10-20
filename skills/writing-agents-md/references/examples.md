# Writing Agents MD Routing Examples

Use these examples only when a rule sits between two routes. Adapt to the target host and repository evidence rather than copying their wording.

## Cheap Lookup vs Canonical Gotcha

Delete a command inventory copied from `package.json`:

```md
- `pnpm dev`
- `pnpm build`
- `pnpm test`
- `pnpm lint`
```

Keep a concise command when the obvious alternative gives false confidence:

```md
Run database tests with `pnpm test -- --runInBand`; the default parallel run intermittently misses transaction cleanup failures.
```

If validation has several branches, defer the protocol to a skill and keep a pointer naming when to use it.

## Purpose vs Directory Tour

Keep brief orientation when it changes interpretation:

```md
This repository contains the shared authentication library consumed by both legacy and current services.
```

Delete framework inventories and directory walkthroughs the agent can recover cheaply from the repository.

## Observable Conflict vs Human Policy

Suppose an existing file says production deploys require owner approval, but no repository check enforces it. Absence of enforcement is not evidence that the policy is stale: keep it and flag it for owner confirmation. A claimed command contradicted by current CI and package configuration is an implementation conflict to investigate and rewrite.
