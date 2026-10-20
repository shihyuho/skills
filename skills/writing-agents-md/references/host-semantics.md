# Host Instruction Semantics

Read this reference only when file placement, discovery, or precedence affects the task. Verify current host documentation when behavior may have changed.

## Codex

- Codex builds its instruction chain once per run. At global scope it reads `AGENTS.override.md`, otherwise `AGENTS.md`, from Codex home (`~/.codex` or `CODEX_HOME`).
- At project scope it walks from the project root, typically the Git root, to the startup working directory. In each directory it selects at most one file in this order: `AGENTS.override.md`, `AGENTS.md`, then the names in `project_doc_fallback_filenames`. Empty files are skipped, so an empty override does not shadow `AGENTS.md`.
- It concatenates selected files from root to working directory, so later, more local guidance has precedence. It stops adding files once the combined size reaches `project_doc_max_bytes`, 32 KiB by default.
- Place repository-wide guidance at root and service-specific guidance in the closest directory that will be part of the intended startup chain. Use `AGENTS.override.md` when that directory must replace its ordinary instruction source.

Source: [Codex — Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

## Portable `AGENTS.md`

The cross-agent format allows arbitrary Markdown. Its reference behavior gives the closest `AGENTS.md` to the edited file precedence and recommends nested files for subprojects. Because host implementations differ, verify the actual runtime before relying on portable precedence beyond this basic convention.

Source: [AGENTS.md](https://agents.md/)

## Claude Code

- Claude Code reads `CLAUDE.md` and `CLAUDE.local.md` (or `.claude/CLAUDE.md`) from the startup working directory and every ancestor, and concatenates them from broadest to most specific. A descendant's file loads once Claude reads, writes, or edits a file in that directory. User-level `~/.claude/CLAUDE.md` and `~/.claude/rules/` load in every project; a managed policy `CLAUDE.md` loads for every user and cannot be excluded.
- Since v2.1.277 it reads `AGENTS.md` as project instructions only while no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the working directory or an ancestor; adding any of them, a personal `CLAUDE.local.md` included, stops that unless the Project instructions setting is `claude-md-and-agents-md`. A nested `AGENTS.md` follows the same rule per directory. When a `CLAUDE.md` must coexist with a shared `AGENTS.md`, import it with `@AGENTS.md`; the import is never read twice. A symlink fails where the Edit and Write tools refuse to write through it, and on Windows without Administrator rights or Developer Mode.
- Use `.claude/rules/*.md` with `paths` frontmatter for file- or directory-specific rules; they load when Claude touches a matching file. Rules without `paths` load every session. In monorepos, `claudeMdExcludes` skips other teams' files.
- `@path` imports expand into startup context, so they organize content without reducing its load.
- `CLAUDE.md` is context, not enforced configuration: requirements that must hold go to hooks such as `PreToolUse` or to `permissions.deny`. Target under 200 lines per file, and move conditional, reference-heavy, or multi-step workflows to skills.

Sources: [Claude Code — How Claude remembers your project](https://code.claude.com/docs/en/memory), [Claude Code — Extend Claude Code](https://code.claude.com/docs/en/features-overview)

## Placement Test

1. Which host or hosts must consume the rule?
2. Which startup directory, edited paths, or file patterns activate it?
3. Is it standing guidance for that scope, or a task-triggered workflow?
4. Does a more specific active file already own or contradict it?
5. Would an import merely reorganize always-loaded content, or does an on-demand pointer provide real progressive disclosure?
