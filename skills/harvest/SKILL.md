---
name: harvest
description: "Harvest knowledge from conversations into a searchable second brain. Capture decisions, problems, lessons across conversations and agents. Triggers: 'harvest', 'harvest this', '/harvest', 'save this to knowledge base'."
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Harvest

Harvest knowledge from conversations into a context-based second brain that persists across conversations, agents, and time.

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

---

## Mandatory Lesson Review

**Before executing any task**, AI MUST check for documented lessons:

1. **Check if knowledge base exists**: Look for `docs/notes/00-INDEX.md`
2. **If exists**:
   - Read the INDEX file
   - Look for lessons-learned MOC reference
   - If `docs/notes/mocs/lessons-learned.md` exists, read it
   - Scan for lessons matching current task:
     - Same technology/framework
     - Similar operation (async, state management, API calls, etc.)
     - Same error pattern
   - Read full context for matching lessons
   - Apply guidance before proceeding
3. **If knowledge base doesn't exist**: Proceed normally

**Why**: Past mistakes are documented to prevent repetition across sessions and agents.

---

## Workflow

### Step 1: Init Knowledge Base

Check if `docs/notes/` exists. If NOT:

1. Create directories: `docs/notes/contexts/` and `docs/notes/mocs/`
2. Use [references/INDEX_TEMPLATE.md](references/INDEX_TEMPLATE.md) as reference to create `docs/notes/00-INDEX.md`
   - **CRITICAL**: Include ALL sections from template (Stats, Recent Updates, Topics, Key Decisions, Open Questions, Recent Lessons)
   - Replace `[Project Name]` with actual project name
   - Initialize Stats with zeros
   - Leave other sections with placeholder content
3. **Check for obsidian-bases skill**: If `obsidian-bases` skill is installed, use [references/CONTEXTS_BASE_TEMPLATE.base](references/CONTEXTS_BASE_TEMPLATE.base) as reference to create `docs/notes/contexts.base`
   - This creates a dynamic table view of all contexts
   - Extracts date/time from filename for easy sorting
   - Assumes Obsidian vault root is `docs/notes/`, so paths are relative to vault root
4. **Agent Config**: Add Lessons Learned section to AGENTS.md or CLAUDE.md:
   - Check which file exists (priority: AGENTS.md > CLAUDE.md)
   - If found, check if `## Lessons Learned` section already exists
   - If section doesn't exist, ask user:
     ```
     Add "Lessons Learned" section to AGENTS.md?
     This enables automatic lesson review before future tasks.
     
     [Yes / No / Show me first]
     ```
   - If user confirms, append section using [references/AGENTS_LESSONS_SECTION.md](references/AGENTS_LESSONS_SECTION.md) as reference
   - If neither file exists, skip (no file to modify)

---

### Step 2: Detect Context

**Generate context_id using this logic**:

1. Search environment variables for any containing "SESSION", "CONVERSATION", or "THREAD" + "ID" (case-insensitive)
   - Match patterns like: `*SESSION*ID*`, `*CONVERSATION*ID*`, `*THREAD*ID*`
   - Take the first match found
2. If no match found, use current timestamp in format `YYYYMMDDHHmmss`
   - Example: `20260211151030` for 2026-02-11 15:10:30
   - Minute precision allows natural merging within same minute

**Search for existing context** with same context_id:
```bash
# Check if file exists matching pattern
docs/notes/contexts/<context_id>-*.md
```

- **Found** → Step 4 (Smart Merge)
- **Not found** → Step 3 (New Context)

---

### Step 3: Create New Context

#### 3.1 Analyze Conversation

Extract:
- **What we worked on**: Main activities, tasks completed
- **Decisions made**: Architecture choices, trade-offs (include WHY)
- **Still unsolved**: Open questions, pending decisions
- **Lessons learned**: Mistakes avoided, patterns discovered

#### 3.2 Generate Filename

Format: `<context_id>-<topic-slug>.md` where:
- `context_id`: From Step 2 (session ID or timestamp)
- `topic-slug`: 2-4 word kebab-case summary

**Examples**:
- Session ID: `claude_session_abc123-payment-gateway.md`
- Timestamp: `20260211151030-ghostty-fix.md`

Confirm with user:
```
Found: [N] decisions, [N] unsolved, [N] lessons
Suggested: contexts/20260211151030-ghostty-fix.md
1. Use this  2. Change slug  3. Cancel
```

#### 3.3 Write Context File

**Check for `obsidian-markdown` skill**: If available, use it for enhanced Obsidian compatibility (wikilinks, frontmatter, heading anchors). If not installed, AI can write files directly but should suggest installing the skill for better Obsidian integration.

**CRITICAL**: Use [references/CONTEXT_TEMPLATE.md](references/CONTEXT_TEMPLATE.md) as reference to create `docs/notes/contexts/<filename>.md`.

**DO NOT deviate from template structure**. Use the template as-is and fill in placeholders.

**MANDATORY Pre-Write Checklist**:

Before writing the file, verify:
- [ ] YAML frontmatter is present with ALL required fields
- [ ] `context_id` field is populated (enables smart merge)
- [ ] File starts with YAML frontmatter (---), NOT plain markdown headers
- [ ] Summary section exists (MANDATORY)
- [ ] "What We Worked On" section exists (MANDATORY)
- [ ] Optional sections (Decisions, Unsolved, Lessons, Notes) are OMITTED if empty
- [ ] Lessons Learned uses `{#anchor-slug}` format if present
- [ ] All wikilinks use `[[page]]` or `[[page#anchor]]` format

**Frontmatter (REQUIRED - Copy from template)**:
```yaml
---
type: context
date: YYYY-MM-DD
time: "HH:MM"
context_id: "<current_context_id>"   # CRITICAL: enables smart merge
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
tags: [tag1, tag2]                   # Optional
project: project-name                # Optional: from git repo
---
```

**Content sections** (see template):
- **Summary** (MANDATORY) - 1-2 sentences
- **What We Worked On** (MANDATORY) - Bullet list
- **Decisions Made** (Optional - omit if none) - Use `{#anchor-slug}`
- **Still Unsolved** (Optional - omit if none) - Use `{#anchor-slug}`
- **Lessons Learned** (Optional - omit if none) - Use structured format with `{#anchor-slug}`
- **Notes** (Optional - omit if none) - Code snippets ≤15 lines

Follow **Content Quality Principles** below.

#### 3.4 Update Indexes

**`docs/notes/00-INDEX.md`**: **MUST update ALL sections**:
- Add to "Recent Updates" (keep top 5 most recent)
- Add to "Key Decisions" if context has decisions
- Add to "Open Questions" if context has unsolved items
- Add to "Recent Lessons" if context has lessons
- Update Stats (increment counts)
- Keep "Topics (MOCs)" section (update when MOCs are created)

**MANDATORY Pre-Update Checklist for 00-INDEX.md**:
- [ ] "Recent Updates" section exists and is updated
- [ ] "Topics (MOCs)" section exists
- [ ] "Key Decisions" section exists (add if context has decisions)
- [ ] "Open Questions" section exists (add if context has unsolved)
- [ ] "Recent Lessons" section exists (add if context has lessons)
- [ ] "Stats" section shows correct counts

#### 3.5 Create/Update Lessons-Learned MOC (If Error-Related Lessons Exist)

**If this context contains error-related lessons** (failures, retries, gotchas >15 min):

1. **Check if `docs/notes/mocs/lessons-learned.md` exists**:
   - If NO: Create it using [references/LESSONS_LEARNED_MOC_TEMPLATE.md](references/LESSONS_LEARNED_MOC_TEMPLATE.md) as reference
   - Add to `00-INDEX.md` under "Topics (MOCs)"

2. **Update the lessons-learned MOC**:
   - Add new lesson entry as a **LINK ONLY** (do NOT copy content)
   - Use format: `- [[contexts/<filename>#lesson-slug|Lesson Title]]`
   - Group by technology/domain

**Example**:
```markdown
# mocs/lessons-learned.md

## By Technology

**React**:
- [[contexts/2026-02-06-1430-async-loops.md#await-loops|Avoid await in loops - use Promise.all]]
```

#### 3.6 Topic-Based MOC Discovery

After creating context, check if topic appears in **3+ contexts** with no existing MOC.

```
This is the 3rd context about "[topic]":
- [context-1], [context-2], [context-3 (today)]
Create MOC: mocs/topic-name.md?
```

If confirmed: use [references/MOC_TEMPLATE.md](references/MOC_TEMPLATE.md) as reference to create the MOC, then add it to `00-INDEX.md`.

#### 3.7 Confirm

```
✓ Created: contexts/YYYY-MM-DD-HHMM-topic.md
✓ Updated: 00-INDEX.md
✓ Created: mocs/topic.md (if applicable)
✓ Created: contexts.base (if obsidian-bases installed)
```

---

### Step 4: Smart Merge

When `context_id` matches an existing file.

#### 4.1 Read + Analyze

Read existing file. Extract new info from current conversation:
- New/updated decisions
- Resolved questions (unsolved → decided)
- New unsolved questions
- New lessons, new work items

#### 4.2 Merge Logic

| Section | Same Topic | New Item |
|---------|-----------|----------|
| Decisions Made | UPDATE existing, note "Updated at HH:MM" | APPEND |
| Still Unsolved | MOVE to Decisions if resolved | APPEND |
| Lessons Learned | MERGE into existing | APPEND |
| What We Worked On | — | APPEND |

**Frontmatter**: Update `updated` timestamp. Keep `created`. Add new tags.

#### 4.3 Write + Update

1. **Update Context File**: Overwrite with merged content.
2. **Update Indexes**: Update 00-INDEX.md (Stats, Recent Updates).
3. **Update Lessons MOC**: If new lessons added:
   - Add **LINK ONLY** to `mocs/lessons-learned.md`
   - `- [[contexts/<filename>#anchor|Title]]`
   - DO NOT copy lesson content to MOC

#### 4.4 Confirm

```
✓ Updated: contexts/YYYY-MM-DD-HHMM-topic.md
Changes: [list what was added/updated/moved]
```

---

## Content Quality Principles

**Core rules**:
- **Quality over quantity**: 5 high-signal bullets > 20 noisy items
- **Keep it fresh**: Write while context is hot (< 2 min)
- **Condensed**: Bullet points, not paragraphs
- **Relevant**: "Will this matter in 3 months?"

**Section limits**:

| Section | Inclusion Rule | Format | Max |
|---------|----------------|--------|-----|
| Summary | **Mandatory** | 2-3 sentences | Overview only |
| What We Worked On | **Mandatory** | Bullets | 5-7 items |
| Decisions | **Optional** (Omit if none) | Heading + 1-2 lines | 5-7 items |
| Still Unsolved | **Optional** (Omit if none) | Heading + 1-2 lines | 3-5 items |
| Lessons Learned | **Optional** (Omit if none) | Heading + structured content | 3-5 items |
| Notes | **Optional** (Omit if none) | Code snippets (≤15 lines each) | 3-5 items |

**Important**: If a section has no content meeting the quality principles, **omit the section entirely**. Do not write "None" or empty headers.

**Lessons Learned — Special Requirements**:

For error-related lessons (failures, retries, gotchas >15 min):
- **Use heading with anchor**: `### Lesson Title {#descriptive-slug}` for deep-linking
- **Include**: What happened, root cause, solution, apply-when conditions
- **Format**:
  ```
  ### [Lesson Title] {#lesson-slug}
  
  **What Happened**: [Issue description]
  **Root Cause**: [Why it happened]
  **Solution**: [How to solve or prevent]
  **Apply When**: [Specific situations/tech/patterns]
  
  **Related**: [[mocs/topic]]
  ```
- **Use imperative mood** in MOC summary: "Avoid X", "Use Y instead of Z"

**Writing rules**:
- One idea per bullet. Include "why" for decisions.
- Code snippets: essential patterns only, not full implementations
- Skip: debugging transcripts, chat logs, obvious practices, process details, dead-ends without insights

**Include**: Non-obvious decisions with rationale, gotchas (>15 min wasted), reusable patterns, blocking questions, continuation context.

**Quality check before writing**:
- Every bullet provides NEW information (no redundancy)
- Future reader can make same decision with this info
- Helps avoid repeating mistakes
- Still relevant in 3 months

---

## Integration

**Recommended**: `obsidian-markdown` skill — If installed, use it for enhanced Obsidian compatibility (proper wikilinks, frontmatter, heading anchors). If not available, AI can write files directly, but suggest installing for better integration:

```
For optimal Obsidian compatibility, consider installing obsidian-markdown skill:
npx skills add <obsidian-markdown-repo>
```

## See Also

Use these files as references.

- [CONTEXT_TEMPLATE.md](references/CONTEXT_TEMPLATE.md)
- [MOC_TEMPLATE.md](references/MOC_TEMPLATE.md)
- [INDEX_TEMPLATE.md](references/INDEX_TEMPLATE.md)
- [LESSONS_LEARNED_MOC_TEMPLATE.md](references/LESSONS_LEARNED_MOC_TEMPLATE.md)
- [CONTEXTS_BASE_TEMPLATE.base](references/CONTEXTS_BASE_TEMPLATE.base)
- [AGENTS_LESSONS_SECTION.md](references/AGENTS_LESSONS_SECTION.md)
