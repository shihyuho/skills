# AGENTS.md

## Global Constraints
- If you change `skills/fanfuaji/scripts/`, also run `python3 -m pytest skills/fanfuaji/tests/test_fanfuaji_security.py -v`.
- Every published directory under `skills/` must include `SKILL.md` and `README.md`.
- If you add, remove, or rename anything under `skills/`, update the corresponding entries in `README.md`, in `.claude-plugin/marketplace.json` (plugin entry, version, `source`), and the skill's own `.claude-plugin/plugin.json` in the same change.
- Every `SKILL.md` frontmatter must include `name`, `description`, and `license`. Per-plugin versions live in `.claude-plugin/marketplace.json`, not in `SKILL.md`.
- Each skill plugin needs `.claude-plugin/plugin.json` at its `source` root with `{"name": "<name>", "skills": ["./"]}`. Plugins that nest multiple skills (e.g. `reveries`) omit `skills` and rely on default `skills/` auto-discovery.
- Under `skills/`, avoid `_`-prefixed subdirectories; use `.`-prefixed names for hidden helpers.
- Skill evals go in the `evals/` directory under the skill's own directory (e.g., `skills/<name>/evals/`).
