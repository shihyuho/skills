# AGENTS.md

## Global Constraints
- The whole repo is a single `skills` plugin for Claude Code and Codex: `.claude-plugin/{plugin,marketplace}.json` configures Claude Code; `.codex-plugin/plugin.json` plus `.agents/plugins/marketplace.json` configure Codex.
- Each skill lives at `skills/<skill>/{SKILL.md, README.md}` and is auto-discovered from the root `skills/` directory; hooks live in root `hooks/hooks.json`.
- Before creating or editing any skill (its `SKILL.md`, `references/`, templates, or scripts), invoke the `skill-creator` and `writing-for-agents` skills and apply [`docs/skill-design.md`](docs/skill-design.md); settle the skill's model with the user before writing a `SKILL.md` or changing what one does.
- Read [`docs/writing-readme.md`](docs/writing-readme.md) before writing a skill's `README.md`, or when a change alters what a skill does, how it starts, or what it needs.
- If you add, remove, or rename anything under `skills/`, `commands/`, or `hooks/`, update `README.md` in the same change.
- In the root `README.md`, list skills alphabetically within each group and describe each in one sentence: the job sentence that opens its own `README.md`.
- Skill files are written in English: `SKILL.md`, `references/*`, scripts, and `README.md`. Examples use placeholders, not environment-specific values.
- Every `SKILL.md` frontmatter must include `name`, `description`, and `license`. Don't add a `version` field to `.claude-plugin/{plugin,marketplace}.json` — the plugin uses commit-SHA versioning (every commit is a new version); a pinned version freezes installed users on a stale snapshot. Codex's `.codex-plugin/plugin.json` instead uses a semantic `version`.
- Treat `SKILL.md` frontmatter `name` as the canonical skill name. Keep the first H1 in `SKILL.md` and, when present, `agents/openai.yaml` `interface.display_name` exactly equal to it.
- Keep `name` stable. Write `description` for its reader: a model-invoke skill's description is the model's trigger, so it names the concrete contexts that should fire it; a user-invoke skill's description reaches only the human browsing `/`, so it is one plain sentence saying what the skill does, with no trigger clauses.
- When adding or modifying a skill, classify it under [`docs/invocation-classification.md`](docs/invocation-classification.md): apply or remove the paired invocation markers as required, and update the root `README.md` grouping.
- Compose skills through trigger contracts: each skill defines what its own trigger accepts and, when calling another skill, constructs that callee's trigger. Keep callee contracts caller-agnostic; express trust as trigger-versus-data boundaries rather than lists of users, workflows, or caller skills.
- For any skill that persists skill-owned config or cache across invocations, read [`docs/skill-user-data.md`](docs/skill-user-data.md) before editing it.
- Keep each skill's runtime and development artifacts in its own directory: `scripts/` for code the skill runs, `evals/` for agent-behavior evaluations (prompts, expected outcomes, assertions, and their fixtures), `tests/` for deterministic tests of skill-owned scripts and contracts. Keep per-execution eval outputs untracked, in an ignored `.*-workspace/` directory or outside the checkout, and share their conclusions and evidence links in the PR.
- Python scripts under `skills/<skill>/scripts/` support Python ≥ 3.8: a script using PEP 604 unions (`X | None`) or subscriptable generics (`dict[...]`) in annotations starts with `from __future__ import annotations`.
- After editing any skill, run the checks `.github/workflows/validate-skills.yml` runs.
- Hook commands reference skill-bundled scripts via `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/...` — the plugin root is the repo root.
- Avoid `_`-prefixed subdirectories; use `.`-prefixed names for hidden helpers.
