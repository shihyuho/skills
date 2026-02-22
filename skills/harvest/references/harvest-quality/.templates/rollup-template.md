---
title: Harvest Optimization Rollup
type: harvest-optimization-rollup
status: draft
tags:
  - harvest-quality
  - optimization
  - project/<project-slug>
summary: "Monthly rollup of harvest review reports with prioritized improvements."
source_files:
  - "../YYYY-MM-DD-<project-slug>-harvest-review.md"
source_date: 2026-02
rollup_scope:
  mode: optimize
  window: YYYY-MM
  dimensions:
    - structure
    - traceability
    - extraction
    - classification
    - dedupe
---

# Harvest Optimization Rollup - <project-slug> - YYYY-MM

## Snapshot

- generated_at: 2026-02-19 22:30
- project_slug: <project-slug>
- window: 2026-02
- included_reports: 0
- skipped_reports: 0

## Source Roots

- default_root: `docs/notes/harvest-quality/`
- additional_roots:
  - `<absolute-or-relative-path>`
- resolved_roots:
  - `<absolute-path>`
- skipped_roots:
  - path: `<path>`
    reason: missing|unreadable|invalid

## Aggregated Score Trends

| Dimension | Mean Score (0-5) | Trend | Evidence |
| --- | --- | --- | --- |
| Structure completeness | 0.0 | flat | `docs/notes/harvest-quality/...` |
| Traceability quality | 0.0 | flat | `docs/notes/harvest-quality/...` |
| Extraction quality | 0.0 | flat | `docs/notes/harvest-quality/...` |
| Classification quality | 0.0 | flat | `docs/notes/harvest-quality/...` |
| Dedupe integrity | 0.0 | flat | `docs/notes/harvest-quality/...` |

- mean_total_score: 0/100

## Repeated Gaps

- <gap summary>
  - frequency: <count>
  - impact: high|medium|low
  - evidence: `<path:line>`

## Prioritized Roadmap

1. [high-impact, low-effort] <improvement item>
2. [high-impact, medium-effort] <improvement item>
3. [medium-impact, low-effort] <improvement item>

## Evidence

- `docs/notes/harvest-quality/YYYY-MM-DD-<project-slug>-harvest-review.md`

## Skipped Inputs

- path: `<path-or-file>`
  reason: `missing|unreadable|invalid|outside-window|missing-scorecard|missing-evidence`

## Rollup Iteration

Append additional rollup iterations for the same month in this file instead of creating duplicates.
