# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[executing-plans-preflight](skills/executing-plans-preflight/)** - Semi-automatic git state gate — detects and fixes branch, dirty files, and remote sync issues before implementation starts.
- **[fanfuaji](skills/fanfuaji/)** - Chinese terminology conversion (Traditional ↔ Simplified) using [Fanhuaji](https://zhconvert.org/) API.
- **[lessons-learned](skills/lessons-learned/)** - Recall relevant lessons before non-trivial work and capture reusable lessons after meaningful corrections or outcomes.
- **[e04](skills/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[writing-agents-md](skills/writing-agents-md/)** - Create or prune `AGENTS.md` and `CLAUDE.md` so they keep only minimal, high-signal global constraints.
- **[promote-claude-settings](skills/promote-claude-settings/)** - Interactively promote entries from a project's `.claude/settings.local.json` into the global `~/.claude/settings.json`.
- **[cover-branches](skills/cover-branches/)** - Find branch coverage gaps in changed code and write missing tests. Supports spec-based scenario coverage analysis.
- **[grill-diff](skills/grill-diff/)** - Review git changes using deep interactive grilling or fast multi-strategy self-review.
- **[tldr](skills/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.

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

- `lessons-learned-init`: Initialize lessons-learned setup for AGENTS.md or CLAUDE.md.
- `lessons-learned-recall`: Recall relevant lessons before work with lessons-learned.
- `lessons-learned-capture`: Capture reusable lessons during corrections or at task end with lessons-learned.

## Naming Rule

- Under `skills/`, do not use `_`-prefixed subdirectories. Prefer `.`-prefixed names (for example, `.templates`).

## License

MIT
