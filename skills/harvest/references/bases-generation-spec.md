# Bases Generation Spec

<!--
Specification only.
This file defines desired base-view semantics for the harvest skill.
`obsidian-bases` owns `.base` syntax details and should translate this spec into valid `.base` files.
-->

## Purpose

Provide a stable, syntax-light contract for default harvest base files so this skill does not own `.base` syntax.

## Generation Trigger

- If `obsidian-bases` is available during harvest initialization, generate default base files.
- Generate missing files by default.
- Preserve existing base files unless explicit update is requested.

## Target Files

- `docs/notes/bases/contexts.base`
- `docs/notes/bases/mocs.base`

## Contexts Base Requirements

- Scope: include markdown notes under `contexts`.
- Mandatory (non-overridable) folder filter: `file.inFolder("contexts")`.
- Use vault-relative folder paths only (for example, `contexts`), not repository paths.
- Default view type: `table`.
- Default view name: `All Contexts`.
- Default display order:
  1. `created`
  2. `file.name`
  3. `tags`

## MOCs Base Requirements

- Scope: include markdown notes under `mocs`.
- Mandatory (non-overridable) folder filter: `file.inFolder("mocs")`.
- Use vault-relative folder paths only (for example, `mocs`), not repository paths.
- Default view type: `table`.
- Default view name: `All MOCs`.
- Default display order:
  1. `file.name`

## Mapping Notes

- `obsidian-bases` should map these requirements to current valid `.base` syntax (for example, filters, views, and order fields).
- Vault root assumption: `docs/notes/` is the Obsidian vault root for this setup.
- Therefore `file.inFolder(...)` paths must be vault-relative (`contexts`, `mocs`), not repository-relative (`docs/notes/...`).
- If Obsidian Bases syntax evolves, update mapping behavior in `obsidian-bases`, not this harvest spec.
