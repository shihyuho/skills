# Quality Reports Contract

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

## Structured Mode Outputs (Phase-Gated)

- Enforcement: recommended until compatibility dry run passes; then raise to required.
- `status`: `{mode, passed, missing_files[], notes_count}` plus one-line summary.
- `audit`: `{mode, passed, issues:[{path, rule, severity}]}` plus brief findings.
- `review`: dimension scores, weighted total, evidence paths.
- `optimize`: input roots, included/skipped reports, aggregates, prioritized roadmap.
