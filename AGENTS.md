# AGENTS.md

## Purpose
- This repository is a published collection of agent skills, not a traditional application.
- Most edits are Markdown under `skills/`; the main executable code is Python under `skills/fanfuaji/scripts/`.
- Prefer repo conventions and CI behavior over generic app assumptions.

## Instruction Sources
- Primary repo instructions live in this file, `README.md`, and each skill's `SKILL.md`.
- No `.cursorrules` file is present.
- No `.cursor/rules/` directory is present.
- No `.github/copilot-instructions.md` file is present.
- Do not invent extra Cursor or Copilot rules; none are checked into this repo today.

## Repository Shape
- `skills/<skill-name>/` contains one published skill.
- Each valid skill directory must include `SKILL.md`.
- Support material usually lives beside it in `references/`, `scripts/`, or `README.md`.
- `commands/` contains reusable command templates, currently centered on `lessons-learned`.
- `.github/workflows/validate-skills.yml` is the canonical validation reference.
- If you add, remove, or rename items under `skills/` or `commands/`, update `README.md` in the same change.
- Keep `README.md` lists in sync: `Available Skills` for `skills/`, `Included Commands` for `commands/`.
- Use the `skill-creator` skill when adding a new skill or adjusting an existing one.

## Build, Lint, and Test
- There is no build pipeline, no transpile step, and no `package.json` scripts.
- There is no dedicated lint command configured via ESLint, Prettier, Biome, Ruff, or similar.
- The main repo-wide verification is skill validation through `skills-ref`.
- The only checked-in unit tests are pytest tests for `fanfuaji`.

### Core Commands
```bash
# Install all published skills from this repository
npx skills add shihyuho/skills --skill='*'

# Install one skill only
npx skills add shihyuho/skills --skill=fanfuaji

# Validate one skill directory (matches CI behavior)
npx --yes skills-ref validate skills/fanfuaji

# Validate all skill directories locally
for dir in skills/*; do
  [ -f "$dir/SKILL.md" ] && npx --yes skills-ref validate "$dir"
done

# Run the checked-in pytest file
python3 -m pytest skills/fanfuaji/scripts/test_fanfuaji_security.py -v
```

### Single-Test Commands
```bash
# Run one exact pytest test
python3 -m pytest \
  skills/fanfuaji/scripts/test_fanfuaji_security.py::test_deny_blocked_secret_filenames \
  -v

# Run a subset by name pattern
python3 -m pytest \
  skills/fanfuaji/scripts/test_fanfuaji_security.py \
  -k allowlist \
  -v

# Validate one skill while iterating on docs
npx --yes skills-ref validate skills/lessons-learned
```

### Command Notes
- Use `npx --yes skills-ref validate <skill-dir>` after editing any `SKILL.md` or skill package content.
- If you change multiple skills, run the local validation loop across all `skills/*` directories.
- If you touch only `skills/fanfuaji/scripts/`, run both `skills-ref validate skills/fanfuaji` and the relevant pytest command.
- Do not claim a lint step passed; this repo currently has no dedicated lint runner.

## Verification Checklist
- `SKILL.md` still validates with `skills-ref`.
- Example commands in docs still match real file paths and filenames.
- Skill directory names under `skills/` still avoid `_`-prefixed subdirectories.
- Python changes in `fanfuaji` still pass the targeted pytest command.

## General Style
- Match existing repo style instead of importing a new formatting system.
- Keep documentation deterministic, explicit, and agent-executable.
- Prefer concise, operational wording over marketing language.
- When documenting commands, use exact paths, flags, and expected behavior.
- If the repo does not define a workflow, say so plainly.

## Markdown Style
- Use ATX headings (`#`, `##`, `###`), not Setext headings.
- Prefer short sections, bullets, tables, and numbered workflows.
- Use fenced code blocks with language tags for commands, JSON, YAML, and Python.
- Prefer explicit examples over abstract summaries.
- Keep command snippets idempotent and deterministic where possible.

## Python Style
- Group imports as standard library first, then third-party, then local imports.
- Use `snake_case` for functions, variables, and test names.
- Use `PascalCase` for classes and `UPPER_SNAKE_CASE` for module-level constants.
- Add type hints for public functions and important helpers.
- Existing code uses `Optional`, `Dict`, and `List` from `typing`; stay consistent within touched files.
- Use `@dataclass` for simple structured return values when appropriate.
- Use docstrings for modules, classes, and non-trivial functions.
- Prefer stdlib solutions when they keep the implementation clear; `fanfuaji.py` intentionally avoids `requests`.

## Naming and Data Modeling
- Match existing skill names exactly across directory names, frontmatter, and docs.
- Use semantic kebab-case for lesson-card IDs and similar document identifiers.
- Keep return types declared on script-facing functions.
- Name tests after behavior, for example `test_allowlist_mode_blocks_outside_directories`.

## Error Handling and Tests
- Raise or surface specific, actionable errors.
- Include enough context in error text for an agent to recover without guessing.
- In CLI code, convert expected failures into clear stderr output plus non-zero exit.
- Re-raise intentionally when preserving semantics is clearer than wrapping everything.
- Pytest is the current test style for Python code in this repo.
- Keep tests isolated with `tmp_path` and assert policy failures with `pytest.raises(..., match=...)`.

## JSON, YAML, and Docs
- Preserve existing indentation and key ordering style in touched files.
- Use valid JSON only; no comments or trailing commas.
- In YAML workflows, keep steps explicit and readable rather than overly compact.
- Keep line length readable rather than maximally dense.

## Working In This Repo
- Do not treat incidental local files as canonical repo configuration unless they are clearly part of the committed project structure.
- Before referencing a workflow in docs, confirm the underlying file or command actually exists in the repository.
- Prefer small, targeted edits because many files are normative instruction documents.

## Safe Defaults For Agents
- If asked for a build command, explain that this repo validates skills rather than building an app.
- If asked for lint, explain that there is no dedicated lint runner configured.
- If asked how to verify a skill change, start with `npx --yes skills-ref validate <skill-dir>`.
- If asked how to verify `fanfuaji` script behavior, run the relevant pytest file or a single pytest test.
