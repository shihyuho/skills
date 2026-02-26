---
title: Harvest Quality Review
type: harvest-quality-review
status: draft
tags:
  - harvest-quality
  - project/<project-slug>
summary: "Quality evaluation report for harvest outputs."
source_files:
  - "../../task_plan.md"
  - "../../findings.md"
  - "../../progress.md"
  - "../index.md"
source_date: 2026-02-19
review_scope:
  mode: review
  dimensions:
    - structure
    - traceability
    - extraction
    - classification
    - dedupe
---

# Harvest Quality Review - <project-slug>

## Snapshot

- reviewed_at: 2026-02-19 22:00
- project_slug: <project-slug>
- notes_root: `docs/notes`
- report_mode: `review`

## Scorecard

| Dimension | Weight | Score (0-5) | Weighted Points | Evidence |
| --- | --- | --- | --- | --- |
| Structure completeness | 20 | 0 | 0 | `docs/notes/...` |
| Traceability quality | 25 | 0 | 0 | `docs/notes/...` |
| Extraction quality | 20 | 0 | 0 | `task_plan.md`, `findings.md`, `progress.md` |
| Classification quality | 20 | 0 | 0 | `docs/notes/projects`, `docs/notes/decisions`, `docs/notes/knowledge` |
| Dedupe integrity | 15 | 0 | 0 | `docs/notes/projects/<project>/timeline/YYYY-MM-DD.md` |

- total_score: 0/100

## Findings

- [severity] <finding summary>
  - impact: <what this affects>
  - evidence: `<path:line>`
  - expected: <what should happen>
  - actual: <what happened>

## Improvement Suggestions

1. <actionable improvement>
2. <actionable improvement>
3. <actionable improvement>

## Evidence

- `task_plan.md#<section>`
- `findings.md#<section>`
- `progress.md#<section>`
- `docs/notes/<path>`

## Review Iteration

Append additional review iterations on the same day in this file instead of creating duplicate files.
