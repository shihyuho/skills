# Zettel Card Template

Use this template when creating or updating a lesson card.

```markdown
---
id: <semantic-kebab-case-id>
date: <YYYY-MM-DD>
scope: <project | module | feature>
tags: [tag1, tag2, tag3]
source: <user-correction | bug-fix | retrospective>
confidence: <0.0-0.9>
related: []
---

# <One-line lesson title>

## Context
<What was happening when the mistake occurred or the insight emerged.>

## Mistake
<What went wrong, or what was suboptimal.>

## Lesson
- <Extracted rule or best practice>
- <Additional key points>

## When to Apply
<Future situations where this lesson is relevant.>
```

## Field Guidelines

- **id**: Use a descriptive semantic slug. Prefer
  `api-timeout-retry-pattern` over `lesson-001`.
- **date**: Use ISO format `YYYY-MM-DD`.
- **scope**: Choose exactly one: `project`, `module`, or `feature`.
- **tags**: Use 3-6 lowercase tags that help future recall match the task.
- **source**: Choose exactly one: `user-correction`, `bug-fix`, or
  `retrospective`.
- **confidence**: Initialize from the source rule defined in
  `references/recall-and-index.md`, then increase only when later evidence shows
  the lesson was useful.
- **related**: Use 0-2 wikilink references in `[[card-id]]` form. This field
  stores related IDs only; selection policy lives outside this file.
- **Context**: Keep to 1-2 sentences. Include only the scenario needed to make
  the lesson understandable.
- **Mistake**: Name the failure, confusion, or bad assumption clearly.
- **Lesson**: Write an actionable prevention rule. Prefer direct guidance over
  vague caution.
- **When to Apply**: Describe the future trigger for reuse, not a recap of what
  already happened.

## Quality Bar

- Capture reusable rules, not session notes.
- Prefer stable prevention language over case-specific storytelling.
- Keep the card compact enough to scan quickly during recall.
- Update an existing card when the lesson meaning is the same.

## Card-Local Validation

- Required fields exist: `id`, `date`, `scope`, `tags`, `source`,
  `confidence`, `related`.
- `scope` is one of `project`, `module`, `feature`.
- `tags` count is between 3 and 6.
- `confidence` is numeric and between 0.0 and 0.9.
- `related` count is between 0 and 2.
- Every `related` entry uses `[[card-id]]` format.

Index synchronization, recall ranking, duplicate handling, and broken-link
recovery are defined in `references/recall-and-index.md`.
