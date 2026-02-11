---
type: context
date: YYYY-MM-DD
time: "HH:MM:SS"
context_id: "<context_id>"  # Session ID (e.g., claude_session_abc) or timestamp (YYYYMMDDHHmmss)
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
tags: [tag1, tag2]
project: project-name
---

<!-- 
⚠️ MANDATORY: Follow this template EXACTLY. Do NOT create custom formats.

REQUIRED:
  [ ] YAML frontmatter (lines 1-10) with `context_id`
  [ ] Summary (2-3 sentences)
  [ ] What We Worked On (bullets)
  [ ] Lessons use `{#anchor-slug}` for deep-linking
  [ ] Omit empty optional sections

FORBIDDEN:
  - Custom frontmatter (e.g., **Date**: 2026-02-10)
  - Starting with markdown headers instead of YAML
  - Empty optional sections (write "None")

FORMAT:
  - Anchors: `### Title {#slug}`
  - Lessons: What Happened, Root Cause, Solution, Apply When
  - Keep concise (1-2 lines), skip obvious details
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
