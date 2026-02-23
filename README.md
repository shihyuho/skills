# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[agent-install-guide](skills/agent-install-guide/)** - Write installation guides that AI agents can reliably execute.
- **[executing-plans-preflight](skills/executing-plans-preflight/)** - Run extensible preflight checks before superpowers:executing-plans, with branch safety as the default gate.
- **[fanfuaji](skills/fanfuaji/)** - Chinese terminology conversion (Traditional ↔ Simplified) using [Fanhuaji](https://zhconvert.org/) API.
- **[harvest](skills/harvest/)** - Capture project memory by combining source-of-truth planning files with Obsidian-friendly second-brain notes.
- **[skill-design](skills/skill-design/)** - Design or refactor agent skills with strict, portable and high-signal documentation structure.

## Installation

### 1. Install Skills (Required)

First, install the skills collection:

```bash
npx skills add shihyuho/skills --skill='*'
```

## Usage

Skills are automatically available once installed. AI will use them when relevant tasks are detected. If you installed the OpenCode plugins, the AI will also proactively remind you to use them.

## Included Commands

This repository includes reusable command templates in [`commands/`](commands/).

## Naming Rule

- Under `skills/`, do not use `_`-prefixed subdirectories. Prefer `.`-prefixed names (for example, `.templates`).

## License

MIT
