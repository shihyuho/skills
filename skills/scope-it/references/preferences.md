# Planning skill preferences

Read this when choosing a role from saved defaults, remembering or changing a choice, or migrating preference data. Role precedence and host invocation rules remain in the main workflow.

## Read and interpret

Use `~/.config/softleader/agent-skills/scope-it/sources.json` for cross-repository defaults. Only when it is absent, read the legacy `~/.config/softleader/agent-skills/scope-it-remake/sources.json`.

```json
{"schema_version":3,"scope":"<skill identity>","tickets":"<skill identity>"}
```

V3 records explicit user selection and consent to future planning delegation on explicit invocations of this coordinator. It grants no publication, Git or implementation authority; internal chaining still follows host invocation rules. Explain that consent when selecting a choice to remember.

For older data:

- **V2:** retain usable choices, but obtain missing delegation consent before invoking explicit-only roles and before v3 migration.
- **V1:** resolve explicit choice > `global` > unanimous legacy `repositories`; clarify conflicting values. Approve conversion/removal of legacy containers with consent for every retained role.
- **Unknown version or unusable file:** clarify the affected choices or recovery before using or replacing it.

Reading legacy data does not authorize migration. Copy accepted values to the canonical path only in an approved preference write; leave the legacy file unchanged unless its removal is approved.

## Save only the approved delta

Include preference writes in final approval. Preserve unrelated fields and omit unresolved roles.

Before saving, reread the file and preserve unrelated concurrent changes. Renew approval when affected values differ from the approved proposal. Verify the saved delta; a save failure leaves only that operation unresolved, without republishing artifacts.
