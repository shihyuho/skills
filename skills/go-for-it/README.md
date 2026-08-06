# go-for-it

Run or resume a settled design from spec through pull request while loading the installed skill for each phase as its source of truth.

This skill must be invoked explicitly.

It loads `to-spec`, `to-tickets`, `create-worktree`, `implement`, `commit`, `push`, and `pr` directly from the active agent environment. Their source files must be installed and visible to the host.

## Installation

```bash
npx skills add shihyuho/skills --skill go-for-it -g
```
