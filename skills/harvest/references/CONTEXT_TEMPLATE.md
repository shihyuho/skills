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
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI INSTRUCTIONS - READ BEFORE WRITING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ CRITICAL: This template is MANDATORY. Do NOT create custom formats.

✅ REQUIRED STRUCTURE:
  1. YAML frontmatter (lines 1-10) - MUST be present EXACTLY as shown
  2. One-line title (line 24)
  3. Summary section (line 26-28) - MANDATORY
  4. What We Worked On section (line 32-35) - MANDATORY
  5. Optional sections (Decisions/Unsolved/Lessons/Notes) - ONLY if content exists

❌ FORBIDDEN:
  - Custom frontmatter format (e.g., **Date**: 2026-02-10)
  - Starting file with plain markdown headers instead of YAML
  - Writing "None" or empty headers for optional sections
  - Omitting `context_id` field (breaks smart merge)

📋 PRE-WRITE CHECKLIST (verify before file creation):
  [ ] File starts with `---` (YAML frontmatter)
  [ ] `context_id` field is populated
  [ ] Summary section exists (2-3 sentences)
  [ ] "What We Worked On" section exists (bullets)
  [ ] Optional sections OMITTED if no quality content
  [ ] Lessons use `{#anchor-slug}` format
  [ ] All links use `[[wikilinks]]` format

📐 FORMATTING RULES:
  - Anchors: `### Decision Title {#decision-slug}`
  - Wikilinks: `[[mocs/topic]]` or `[[contexts/file#anchor]]`
  - Lessons structure: What Happened, Root Cause, Solution, Apply When
  - Keep items 1-2 lines max
  - Code snippets ≤15 lines

📊 QUALITY PRINCIPLES:
  - Include ONLY what matters in 3 months
  - 5 high-signal bullets > 20 noisy items
  - Every bullet provides NEW information
  - Skip: debugging transcripts, obvious practices, dead-ends

🔗 INTEGRATION:
  - Error-related lessons → indexed in `mocs/lessons-learned.md`
  - MOC links in frontmatter and content
  - Deep links to INDEX sections via anchors

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
