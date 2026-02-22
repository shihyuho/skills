---
name: harvest
description: "Capture project memory from planning-with-files source-of-truth into Obsidian-compatible second-brain notes in docs/notes. Use for milestone summaries, decision capture, and timeline snapshots. Trigger on: harvest, /harvest, harvest this, save this to second brain, save what we just did, document this work, capture this knowledge."
license: MIT
metadata:
  author: shihyuho
  version: "2.4.0"
---

# Planning Second Brain

Create and maintain a project second brain without replacing source-of-truth planning files.

## Core Contract

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
- read intents: find prior decision, look up past context, trace project timeline, retrieve existing second-brain note

Do not use this skill for unrelated implementation work that does not involve capture, summarization, or project memory publishing.

## Output Locations

- `docs/notes/index.md`
- `docs/notes/projects.md`
- `docs/notes/decisions.md`
- `docs/notes/knowledge.md`
- `docs/notes/harvest-quality.md`
- `docs/notes/projects/<project>/timeline/YYYY-MM-DD.md`
- `docs/notes/decisions/*.md`
- `docs/notes/knowledge/*.md`
- `docs/notes/harvest-quality/YYYY-MM-DD-<project-slug>-harvest-review.md`
- `docs/notes/harvest-quality/rollups/YYYY-MM-<project-slug>-harvest-optimization.md`

Create missing folders/files when absent.

## Progressive Disclosure Read Workflow (Required)

Follow this read order before any retrieval or context lookup:

1. Read `docs/notes/index.md` to discover available hubs.
2. Read the intent hub: `docs/notes/projects.md`, `docs/notes/decisions.md`, or `docs/notes/knowledge.md`.
3. Read only targeted leaf notes that match the intent.

Stop condition:

- Stop when the target note is found, or after two consecutive reads that add no novel information.

Hard constraints:

- Never start from deep leaves unless the user provides an exact path.
- Treat `docs/notes` as retrieval-only; never capture or summarize `docs/notes` back into `docs/notes`.
- Preserve the anti-recursion guard and existing SOT-only contract (`task_plan.md`, `findings.md`, `progress.md`).
- Do not expand read scope beyond the minimal files needed for the requested intent.

Reference example:

- [references/progressive-disclosure-read-example.md](references/progressive-disclosure-read-example.md)

## Deterministic Workflow (Required)

Run this workflow in order for every entrypoint (manual trigger phrases, slash-command wrappers, and plugin-driven invocation):

1. **Preflight**
   - Confirm SOT inputs exist: `task_plan.md`, `findings.md`, `progress.md`.
   - Confirm output root: `docs/notes`.
   - Set mode: `capture`, `status`, `audit`, `review`, or `optimize`.
   - For `optimize` mode, collect optional user-provided report directories as additional input roots.

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
   - For `review` mode: write one quality report file in `docs/notes/harvest-quality/`.
   - For `optimize` mode: write one rollup roadmap file in `docs/notes/harvest-quality/rollups/`.

## Candidate Schema and Extraction Rules (Required)

- Candidate fields: `source_ref`, `change`, `why`, `candidate_type`, `confidence`, `sot_fingerprint?`, `exclusion_reason?`, `unresolved_source_ref?`.
- If source pointer is unresolved, keep candidate as `draft` with `unresolved_source_ref`.
- Extraction thresholds:
  - timeline: phase status change, finalized decision line, or validated fix.
  - decision: clear conclusion plus rationale.
  - knowledge: reusable pattern plus at least one caveat or constraint.
- Skip criteria: tool chatter, placeholders, harvest self-logs, and format churn with no reusable value.

## Publish Confirmation Semantics (Required)

1. Extract candidate.
2. Validate schema fields and thresholds.
3. Publish into target note.
4. Mark committed after publish succeeds.

## First-Run Bootstrap (Required)

If `docs/notes` is missing, or if any required minimal file is missing, bootstrap from `references/`.

Required minimal files:

- `docs/notes/index.md`
- `docs/notes/projects.md`
- `docs/notes/decisions.md`
- `docs/notes/knowledge.md`
- `docs/notes/harvest-quality.md`
- `docs/notes/projects/.templates/timeline-template.md`
- `docs/notes/decisions/.templates/decision-template.md`
- `docs/notes/knowledge/.templates/knowledge-template.md`
- `docs/notes/harvest-quality/.templates/review-template.md`
- `docs/notes/harvest-quality/.templates/rollup-template.md`

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

## Review Report Mode (Required)

Use `review` mode to evaluate harvest output quality and persist one reusable report for later optimization planning.

Report output contract:

- Path: `docs/notes/harvest-quality/YYYY-MM-DD-<project-slug>-harvest-review.md`
- Create `docs/notes/harvest-quality/` if missing.
- Use `docs/notes/harvest-quality/.templates/review-template.md` when creating a new report.
- If report for same date and project exists, append a new `## Review Iteration` section instead of overwriting.

Review scope (repo-agnostic):

- structure completeness (`docs/notes` required hubs/templates present)
- traceability quality (`source_files`, `source_date`, `source_ref`, `sot_fingerprint`)
- extraction quality (allowlist coverage, denylist leakage)
- classification quality (timeline vs decisions vs knowledge routing)
- dedupe behavior (`same day + same fingerprint` no-op integrity)

Required report sections:

- `## Snapshot`
- `## Scorecard`
- `## Findings`
- `## Improvement Suggestions`
- `## Evidence`

Scoring rules:

- Score each dimension from 0 to 5.
- Provide weighted total out of 100.
- Default weights: structure 20, traceability 25, extraction 20, classification 20, dedupe 15.
- Keep scoring deterministic; tie every deduction to concrete evidence path.

## Review Rollup Mode (Required)

Use `optimize` mode to aggregate multiple review reports into one optimization roadmap.

Rollup input contract:

- Read reports from `docs/notes/harvest-quality/YYYY-MM-DD-<project-slug>-harvest-review.md`.
- Include only reports with explicit scorecard values and evidence paths.
- Default window: current calendar month (`YYYY-MM`).

External input roots contract:

- Default root is `docs/notes/harvest-quality/`.
- Accept zero or more additional report directories from user input.
- Accept absolute and relative paths.
- Resolve relative paths from current workspace root.
- Search each input root recursively for `*-harvest-review.md` only.
- Exclude rollup files (`*-harvest-optimization.md`) and non-review notes.
- Dedupe by normalized absolute file path.
- Sort report paths lexicographically before aggregation for deterministic output.
- If an input root is missing or unreadable, skip it and record reason in rollup report.

Rollup output contract:

- Path: `docs/notes/harvest-quality/rollups/YYYY-MM-<project-slug>-harvest-optimization.md`
- Create `docs/notes/harvest-quality/rollups/` if missing.
- Use `docs/notes/harvest-quality/.templates/rollup-template.md` when creating a new rollup file.
- If the same month rollup exists, append a new `## Rollup Iteration` section instead of overwriting.

Required rollup sections:

- `## Snapshot`
- `## Source Roots`
- `## Aggregated Score Trends`
- `## Repeated Gaps`
- `## Prioritized Roadmap`
- `## Evidence`

Aggregation rules:

- Report coverage: include report count, skipped report count, and skip reasons.
- Dimension score: arithmetic mean (0-5) across included reports per dimension.
- Total score: arithmetic mean of included report totals (0-100).
- Prioritization: sort roadmap items by `impact desc`, then `effort asc`.
- For empty input after filtering, still write rollup file with `status: draft` and explicit `no-report-input` reason.

## Execution Contract (Required)

- Treat trigger methods as entrypoints only (manual phrases, slash-command wrappers, plugin-driven calls).
- MUST route all entrypoints through the same deterministic workflow.
- Produce equivalent output for equivalent source input regardless of trigger method.
- Do not implement separate dedupe behavior per trigger entrypoint.
- Keep plugin-driven capture behavior contract-compatible with manual entrypoints.
- Keep `review` mode repo-agnostic. Do not hardcode project-specific heuristics as universal rules.
- Keep `optimize` mode repo-agnostic. Do not hardcode project-specific heuristics as universal rules.

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

Fingerprint normalization:

1. Trim leading/trailing whitespace on `source_ref`, `change`, and `why`.
2. Collapse internal whitespace to single spaces.
3. Lowercase each part.
4. Join as `<source_ref>||<change>||<why>`.
5. Compute SHA-256 hex lowercase.

Example:

- source_ref: `progress.md#Cache rollout`
- change: `Increased API cache TTL from 60s to 120s.`
- why: `Reduce miss spikes under peak traffic.`
- normalized string: `progress.md#cache rollout||increased api cache ttl from 60s to 120s.||reduce miss spikes under peak traffic.`
- `sot_fingerprint`: `5f8b8cfa8b6fdc9f2d5e3c7f92f02c6aa4f4b2b4cb0d2d8e3f50f0f5d7d6e4a3`

## Note Rules

- Keep notes concise and reusable.
- Include traceability metadata in formal notes.
- Summarize; do not paste large verbatim source-of-truth sections.

Read templates before writing:

- [references/projects/.templates/timeline-template.md](references/projects/.templates/timeline-template.md)
- [references/decisions/.templates/decision-template.md](references/decisions/.templates/decision-template.md)
- [references/knowledge/.templates/knowledge-template.md](references/knowledge/.templates/knowledge-template.md)
- [references/harvest-quality/.templates/review-template.md](references/harvest-quality/.templates/review-template.md)
- [references/harvest-quality/.templates/rollup-template.md](references/harvest-quality/.templates/rollup-template.md)

## Verification Checklist

Before finalizing updates:

1. Every formal note has `source_files`, `source_date`, and `source_ref`.
2. Every timeline event has `source_ref` and `sot_fingerprint`.
3. `docs/notes/index.md` links to latest decisions and knowledge.
4. No reverse edits were made to `task_plan.md`, `findings.md`, `progress.md` by second-brain steps.
5. No large copied source-of-truth blocks appear in formal notes.
6. In `review` mode, report file includes scorecard, deductions, and path-based evidence.
7. In `optimize` mode, rollup file includes coverage counts, aggregated scores, roadmap priority, and source report paths.
8. In `optimize` mode, rollup file includes input root resolution results (included + skipped + reasons).

## Structured Mode Outputs (Phase-Gated)

- Enforcement: recommended until compatibility dry run passes; then raise to required.
- `status`: `{mode, passed, missing_files[], notes_count}` plus one-line summary.
- `audit`: `{mode, passed, issues:[{path, rule, severity}]}` plus brief findings.
- `review`: dimension scores, weighted total, evidence paths.
- `optimize`: input roots, included/skipped reports, aggregates, prioritized roadmap.

## Failure Handling

- If `source_ref` cannot be resolved, set note `status: draft` and record `unresolved_source_ref`.
- Do not block the source-of-truth workflow because of second-brain publish errors.

## Non-Goals

- Do not modify global IDE/user rule files.
- Do not add mandatory always-on conversation loops.
- Do not turn this skill into a general cross-skill memory engine.
- Do not collect or persist tool chatter as project knowledge.

## Anti-Patterns

- Treating second-brain notes as execution-state files.
- Creating parallel truth that conflicts with source-of-truth planning files.
- Defining trigger-specific behavior that diverges from the deterministic workflow.
