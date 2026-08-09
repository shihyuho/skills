# scope-it

Turn a settled conversation or issue into a published spec and ready-for-agent ticket scope, preferring one ticket while delegating multi-ticket structure to the ticket source.

This skill must be invoked explicitly.

It uses `resolving-skills` to load `to-spec` and `to-tickets` from the active agent environment. Their source files must be installed and visible to the agent.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it -g
```
