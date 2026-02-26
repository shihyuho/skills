---
title: Decision Title
type: decision
status: confirmed
tags:
  - decision
  - project/<project-name>
summary: "One-sentence decision summary."
source_files:
  - "task_plan.md"
  - "findings.md"
source_date: 2026-02-13
source_ref:
  - "findings.md#<section-or-keyword>"
---

# Decision: <Title>

## Conclusion

<One sentence describing the final decision>

## Context and Rationale

<Why this decision was needed and why this option was chosen>

## Impact

- <impact on workflow, architecture, or maintenance>

## Source Pointers

- `task_plan.md`
- `findings.md`
- `findings.md#<section-or-keyword>`

## Draft Fallback

If source pointers are incomplete:

- set `status: draft`
- add frontmatter `unresolved_source_ref: ["<missing pointer>"]`
