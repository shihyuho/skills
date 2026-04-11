# AGENTS.md

## Global Constraints
- If you change `skills/fanfuaji/scripts/`, also run `python3 -m pytest skills/fanfuaji/tests/test_fanfuaji_security.py -v`.
- Every published directory under `skills/` must include `SKILL.md` and `README.md`.
- If you add, remove, or rename anything under `skills/`, update the corresponding lists in `README.md` and `.claude-plugin/marketplace.json` (including version) in the same change.
- Every `SKILL.md` frontmatter must include `license`, `metadata.author`, and `metadata.version`. The version in `SKILL.md` must match the corresponding entry in `.claude-plugin/marketplace.json`.
- Under `skills/`, avoid `_`-prefixed subdirectories; use `.`-prefixed names for hidden helpers.
- Skill evals go in the `evals/` directory under the skill's own directory (e.g., `skills/<name>/evals/`).
