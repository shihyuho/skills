# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[executing-plans-preflight](skills/executing-plans-preflight/)** - Semi-automatic git state gate — detects and fixes branch, dirty files, and remote sync issues before implementation starts.
- **[fanfuaji](skills/fanfuaji/)** - Chinese terminology conversion (Traditional ↔ Simplified) using [Fanhuaji](https://zhconvert.org/) API.
- **[lessons-learned](skills/lessons-learned/)** - Recall relevant lessons before non-trivial work and capture reusable lessons after meaningful corrections or outcomes.
- **[e04](skills/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[writing-agents-md](skills/writing-agents-md/)** - Create or prune `AGENTS.md` and `CLAUDE.md` so they keep only minimal, high-signal global constraints.
- **[promote-claude-settings](skills/promote-claude-settings/)** - Interactively promote entries from a project's `.claude/settings.local.json` into the global `~/.claude/settings.json`.
- **[sdkman](skills/sdkman/)** - Switch JDK (or any SDKMAN-managed candidate) correctly on a machine configured with [SDKMAN](https://sdkman.io/) — handles the `sdk`-is-a-shell-function gotcha.
- **[cover-branches](skills/cover-branches/)** - Find branch coverage gaps in changed code and write missing tests. Supports spec-based scenario coverage analysis.
- **[grill-diff](skills/grill-diff/)** - Grill the diff. Specialists evaluate every finding internally — only high-value findings reach the user.
- **[grill-me-quick](skills/grill-me-quick/)** - Grill the user's plan or design, auto-deciding confident calls. Borderline decisions trigger Chain-of-Verification via independent subagents.
- **[tldr](skills/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.
- **[ultrabrain](skills/ultrabrain/)** - Drive a personal LLM-maintained wiki at `~/.ultrabrain/` that compounds knowledge across sessions — based on Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern.

## Installation

### Claude Code Plugin

```bash
claude plugin add --from shihyuho/skills
```

### Skills CLI

```bash
npx skills add shihyuho/skills --skill '*' -g
```

## License

MIT
