# Harvest - Durable Project Memory

Keep planning files as source-of-truth and publish reusable project knowledge into `docs/notes`.

`harvest` is for teams who want AI-generated memory that stays auditable, concise, and Obsidian-friendly.

## Problem It Solves

Long sessions lose critical context:

- final decisions are buried in chat logs
- validated fixes are mixed with execution noise
- future contributors cannot recover the "why"

`harvest` captures only reusable, traceable outcomes.

## What You Get

When the skill triggers, the agent:

1. treats `task_plan.md`, `findings.md`, and `progress.md` as source-of-truth
2. bootstraps missing `docs/notes` files from templates without overwriting existing user files
3. routes updates through one deterministic workflow
4. publishes timeline snapshots, decision notes, and knowledge notes with traceability metadata
5. applies dedupe rules (`sot_fingerprint`) and skips recursive/noisy content

## Trigger Phrases

- `harvest`
- `/harvest`
- `/harvest-capture`
- `/harvest-review`
- `/harvest-optimize`
- `harvest this`
- `save this to second brain`
- `save what we just did`
- `document this work`
- `capture this knowledge`

## Input and Output Model

Source-of-truth inputs:

- `task_plan.md`
- `findings.md`
- `progress.md`

Published outputs:

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

## Capture Behavior

`harvest` uses one execution path across manual commands and plugin automation:

1. preflight and bootstrap
2. candidate extraction from source-of-truth files
3. classification (timeline vs decision vs knowledge)
4. publish with dedupe
5. verification and compact report

For `review` mode, `harvest` writes one reusable quality report file so teams can aggregate cross-repo quality trends.

For `optimize` mode, `harvest` aggregates multiple review reports into one monthly optimization roadmap.

`optimize` mode can use default local review reports and optional additional report directories provided by the user.

For timeline events, the agent records:

- `when`
- `change`
- `why`
- `source_ref`
- `sot_fingerprint`

Same-day + same fingerprint becomes no-op.

## Minimal Example

Input change in `progress.md`:

```markdown
## Cache rollout
- Updated API cache TTL from 60s to 120s to reduce miss spikes.
```

`harvest` publishes one timeline event:

```markdown
## 14:30 - Cache TTL update
- when: 2026-02-18 14:30
- change: Increased API cache TTL from 60s to 120s.
- why: Reduce miss spikes under peak traffic.
- source_ref: `progress.md#Cache rollout`
- sot_fingerprint: `3f3f...`
```

If the same `source_ref + change + why` appears again on the same day, `harvest` performs no-op and does not append a duplicate block.

## Safety Boundaries

`harvest` excludes:

- tool chatter and operation traces
- placeholder scaffolding
- unresolved fragments without actionable conclusions
- recursive summarization of `docs/notes`

You can force exclusion inside source-of-truth files with:

- `<!-- harvest:exclude:start -->`
- `<!-- harvest:exclude:end -->`

## Commands

- `commands/harvest.md`
- `commands/harvest-start.md`
- `commands/harvest-capture.md`
- `commands/harvest-status.md`
- `commands/harvest-audit.md`
- `commands/harvest-review.md`
- `commands/harvest-optimize.md`

These commands are entrypoints only. `SKILL.md` remains the single source of truth for behavior.

## Optional Plugin Automation

You can enable auto-capture with `.opencode/plugins/harvest.js`.

Recommended sequence:

1. run one manual `harvest` (or `/harvest-start`) to initialize structure
2. enable plugin auto-capture for day-to-day SOT changes

Reference: `../../.opencode/INSTALL.md`

## Related Files

- [SKILL.md](SKILL.md)
- [references/index.md](references/index.md)
- [references/projects/.templates/timeline-template.md](references/projects/.templates/timeline-template.md)
- [references/decisions/.templates/decision-template.md](references/decisions/.templates/decision-template.md)
- [references/knowledge/.templates/knowledge-template.md](references/knowledge/.templates/knowledge-template.md)
- [references/harvest-quality/.templates/review-template.md](references/harvest-quality/.templates/review-template.md)
- [references/harvest-quality/.templates/rollup-template.md](references/harvest-quality/.templates/rollup-template.md)

## License

MIT
