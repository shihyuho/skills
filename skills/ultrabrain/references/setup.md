# Hooks — Install & Uninstall

This file guides installation of two hooks that surface ultrabrain at useful moments in a Claude Code session. Installation is opt-in — only run this when the user explicitly asks. The two hooks install together as a bundle.

Trigger phrases that mean "install":

- "install ultrabrain hooks", "setup ultrabrain reminders", "enable ultrabrain hooks", "裝 ultrabrain hook"

Trigger phrases that mean "uninstall":

- "uninstall ultrabrain hooks", "remove ultrabrain hooks", "disable ultrabrain reminders", "移除 ultrabrain hook"

## What the hooks do

Both hooks emit Claude Code hook JSON payloads that inject a one-line message into Claude's context. Both are silent (exit 0 with no output) when `~/.ultrabrain/` does not exist, so non-ultrabrain users see nothing. Both never fail the session.

### `SessionStart` — vault awareness

Fires once at session start. Injects current vault stats so Claude is aware the vault is available from the user's first message.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "ultrabrain vault available at ~/.ultrabrain/ — 42 wiki pages, 3 unprocessed raw entries, last ingest 2026-04-13T10:12:33Z. Consult index.md before answering factual questions that may be covered."
  }
}
```

### `PreCompact` — capture reminder before compaction

Fires before Claude Code compacts context. Injects a reminder that the user should capture any important session content before detail is lost. Static message — no vault stats.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "additionalContext": "Context compaction is imminent. If this session contains decisions, patterns, or facts worth keeping beyond compaction, say 'capture X' to file them into ~/.ultrabrain/raw/ before detail is lost."
  }
}
```

## Install

1. **Copy both scripts** to the user-level hooks directory:
   ```bash
   cp <skill-path>/references/hooks/session-start.sh ~/.claude/hooks/using-ultrabrain-session.sh
   cp <skill-path>/references/hooks/pre-compact.sh ~/.claude/hooks/using-ultrabrain-precompact.sh
   chmod +x ~/.claude/hooks/using-ultrabrain-session.sh ~/.claude/hooks/using-ultrabrain-precompact.sh
   ```
   (Replace `<skill-path>` with the actual path where this skill is installed. Create `~/.claude/hooks/` if it doesn't exist.)

2. **Merge the hook entries into `~/.claude/settings.json`** — discipline for JSON editing:

   **Step 1: Read.** Load `~/.claude/settings.json` with the Read tool first. If it doesn't exist, create it with the final shape shown below. The user sees the current state in the conversation.

   **Step 2: Plan the diff.** Check whether `SessionStart` or `PreCompact` entries already point at the ultrabrain scripts (idempotency check per hook). Skip any hook that's already installed. Determine the minimal merge: add missing entries without disturbing unrelated ones.

   **Step 3: Show the user the proposed diff** as a code block before applying. Example (both hooks new):
   ```diff
     "hooks": {
   +   "SessionStart": [
   +     {
   +       "hooks": [
   +         {
   +           "type": "command",
   +           "command": "~/.claude/hooks/using-ultrabrain-session.sh"
   +         }
   +       ]
   +     }
   +   ],
   +   "PreCompact": [
   +     {
   +       "hooks": [
   +         {
   +           "type": "command",
   +           "command": "~/.claude/hooks/using-ultrabrain-precompact.sh"
   +         }
   +       ]
   +     }
   +   ]
     }
   ```

   **Step 4: Wait for confirmation.** Do not edit until the user explicitly approves.

   **Step 5: Apply with `Edit`.** Use anchored `old_string` / `new_string` pairs; never rewrite the whole file. If the file doesn't already have a `hooks` key, add it. If `hooks.SessionStart` or `hooks.PreCompact` don't exist, add each as a single-element array.

   The final entry shape for both hooks:
   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "~/.claude/hooks/using-ultrabrain-session.sh"
             }
           ]
         }
       ],
       "PreCompact": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "~/.claude/hooks/using-ultrabrain-precompact.sh"
             }
           ]
         }
       ]
     }
   }
   ```

3. **Confirm**: tell the user both hooks are installed. `SessionStart` fires at the start of each new Claude Code session; `PreCompact` fires whenever Claude Code is about to compact context.

## Vault permissions (optional)

To let ultrabrain operations (`bootstrap`, `capture`, `ingest`, `query`, `lint`) read and write the vault without per-session permission prompts, add these three entries to `~/.claude/settings.json` under `permissions.allow`:

```json
"Read(~/.ultrabrain/**)",
"Write(~/.ultrabrain/**)",
"Edit(~/.ultrabrain/**)"
```

Use the same Read → diff → confirm → Edit discipline as the hook merge: load the file, show the proposed additions as a diff, wait for confirmation, then Edit with anchored `old_string` / `new_string` pairs.

Without these, the first vault touch each session — a raw write during `capture`, a wiki edit during `ingest`, or a page update during `lint` — will trigger a permission prompt.

To remove them, delete the three entries with the same Read → diff → confirm → Edit flow.

## Uninstall

1. **Remove both scripts**:
   ```bash
   rm -f ~/.claude/hooks/using-ultrabrain-session.sh ~/.claude/hooks/using-ultrabrain-precompact.sh
   ```

2. **Remove the entries from `~/.claude/settings.json`** using the same Read → diff → confirm → Edit discipline:
   - Read the current settings.
   - Locate the entries whose commands point to `using-ultrabrain-session.sh` and `using-ultrabrain-precompact.sh`.
   - Show the user the diff (entries being removed).
   - Wait for confirmation, then Edit to remove exactly those entries. Leave other hook entries untouched. If removing an entry leaves an empty array, either remove the key or leave the empty array — both are valid.

3. **Confirm uninstall** with the user.

## Notes

- `~/.claude/settings.json` is a user-global file. Other skills and user customizations may share it. **Never overwrite wholesale** — only edit the minimal entries we own.
- The two hooks install as a bundle, but if a user wants to remove just one, they can ask ("remove only the PreCompact hook") and the same Read → diff → confirm → Edit flow applies to a single entry.
- If the user stores their Claude Code config somewhere other than `~/.claude/` (rare), ask before proceeding.
- This skill does not ship a `SessionEnd` hook in v1.0.0. `SessionEnd`'s `additionalContext` behavior wasn't conclusively verified (the session is ending, so there may be no consumer for the injected text). Revisit in a later version if the need surfaces.
