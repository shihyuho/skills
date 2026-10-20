---
name: writing-agents-md
description: Route each rule in `AGENTS.md` or `CLAUDE.md` to the smallest scope and mechanism where it applies. Use when creating, rewriting, pruning, or reviewing either file, adding even one rule to it, or deciding whether guidance belongs in a nested file, path-scoped rule, skill, or tooling.
license: MIT
---

# writing-agents-md

Route every rule in `AGENTS.md` and `CLAUDE.md` to the smallest scope and mechanism that still loads it where it applies. An always-on line is load paid on every task in its scope, so the file stays a small instruction interface rather than a repository handbook: a rule stays only where it changes what the agent does on every task there, and the rest is routed to a narrower file, a skill, tooling, or nowhere.

When `writing-for-agents` is available, it sets how each retained line is written; this skill decides where each line goes.

## Bound the request

Identify the target host, file, directory scope, and mode:

| Mode | What changes |
|---|---|
| `create` | A new file, or a reasoned proposal for none |
| `add` | One new rule, written at its routed destination; other rules that fail routing are reported, not changed |
| `update` | Every rule is routed; rules that survive routing keep their wording |
| `rewrite` | Every rule is routed, and the file is rewritten as a whole |
| `review` | Nothing unless the user also asks for changes; report routes and conflicts |

Edit only the destinations the request authorizes; recommend moves to other files and leave those files unchanged. An output-only request gets only the resulting file.

## Read the active chain

Before routing, find every instruction source that loads with the target: ancestor, override, nested, imported, and path-scoped files. Read [host-semantics.md](references/host-semantics.md) when the host's discovery or precedence decides where a rule lands.

Treat existing rules as a standing contract. Code, config, CI, and documentation can disprove an implementation claim, such as a renamed command or a moved directory. Human policy (safety, release, compliance, operations, external systems) stands until its owner retires it, whether or not the repository enforces it.

## Route each rule

Give each rule, existing or proposed, exactly one route:

- **Keep**: standing across this file's whole loading scope and changes what the agent does there: a gotcha, a decision-changing convention, a safe path, durable policy. Concise, specific, verifiable, and stable enough to justify always-on load. A user-level file loads in every repository, so repository rules belong in the repository.
- **Narrow**: standing, but only for a subtree or file class: the nearest nested `AGENTS.md` or `CLAUDE.md`, or a path-scoped rule.
- **Defer**: conditional, reference-heavy, or multi-step work: a skill or documentation. Leave a pointer naming the material and the condition for loading it when agents must find it on their own or the rule required the workflow.
- **Enforce**: deterministic requirements: code, config, tests, CI, permissions, or hooks. Keep the safe path or the non-obvious reason when the agent would otherwise meet it only as a failure.
- **Delete**: repetition, stale claims, defaults the target model already follows, directory tours, and one-file or one-command lookups.

A rule whose authority you cannot settle is kept and flagged for owner confirmation. A rule the user asks you to add carries owner authority: when it is too vague to act on, write the concrete behavior it most likely means and ask the user to confirm it, rather than dropping it.

A discoverable command or a one- or two-sentence repository purpose is kept when it prevents a repeated wrong choice or costly exploration; a verification protocol with branches is deferred to a skill. Read [examples.md](references/examples.md) when a rule sits between two routes.

Propose a new standing rule when repeated mistakes, review findings, a costly landmine, or durable policy reveal a behavior gap. Reserve strong constraints for costly mistakes, durable policy, and capability gaps that evaluation on the target host demonstrates. Write each rule as the target behavior; a prohibition stays only as a guardrail, paired with the safe path.

When no rule earns always-on load, propose no file or a tiny one, and say why when the user asked for one.

## Done when

- Every rule in the active chain that bears on the request has one route, backed by its authority (policy, configuration, implementation, or unsupported claim), the wrong default or costly mistake it prevents, and its currentness.
- Conflicts are resolved by scope and authority, or reported; unsettled policy stays visible for owner confirmation.
- Only authorized destinations changed, and changed files still load: imports resolve and path-scoped rules match their paths.
- The reply explains moves and deletions, unless the user asked only for the file.
