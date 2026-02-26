# Zettel Card Template

Use this template when creating a new lesson card.

```markdown
---
id: <semantic-kebab-case-id>
date: <YYYY-MM-DD>
tags: [tag1, tag2, tag3]
source: <user-correction | bug-fix | retrospective>
related: ["[[related-card-id-1]]", "[[related-card-id-2]]"]
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

- **id**: Use descriptive slugs. Prefer `api-timeout-retry-pattern` over `lesson-001`.
- **tags**: 3–6 lowercase tags. Include technology names, error categories, and domain concepts.
- **source**: Choose one — `user-correction` (user pointed out a mistake), `bug-fix` (discovered during debugging), `retrospective` (insight from task review).
- **related**: 0-3 wikilink references in `[[card-id]]` form. Add links only when high-value criteria are met (2-of-4 gate in `references/linking-heuristics.md`).
- **Context**: Keep to 1–2 sentences. Enough context to understand the scenario.
- **Mistake**: Be specific. Include error messages or symptoms when available.
- **Lesson**: Write actionable rules, not vague advice. Prefer "always do X before Y" over "be careful with X".
- **When to Apply**: Think in terms of triggers — what keywords or task types should activate recall of this lesson.

## Validation Checklist

- Required fields exist: `id`, `date`, `tags`, `source`, `related`.
- `tags` count is between 3 and 6.
- `related` count is between 0 and 3.
- Every `related` target resolves to an existing card ID.
