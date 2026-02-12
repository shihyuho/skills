---
type: context
context_id: "<context_id>"   # Session ID (e.g., claude_session_abc) or fallback timestamp (YYYYMMDDHHmmss)
created: YYYY-MM-DDTHH:MM:SS   # Canonical creation timestamp
updated: YYYY-MM-DDTHH:MM:SS   # Canonical update timestamp
tags: [tag1, tag2]
project: project-name
---

<!-- 
⚠️ Structure template only.
Behavioral workflow and merge rules live in `skills/harvest/SKILL.md`.

Required:
  - YAML frontmatter with `context_id`
  - Summary + What We Worked On
  - Optional sections omitted when empty
  - Stable item identifiers for Decisions/Questions/Lessons (`D-*`, `Q-*`, `LL-*`)
  - Item headings use `{#anchor-slug}`

Formatting policy:
  - Default to lists for narrative content (better readability when text is long)
  - Use tables only for short, comparable fields (for example `ID | Question | Next`)
  - Keep section-level MOC links once; avoid repeating the same `Related` link per item

TERMINOLOGY MAPPING (canonical -> alias in index/moc files):
  - Decisions Made -> Key Decisions
  - Still Unsolved -> Open Questions
  - Lessons Learned -> Recent Lessons / Lessons
-->

# [One-Line Summary]

**Summary**: [1-2 sentence overview of what was accomplished]

**MOCs**: [[mocs/topic-1]], [[mocs/topic-2]]

---

## What We Worked On

- [Activity 1]
- [Activity 2]

---

## Decisions Made (Optional)

### D-001: [Decision Title] {#d-001-decision-slug}

- **Decision**: [What was decided]
- **Why**: [Why this decision was made]
- **Impact**: [Expected impact or follow-up]
- **Alternatives**: [Rejected option and reason] (optional, only when trade-off is important)

### D-002: [Another Decision] {#d-002-another-decision-slug}

- **Decision**: [What was decided]
- **Why**: [Why this decision was made]

---

## Still Unsolved (Optional)

### Q-001: [Question Title] {#q-001-question-slug}

- **Question**: [What remains unresolved]
- **Options**: [A vs B] (optional)
- **Next**: [Action needed]
- **Owner/Target**: [Owner and date/target] (optional; include only when meaningful)

**Optional compact table (use only when cells stay short):**

| ID | Question | Next |
|---|---|---|
| Q-001 | [Short question] | [Short next action] |

---

## Lessons Learned (Optional)

**Related MOC**: [[mocs/lessons-learned]]

### LL-001: [Lesson Title] {#ll-001-lesson-slug}

- **Issue**: [Description of the issue or discovery]
- **Root Cause**: [Why it happened]
- **Fix**: [How it was solved or what pattern to follow]
- **Guardrail**: [Check/process/test to prevent recurrence] (optional)
- **Apply When**: [Situations where this lesson is relevant] (optional)

---

## Source Notes (Optional)

[Use plain-text provenance for external planning files. Do not add wikilinks to files outside `docs/notes`.]

- Source: planning/findings.md (captured YYYY-MM-DD)
  - Conclusion: [One-line conclusion]
  - Evidence: [One-line evidence or rationale]

- Source: planning/task_plan.md (captured YYYY-MM-DD)
  - Conclusion: [One-line conclusion]
  - Evidence: [One-line evidence or rationale]

---

## Notes (Optional)

[Code snippets, links, or observations that don't fit above. Do not include harvest command menus, confirmation prompts, or created/updated/skipped bookkeeping text.]

```language
[Code example if applicable, ≤15 lines]
```
