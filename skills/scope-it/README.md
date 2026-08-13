# scope-it

Publish settled work as a durable spec, minimal ready-for-agent ticket scope, and an optional Planning Baseline.

This skill must be invoked explicitly.

It uses `resolve-user-invoke-skill` to load `to-spec`, `to-tickets`, `create-branch`, `create-worktree`, `commit`, and `push` from the active agent environment. Their source files must be installed and visible to the agent.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it -g
```
