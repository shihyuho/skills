---
id: right-size-review-rigor-to-task-complexity
date: 2026-04-09
scope: project
tags:
  - skill-writing
  - subagent-driven-development
  - process
  - review-rigor
source: retrospective
confidence: 0.3
related: []
---

# Right-size subagent review rigor to the task it protects

## Context

While executing the `tldr` skill plan under `superpowers:subagent-driven-development`, every plan task was supposed to get a three-dispatch cycle: implementer → spec reviewer → code quality reviewer. The plan had 6 tasks, so the strict reading prescribed ~18 subagent dispatches. The actual work was creating 3 verbatim Markdown files and adding one line to the repo README. The overhead-to-value ratio was poor for Tasks 2-4, where the "implementation" was a literal copy of content already drafted in the plan.

## Mistake

Following the full three-dispatch pattern mechanically for verbatim Markdown file creation was treating process rigor as a goal rather than a tool. For a complex implementation task — novel logic, multi-file coordination, subtle API contracts — three dispatches per task is cheap insurance. For writing a 40-line README whose content is already quoted in the plan, three dispatches is bureaucracy and burns tokens without catching anything a single consolidated review wouldn't also catch.

## Lesson

Before mechanically applying the subagent-driven three-dispatch pattern, grade the task on (a) implementation novelty — does the implementer have to make any real decisions, or is it a transcription? and (b) review surface — are there multiple distinct failure modes (spec compliance AND code quality AND integration), or does the work collapse into a single review concern? When both axes are low — as in transcribing pre-written Markdown content — collapse to a single consolidated review per task, and save the three-stage pattern for tasks with genuine implementation risk. The skill's process is the default, not the mandate.

## When to Apply

Apply when executing plans whose tasks include file creation from pre-written templates (README files, markdown prompt skills, slash command stubs, fixture data). Also apply when review cycles are visibly consuming more tokens than the work they review. Do **not** apply as an excuse to skip reviews entirely — the trigger is "consolidate", not "omit".
