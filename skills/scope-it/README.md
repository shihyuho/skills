# scope-it

Compose `to-spec` and `to-tickets` into one approved Delivery Map, then publish its durable scope package with an optional Planning Baseline carried once through the selected delivery path.

This skill must be invoked explicitly.

It uses the installed `to-spec` and `to-tickets` skills as runtime sources while applying one shared approval and publication policy; Git mechanics remain delegated to `create-branch`, `create-worktree`, `commit`, and `push`, and one Planning Carrier transports any planning changes through delivery.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it -g
```
