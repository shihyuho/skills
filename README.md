# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[lessons-learned](plugins/lessons-learned/)** - Recall relevant lessons before non-trivial work and capture reusable lessons after meaningful corrections or outcomes.
- **[e04](plugins/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[writing-agents-md](plugins/writing-agents-md/)** - Create or prune `AGENTS.md` and `CLAUDE.md` so they keep only minimal, high-signal global constraints.
- **[promote-claude-settings](plugins/promote-claude-settings/)** - Interactively promote entries from a project's `.claude/settings.local.json` into the global `~/.claude/settings.json`.
- **[reveries](plugins/reveries/)** - Saves session context across `/clear` and `/compact` — so your host remembers the previous loop after a wipe. `/reveries:freeze` before the wipe, `/reveries:wake` after.
- **[sdkman](plugins/sdkman/)** - Switch JDK (or any SDKMAN-managed candidate) correctly on a machine configured with [SDKMAN](https://sdkman.io/) — handles the `sdk`-is-a-shell-function gotcha, and ships hooks that nudge toward the project's default JDK and flag Java version-mismatch build failures.
- **[cover-branches](plugins/cover-branches/)** - Find branch coverage gaps in changed code and write missing tests. Supports spec-based scenario coverage analysis.
- **[tldr](plugins/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.
- **[ultrabrain](plugins/ultrabrain/)** - Drive a personal LLM-maintained wiki at `~/.ultrabrain/` that compounds knowledge across sessions — based on Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern.
- **[tutor](plugins/tutor/)** - Turn Claude into a learning on-ramp, with two skills. `explain` opens up a single subject whole-picture-first, then drills into the parts you pick; `course` runs a full guided curriculum — consultative diagnosis → custom syllabus → unit-by-unit guided lessons → dynamic adjustment from an accumulating learner profile.
- **[rephrase](plugins/rephrase/)** - Re-express a passage from scratch, along two axes. Length: `tighten` rewrites it shorter with every point kept, `distil` cuts it down to its core message. Readability: `humanize` strips the telltale AI tics so it reads like a person wrote it, `plain` strips jargon so a non-specialist can follow. All act only on a passage you ask them to.
- **[kickoff](plugins/kickoff/)** - Two go-signals for handing reviewed work back to Claude. `lgtm` re-reads from disk every file you had under review before Claude takes the next step — so your mid-review edits are never silently dropped. `kickoff` re-reads a reviewed SPEC/PLAN, then builds it while keeping a running implementation-notes file of design decisions, deviations, tradeoffs, and open questions.

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
