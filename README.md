# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

### Model-invoke

- **[e04](skills/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[sdkman](skills/sdkman/)** - Validate and run commands under applicable [SDKMAN](https://sdkman.io/) candidates while preserving worktree boundaries, project-owned toolchains, exact vendor identity, and persistent user settings.
- **[writing-agents-md](skills/writing-agents-md/)** - Create, update, prune, or review `AGENTS.md` and `CLAUDE.md` by routing standing guidance to the smallest correct scope and mechanism.

### User-invoke

- **[commit](skills/commit/)** - Commit the changes selected by the request or conversation while preserving unrelated staged and unstaged work.
- **[commit-push](skills/commit-push/)** - Commit selected changes and push to the intended branch, reusing authorization for the same destination.
- **[commit-push-pr](skills/commit-push-pr/)** - Commit selected changes, push the intended branch, and create or resume its pull request.
- **[create-branch](skills/create-branch/)** - Create or safely resume a descriptive local or issue-linked remote branch without duplicate branches.
- **[create-worktree](skills/create-worktree/)** - Create or resume isolated work in a descriptive Git worktree, including an existing Planning Baseline branch.
- **[grill-on-point](skills/grill-on-point/)** - Run the external `grill-with-docs` skill over a doc, plan, or rough idea while surfacing only findings that truly need your input.
- **[pr](skills/pr/)** - Publish committed feature-branch changes and return a verified new or existing pull request.
- **[push](skills/push/)** - Push to the intended remote branch with verified default-branch authorization and publication results.
- **[skill-review](skills/skill-review/)** - Review a skill using writing-for-agents and skill-creator, and optionally apply fixes.
- **[splitoff](skills/splitoff/)** - Hand the current conversation to a Claude Code background agent or a native Codex subagent using a generated handoff summary.
- **[scope-it](skills/scope-it/)** - Coordinate interchangeable planning skills into one Delivery Map whose embedded protocol lets later sessions continue from its parent.
- **[tradeoffs](skills/tradeoffs/)** - Judge which discussed option is most worth choosing by comparing its incremental value with its incremental cost, risk, and complexity.

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
