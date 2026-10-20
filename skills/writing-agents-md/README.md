# writing-agents-md

Create, update, prune, or review `AGENTS.md` and `CLAUDE.md` by routing each standing rule to the smallest scope and mechanism where it still applies. Unlike a `/init`-style handbook that piles every command, directory and convention into the root file, it treats each always-on line as load paid on every task in that scope: a rule stays only where it changes what the agent does there, and the rest goes to a nested file, a path-scoped rule, a skill, tooling, or nowhere.

## When to use

- A generated or long-lived root file has grown into a handbook: a directory tour, copied package scripts, rules only one package needs.
- You are adding a rule and it could live at the root, in a nested file, in a skill, or in CI.
- A repository needs its first `AGENTS.md` or `CLAUDE.md`, or Claude Code support for an existing `AGENTS.md`.
- You want a read-only review of every instruction that loads for one directory.

The agent uses it on its own when it creates, edits, or reviews `AGENTS.md` or `CLAUDE.md`, including adding a single rule mid-task; you can also invoke it directly. To sharpen the wording of lines that stay rather than decide where they go, use `writing-for-agents` from [mattpocock/skills](https://github.com/mattpocock/skills), because this skill only decides placement.

## Getting started

```text
Rewrite the root AGENTS.md and tell me where the displaced guidance belongs.
```

### Options

| Ask | What you get |
|---|---|
| "Rewrite `AGENTS.md`" | Every rule routed, with moves and deletions explained |
| "Add this rule to `CLAUDE.md`: …" | That rule placed at its scope; the rest of the file untouched |
| "Review the instructions for `services/billing/`" | A report of routes and conflicts across the whole chain, no edits |
| "Return only the updated `AGENTS.md`" | The resulting file and nothing else |
| "Create a `CLAUDE.md`" | A small file, or the reason none is needed |

## The five routes

Every rule, existing or proposed, gets exactly one route:

| Route | Where it goes | Typical rule |
|---|---|---|
| Keep | This file | A gotcha, a canonical command the obvious alternative gets wrong, durable policy |
| Narrow | A nested `AGENTS.md` or `CLAUDE.md`, or a path-scoped rule | A test command valid in one service only |
| Defer | A skill or a doc, with a pointer when agents must find it unaided or the rule required the workflow | A multi-step release checklist |
| Enforce | Code, config, tests, CI, permissions, or hooks, keeping the safe path the agent would otherwise learn from a failure | "Never hand-edit generated files" when CI can reject it |
| Delete | Nowhere | A directory tour, a copied script list, a default the model already follows |

A rule whose authority cannot be settled, such as a deploy approval no repository check enforces, is kept and flagged for its owner rather than deleted.

## It's working if

- The root file gets shorter while the commands and warnings that have actually bitten someone stay.
- Every line that leaves the root has a stated destination or a reason it can go.
- A rule only one package needs lands in that package's nested file or path-scoped rule.
- A production or release policy the repository cannot verify is still there, marked for owner confirmation.
- After a review-only request, `git status` shows no changes.

## Common questions

**Why keep a command the agent could find in `package.json`?**
Because finding it is not the same as choosing it. When the obvious command validates the wrong thing, as a root `pnpm test` that only covers one package of a monorepo does, the canonical one stays. A cheap lookup that nobody gets wrong still goes.

**Why not move everything out of the root into skills?**
A skill loads only when its task comes up, so it suits conditional, multi-step work. A rule every task in a directory must follow is standing guidance: it belongs in that directory's nested file or a path-scoped rule, where it loads automatically.

## Limitations

- It decides placement and pruning; wording quality comes from the model, or from `writing-for-agents` when installed.
- Host knowledge covers Codex, Claude Code, and the portable `AGENTS.md` convention; other hosts need their own documentation checked.
- It recommends moving a requirement into CI, hooks, or tests, and edits those files only when the request covers them.
