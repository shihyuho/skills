# writing-agents-md

## Purpose

This skill creates, updates, prunes, or reviews `AGENTS.md` and `CLAUDE.md` as small instruction interfaces rather than repository handbooks.

It first removes repetition, conflicts, stale claims, and model-relative no-ops. It then routes each surviving rule to the smallest correct scope and mechanism:

- the current instruction file for standing guidance across its scope
- a nested instruction file or path-scoped rule for local standing guidance
- a skill or documentation for conditional workflows and reference material
- code, config, tests, CI, permissions, or hooks for deterministic enforcement

## Source handling

Existing instruction files are standing contracts under review, not disposable history. Repository code, config, CI, and documentation verify observable implementation, but they do not automatically override human safety, release, compliance, or operational policy.

Discoverability is evidence, not an automatic deletion rule. Cheap lookups and directory tours usually go; concise repository purpose, canonical gotchas, and costly safe paths may stay when they change decisions.

## Installation

```bash
npx skills add shihyuho/skills --skill writing-agents-md -g
```

## Primary references

- [OpenAI Codex: Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [AGENTS.md format](https://agents.md/)
- [Claude Code: How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Claude: The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
