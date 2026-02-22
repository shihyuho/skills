# Publishing and Dedupe Contract

## Publish Confirmation Semantics (Required)

1. Extract candidate.
2. Validate schema fields and thresholds.
3. Publish into target note.
4. Mark committed after publish succeeds.

## First-Run Bootstrap (Required)

If `docs/notes` is missing, or if any required minimal file is missing, bootstrap from `references/bootstrap/`.

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
- Create missing files from `references/bootstrap` templates.
- Do not overwrite existing user files during bootstrap.
- Continue normal publish behavior after bootstrap.

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
