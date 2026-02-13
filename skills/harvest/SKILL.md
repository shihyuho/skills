---
name: harvest
description: "Capture project memory by combining planning-with-files (source-of-truth) with Obsidian-compatible second-brain notes in docs/notes. Use for milestone summaries and decision capture. Trigger on: harvest, /harvest, harvest this, harvest this conversation, save this to second brain, save what we just did, document this work, capture this knowledge."
license: MIT
metadata:
  author: shihyuho
  version: "2.0.0"
---

# Planning Second Brain

Create and maintain a project second brain without replacing source-of-truth planning files.

## Core Contract

- Soft-integrate external skills by invocation; do not copy their instruction bodies.
- Treat `task_plan.md`, `findings.md`, and `progress.md` as the only source of truth.
- Write second-brain outputs into `docs/notes` using Obsidian-compatible Markdown.
- Do not let `docs/notes` overwrite or redefine source-of-truth files.

## Required Skill Composition

1. Invoke `planning-with-files` first for primary planning workflow.
2. Invoke `obsidian-markdown` when writing or updating second-brain Markdown.

## When to Use

Use this skill when users ask to:

- keep project memory over time
- summarize milestones into reusable notes
- record stable decisions and knowledge
- build an Obsidian-friendly project knowledge base

## Output Locations

- `docs/notes/index.md`
- `docs/notes/projects.md`
- `docs/notes/decisions.md`
- `docs/notes/knowledge.md`
- `docs/notes/projects/<project>/timeline/YYYY-MM-DD.md`
- `docs/notes/decisions/*.md`
- `docs/notes/knowledge/*.md`

Create missing folders/files when absent.

## First-Run Bootstrap (Required)

If `docs/notes` is missing, or if any required minimal file is missing, bootstrap from `references/bootstrap/`.

Required minimal files:

- `docs/notes/index.md`
- `docs/notes/projects.md`
- `docs/notes/decisions.md`
- `docs/notes/knowledge.md`
- `docs/notes/projects/_template/timeline-template.md`
- `docs/notes/decisions/decision-template.md`
- `docs/notes/knowledge/knowledge-template.md`

Bootstrap rules:

- Create missing directories first.
- Create missing files from `references/bootstrap` templates.
- Do not overwrite existing user files during bootstrap.
- Continue normal publish behavior after bootstrap.

## Publishing Strategy

### Milestone Publish (formal notes)

Publish formal notes when one of these is true:

- a phase becomes `complete`
- a technical decision becomes final
- an issue resolution is validated and reusable

### Key-Update Snapshot (anti-drift)

When source-of-truth files change significantly, append a timeline event with:

- `when`
- `change`
- `why`
- `source_ref`

If a same-day timeline file exists, append a new block instead of creating a new file.

## Execution Contract (Required)

- Treat trigger methods as entrypoints only (`harvest`, `/harvest`, `/harvest-capture`, plugin-driven calls).
- MUST route all entrypoints through the same capture contract.
- Produce equivalent output for equivalent source input regardless of trigger method.
- Do not implement separate dedupe behavior per trigger entrypoint.

## Source Extraction Boundaries (Required)

Extract with allowlist rules from source-of-truth files. Do not summarize everything.

Allowlist (preferred extraction targets):

- finalized decisions
- validated resolutions
- completed phase outcomes
- reusable technical findings
- stable references that aid future execution

Denylist (always exclude):

- harvest operation traces, bootstrap logs, and tool chatter
- progress noise without reusable value
- placeholders or scaffolding text (for example `<...>`, empty bullets, TODO placeholders)
- unresolved draft fragments with no actionable conclusion

## Harvest Exclusion Markers

Support explicit exclusion markers inside source-of-truth files:

- `<!-- harvest:exclude:start -->`
- `<!-- harvest:exclude:end -->`

Ignore content inside this block during harvest publishing.

## Anti-Recursion Guard

- Do not summarize notes under `docs/notes` back into new notes.
- Use source-of-truth files as input only (`task_plan.md`, `findings.md`, `progress.md`).
- Skip entries that only describe harvest's own publishing activity.

## Note Rules

- Keep notes concise and reusable.
- Include traceability metadata in formal notes.
- Summarize; do not paste large verbatim source-of-truth sections.

Read templates before writing:

- [references/bootstrap/projects/_template/timeline-template.md](references/bootstrap/projects/_template/timeline-template.md)
- [references/bootstrap/decisions/decision-template.md](references/bootstrap/decisions/decision-template.md)
- [references/bootstrap/knowledge/knowledge-template.md](references/bootstrap/knowledge/knowledge-template.md)

## Verification Checklist

Before finalizing updates:

1. Every formal note has `source_files` and `source_date`.
2. `docs/notes/index.md` links to latest decisions and knowledge.
3. No reverse edits were made to `task_plan.md`, `findings.md`, `progress.md` by second-brain steps.
4. No large copied source-of-truth blocks appear in formal notes.

## Failure Handling

- If `source_ref` cannot be resolved, set note `status: draft` and record `unresolved_source_ref`.
- Do not block the source-of-truth workflow because of second-brain publish errors.

## Anti-Patterns

- Copying external skill bodies into this skill.
- Treating second-brain notes as execution-state files.
- Creating parallel truth that conflicts with source-of-truth planning files.
