# Writing Agents MD Principles

## 1. Context is scarce and model-relative

Always-loaded instructions spend tokens and attention on every task in their scope. Their value depends on whether they change the target model's behavior, so settle suspected no-ops with target-host evaluation rather than intuition alone.

Anthropic reports removing more than 80% of Claude Code's system prompt for Claude 5 generation models without measurable loss on its coding evaluations. That result supports aggressive simplification for those models, but it does not prove the same defaults for every Codex or third-party model.

## 2. Scope is part of correctness

Root, nested, imported, and path-scoped instructions are different loading interfaces. Place a standing rule at the smallest scope where it always applies. Task-specific guidance belongs behind an on-demand pointer, not in a broader file merely because the rule is important.

## 3. The environment is a source, not the only authority

Code, config, CI, and repository layout are authoritative for observable implementation. Repeating cheap lookups creates a stale cache. Human-written instructions can also encode policy or external constraints that the repository cannot reveal, so verify conflicts instead of assuming either source always wins.

## 4. Progressive disclosure needs a strong pointer

Move conditional workflows and reference-heavy material into skills or documentation. Keep a pointer only when agents need to know the material exists; name both what to load and the condition that triggers it. Imports that load unconditionally organize content but do not reduce context load.

## 5. Deterministic requirements need deterministic mechanisms

Instructions guide model judgment; they do not enforce behavior. Put mandatory formatting, validation, permissions, and lifecycle actions in formatters, tests, CI, settings, or hooks where practical. Instructions may retain the non-obvious rationale or safe fallback.

## 6. Friction and evaluation drive edits

Add standing instructions after repeated mistakes, review findings, costly landmines, or explicit durable policy reveal a behavior gap. Remove rules that are stale, conflicting, duplicated, or empirically unnecessary. Strong constraints earn their cost in high-impact areas; general work benefits from model judgment and surrounding context.

## Primary Sources

- [OpenAI Codex: Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [AGENTS.md format](https://agents.md/)
- [Claude Code: How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Claude: The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
