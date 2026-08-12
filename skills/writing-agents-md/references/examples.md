# Writing Agents MD Routing Examples

Use these examples only when the routing interface leaves a real ambiguity. Adapt to the target host and repository evidence rather than copying their wording.

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

If validation has several branches, move the protocol to a skill and retain a pointer naming when to use it.

## Purpose vs Directory Tour

Keep brief orientation when it changes interpretation:

```md
This repository contains the shared authentication library consumed by both legacy and current services.
```

Delete framework inventories and directory walkthroughs the agent can recover cheaply from the repository.

## Root vs Nested Scope

A rule such as "use `make test-payments`" belongs in the instruction file nearest `services/payments/` when other services use different validation. It is standing subtree guidance, not a task-specific skill and not a root-wide default.

## Instruction vs Skill

Keep a trigger pointer in always-on context only when autonomous routing needs it:

```md
For releases, use the `release-checklist` skill; it owns versioning, verification, and publication steps.
```

Put the multi-step release procedure in the skill. Omit the pointer if the workflow is always explicitly invoked and agents do not need autonomous discovery.

## Guidance vs Enforcement

Move a mandatory formatter or generated-file check into CI or tooling. Keep a short instruction only when the safe path is not otherwise visible:

```md
Edit `schema/`, then run the checked-in generator; CI rejects direct edits under `generated/`.
```

## Observable Conflict vs Human Policy

Suppose an existing file says production deploys require owner approval, but no repository check enforces it. Absence of code is not evidence that the policy is stale. Preserve or flag it for owner confirmation. Conversely, a claimed command contradicted by current CI and package configuration is an implementation conflict to investigate and rewrite.

## Cross-Host Bridge

When `AGENTS.md` is the shared source and Claude Code needs the same guidance, keep `CLAUDE.md` as a bridge instead of duplicating content:

```md
@AGENTS.md
```

Add host-specific guidance below the import only when it cannot live in the shared file.
