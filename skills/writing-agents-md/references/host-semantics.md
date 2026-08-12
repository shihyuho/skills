# Host Instruction Semantics

Read this reference only when file placement, discovery, or precedence affects the task. Verify current host documentation when behavior may have changed.

## Codex

- Codex builds its instruction chain once per run. At global scope it reads `AGENTS.override.md`, otherwise `AGENTS.md`, from Codex home.
- At project scope it walks from the project root to the startup working directory. In each directory it selects at most one file in this order: `AGENTS.override.md`, `AGENTS.md`, then configured fallback names.
- It concatenates selected files from root to working directory, so later, more local guidance has precedence. The default combined limit is 32 KiB.
- Place repository-wide guidance at root and service-specific guidance in the closest directory that will be part of the intended startup chain. Use `AGENTS.override.md` when that directory must replace its ordinary instruction source.

Source: [OpenAI Codex — Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)

## Portable `AGENTS.md`

The cross-agent format allows arbitrary Markdown. Its reference behavior gives the closest `AGENTS.md` to the edited file precedence and recommends nested files for subprojects. Because host implementations differ, verify the actual runtime before relying on portable precedence beyond this basic convention.

Source: [AGENTS.md](https://agents.md/)

## Claude Code

- Claude Code reads `CLAUDE.md` and `CLAUDE.local.md` from ancestors of the startup working directory and concatenates them from broadest to most specific. It discovers descendant files lazily when reading files in those directories.
- Use `.claude/rules/*.md` with `paths` frontmatter for file- or directory-specific rules. Unscoped rules load every session.
- `@path` imports organize content but expand into startup context, so they do not provide progressive disclosure.
- Claude Code does not natively treat `AGENTS.md` as its project instruction file. When `AGENTS.md` is the shared source, import it from `CLAUDE.md` with `@AGENTS.md`; use a symlink only when platform constraints and the absence of Claude-specific additions make that preferable.
- Keep each `CLAUDE.md` concise and concrete. Move conditional, reference-heavy, or multi-step workflows to skills.

Sources: [Claude Code — How Claude remembers your project](https://code.claude.com/docs/en/memory), [Claude Code — Extend Claude Code](https://code.claude.com/docs/en/features-overview)

## Placement Test

1. Which host or hosts must consume the rule?
2. Which startup directory, edited paths, or file patterns activate it?
3. Is it standing guidance for that scope, or a task-triggered workflow?
4. Does a more specific active file already own or contradict it?
5. Would an import merely reorganize always-loaded content, or does an on-demand pointer provide real progressive disclosure?
