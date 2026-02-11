---
type: context
date: YYYY-MM-DD
time: "HH:MM"
context_id: "<context_id>"
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
tags: [tag1, tag2]
project: project-name
---

<!-- 
AI INSTRUCTIONS:
1. **Mandatory vs Optional**: Only "Summary" and "What We Worked On" are MANDATORY. All other sections are OPTIONAL. 
2. **Omit Empty Sections**: If a section (Decisions, Unsolved, Lessons, Notes) has no content meeting the quality principles, OMIT IT ENTIRELY. Do not write "None" or empty headers.
3. **Quality Principles**: Follow strict quality rules in SKILL.md. Keep it condensed, fresh, and relevant (>3 months).
4. **Formatting**:
   - Use `{#anchor-slug}` for items that MOCs/INDEX will deep-link to.
   - Keep items concise (1-2 lines).
   - Link to MOCs/contexts using `[[wikilinks]]`.
5. **Lessons**: Error-related lessons will be indexed in `mocs/lessons-learned.md`. Make them actionable.
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
