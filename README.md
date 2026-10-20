# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

### Model-invoke

- **[e04](skills/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[sdkman](skills/sdkman/)** - Run development tools in the environment the task requires, and manage host tool versions through [SDKMAN](https://sdkman.io/).
- **[writing-agents-md](skills/writing-agents-md/)** - Create, update, prune, or review `AGENTS.md` and `CLAUDE.md` by routing standing guidance to the smallest correct scope and mechanism.

### User-invoke

- **[ask-owners](skills/ask-owners/)** - Run a chosen discussion skill with questions routed to the responsible people and channels, collecting their answers into one shared design.
- **[commit](skills/commit/)** - Commit the selected changes, leaving everything outside the selection as found.
- **[create-branch](skills/create-branch/)** - Create or safely resume a descriptive local or issue-linked remote branch without duplicate branches.
- **[create-worktree](skills/create-worktree/)** - Create or resume isolated work in a descriptive Git worktree, including an existing Planning Baseline branch.
- **[fire-in-the-hole](skills/fire-in-the-hole/)** - Run `scope-it --publish` and `go-for-it` for the current work.
- **[grill-minimal](skills/grill-minimal/)** - Discuss a plan, decision, or idea with the external `grill-with-docs` skill, prioritizing the simplest approach and narrowest scope that meet your goals and constraints.
- **[open-pr](skills/open-pr/)** - Get the current work into a verified pull request, doing only the steps still missing.
- **[push](skills/push/)** - Push the current work to one verified destination, committing it first only if it is still uncommitted.
- **[revisit](skills/revisit/)** - Recover the context of a ticket or PR, assess what still applies to the current version, and discuss the smallest complete change if needed.
- **[scope-it](skills/scope-it/)** - Coordinate interchangeable planning skills into a Ticket Map and a verified AFK handoff through `to-afk-agent`, using `--publish` to complete the agreed workflow without routine confirmation.
- **[skill-review](skills/skill-review/)** - Review a skill using writing-for-agents and skill-creator, with `--fix` applying only corrections judged warranted by the evidence and criteria.
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
