---
name: promote-claude-settings
description: Promote entries from the current project's .claude/settings.local.json into the global ~/.claude/settings.json. Use when user says "promote settings", "升級 settings", "sync settings to global", "把 local settings 搬到全域", or wants to move project-local Claude Code settings to global scope.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# promote-claude-settings

Interactively promote entries from `.claude/settings.local.json` (project) to `~/.claude/settings.json` (global).

## Workflow

### 1. Read both files

- Read `.claude/settings.local.json` from the current project root
- Read `~/.claude/settings.json`
- If local file is missing or empty (`{}`), tell the user and stop

### 2. Diff

Compare every top-level key in local against global. For array values (e.g. `permissions.allow`), compare per-element, not the whole array.

Classify each entry:

| Status | Meaning |
|--------|---------|
| **New** | Not in global — can be added |
| **Exists** | Already identical in global — skip |
| **Conflict** | Present in global with a different value |

Present the full diff summary to the user before asking anything.

### 3. Interactive confirm (per item)

Walk through every non-"Exists" entry and ask:

- **New** → "Add to global? (Y/N)"
- **Conflict** → show both values, ask "Use local / Keep global / Skip"

Use the question tool for each prompt.

### 4. Write to global

Apply confirmed changes to `~/.claude/settings.json` with the Edit tool. If the file does not exist, create it.

### 5. Cleanup confirm

Ask whether to remove promoted entries from `settings.local.json`. If the user agrees and the file becomes `{}`, ask whether to delete it entirely.

## Edge cases

- `~/.claude/settings.json` missing → create with confirmed entries
- JSON parse error → report and stop; do not attempt repair
- Do NOT touch `.claude/settings.json` (project shared settings)
