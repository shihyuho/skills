---
name: harvest
description: "Capture project memory from planning-with-files source-of-truth into Obsidian-compatible second-brain notes in docs/notes. Use for milestone summaries, decision capture, and timeline snapshots. Trigger on: harvest, /harvest, harvest this, save this to second brain, save what we just did, document this work, capture this knowledge."
license: MIT
metadata:
  author: shihyuho
  version: "2.1.0"
---

# Planning Second Brain

Create and maintain a project second brain without replacing source-of-truth planning files.

## Core Contract

- Soft-integrate external skills by invocation; never copy their instruction bodies.
- Treat `task_plan.md`, `findings.md`, and `progress.md` as the only source of truth (SOT).
- Write second-brain outputs into `docs/notes` using Obsidian-compatible Markdown.
- Never let `docs/notes` overwrite or redefine source-of-truth files.
- Route all entrypoints through one deterministic capture workflow.

## Required Skill Composition

1. Invoke `planning-with-files` first for primary planning workflow.
2. Invoke `obsidian-markdown` when writing or updating second-brain Markdown.

## Trigger Contract

Use this skill when users ask to:

- keep project memory over time
- summarize milestones into reusable notes
- record stable decisions and knowledge
- build an Obsidian-friendly project knowledge base

Do not use this skill for unrelated implementation work that does not involve capture, summarization, or project memory publishing.

## Output Locations

- `docs/notes/index.md`
- `docs/notes/projects.md`
- `docs/notes/decisions.md`
- `docs/notes/knowledge.md`
- `docs/notes/projects/<project>/timeline/YYYY-MM-DD.md`
- `docs/notes/decisions/*.md`
- `docs/notes/knowledge/*.md`

Create missing folders/files when absent.

## Deterministic Workflow (Required)

Run this workflow in order for every entrypoint (manual trigger phrases, slash-command wrappers, and plugin-driven invocation):

1. **Preflight**
   - Confirm SOT inputs exist: `task_plan.md`, `findings.md`, `progress.md`.
   - Confirm output root: `docs/notes`.
   - Set mode: `capture`, `status`, or `audit`.

2. **Bootstrap**
   - Ensure required minimal `docs/notes` files and templates exist.
   - Create missing files from `references/` without overwriting existing files.

3. **Extract Candidates**
   - Read SOT files using allowlist/denylist boundaries.
   - Apply exclusion markers.
   - Produce candidate entries with traceability fields.

4. **Classify**
   - Route each candidate to timeline snapshot, decision note, or knowledge note using the decision table.
   - If source pointer is unresolved, keep candidate as `draft`.

5. **Publish**
   - Append same-day timeline events.
   - Create or update decision/knowledge notes.
   - Apply dedupe and `sot_fingerprint` no-op rules.

6. **Verify and Report**
   - Run verification checklist.
   - For `status` mode: return compact state summary.
   - For `audit` mode: return pass/fail with concrete file paths.

## First-Run Bootstrap (Required)

If `docs/notes` is missing, or if any required minimal file is missing, bootstrap from `references/`.

Required minimal files:

- `docs/notes/index.md`
- `docs/notes/projects.md`
- `docs/notes/decisions.md`
- `docs/notes/knowledge.md`
- `docs/notes/projects/.templates/timeline-template.md`
- `docs/notes/decisions/.templates/decision-template.md`
- `docs/notes/knowledge/.templates/knowledge-template.md`

Bootstrap rules:

- Create missing directories first.
- Create missing files from `references` templates.
- Do not overwrite existing user files during bootstrap.
- Continue normal publish behavior after bootstrap.

## Publishing Strategy

### Classification Decision Table

| Condition | Output | Required Fields | Default Status |
| --- | --- | --- | --- |
| Significant SOT update in current session/day | timeline event (`projects/<project>/timeline/YYYY-MM-DD.md`) | `when`, `change`, `why`, `source_ref`, `sot_fingerprint` | `draft` |
| Final technical decision with clear rationale | decision note (`decisions/*.md`) | `summary`, `conclusion`, `source_files`, `source_date`, `source_ref` | `confirmed` |
| Reusable validated pattern/fix/heuristic | knowledge note (`knowledge/*.md`) | `summary`, `insight`, `how_to_apply`, `source_files`, `source_date`, `source_ref` | `confirmed` |
| Missing or ambiguous source pointer | keep candidate in target note but mark unresolved | `unresolved_source_ref` | `draft` |

### Key-Update Snapshot (timeline)

Create or append timeline events when source-of-truth files change significantly.

Timeline event fields:

- `when`
- `change`
- `why`
- `source_ref`
- `sot_fingerprint`

If a same-day timeline file exists, append a new event block instead of creating a new file.

### Milestone Publish (formal notes)

Publish formal notes when one of these is true:

- a phase becomes `complete`
- a technical decision becomes final
- an issue resolution is validated and reusable

## Execution Contract (Required)

- Treat trigger methods as entrypoints only (manual phrases, slash-command wrappers, plugin-driven calls).
- MUST route all entrypoints through the same deterministic workflow.
- Produce equivalent output for equivalent source input regardless of trigger method.
- Do not implement separate dedupe behavior per trigger entrypoint.
- Keep plugin-driven capture behavior contract-compatible with manual entrypoints.

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

## Dedupe and Fingerprint Contract (Required)

- Timeline events MUST include `sot_fingerprint`.
- Compute `sot_fingerprint` from normalized `source_ref + change + why`.
- Same timeline day + same `sot_fingerprint` means no-op (do not append duplicate block).
- Equivalent source input must produce equivalent no-op behavior across manual and plugin entrypoints.

## Note Rules

- Keep notes concise and reusable.
- Include traceability metadata in formal notes.
- Summarize; do not paste large verbatim source-of-truth sections.

Read templates before writing:

- [references/projects/.templates/timeline-template.md](references/projects/.templates/timeline-template.md)
- [references/decisions/.templates/decision-template.md](references/decisions/.templates/decision-template.md)
- [references/knowledge/.templates/knowledge-template.md](references/knowledge/.templates/knowledge-template.md)

## Verification Checklist

Before finalizing updates:

1. Every formal note has `source_files`, `source_date`, and `source_ref`.
2. Every timeline event has `source_ref` and `sot_fingerprint`.
3. `docs/notes/index.md` links to latest decisions and knowledge.
4. No reverse edits were made to `task_plan.md`, `findings.md`, `progress.md` by second-brain steps.
5. No large copied source-of-truth blocks appear in formal notes.

## Failure Handling

- If `source_ref` cannot be resolved, set note `status: draft` and record `unresolved_source_ref`.
- Do not block the source-of-truth workflow because of second-brain publish errors.

## Non-Goals

- Do not modify global IDE/user rule files.
- Do not add mandatory always-on conversation loops.
- Do not turn this skill into a general cross-skill memory engine.
- Do not collect or persist tool chatter as project knowledge.

## Anti-Patterns

- Copying external skill bodies into this skill.
- Treating second-brain notes as execution-state files.
- Creating parallel truth that conflicts with source-of-truth planning files.
- Defining trigger-specific behavior that diverges from the deterministic workflow.
