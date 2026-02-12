---
description: "Initialize Harvest second brain storage in docs/notes without creating a new context entry."
disable-model-invocation: true
---

Invoke the `harvest` skill and execute only the initialization part of the workflow.

Required actions:
1. Use `skills/harvest/references/initialization-manifest.md` as the initialization inventory source.
2. Ensure `docs/notes/` structure exists (`contexts/`, `mocs/`, `00-INDEX.md`).
3. If `obsidian-bases` is available, create `docs/notes/contexts/contexts.base` and `docs/notes/mocs/mocs.base`.
4. Check `AGENTS.md` then `CLAUDE.md`; if both exist or neither exists, ask user which file to append before adding lessons section.
5. Run idempotently: create missing items and preserve existing files unless explicit update is requested.

Stop after initialization.

Do not create or merge any `contexts/<context_id>-<topic>.md` file in this command.

Finish by reporting `created`, `updated`, and `skipped` items.
