---
name: time-to-skill
description: Use when detecting repeated task patterns (3+ similar tasks) or when user explicitly requests skill creation. Monitors workflows and suggests converting repetitive patterns into skills.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Time to Skill

A skill for AI agents to detect repeated workflows and suggest converting them into reusable skills.

## Overview

This skill enables AI agents to:
- Monitor task patterns and identify repetition
- Detect when similar workflows are performed multiple times
- Suggest creating skills at appropriate moments
- Record workflow information for future skill creation

**Key principle**: If you do something more than once a day, turn it into a skill.

**Scope**: This skill focuses on **detection and suggestion only**. For actually creating skills, delegate to the `skill-creator` skill or ask the user to create manually.

## When to Trigger

AI should suggest creating a skill in these situations:

### 1. After Detecting Similar Task Pattern (3+ Times)

When the AI identifies that similar tasks have been performed 3 or more times within a session or day.

**Example triggers**:
- User asks to create React components following the same structure 3 times
- User repeatedly performs "create branch → write code → test → create PR" workflow
- Similar refactoring operations performed across different files

**Detection method**: AI uses semantic analysis to identify conceptually similar tasks, not just identical commands.

### 2. User Explicit Request

When the user directly asks to convert a workflow into a skill.

**Examples**:
- "Turn this into a skill"
- "Let's automate this workflow"
- "Create a skill for this pattern"
- "I keep doing this repeatedly"

## Workflow

### Step 1: Monitor and Detect Patterns

Throughout the session, track:
- **Task descriptions**: What the user is asking for (semantic similarity)
- **Workflow sequences**: Series of operations that form a pattern
- **Tool usage patterns**: Repeated tool call sequences
- **File/directory patterns**: Similar file structures being created

**Similarity threshold**: 3 occurrences of conceptually similar tasks.

**Quality filter**: Only track patterns with:
- 3+ steps in the workflow
- Clear, repeatable structure
- Potential time savings

### Step 2: Suggest Skill Creation

When a pattern reaches the threshold, **ask the user for confirmation**:

**Template**:
```
I noticed you've performed similar tasks [N] times: [brief description of pattern].

This workflow appears repetitive and could be automated as a skill.

Pattern detected:
- [Step 1 of the pattern]
- [Step 2 of the pattern]
- [Step 3 of the pattern]

Would you like to create a skill for this workflow?
```

**Examples**:
```
I noticed you've created React components with the same structure 3 times.

This workflow appears repetitive and could be automated as a skill.

Pattern detected:
- Create TypeScript component file with props interface
- Create Jest test file with basic test setup
- Create Storybook story file with default story

Would you like to create a skill for this workflow?
```

```
I noticed you've performed the feature branch workflow 3 times today.

This workflow appears repetitive and could be automated as a skill.

Pattern detected:
- Create feature branch from main
- Implement changes
- Run tests
- Create pull request with template

Would you like to create a skill for this workflow?
```

### Step 3: Wait for User Confirmation

**Do not proceed without explicit user confirmation.**

Valid confirmations:
- "Yes"
- "Sure"
- "Go ahead"
- "Please do"
- Any affirmative response

If user declines, ask if they want to be reminded about this pattern again:

**Template**:
```
Understood. Should I:
1. Stop tracking this pattern (won't remind you again)
2. Keep monitoring (might suggest again if pattern continues)
```

### Step 4: Record Pattern Information

If user confirms, document the pattern details for skill creation:

**Information to capture**:
1. **Pattern name** (suggest a descriptive name)
2. **Trigger conditions** (when should this skill be used?)
3. **Workflow steps** (what actions are performed?)
4. **File patterns** (what files/directories are created?)
5. **Commands used** (bash, git, npm commands)
6. **Templates/snippets** (code structures that repeat)

### Step 5: Delegate to Skill Creation

After recording pattern information, suggest next steps:

**Option A: Use skill-creator skill (recommended)**
```
I've documented the pattern. Would you like me to:

1. Use the skill-creator skill to generate a complete skill (recommended)
2. Save the pattern documentation for manual skill creation later
3. Just remember the pattern without creating files

Which would you prefer?
```

**Option B: Manual creation**
```
I've documented the pattern. You can create a skill manually using this information, or ask me to use the skill-creator skill.

The pattern documentation is ready for skill creation.
```

**This skill does NOT create skill files directly.** Delegate to `skill-creator` or provide pattern information for user to create manually.

## Pattern Documentation Format

When recording a detected pattern, use this format: [PATTERN_TEMPLATE.md](references/PATTERN_TEMPLATE.md)

## Best Practices

### For AI Agents

1. **Be selective** - Only suggest skills for genuinely repetitive patterns (3+ occurrences)
2. **Track semantically** - Look for conceptually similar tasks, not just identical commands
3. **Show value** - Explain estimated time savings when suggesting
4. **Don't auto-create** - Always wait for user confirmation before recording patterns
5. **Delegate skill creation** - Use skill-creator skill or provide info for manual creation

### For Users

1. **Review suggestions** - AI might detect false positives, confirm only valuable patterns
2. **Be selective** - Not every repetition needs a skill
3. **Provide feedback** - Tell AI to stop tracking if pattern isn't valuable
4. **Use skill-creator** - Leverage the skill-creator skill for proper skill generation

## Quality Control

To avoid generating too many trivial suggestions:

1. **Complexity threshold**: Only suggest for workflows with 3+ steps
2. **User confirmation required**: Never auto-create without approval
3. **Allow ignoring**: Let users decline and mark patterns to stop tracking
4. **Show ROI**: Explain estimated time savings when suggesting
5. **Semantic matching**: Avoid suggesting for superficially similar but conceptually different tasks

## Examples

### Example 1: React Component Creation

**Detected Pattern** (after 3 occurrences):
```
I noticed you've created React components with the same structure 3 times.

Pattern detected:
- Create component file: src/components/[Name].tsx
- Create test file: src/components/[Name].test.tsx
- Create story file: src/components/[Name].stories.tsx
- Apply TypeScript + props interface template
- Apply test boilerplate
- Apply story boilerplate

Would you like to create a skill for this workflow?
```

**User**: Yes

**AI Response**:
```
Great! I've documented the pattern.

Would you like me to:
1. Use the skill-creator skill to generate a complete skill (recommended)
2. Save the pattern documentation for manual creation later

Which would you prefer?
```

### Example 2: Feature Branch Workflow

**Detected Pattern** (after 3 occurrences):
```
I noticed you've performed the feature branch workflow 3 times today.

Pattern detected:
- git checkout -b feature/[name]
- Implement changes
- Run npm test
- git add . && git commit -m "[message]"
- gh pr create with template

Would you like to create a skill for this workflow?
```

**User**: No, this is project-specific

**AI Response**:
```
Understood. Should I:
1. Stop tracking this pattern (won't remind you again)
2. Keep monitoring (might suggest again if pattern continues)
```

### Example 3: User Explicit Request

**User**: "I keep doing this database migration flow. Can we turn it into a skill?"

**AI Response**:
```
Absolutely! Let me document the pattern.

Can you describe the typical steps you follow for database migrations?
```

[AI collects workflow information through conversation]

```
I've documented your database migration workflow.

Would you like me to:
1. Use the skill-creator skill to generate a complete skill (recommended)
2. Provide the pattern documentation for you to create manually

Which would you prefer?
```

## Relationship with Other Skills

**time-to-skill** works with other skills:

| Skill | Relationship |
|-------|--------------|
| **skill-creator** | time-to-skill detects patterns → skill-creator generates skill files |
| **lessons-learned** | Different focus: time-to-skill = efficiency, lessons-learned = error prevention |

**Recommended workflow**:
1. time-to-skill detects repetition
2. User confirms pattern is valuable
3. time-to-skill documents pattern
4. Delegate to skill-creator to generate actual skill
5. User reviews and refines generated skill

## Limitations

1. **Detection is imperfect** - AI may miss patterns or suggest incorrectly
2. **Requires user judgment** - Not all repetitive tasks need skills
3. **No auto-creation** - This skill only detects and suggests, doesn't create skills
4. **Semantic matching challenges** - AI might conflate superficially similar but different tasks

## See Also

- **skill-creator** - Use this skill to actually generate skill files from detected patterns

