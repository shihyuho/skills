# Hooks — Install & Uninstall

These hooks make the skill's preferences surface automatically. Installation is
opt-in — only run this when the user explicitly asks.

> **If you installed the `sdkman` plugin from the marketplace (Claude Code),
> skip this file.** The plugin already ships these hooks via `hooks/hooks.json`
> and they are active automatically; installing them again would make them fire
> twice. This manual setup is for the `npx skills add` style install (just the
> skill directory copied, no plugin hook wiring) and for **Codex**.

Requirements: Python 3.8+ on `PATH`. No `jq`, `grep`, or POSIX shell needed.

## What the hooks do

Neither hook ever forces a version — a project's declared JDK is a default the
user may override, so enforcement would be wrong.

- **`SessionStart` (advisory nudge)** — `session-start.py`. Once per session, if
  the machine has SDKMAN and the directory is a JVM project, injects a one-line
  reminder to prefer `sdk` for version changes (over `JAVA_HOME` edits or
  jenv/asdf) and to treat project-declared versions as defaults the user can
  override. Silent in non-JVM directories or without SDKMAN.
- **`PostToolUse` (reactive catch-all)** — `post-build-version-check.py`. After
  any Bash call, scans output for Java version-mismatch error signatures
  (`UnsupportedClassVersionError`, `invalid target release`, `Unsupported class
  file major version`, `requires a Java N toolchain`, …). Because it keys off
  the *error*, it covers builds launched through any wrapper (make, just, npm
  scripts, custom shell scripts). On a hit it injects guidance to switch via
  SDKMAN and retry. It only fires on a real failure, so it never second-guesses
  an intentional version choice.

Both stay silent when `$SDKMAN_DIR/bin/sdkman-init.sh` is absent, and any
internal error exits 0 — they never break a build.

The **same two scripts run unchanged on both Claude Code and Codex** — both
deliver `SessionStart`/`PostToolUse` payloads with the same field names (`cwd`,
`tool_name`, `tool_response`) and accept the same `additionalContext` responses.
Only the wiring differs.

## Claude Code

### Install (Claude Code)

1. **Copy both scripts** into the user-level hooks directory (create it if
   needed):

   ```bash
   mkdir -p ~/.claude/hooks
   cp <skill-path>/references/hooks/session-start.py            ~/.claude/hooks/sdkman-session-start.py
   cp <skill-path>/references/hooks/post-build-version-check.py ~/.claude/hooks/sdkman-post-build-version-check.py
   chmod +x ~/.claude/hooks/sdkman-session-start.py ~/.claude/hooks/sdkman-post-build-version-check.py
   ```

   Replace `<skill-path>` with where this skill is installed. On Windows the
   `chmod` is unnecessary — the interpreter is named explicitly below.

2. **Merge the hook entries into `~/.claude/settings.json`.** Discipline for
   editing this shared, user-global file:

   - **Read** it first with the Read tool. If it doesn't exist, create it with
     the shape below.
   - **Plan the diff:** check whether `SessionStart`/`PostToolUse` entries
     already point at the sdkman scripts (idempotency — skip any already
     present). Add missing entries without disturbing unrelated ones.
   - **Show the user the proposed diff** as a code block, then **wait for
     confirmation**.
   - **Apply with `Edit`** using anchored `old_string`/`new_string` pairs; never
     rewrite the whole file.

   **macOS / Linux** entry shape:

   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "matcher": "startup|resume|clear",
           "hooks": [
             { "type": "command", "command": "python3 ~/.claude/hooks/sdkman-session-start.py" }
           ]
         }
       ],
       "PostToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             { "type": "command", "command": "python3 ~/.claude/hooks/sdkman-post-build-version-check.py" }
           ]
         }
       ]
     }
   }
   ```

   **Windows** — use the `py` launcher and `%USERPROFILE%`:

   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "matcher": "startup|resume|clear",
           "hooks": [
             { "type": "command", "command": "py %USERPROFILE%\\.claude\\hooks\\sdkman-session-start.py" }
           ]
         }
       ],
       "PostToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             { "type": "command", "command": "py %USERPROFILE%\\.claude\\hooks\\sdkman-post-build-version-check.py" }
           ]
         }
       ]
     }
   }
   ```

3. **Confirm** with the user.

### Uninstall (Claude Code)

1. Remove the scripts:

   ```bash
   rm -f ~/.claude/hooks/sdkman-session-start.py ~/.claude/hooks/sdkman-post-build-version-check.py
   ```

2. Remove the `SessionStart`/`PostToolUse` entries whose commands reference the
   `sdkman-*` scripts from `~/.claude/settings.json`, using the same Read → diff
   → confirm → Edit discipline. Leave other hook entries untouched.

3. Confirm with the user.

## Codex

Codex hooks use the same events, payload schema, and response format as Claude
Code, so the scripts are reused as-is — only the config file differs. Hooks live
in `~/.codex/hooks.json` (user-global) or `<repo>/.codex/hooks.json`
(project-local); a `[hooks]` table in `config.toml` works too, but the JSON file
is cleaner to merge.

### Install (Codex)

1. **Copy both scripts** into a Codex hooks directory:

   ```bash
   mkdir -p ~/.codex/hooks
   cp <skill-path>/references/hooks/session-start.py            ~/.codex/hooks/sdkman-session-start.py
   cp <skill-path>/references/hooks/post-build-version-check.py ~/.codex/hooks/sdkman-post-build-version-check.py
   chmod +x ~/.codex/hooks/sdkman-session-start.py ~/.codex/hooks/sdkman-post-build-version-check.py
   ```

2. **Merge into `~/.codex/hooks.json`** using the same Read → diff → confirm →
   Edit discipline (create the file with this shape if absent). Use an **absolute
   path** in `command` — Codex does not expand `~`:

   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "matcher": "startup|resume|clear",
           "hooks": [
             { "type": "command", "command": "python3 /ABSOLUTE/HOME/.codex/hooks/sdkman-session-start.py", "timeout": 30 }
           ]
         }
       ],
       "PostToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             { "type": "command", "command": "python3 /ABSOLUTE/HOME/.codex/hooks/sdkman-post-build-version-check.py", "timeout": 30 }
           ]
         }
       ]
     }
   }
   ```

   Replace `/ABSOLUTE/HOME` with the real home path (e.g. `/Users/you`). On
   Windows, use the `py` launcher and the full `%USERPROFILE%`-expanded path.

3. **Confirm** with the user.

### Uninstall (Codex)

1. Remove the scripts:

   ```bash
   rm -f ~/.codex/hooks/sdkman-session-start.py ~/.codex/hooks/sdkman-post-build-version-check.py
   ```

2. Remove the `SessionStart`/`PostToolUse` entries referencing the `sdkman-*`
   scripts from `~/.codex/hooks.json` (same Read → diff → confirm → Edit
   discipline). Leave other hook entries untouched.

3. Confirm with the user.

## Notes

- `~/.claude/settings.json` and `~/.codex/hooks.json` are shared with other
  skills. **Never overwrite wholesale** — only edit the entries we own.
- Neither hook enforces a version. Proactive *enforcement* was deliberately left
  out: a project's declared JDK is a default, and the user must stay free to
  build or test under a different version. The SessionStart nudge states the
  preference; the PostToolUse hook only reacts to genuine build failures.
