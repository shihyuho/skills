---
type: context
date: YYYY-MM-DD          # Compatibility field (derived from `created`)
time: "HH:MM:SS"         # Compatibility field (derived from `created`)
context_id: "<context_id>"  # Session ID (e.g., claude_session_abc) or timestamp (YYYYMMDDHHmmss)
created: YYYY-MM-DDTHH:MM:SS  # Canonical creation timestamp
updated: YYYY-MM-DDTHH:MM:SS  # Canonical update timestamp
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
  - Lesson headings use `{#anchor-slug}`

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

### [Decision Title] {#decision-slug}

[What was decided] — _Why_: [rationale]. Alternatives: [what was rejected and why]

**Related**: [[mocs/topic]], [[contexts/YYYY-MM-DD-HHMM-context]]

### [Another Decision] {#another-decision-slug}

[What was decided] — _Why_: [rationale]

---

## Still Unsolved (Optional)

### [Question Title] {#question-slug}

[Description]. Options: [A vs B]. Next: [action needed]. Deadline: [YYYY-MM-DD]

**Related**: [[mocs/topic]]

---

## Lessons Learned (Optional)

### [Lesson Title] {#lesson-slug}

**What Happened**: [Description of the issue or discovery]

**Root Cause**: [Why it happened] (if applicable)

**Solution**: [How it was solved or what pattern to follow]

**Apply When**: [Situations where this lesson is relevant]
- [Situation 1: specific technology or operation]
- [Situation 2: specific error pattern]

**Related**: [[mocs/lessons-learned]], [[mocs/topic]]

---

## Notes (Optional)

[Code snippets, links, or observations that don't fit above]

```language
[Code example if applicable, ≤15 lines]
```
