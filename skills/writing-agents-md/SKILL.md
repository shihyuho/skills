---
name: writing-agents-md
description: Create, rewrite, prune, or review `AGENTS.md` and `CLAUDE.md` by routing standing guidance to the smallest correct scope and mechanism. Use for stale or conflicting instructions, nested or path-scoped rules, task-specific skill boundaries, or deterministic enforcement.
license: MIT
---

# writing-agents-md

Design a small instruction interface, not a repository handbook. First remove repetition and conflicts; then place each surviving rule at its smallest correct scope. Add strong constraints only for costly mistakes, durable policy, or capability gaps demonstrated by target-host evaluation.

## Workflow

1. **Bound the task.** Identify the target host, file, directory scope, and requested mode: `create`, `update`, `rewrite`, or `review`. A review stays read-only unless the user also asks for changes. Preserve output-only requests.
2. **Discover the active chain.** Locate applicable ancestor, target, override, nested, imported, and path-scoped instruction files before editing. Read [host-semantics.md](references/host-semantics.md) when host discovery or precedence affects the result.
3. **Establish authority.** Read the existing instruction file as a standing contract, then check repository code, config, CI, documentation, and recent evidence for drift. Observable implementation can disprove stale implementation claims; it does not automatically override human safety, release, compliance, or operational policy. Mark unresolved conflicts for owner confirmation.
4. **Route every candidate.** Use the routing interface below. When reviewing or revising an existing instruction chain, read [checklist.md](references/checklist.md) for a line-by-line audit.
5. **Rewrite only the selected destinations.** Edit only destinations authorized by the request; report recommended moves outside that scope and leave those files unchanged. Keep one source of truth, use concrete and verifiable wording, and preserve unrelated valid rules during an update. State the desired behavior positively; reserve prohibitions for real guardrails and pair them with the safe path.
6. **Verify completion.** Account for the full active chain, resolve or report conflicts, validate changed files, and explain moves or deletions unless the user requested only the resulting file.

## Routing Interface

For each rule, choose one action:

- **Keep** — Retain it here when it changes decisions across this file's scope and is concise, specific, verifiable, and stable enough to justify always-on load.
- **Narrow** — Move standing guidance to the nearest nested `AGENTS.md`, nested `CLAUDE.md`, or path-scoped rule when only a subtree or file class needs it.
- **Defer** — Move conditional, reference-heavy, or multi-step work to a skill or documentation. Leave a short pointer only when agents must know what material exists and the condition for loading it.
- **Enforce** — Put deterministic requirements in code, config, tests, CI, permissions, or hooks. Keep only the non-obvious rationale or fallback in instructions when it still changes decisions.
- **Delete** — Remove repetition, stale claims, generic defaults, behavioral no-ops, directory tours, and cheap one-file or one-command lookups.
- **Verify** — Preserve or clearly flag an unresolved rule when authority is uncertain, especially for safety, production, release, legal, or external-system constraints.

Discoverability is evidence, not an automatic deletion rule. A short canonical command or repository-purpose sentence may stay when it prevents repeated wrong choices or costly exploration. Move branched verification protocols to a skill instead of expanding always-on context.

## Writing Standard

- Spend most always-on tokens on gotchas, decision-changing conventions, and safe paths.
- Match the rule's scope to its loading scope; repository-wide does not mean globally applicable outside the repository, and subtree-wide does not mean task-specific.
- Prefer pointers that name both the material and its trigger over copied reference content.
- Treat examples as optional reference, not rules to imitate mechanically. Read [examples.md](references/examples.md) only when a routing decision remains ambiguous.
- Prefer a tiny file—or propose no file—when no standing instruction earns its load. When the user explicitly requested creation, explain that conclusion rather than silently skipping the deliverable.

For the rationale behind this interface and model-relative pruning, read [principles.md](references/principles.md).
