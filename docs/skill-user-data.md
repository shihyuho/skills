# Skill User Data

This document defines where this repository's skills keep skill-owned data that persists across invocations. It fixes only the config and cache roots; each skill still decides whether it needs such data, and the file names and structure inside its own directory.

## Classify first, then choose the directory

Classify by what happens when the data is deleted:

- **Config**: deleting it loses user settings, credentials, presets, durable metadata or state, changes later behavior, or makes the normal flow wait for reconfiguration, input or migration before it can continue equivalently. It goes in the config directory.
- **Cache**: after deletion, the normal flow downloads or recomputes it automatically with an equivalent result; only time, network or compute cost is affected, and no sole copy of user data is lost. It goes in the cache directory.

When unsure, classify as config. Cache must be safe to delete and recover automatically through the normal flow; never keep secrets, user settings or data that cannot be rebuilt automatically only in cache.

## Root resolution

The config root and the cache root resolve separately; they never share one root. Each resolves through the same order and stops at the first hit:

1. **Effective user-level instructions**: when the agent's effective user-level instructions explicitly name a skill config root or cache root, use that path for the matching kind. The agent does not search for setting files that are not loaded.
2. **Default location**:
   - Config root: `~/.config/shihyuho/skills`
   - Cache root: `~/.cache/shihyuho/skills`

`~` is the current user's home directory. Every operating system uses the same default locations, with no switch to XDG, `APPDATA`, `LOCALAPPDATA` or other platform directories. When the instructions name only one of the roots, the other still resolves through its own order.

When a higher-priority root is explicitly set but unusable, report the path and the reason instead of silently falling back to the next one.

## Per-skill directory

After resolving the root, create the skill's directory under the canonical `name` from its `SKILL.md` frontmatter:

```text
<resolved-config-root>/<canonical-skill-name>/
<resolved-cache-root>/<canonical-skill-name>/
```

For example, with the default roots, `scope-it` uses:

```text
~/.config/shihyuho/skills/scope-it/
~/.cache/shihyuho/skills/scope-it/
```

A skill creates only the kinds it actually needs, not both directories by default. It may arrange file names and subdirectories freely inside its own config or cache directory; new documents, examples and code never write this data into the skill source, the installation directory or the marketplace installation cache.

## Scope

- Skill-owned data created by the user by hand and data the skill generates are both classified under this document.
- Deliverables at a user-specified output location, and files managed by the repository or workspace itself, are not skill-owned data.
- Temporary data used only during one run and cleared when it ends is neither config nor cache.
- Plain environment variables, the system keychain, `gh auth`, the kubectl credential store, the agent host's native hook or plugin settings, and other data owned by external tools keep their native handling; they are not copied into these directories.
- This document does not require a shared CLI flag, resolver library or host protocol. Each agent and skill implements the same classification and resolution in its own execution environment.

## Legacy paths and migration

When an existing skill already keeps config or cache elsewhere, apply these rules to each kind of data separately:

1. The canonical config or cache directory always wins.
2. Only when the matching canonical data is absent may the skill fall back to reading the same kind of legacy data, read-only.
3. A legacy fallback may stay indefinitely, but every hit warns the user and names the matching canonical destination.
4. Never merge canonical and legacy content, and never treat legacy config as cache.
5. Move legacy data only when the user explicitly asks for the migration.

When migrating:

- First confirm, read-only, the exact source, data kind, destination and any conflict.
- Create the matching canonical skill directory without overwriting or merging canonical data that already exists.
- After moving, confirm the new location works using the skill's own verification; across file systems, finish a safe copy and its verification before removing the legacy original.
- Unless the user asks otherwise, leave no second usable copy of a secret behind.
- Report the data kind, the old path, the new path and the verification result.
