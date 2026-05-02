# AGENTS.md

## Global Constraints
- Each plugin lives at `plugins/<plugin>/` with its skill content under `plugins/<plugin>/skills/<skill>/{SKILL.md, README.md}`. A plugin may host multiple skills (e.g. `reveries`).
- If you add, remove, or rename anything under `plugins/`, update the corresponding entries in `README.md`, in `.claude-plugin/marketplace.json` (plugin entry, version, `source`), and the plugin's own `.claude-plugin/plugin.json` in the same change.
- Every `SKILL.md` frontmatter must include `name`, `description`, and `license`. Per-plugin versions live in `.claude-plugin/marketplace.json`, not in `SKILL.md`.
- Each plugin needs `.claude-plugin/plugin.json` at its `source` root with at least `{"name": "<plugin>"}`. Skills are auto-discovered from the default `skills/` directory inside the plugin root.
- Under `plugins/`, avoid `_`-prefixed subdirectories; use `.`-prefixed names for hidden helpers.
- Skill evals go in the `evals/` directory next to that skill's `SKILL.md` (e.g., `plugins/<plugin>/skills/<skill>/evals/`).
