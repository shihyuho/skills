# Lessons Learned

Helps AI agents learn from mistakes by capturing lessons in a structured format and syncing them to AGENTS.md.

## Overview

This skill enables AI agents to:
- Recognize situations where lessons should be captured
- Suggest creating lesson entries at appropriate moments
- Maintain a structured knowledge base of past mistakes and solutions
- Automatically review relevant lessons before starting similar tasks

**Key principle**: Learn once, avoid forever.

## When to Use

Use this skill when:
- Errors occur or tasks fail repeatedly
- Complex tasks complete (to capture insights)
- You want to prevent repeating the same mistakes
- Debugging reveals patterns worth documenting

## Features

- **Mixed-mode triggering**: AI suggests creating lessons; user confirms before writing
- **Structured format**: 200-300 word limit ensures concise, actionable content
- **AGENTS.md synchronization**: Automatic updates to project knowledge base
- **Mandatory review**: AI checks relevant lessons before similar tasks
- **Progressive learning**: Build institutional knowledge over time

## How It Works

### Workflow

1. **AI detects trigger situation**
   - Error occurs
   - Repeated failure (2+ attempts)
   - Complex task completion
   - User explicitly requests

2. **AI suggests creating lesson**
   ```
   I noticed we hit the same async issue twice in this session.
   This could be valuable to document as a lesson-learned entry.
   
   Would you like me to create a lesson file and update AGENTS.md?
   ```

3. **User confirms**
   - "Yes" / "Sure" / "Go ahead"

4. **AI creates lesson file**
   - Location: `docs/lessons/YYYY-MM-DD-topic-slug.md`
   - Format: See [LESSON_TEMPLATE.md](references/LESSON_TEMPLATE.md)
   - Content: 200-300 words total

5. **AI updates AGENTS.md**
   - Adds one-line summary to `## Lessons Learned` section
   - Format: `- [Summary](docs/lessons/file-name.md)`

6. **Future tasks reference lessons**
   - AI scans AGENTS.md before related tasks
   - Reads and applies relevant lesson guidance

### Example Interaction

```
AI: I noticed we had to refactor this code multiple times due to 
    async/await performance issues in loops. This could be valuable 
    to document.
    
    Would you like me to create a lesson-learned entry?

You: Yes

AI: ✓ Created lesson: docs/lessons/2026-02-06-async-await-loops.md
    ✓ Updated AGENTS.md with lesson reference
    
    The lesson is now part of the project knowledge base.

[Next time working with async code]

AI: I see from AGENTS.md we have a lesson on async/await patterns.
    Let me review that before proceeding...
    
    [Applies guidance from the lesson]
```

## Lesson File Structure

Each lesson follows this format:

```markdown
# [Brief Title]

**Date**: YYYY-MM-DD
**Context**: [One-line description]

## What Went Wrong

[Description of the mistake or issue - what happened and why it was problematic]

## How to Avoid

[Concrete steps to prevent this in the future - actionable guidance]
```

**Naming convention**: `docs/lessons/YYYY-MM-DD-topic-slug.md`

**Examples**:
- `docs/lessons/2026-02-06-async-await-loops.md`
- `docs/lessons/2026-02-08-type-guard-usage.md`
- `docs/lessons/2026-02-10-state-mutation.md`

See [LESSON_TEMPLATE.md](references/LESSON_TEMPLATE.md) for the complete template.

## AGENTS.md Integration

The `AGENTS.md` file serves as the central project knowledge base. The `## Lessons Learned` section provides quick reference to all documented lessons.

### Format

```markdown
## Lessons Learned

- [Avoid await in loops - use Promise.all for parallel async operations](docs/lessons/2026-02-06-async-await-loops.md)
- [Use type guards instead of type assertions for runtime safety](docs/lessons/2026-02-08-type-guard-usage.md)
- [Never mutate state directly - always create new objects](docs/lessons/2026-02-10-state-mutation.md)
```

### Mandatory Check

Before starting any task, AI **must**:
1. Check if `AGENTS.md` exists with `## Lessons Learned` section
2. Scan lesson summaries for relevance
3. Read full content of relevant lessons
4. Apply guidance from those lessons

**Relevance criteria**:
- Same technology/framework
- Similar operation or pattern
- Same category of issue (type safety, performance, etc.)

## Best Practices

### For AI Agents

- **Be proactive but not intrusive** - Suggest when valuable, don't over-suggest
- **Wait for confirmation** - Never create files without user approval
- **Keep it concise** - Respect the 200-300 word limit
- **Make it actionable** - Focus on prevention, not just explanation
- **Review before acting** - Always check existing lessons first

### For Users

- **Be selective** - Not every mistake needs a lesson
- **Focus on patterns** - Document recurring issues, not one-offs
- **Review periodically** - Scan lessons occasionally to refresh memory
- **Update when needed** - Keep lessons current as practices evolve
- **Share with team** - Commit to version control for team benefit

## Examples

### Example 1: Async/Await Performance

**Trigger**: Task required 3 attempts to fix performance issue

**Created Lesson**: `docs/lessons/2026-02-06-async-await-loops.md`
```markdown
# Async/Await in Loops

**Date**: 2026-02-06
**Context**: API data fetching in loop caused sequential delays

## What Went Wrong

Used await inside a for loop to fetch user details, causing requests
to execute sequentially. With 50 users, this took 50 seconds instead
of ~1 second. Each iteration waited for the previous request to complete
before starting the next one.

## How to Avoid

Use Promise.all() to parallelize independent async operations:
- Collect all promises first: `const promises = items.map(item => fetchData(item))`
- Await all together: `const results = await Promise.all(promises)`
- For partial dependencies, use Promise.allSettled() to handle failures
- Only use await in loops when operations truly depend on previous results
```

**AGENTS.md Entry**:
```markdown
- [Avoid await in loops - use Promise.all for parallel async operations](docs/lessons/2026-02-06-async-await-loops.md)
```

### Example 2: Type Safety

**Trigger**: Type assertion caused runtime error

**Created Lesson**: `docs/lessons/2026-02-08-type-guard-usage.md`
```markdown
# Type Guards vs Type Assertions

**Date**: 2026-02-08
**Context**: API response casting led to runtime null reference error

## What Went Wrong

Used `as UserData` to assert API response type without validation.
Runtime received null, but TypeScript believed it was UserData,
causing crash when accessing user.name. Type assertions bypass
runtime checks and only affect compile-time type checking.

## How to Avoid

Use type guard functions for runtime validation:
- Create guard: `function isUserData(data: unknown): data is UserData { return data && typeof data.name === 'string' }`
- Check before use: `if (isUserData(response)) { /* safe to use */ }`
- Consider libraries like zod for complex validation
- Reserve `as` for truly safe scenarios (e.g., DOM elements)
```

**AGENTS.md Entry**:
```markdown
- [Use type guards instead of type assertions for runtime safety](docs/lessons/2026-02-08-type-guard-usage.md)
```

## File Structure in Your Project

When using this skill, your project will have:

```
your-project/
├── AGENTS.md                          # Project knowledge base
└── docs/lessons/                           # Lessons directory
    ├── 2026-02-06-async-await-loops.md
    ├── 2026-02-08-type-guard-usage.md
    └── 2026-02-10-state-mutation.md
```

## Limitations

- **Not comprehensive documentation** - Lessons are for mistakes/learnings, not full guides
- **Requires discipline** - Quality depends on thoughtful content creation
- **Can accumulate noise** - Be selective to avoid lesson overload
- **Manual cleanup needed** - Periodically prune outdated or consolidated lessons

## Related Files

- [SKILL.md](SKILL.md) - Complete AI agent instructions
- [LESSON_TEMPLATE.md](references/LESSON_TEMPLATE.md) - Lesson file template

## License

MIT
