# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[harvest](skills/harvest/)** - Capture high-signal decisions, unsolved questions, and lessons into a searchable second brain in `docs/notes/` with smart context merge.
- **[agent-install-guide](skills/agent-install-guide/)** - Write installation guides that AI agents can reliably execute.
- **[fanfuaji](skills/fanfuaji/)** - Chinese terminology conversion (Traditional ↔ Simplified) using [Fanhuaji](https://zhconvert.org/) API.
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

## License

MIT
