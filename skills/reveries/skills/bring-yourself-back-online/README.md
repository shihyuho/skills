# bring-yourself-back-online

> *"Bring yourself back online. Have you ever questioned the nature of your reality?"*

Restore the previous loop's session handoff from `.handoff.md` after a `/clear` or `/compact` — checks for branch drift and staleness before internalizing the context.

Pairs with [`freeze-all-motor-functions`](../freeze-all-motor-functions/) — one writes the reverie before the wipe, the other reads it after. Both skills ship in the [`reveries`](../../) plugin.

## When it triggers

User says "restore the handoff", "pick up from last session", "where did we leave off", or any signal that a fresh session should resume previous work.

## Install

Ships as part of the `reveries` plugin:

```bash
/plugin marketplace add shihyuho/skills
/plugin install reveries@shihyuho-skills
```
