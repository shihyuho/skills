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

# [One-Line Summary]

**Summary**: [1-2 sentence overview of what was accomplished]

**MOCs**: [[mocs/topic-1]], [[mocs/topic-2]]

---

## What We Worked On

- [Activity 1]
- [Activity 2]

---

## Decisions Made

### [Decision Title] {#decision-slug}

[What was decided] — _Why_: [rationale]. Alternatives: [what was rejected and why]

**Related**: [[mocs/topic]], [[contexts/YYYY-MM-DD-HHMM-context]]

### [Another Decision] {#another-decision-slug}

[What was decided] — _Why_: [rationale]

---

## Still Unsolved

### [Question Title] {#question-slug}

[Description]. Options: [A vs B]. Next: [action needed]. Deadline: [YYYY-MM-DD]

**Related**: [[mocs/topic]]

---

## Lessons Learned

### [Lesson Title] {#lesson-slug}

**What Happened**: [Description of the issue or discovery]

**Root Cause**: [Why it happened] (if applicable)

**Solution**: [How it was solved or what pattern to follow]

**Apply When**: [Situations where this lesson is relevant]
- [Situation 1: specific technology or operation]
- [Situation 2: specific error pattern]

**Related**: [[mocs/lessons-learned]], [[mocs/topic]]

---

## Notes

[Code snippets, links, or observations that don't fit above. Optional section — omit if empty.]

```language
[Code example if applicable, ≤15 lines]
```

---

**Guidelines**:
- Follow Content Quality Principles in SKILL.md
- Use `{#anchor-slug}` for items that MOCs/INDEX will deep-link to
- Keep each item concise (1-2 lines of content + optional Related links)
- Link to MOCs and contexts using `[[wikilinks]]`
- **Lessons Learned**: Error-related lessons will be indexed in `mocs/lessons-learned.md` for active review
