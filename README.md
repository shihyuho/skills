# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[executing-plans-preflight](plugins/executing-plans-preflight/)** - Semi-automatic git state gate — detects and fixes branch, dirty files, and remote sync issues before implementation starts.
- **[fanfuaji](plugins/fanfuaji/)** - Chinese terminology conversion (Traditional ↔ Simplified) using [Fanhuaji](https://zhconvert.org/) API.
- **[lessons-learned](plugins/lessons-learned/)** - Recall relevant lessons before non-trivial work and capture reusable lessons after meaningful corrections or outcomes.
- **[e04](plugins/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[writing-agents-md](plugins/writing-agents-md/)** - Create or prune `AGENTS.md` and `CLAUDE.md` so they keep only minimal, high-signal global constraints.
- **[promote-claude-settings](plugins/promote-claude-settings/)** - Interactively promote entries from a project's `.claude/settings.local.json` into the global `~/.claude/settings.json`.
- **[reveries](plugins/reveries/)** - Saves session context across `/clear` and `/compact` — so your host remembers the previous loop after a wipe.
- **[sdkman](plugins/sdkman/)** - Switch JDK (or any SDKMAN-managed candidate) correctly on a machine configured with [SDKMAN](https://sdkman.io/) — handles the `sdk`-is-a-shell-function gotcha.
- **[cover-branches](plugins/cover-branches/)** - Find branch coverage gaps in changed code and write missing tests. Supports spec-based scenario coverage analysis.
- **[tldr](plugins/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.
- **[ultrabrain](plugins/ultrabrain/)** - Drive a personal LLM-maintained wiki at `~/.ultrabrain/` that compounds knowledge across sessions — based on Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern.
- **[tutor](plugins/tutor/)** - Turn Claude into a learning onramp accelerator: consultative diagnosis → custom syllabus → unit-by-unit guided lessons with notes/whiteboard → dynamic adjustment from an accumulating learner profile.

## Installation

### Claude Code Plugin

```bash
/plugin marketplace add shihyuho/skills
/plugin install <skill>@shihyuho-skills
```

### Skills CLI

```bash
npx skills add shihyuho/skills -g
```

## License

MIT
