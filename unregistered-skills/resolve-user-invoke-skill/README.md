# resolve-user-invoke-skill

Resolve an exact, authorized user-invoke skill dependency to one active, pinned instruction source across agent environments.

This skill remains model-invoked so it can bridge a user's direct request or an explicitly invoked orchestrator's fixed allowlist to user-invoke dependencies without exposing those dependencies to ambient model selection.

## Installation

```bash
npx skills add shihyuho/skills --skill resolve-user-invoke-skill -g
```
