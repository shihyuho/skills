---
id: skill-md-carries-runtime-rules-not-rationale
date: 2026-04-09
scope: project
tags:
  - skill-writing
  - skill-md
  - runtime-rules
  - rationale
  - separation-of-concerns
source: user-correction
confidence: 0.7
related:
  - "[[agent-rule-discoverability-needs-costly-mistake-exception]]"
---

# SKILL.md carries runtime-actionable rules, not design rationale

## Context

While building the `tldr` skill, the first SKILL.md draft packed its "Output shape" section with 8 bullets mixing pure format rules (title, subtitle, sections, headline, body) with content-selection semantics (items are conceptual units, typical count, grouping fallback). Several bullets also carried rationale sentences — "Rule taken verbatim from tldr.tech: '1-3 sentence description' and '2-4 sentences maximum'. Language-agnostic." and "Without this rule agents default to mechanical one-per-file slicing that preserves the format but loses the spirit."

## Mistake

The rationale sentences felt load-bearing during drafting — they explained *why* each rule exists. They were actually noise at runtime. The agent loading SKILL.md does not benefit from knowing that a rule was "taken verbatim from tldr.tech" or that an earlier agent generation tended to get the rule wrong. The agent needs to know *what to do*, not the archaeology of the rule. All the historical justification belongs in the design spec, where a future reader debating the design can find it.

The user surfaced this implicitly by saying "Output shape 那段很複雜" — the section was cognitively overloaded because actionable rules and inactionable rationale were fighting for attention in the same bullets.

## Lesson

`SKILL.md` is a runtime prompt. Every line should be either (a) a rule the agent must follow, or (b) an example that makes a rule concrete. Rationale — provenance, motivation, historical hedges explaining what earlier models got wrong — belongs in the design spec (`docs/superpowers/specs/...`), not the skill file. If a reader of `SKILL.md` wants the why, they can read the spec; if they need the what, every word should earn its place.

This is a stricter version of the existing discoverability heuristic. That rule says "don't include what's already discoverable". This one adds: "don't include what's already understood" — once a rule is stated clearly, further justification does not make the agent follow it harder, only read more text.

## When to Apply

Apply when drafting or reviewing any `SKILL.md`. Ask of each sentence: "If I delete this, does the agent behave differently at runtime?" If the answer is no, the sentence belongs in the spec, not the skill. Also apply when a SKILL.md section feels "complex" or "crowded" — that's often the signal that rationale has infiltrated rule space.
