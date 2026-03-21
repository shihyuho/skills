---
id: agent-rule-discoverability-needs-costly-mistake-exception
date: 2026-03-21
scope: project
tags:
  - skill-writing
  - agents-md
  - heuristics
  - prompting
source: retrospective
confidence: 0.3
related: []
---

# Discoverability alone is not enough to delete an agent rule

## Context

While writing the `writing-agents-md` skill, the first draft used an almost absolute heuristic: if information is discoverable from the repo, delete it from `AGENTS.md` or `CLAUDE.md`.

## Mistake

That rule was too rigid. Some facts are technically discoverable but still worth keeping globally when missing them causes costly mistakes and the model is unlikely to infer the correct choice reliably.

## Lesson

When writing pruning heuristics for agent instruction files, treat discoverability as the default delete signal, not an absolute delete rule. Keep a narrow exception for high-impact operational choices that are easy for the model to get wrong.

## When to Apply

Apply this when writing or revising skills, docs, or checklists that teach models what to keep versus remove from global instruction files.
