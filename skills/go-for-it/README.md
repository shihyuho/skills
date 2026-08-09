# go-for-it

Run or resume a settled design through scoping, implementation, and pull request while loading the installed skill for each phase as its source of truth.

This skill must be invoked explicitly.

It uses `resolving-skills` to load `scope-it`, `create-worktree`, `implement`, `commit`, `push`, and `pr` from the active agent environment. Their source files must be installed and visible to the agent.

## Installation

```bash
npx skills add shihyuho/skills --skill go-for-it -g
```
