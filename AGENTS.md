# AGENTS.md

## Global Constraints
- The whole repo is a single Claude Code plugin named `skills`. The plugin manifest is `.claude-plugin/plugin.json` at the repo root; `.claude-plugin/marketplace.json` exposes it as the lone plugin (`source: "."`).
- Each skill lives at `skills/<skill>/{SKILL.md, README.md}` and is auto-discovered from the root `skills/` directory. Slash commands live in root `commands/`, hooks in root `hooks/hooks.json`.
- If you add, remove, or rename anything under `skills/`, `commands/`, or `hooks/`, update `README.md` in the same change.
- In `README.md`, keep each skill's description to a single sentence.
- Every `SKILL.md` frontmatter must include `name`, `description`, and `license`. Don't add a `version` field to `.claude-plugin/{plugin,marketplace}.json` — the plugin uses commit-SHA versioning (every commit is a new version); a pinned version freezes installed users on a stale snapshot.
- Hook commands reference skill-bundled scripts via `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/...` — the plugin root is the repo root.
- Avoid `_`-prefixed subdirectories; use `.`-prefixed names for hidden helpers.
- Skill evals go in the `evals/` directory next to that skill's `SKILL.md` (e.g., `skills/<skill>/evals/`).
