# scope-it

Compose `to-spec` and `to-tickets` into one approved Delivery Map, then publish its durable scope package with an optional Planning Baseline and Integration Delivery Lane.

This skill must be invoked explicitly.

It uses the installed `to-spec` and `to-tickets` skills as runtime sources while applying one shared approval and publication policy; Git phases use `create-branch`, `create-worktree`, `commit`, and `push` only when needed.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it -g
```
