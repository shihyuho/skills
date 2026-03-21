# AGENTS.md

## Scope
- This repository publishes agent skills, not a traditional application.
- Most edits are Markdown under `skills/` and `commands/`; executable code is mainly in `skills/fanfuaji/scripts/`.
- Read `README.md` first, then the touched skill's `SKILL.md` and adjacent files.

## Editor Rules
- No `.cursorrules` file is present.
- No `.cursor/rules/` directory is present.
- No `.github/copilot-instructions.md` file is present.
- Do not imply hidden Cursor or Copilot policy when those files are absent.

## Validation
- There is no build pipeline and no dedicated lint runner.
- `package.json` is metadata only; do not look for npm scripts.
- Repo-wide verification is `npx --yes skills-ref validate <skill-dir>`.
- CI in `.github/workflows/validate-skills.yml` validates discovered `skills/*/SKILL.md` directories with `skills-ref`; it does not run pytest.
- Python tests exist only for `fanfuaji`; if you change `skills/fanfuaji/scripts/`, also run `python3 -m pytest skills/fanfuaji/scripts/test_fanfuaji_security.py -v`.
- For a single pytest test, use `python3 -m pytest skills/fanfuaji/scripts/test_fanfuaji_security.py::test_name -v`.

## High-Value Constraints
- Every published skill directory under `skills/` must include `SKILL.md`.
- If you add, remove, or rename items under `skills/` or `commands/`, update `README.md` in the same change.
- Keep `README.md` lists in sync for both published skills and included commands.
- Under `skills/`, avoid `_`-prefixed subdirectories; prefer `.`-prefixed names for hidden helpers.
- Treat checked-in workflows and tests as the source of truth for verification behavior.
- Do not treat local planning or workspace artifacts as canonical repo policy unless checked-in docs or workflows support them.

## Working Style
- Prefer small, targeted edits; many files here are normative instructions.
- Match the existing style of the touched file rather than importing a new formatting system.
- When a workflow is not defined by the repo, say so plainly instead of inventing one.
