---
name: harvest
description: "Use when users ask to capture conversation decisions, problems, and lessons into persistent notes (e.g. 'harvest', '/harvest', 'save this to second brain', 'document this work')."
license: MIT
metadata:
  author: shihyuho
  version: "1.5.0"
---

# Harvest

Capture high-signal conversation knowledge into `docs/notes/` for reuse across sessions.

> **Terminology**: `harvest` is the skill name (the action of capturing knowledge). The second brain it builds belongs to the project — name it `[Project Name] Second Brain`, not "Harvest".

## When to Trigger

**Explicit request**:
- "harvest", "/harvest"
- "harvest this", "harvest this conversation"
- "save this to second brain"
- "document this work", "capture this knowledge"

**Natural breakpoints** — AI may **suggest** (never auto-execute):
- Significant decision made
- Complex problem solved after multiple attempts
- Important lesson learned
- Discussion wrapping up with valuable content

```
We just [made a decision/solved X/learned Y].
Would you like me to update the second brain?
```

Wait for user confirmation. Never auto-execute.

## Non-Negotiables

- Never auto-execute. Always wait for explicit user confirmation.
- Use template files as the single source of structure.
- Keep `context_id` in frontmatter for smart merge.
- Keep MOCs as index files: link to context anchors, do not duplicate full lesson content.
- Omit optional empty sections. Do not write empty headers or "None" placeholders.
- Keep behavior logic in this file; keep structure/manifest data in `references/`.
- Use list-first formatting for context content. Use tables only for short, fixed-width, easy-to-scan fields.

## Quick Start

1. Ensure `docs/notes/` exists (initialize when missing).
2. Run lesson review for this harvest run.
3. Detect `context_id` and check whether matching context file exists.
4. Create new context or smart-merge existing context.
5. Update `docs/notes/00-INDEX.md` and related MOCs.
6. Confirm created/updated files to user.

## Workflow

### Phase 1: Prepare

1. Initialize second brain storage when `docs/notes/` is missing:
   - Use [references/initialization-manifest.md](references/initialization-manifest.md) as the single source for initialization inventory.
   - Follow idempotent behavior: create missing files/directories, preserve existing files unless explicit update is requested.
   - Check `AGENTS.md` then `CLAUDE.md`; if both exist or neither exists, ask user which file to append, then append section from [references/agents-lessons-section.md](references/agents-lessons-section.md).
   - Do not own or maintain `.base` template syntax in this skill. If `obsidian-bases` is available, delegate default base-file creation to `obsidian-bases` using [references/bases-generation-spec.md](references/bases-generation-spec.md).
2. Mandatory lesson review for this harvest run:
   - Read `docs/notes/00-INDEX.md` when available.
   - Scan `docs/notes/mocs/lessons-learned.md` when available.
   - Apply matched lessons (tech, operation type, error pattern).

### Phase 2: Detect + Route

1. Build `context_id`:
   - Prefer helper script `scripts/context_id.py` (Python stdlib only, no third-party packages).
   - Default call: `python3 scripts/context_id.py --format json` (or `python` when `python3` is unavailable).
   - Stateless policy (no state file): env keys (`OPENCODE_*_ID`/`*_ID`) -> optional `--infer-latest-session` -> generated `ctx-YYYYMMDDHHMMSS-<hex6>`.
   - Do not pass `--infer-latest-session` by default. Use it only when the user explicitly requests latest-session inference.
   - If script is unavailable or fails, use inline fallback: first env var matching `*SESSION*ID*`/`*CONVERSATION*ID*`/`*THREAD*ID*`; otherwise generate `ctx-YYYYMMDDHHMMSS-<hex6>`.
2. Look for `docs/notes/contexts/<context_id>-*.md`.

| Condition | Action |
|---|---|
| Matching context file exists | Run **Phase 4 (Smart Merge)** |
| No matching context file | Run **Phase 3 (New Context)** |
| User rejects suggested filename | Ask for new slug and regenerate filename |
| User cancels confirmation | Stop without writing files |

### Phase 3: New Context

1. Extract high-signal items: work, decisions (with rationale), unsolved, lessons, optional source notes.
   - Use stable item IDs for merge safety: `D-*`, `Q-*`, `LL-*`.
   - Keep technical signal high: merge routine process/SOP chatter into one short note instead of many standalone decisions.
   - If planning files (`task_plan.md`, `findings.md`, `progress.md`) are present, capture medium-density snapshots (`conclusion + evidence + source note`) into context content.
   - Do not copy full planning files. Do not create Obsidian wikilinks to files outside `docs/notes/`.
   - Exclude harvest-process artifacts from captured knowledge (command menus, filename suggestion prompts, merge/update status lines, and other capture bookkeeping).
2. Generate filename `<context_id>-<topic-slug>.md` and confirm:

```
Found: [N] decisions, [N] unsolved, [N] lessons
Suggested: contexts/<context_id>-<topic-slug>.md
1. Use this  2. Change slug  3. Cancel
```

3. Create `docs/notes/contexts/<filename>.md` from [references/context-template.md](references/context-template.md).
4. Use `obsidian-markdown` when available for wikilinks/frontmatter/anchors.
5. Update `docs/notes/00-INDEX.md` according to [references/index-template.md](references/index-template.md):
   - Recent Updates (top 5), Topics, Key Decisions, Open Questions, Recent Lessons, Stats.
6. Manage MOCs:
   - Lessons MOC: for error-related lessons (>15 min impact), ensure `docs/notes/mocs/lessons-learned.md` exists via [references/lessons-learned-moc-template.md](references/lessons-learned-moc-template.md), then append links only.
   - Topic MOC: when a topic appears in 3+ contexts without MOC, ask user first; create from [references/moc-template.md](references/moc-template.md) after confirmation.
7. Confirm:

```
✓ Created: contexts/<filename>.md
✓ Updated: 00-INDEX.md
✓ Updated: mocs/lessons-learned.md (when relevant)
✓ Created: mocs/<topic>.md (when relevant)
```

### Phase 4: Smart Merge

1. Read the existing context file.
2. Merge new items from current conversation.

| Section | Existing Topic | New Item |
|---|---|---|
| Decisions Made | Match by `D-*` first, update entry and preserve anchor | Append |
| Still Unsolved | Match by `Q-*`; move resolved items to Decisions with trace | Append |
| Lessons Learned | Match by `LL-*` first; merge same lesson and preserve anchor | Append |
| What We Worked On | Keep existing | Append |
| Source Notes | Merge by source note signature if duplicated | Append |

3. Update frontmatter (`updated`, tags), keep `created` unchanged.
4. Update `00-INDEX.md` stats and recent updates.
5. Update `mocs/lessons-learned.md` with links only when new error-related lessons were added.
6. Confirm:

```
✓ Updated: contexts/<filename>.md
Changes: [added/updated/moved items]
```

## Content Quality Rules

- Quality over quantity: concise, reusable, high-signal notes.
- One idea per bullet; include rationale for decisions.
- Keep content relevant for future reuse (3+ months horizon).
- Skip raw transcripts, dead ends without insight, and obvious process noise.
- Exclude harvest operational chatter: confirmation menus, `created/updated/skipped` summaries, and "how harvest processed this" narration unless it records a reusable lesson.
- Use stable IDs (`D-*`, `Q-*`, `LL-*`) with anchored headings for merge-safe entries.
- Prefer list-first sections for long text. Use tables only when each cell stays short (for example `ID | Question | Next`).
- Avoid duplicate restatement: decision headings should carry title intent; item body should add why/impact.
- For lessons, default to compact triad (`Issue`, `Root Cause`, `Fix`); add `Guardrail`/`Apply When` only when they provide non-obvious value.
- Avoid repeating `Related` links on every item; prefer one section-level related MOC link.
- Omit low-signal metadata (`Deadline`, `Carry-Over`) unless it materially changes follow-up decisions.
- For carry-over items from prior sessions, label clearly and avoid presenting them as new outcomes.
- For planning-derived content, store medium-density snapshots (`conclusion + evidence + source note`) in context files; avoid external-file wikilinks outside `docs/notes/`.

Recommended section limits:

| Section | Requirement | Typical Size |
|---|---|---|
| Summary | Required | 1-2 sentences |
| What We Worked On | Required | 5-7 bullets |
| Decisions | Optional | up to 5 items |
| Still Unsolved | Optional | up to 3-5 items |
| Lessons Learned | Optional | up to 3 items |
| Source Notes | Optional | up to 3-5 items |
| Notes | Optional | short snippets only |

---

## Integration

**Recommended**: `obsidian-markdown` skill for enhanced Obsidian compatibility. Without it, AI may write files directly and suggest installation:

```
For optimal Obsidian compatibility, consider installing obsidian-markdown skill:
npx skills add <obsidian-markdown-repo>
```

**Optional companion**: `obsidian-bases` for `.base` file generation.

- This skill does not own `.base` syntax templates.
- When `obsidian-bases` is available, delegate generation of default base files to that skill.
- Keep desired base content in [references/bases-generation-spec.md](references/bases-generation-spec.md), not `.base` syntax templates.
- If `obsidian-bases` is unavailable, skip `.base` creation and continue markdown-only harvest flow.

**Optional companion**: `planning-with-files` for stronger in-progress capture.

- This skill remains fully functional without it.
- When available, this skill may consume planning outputs (`task_plan.md`, `findings.md`, `progress.md`) as snapshot sources, then persist reusable knowledge into `docs/notes/contexts/`.
- Prefer provenance text over external links when planning files are outside Obsidian vault scope.

## See Also

Use these files as references (single source for structure and formats).

- [context-template.md](references/context-template.md)
- [moc-template.md](references/moc-template.md)
- [index-template.md](references/index-template.md)
- [lessons-learned-moc-template.md](references/lessons-learned-moc-template.md)
- [bases-generation-spec.md](references/bases-generation-spec.md)
- [agents-lessons-section.md](references/agents-lessons-section.md)
- [initialization-manifest.md](references/initialization-manifest.md)
- [context_id.py](scripts/context_id.py)
