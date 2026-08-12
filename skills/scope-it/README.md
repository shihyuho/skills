# scope-it

Publish a settled spec and ready-for-agent ticket scope, plus a durable Planning Baseline when the scope produced repository files.

This skill must be invoked explicitly.

It uses `resolve-user-invoke-skill` to load `to-spec`, `to-tickets`, `create-branch`, `commit`, and `push` from the active agent environment. Their source files must be installed and visible to the agent.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it -g
```
