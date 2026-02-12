# Bases Generation Spec

<!--
Specification only.
This file defines desired base-view semantics for Harvest.
`obsidian-bases` owns `.base` syntax details and should translate this spec into valid `.base` files.
-->

## Purpose

Provide a stable, syntax-light contract for default Harvest base files so Harvest does not own `.base` syntax.

## Generation Trigger

- If `obsidian-bases` is available during Harvest initialization, generate default base files.
- Generate missing files by default.
- Preserve existing base files unless explicit update is requested.

## Target Files

- `docs/notes/contexts/contexts.base`
- `docs/notes/mocs/mocs.base`

## Contexts Base Requirements

- Scope: include markdown notes under `notes/contexts`.
- Default view type: `table`.
- Default view name: `All Contexts`.
- Default display order:
  1. `created`
  2. `file.name`
  3. `tags`

## MOCs Base Requirements

- Scope: include markdown notes under `notes/mocs`.
- Default view type: `table`.
- Default view name: `All MOCs`.
- Default display order:
  1. `file.name`

## Mapping Notes

- `obsidian-bases` should map these requirements to current valid `.base` syntax (for example, filters, views, and order fields).
- If Obsidian Bases syntax evolves, update mapping behavior in `obsidian-bases`, not this Harvest spec.
