# Extraction and Classification Contract

## Candidate Schema and Extraction Rules (Required)

- Candidate fields: `source_ref`, `change`, `why`, `candidate_type`, `confidence`, `sot_fingerprint?`, `exclusion_reason?`, `unresolved_source_ref?`.
- If source pointer is unresolved, keep candidate as `draft` with `unresolved_source_ref`.
- Extraction thresholds:
  - timeline: phase status change, finalized decision line, or validated fix.
  - decision: clear conclusion plus rationale.
  - knowledge: reusable pattern plus at least one caveat or constraint.
- Skip criteria: tool chatter, placeholders, harvest self-logs, and format churn with no reusable value.

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

## Classification Decision Table

| Condition | Output | Required Fields | Default Status |
| --- | --- | --- | --- |
| Significant SOT update in current session/day | timeline event (`projects/<project>/timeline/YYYY-MM-DD.md`) | `when`, `change`, `why`, `source_ref`, `sot_fingerprint` | `draft` |
| Final technical decision with clear rationale | decision note (`decisions/*.md`) | `summary`, `conclusion`, `source_files`, `source_date`, `source_ref` | `confirmed` |
| Reusable validated pattern/fix/heuristic | knowledge note (`knowledge/*.md`) | `summary`, `insight`, `how_to_apply`, `source_files`, `source_date`, `source_ref` | `confirmed` |
| Missing or ambiguous source pointer | keep candidate in target note but mark unresolved | `unresolved_source_ref` | `draft` |

## Key-Update Snapshot (timeline)

Create or append timeline events when source-of-truth files change significantly.

Timeline event fields:

- `when`
- `change`
- `why`
- `source_ref`
- `sot_fingerprint`

If a same-day timeline file exists, append a new event block instead of creating a new file.

## Milestone Publish (formal notes)

Publish formal notes when one of these is true:

- a phase becomes `complete`
- a technical decision becomes final
- an issue resolution is validated and reusable

## Harvest Exclusion Markers

Support explicit exclusion markers inside source-of-truth files:

- `<!-- harvest:exclude:start -->`
- `<!-- harvest:exclude:end -->`

Ignore content inside this block during harvest publishing.
