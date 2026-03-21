# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[agent-install-guide](skills/agent-install-guide/)** - Write installation guides that AI agents can reliably execute.
- **[executing-plans-preflight](skills/executing-plans-preflight/)** - Run extensible preflight checks before superpowers:executing-plans, with branch safety as the default gate.
- **[fanfuaji](skills/fanfuaji/)** - Chinese terminology conversion (Traditional ↔ Simplified) using [Fanhuaji](https://zhconvert.org/) API.
- **[ultrabrain](skills/ultrabrain/)** - Organize a linked-note knowledge base with MOCs, note-first capture, provenance-aware source notes, and manual MOC grooming.
- **[lessons-learned](skills/lessons-learned/)** - Recall relevant lessons before non-trivial work and capture reusable lessons after meaningful corrections or outcomes.
- **[writing-agents-md](skills/writing-agents-md/)** - Create or prune `AGENTS.md` and `CLAUDE.md` so they keep only minimal, high-signal global constraints.

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

- `ultrabrain-init`: Initialize the canonical ultrabrain reminder block in `AGENTS.md` or `CLAUDE.md`.
- `ultrabrain-recall`: Recall relevant knowledge maps before planning with ultrabrain.
- `ultrabrain-capture`: Capture reusable knowledge after work with ultrabrain.
- `ultrabrain-groom`: Run manual MOC grooming with ultrabrain.
- `lessons-learned-init`: Initialize lessons-learned setup for AGENTS.md or CLAUDE.md.
- `lessons-learned-recall`: Recall relevant lessons before work with lessons-learned.
- `lessons-learned-capture`: Capture reusable lessons during corrections or at task end with lessons-learned.

## Naming Rule

- Under `skills/`, do not use `_`-prefixed subdirectories. Prefer `.`-prefixed names (for example, `.templates`).

## License

MIT
