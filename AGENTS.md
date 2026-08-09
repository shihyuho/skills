# AGENTS.md

## Global Constraints
- The whole repo is a single `skills` plugin for Claude Code and Codex: `.claude-plugin/{plugin,marketplace}.json` configures Claude Code; `.codex-plugin/plugin.json` plus `.agents/plugins/marketplace.json` configure Codex.
- Each skill lives at `skills/<skill>/{SKILL.md, README.md}` and is auto-discovered from the root `skills/` directory; hooks live in root `hooks/hooks.json`.
- If you add, remove, or rename anything under `skills/`, `commands/`, or `hooks/`, update `README.md` in the same change.
- In `README.md`, keep each skill's description to a single sentence.
- Every `SKILL.md` frontmatter must include `name`, `description`, and `license`. Don't add a `version` field to `.claude-plugin/{plugin,marketplace}.json` — the plugin uses commit-SHA versioning (every commit is a new version); a pinned version freezes installed users on a stale snapshot. Codex's `.codex-plugin/plugin.json` instead uses a semantic `version`.
- Treat `SKILL.md` frontmatter `name` as the canonical skill name. Keep the first H1 in `SKILL.md` and, when present, `agents/openai.yaml` `interface.display_name` exactly equal to it.
- When adding or modifying a skill, classify it under [`docs/invocation-classification.md`](docs/invocation-classification.md): apply or remove the paired invocation markers as required, and update the root `README.md` grouping.
- Hook commands reference skill-bundled scripts via `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/...` — the plugin root is the repo root.
- Avoid `_`-prefixed subdirectories; use `.`-prefixed names for hidden helpers.
- Skill evals go in the `evals/` directory next to that skill's `SKILL.md` (e.g., `skills/<skill>/evals/`).
