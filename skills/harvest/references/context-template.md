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

**Decision**: [What was decided]

**Rationale**: [Why this decision was made]

**Alternatives**: [What was rejected and why]

**Impact**: [Expected impact or follow-up]

**Related**: [[mocs/topic]], [[contexts/YYYY-MM-DD-HHMM-context]]

### D-002: [Another Decision] {#d-002-another-decision-slug}

**Decision**: [What was decided]

**Rationale**: [Why this decision was made]

---

## Still Unsolved (Optional)

### Q-001: [Question Title] {#q-001-question-slug}

**Description**: [What remains unresolved]

**Options**: [A vs B]

**Next**: [Action needed]

**Deadline**: [YYYY-MM-DD or TBD]

**Carry-Over**: [yes/no]  # Use yes when inherited from previous sessions

**Related**: [[mocs/topic]]

---

## Lessons Learned (Optional)

### LL-001: [Lesson Title] {#ll-001-lesson-slug}

**What Happened**: [Description of the issue or discovery]

**Root Cause**: [Why it happened] (if applicable)

**Solution**: [How it was solved or what pattern to follow]

**Guardrail**: [Check/process/test to prevent recurrence]

**Apply When**: [Situations where this lesson is relevant]
- [Situation 1: specific technology or operation]
- [Situation 2: specific error pattern]

**Related**: [[mocs/lessons-learned]], [[mocs/topic]]

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

[Code snippets, links, or observations that don't fit above]

```language
[Code example if applicable, ≤15 lines]
```
