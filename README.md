# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

### Model-invoke

- **[e04](skills/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[sdkman](skills/sdkman/)** - Run Java, Maven, Gradle, and other SDKMAN-managed tools in the environment the project declares, and manage host tool versions through [SDKMAN](https://sdkman.io/).
- **[writing-agents-md](skills/writing-agents-md/)** - Create, update, prune, or review `AGENTS.md` and `CLAUDE.md` by routing standing guidance to the smallest correct scope and mechanism.

### User-invoke

- **[ask-owners](skills/ask-owners/)** - Run a design discussion with each decision's owner through their agreed channel, gathering the answers into one design.
- **[commit](skills/commit/)** - Commit the selected changes, leaving everything outside the selection as found.
- **[create-branch](skills/create-branch/)** - Put the current work on its own descriptive branch, linked to its issue when there is one.
- **[create-worktree](skills/create-worktree/)** - Start the work in its own Git worktree under `~/code/worktrees` and continue there.
- **[fire-in-the-hole](skills/fire-in-the-hole/)** - Run `scope-it --publish` and `go-for-it` for the current work.
- **[grill-minimal](skills/grill-minimal/)** - Grill a plan, decision, or idea toward the smallest complete solution: the simplest approach and narrowest scope that still meet its goals and constraints.
- **[open-pr](skills/open-pr/)** - Get the current work into a verified pull request, doing only the steps still missing.
- **[push](skills/push/)** - Push the current work to one verified destination, committing it first only if it is still uncommitted.
- **[revisit](skills/revisit/)** - Recover why a ticket or PR exists and what changed, reassess it against the current version, and discuss the smallest complete change if one is still needed.
- **[scope-it](skills/scope-it/)** - Coordinate interchangeable planning skills into a Ticket Map and a verified AFK handoff through `to-afk-agent`, using `--publish` to complete the agreed workflow without routine confirmation.
- **[skill-review](skills/skill-review/)** - Review a skill against writing-for-agents, skill-creator and its repository's guidance, applying the warranted corrections with `--fix`.
- **[splitoff](skills/splitoff/)** - Hand the current conversation to a Claude Code background agent or a native Codex subagent using a generated handoff summary.

## Installation

### Claude Code Plugin

Everything ships as a single plugin — install once and all skills above are available:

```bash
/plugin marketplace add shihyuho/skills
/plugin install skills@shihyuho-skills
```

### Codex Marketplace

```bash
codex plugin marketplace add shihyuho/skills
codex plugin add skills@shihyuho-skills
```

### Skills CLI

```bash
npx skills add shihyuho/skills -g
```

## License

MIT
