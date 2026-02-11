---
name: harvest
description: "Use when users ask to capture conversation decisions, problems, and lessons into persistent notes (e.g. 'harvest', '/harvest', 'save this to knowledge base', 'document this work')."
license: MIT
metadata:
  author: shihyuho
  version: "1.1.0"
---

# Harvest

Capture high-signal conversation knowledge into `docs/notes/` so future sessions can reuse decisions, lessons, and open questions.

## When to Trigger

**Explicit request**:
- "harvest", "/harvest"
- "harvest this", "harvest this conversation"
- "save this to knowledge base"
- "document this work", "capture this knowledge"

**Natural breakpoints** — AI may **suggest** (never auto-execute):
- Significant decision made
- Complex problem solved after multiple attempts
- Important lesson learned
- Discussion wrapping up with valuable content

```
We just [made a decision/solved X/learned Y].
Would you like me to update the knowledge base?
```

Wait for user confirmation. Never auto-execute.

## Non-Negotiables

- Never auto-execute. Always wait for explicit user confirmation.
- Use template files as the single source of structure.
- Keep `context_id` in frontmatter for smart merge.
- Keep MOCs as index files: link to context anchors, do not duplicate full lesson content.
- Omit optional empty sections. Do not write empty headers or "None" placeholders.

## Quick Start

1. Ensure `docs/notes/` exists (initialize if missing).
2. Run lesson review for this harvest run.
3. Detect `context_id` and check whether matching context file exists.
4. Create new context or smart-merge existing context.
5. Update `docs/notes/00-INDEX.md` and related MOCs.
6. Confirm created/updated files to user.

## Workflow

### Phase 1: Initialize + Lesson Review

#### 1.1 Initialize Knowledge Base (if missing)

If `docs/notes/` does not exist:

1. Create `docs/notes/contexts/` and `docs/notes/mocs/`.
2. Create `docs/notes/00-INDEX.md` from [references/INDEX_TEMPLATE.md](references/INDEX_TEMPLATE.md).
3. If `obsidian-bases` skill is available, create `docs/notes/contexts.base` from [references/CONTEXTS_BASE_TEMPLATE.base](references/CONTEXTS_BASE_TEMPLATE.base).
4. Check `AGENTS.md` then `CLAUDE.md`:
   - If found and no `## Lessons Learned` section, ask user whether to append section from [references/AGENTS_LESSONS_SECTION.md](references/AGENTS_LESSONS_SECTION.md).

#### 1.2 Mandatory Lesson Review (for this harvest run)

Before creating or merging context data:

1. If `docs/notes/00-INDEX.md` exists, read it.
2. If `docs/notes/mocs/lessons-learned.md` exists, scan for lessons related to this conversation:
   - Same technology/framework
   - Same operation type (async, state, API, integration)
   - Same error pattern
3. Apply relevant guidance while generating the context summary.

### Phase 2: Detect Context

Generate `context_id` using this priority:

1. First env var matching case-insensitive pattern:
   - `*SESSION*ID*`
   - `*CONVERSATION*ID*`
   - `*THREAD*ID*`
2. Fallback: timestamp `YYYYMMDDHHmmss`.

Then check for an existing file:

`docs/notes/contexts/<context_id>-*.md`

### Decision Matrix

| Condition | Action |
|---|---|
| Matching context file exists | Go to **Phase 4: Smart Merge** |
| No matching context file | Go to **Phase 3: Create New Context** |
| User rejects suggested filename | Ask for new slug and regenerate filename |
| User cancels confirmation | Stop without writing files |

### Phase 3: Create New Context

#### 3.1 Analyze Conversation Once

Extract only high-signal items:

- What we worked on
- Decisions with rationale
- Still unsolved questions
- Lessons learned

#### 3.2 Generate Filename + Confirm

Format: `<context_id>-<topic-slug>.md` (`topic-slug` is 2-4 words, kebab-case).

Prompt template:

```
Found: [N] decisions, [N] unsolved, [N] lessons
Suggested: contexts/<context_id>-<topic-slug>.md
1. Use this  2. Change slug  3. Cancel
```

#### 3.3 Write Context File

Create `docs/notes/contexts/<filename>.md` using [references/CONTEXT_TEMPLATE.md](references/CONTEXT_TEMPLATE.md).

If `obsidian-markdown` skill is available, use it for wikilinks/frontmatter/anchors.

Do not restate template rules here; template is authoritative.

#### 3.4 Update Index

Update `docs/notes/00-INDEX.md` from template rules:

- Recent Updates (keep top 5)
- Topics (MOCs)
- Key Decisions (if any)
- Open Questions (if any)
- Recent Lessons (if any)
- Stats counters

#### 3.5 Update Lessons-Learned MOC (Error-Related Lessons Only)

If lessons include failures/retries/gotchas (>15 min impact):

1. Ensure `docs/notes/mocs/lessons-learned.md` exists (create via [references/LESSONS_LEARNED_MOC_TEMPLATE.md](references/LESSONS_LEARNED_MOC_TEMPLATE.md) if missing).
2. Add links only:
   - `- [[contexts/<filename>#lesson-slug|Lesson Title]]`

#### 3.6 Topic MOC Discovery

If topic appears in 3+ contexts and no MOC exists, ask user whether to create one.

If confirmed, create from [references/MOC_TEMPLATE.md](references/MOC_TEMPLATE.md) and add to `00-INDEX.md`.

#### 3.7 Confirm

```
✓ Created: contexts/<filename>.md
✓ Updated: 00-INDEX.md
✓ Updated: mocs/lessons-learned.md (if applicable)
✓ Created: mocs/<topic>.md (if applicable)
```

### Phase 4: Smart Merge

When `context_id` matches existing file:

1. Read existing context file.
2. Merge new information from current conversation.

| Section | Existing Topic | New Item |
|---|---|---|
| Decisions Made | Update existing entry, note update time | Append |
| Still Unsolved | Move resolved items to Decisions | Append |
| Lessons Learned | Merge if same lesson, preserve anchor | Append |
| What We Worked On | Keep existing | Append |

3. Update frontmatter:
   - Keep `created`
   - Update `updated`
   - Add new tags if needed
4. Update `00-INDEX.md` stats/recent updates.
5. If new error-related lessons were added, update `mocs/lessons-learned.md` with links only.

Confirm:

```
✓ Updated: contexts/<filename>.md
Changes: [added/updated/moved items]
```

## Content Quality Rules

- Quality over quantity: concise, reusable, high-signal notes.
- One idea per bullet; include rationale for decisions.
- Keep content relevant for future reuse (3+ months horizon).
- Skip raw transcripts, dead ends without insight, and obvious process noise.
- For lessons, use anchored headings and include: what happened, root cause, solution, apply-when.

Recommended section limits:

| Section | Requirement | Typical Size |
|---|---|---|
| Summary | Required | 1-2 sentences |
| What We Worked On | Required | 5-7 bullets |
| Decisions | Optional | up to 5-7 items |
| Still Unsolved | Optional | up to 3-5 items |
| Lessons Learned | Optional | up to 3-5 items |
| Notes | Optional | short snippets only |

---

## Integration

**Recommended**: `obsidian-markdown` skill — If installed, use it for enhanced Obsidian compatibility (proper wikilinks, frontmatter, heading anchors). If not available, AI can write files directly, but suggest installing for better integration:

```
For optimal Obsidian compatibility, consider installing obsidian-markdown skill:
npx skills add <obsidian-markdown-repo>
```

## See Also

Use these files as references (single source for structure and formats).

- [CONTEXT_TEMPLATE.md](references/CONTEXT_TEMPLATE.md)
- [MOC_TEMPLATE.md](references/MOC_TEMPLATE.md)
- [INDEX_TEMPLATE.md](references/INDEX_TEMPLATE.md)
- [LESSONS_LEARNED_MOC_TEMPLATE.md](references/LESSONS_LEARNED_MOC_TEMPLATE.md)
- [CONTEXTS_BASE_TEMPLATE.base](references/CONTEXTS_BASE_TEMPLATE.base)
- [AGENTS_LESSONS_SECTION.md](references/AGENTS_LESSONS_SECTION.md)
