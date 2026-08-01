# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

### Model-invoke

- **[e04](skills/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[lgtm](skills/lgtm/)** - On a go-signal (`lgtm`, `looks good`, `approved`), re-read from disk every file you had under review so mid-review edits aren't dropped before the next step.
- **[sdkman](skills/sdkman/)** - Switch JDK (or any [SDKMAN](https://sdkman.io/)-managed candidate) correctly despite the `sdk`-is-a-shell-function gotcha, with hooks that nudge toward the project's default JDK and flag Java version-mismatch build failures.
- **[writing-agents-md](skills/writing-agents-md/)** - Create or prune `AGENTS.md` and `CLAUDE.md` so they keep only minimal, high-signal global constraints.

### User-invoke

- **[browse](skills/browse/)** - Open the current repository in a browser, preferring the current branch when it exists on the remote.
- **[clean-gone-branches](skills/clean-gone-branches/)** - Remove local branches marked gone and any worktrees associated with them.
- **[commit](skills/commit/)** - Create one cohesive commit, or ask before splitting clearly unrelated changes into atomic commits.
- **[commit-push](skills/commit-push/)** - Create a commit and push its branch with safeguards for default-branch pushes.
- **[commit-push-pr](skills/commit-push-pr/)** - Create a commit, push its branch, and open a pull request with safeguards for default-branch pushes.
- **[cover-branches](skills/cover-branches/)** - Find branch coverage gaps in changed code and write the missing tests, with optional spec-based scenario coverage analysis.
- **[create-branch](skills/create-branch/)** - Create a descriptive local or issue-linked remote branch while guarding against duplicate branches.
- **[create-worktree](skills/create-worktree/)** - Create and continue work in an isolated, descriptively named Git worktree.
- **[distil](skills/distil/)** - Re-express a passage by dropping peripheral detail and keeping its core message.
- **[grill-on-point](skills/grill-on-point/)** - Run the external `grill-with-docs` skill over a doc, plan, or rough idea while surfacing only findings that truly need your input.
- **[kibana-user-story](skills/kibana-user-story/)** - Save a reusable, environment-agnostic Kibana investigation user story from the current conversation.
- **[merge-train](skills/merge-train/)** - Merge approved pull requests one at a time through an auto-merge update-branch queue.
- **[plain](skills/plain/)** - Rewrite jargon-heavy text in clear language while preserving every point.
- **[post-gh-comment](skills/post-gh-comment/)** - Post local files or confirmed chat content as individual comments on a GitHub issue or pull request.
- **[pr](skills/pr/)** - Push the current feature branch and open a pull request with a default-branch safety gate.
- **[promote-claude-settings](skills/promote-claude-settings/)** - Interactively promote entries from a project's `.claude/settings.local.json` into the global `~/.claude/settings.json`.
- **[push](skills/push/)** - Push the current branch to origin with a safety gate for direct default-branch pushes.
- **[skill-review](skills/skill-review/)** - Review a skill against the available skill-authoring rubrics and optionally apply fixes.
- **[splitoff](skills/splitoff/)** - Hand the current conversation to a named background agent using a generated handoff summary.
- **[tighten](skills/tighten/)** - Re-express a passage in fewer words while keeping every point.
- **[tldr](skills/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.
- **[tradeoffs](skills/tradeoffs/)** - Turn discussed approaches into a Traditional Chinese decision brief with a recommendation.

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
