---
id: eval-coverage-and-discrimination-are-different
date: 2026-03-21
scope: project
tags:
  - skill-writing
  - evals
  - benchmarking
  - agents-md
source: retrospective
confidence: 0.3
related: []
---

# Coverage improvements do not guarantee discriminating evals

## Context

While expanding `writing-agents-md` evals, new prompts were added for stale existing files, short files that still needed re-audit, vague discussion notes that should not become invented commands, and an output-only replacement prompt that suppressed reasoning and removed a direct current-reality checklist.

## Mistake

It was tempting to treat these additions as automatically stronger benchmarks because they covered newly identified behaviors and looked harsher on the surface. In practice, both with-skill and baseline runs still passed when the prompt contained enough explicit signal for a careful model to infer the right output, even after suppressing reasoning output.

## Lesson

When designing evals for agent skills, separate behavior coverage from benchmark discrimination. A prompt can validly test the intended behavior and still fail to distinguish the skill from baseline if the clues are too direct. Output-only formatting and harsher tone help realism, but they do not by themselves create benchmark separation. Exploratory prompts that improve understanding but do not earn a durable place in the maintained eval set should stay in benchmark workspaces, not necessarily in the canonical `evals.json`.

## When to Apply

Apply this when expanding eval suites for skills, prompts, or agent workflows and deciding whether a new case should stay as coverage only, live only in benchmark history, or be used as evidence that the skill materially improves behavior.
