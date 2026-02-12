# Initialization Manifest

<!--
⚠️ Manifest only.
Behavioral workflow, decision rules, and user interaction logic live in `skills/harvest/SKILL.md`.

Use this file as the single source for initialization file/path inventory.
-->

## Required Paths

- `docs/notes/`
- `docs/notes/contexts/`
- `docs/notes/mocs/`

## Required Files

| Target | Source Template |
|---|---|
| `docs/notes/00-INDEX.md` | [index-template.md](index-template.md) |

## Optional Files

Create only when matching capability is available.

| Condition | Target | Provisioning Method |
|---|---|---|
| `obsidian-bases` available | `docs/notes/bases/contexts.base` | Delegate creation to `obsidian-bases` skill using [bases-generation-spec.md](bases-generation-spec.md) |
| `obsidian-bases` available | `docs/notes/bases/mocs.base` | Delegate creation to `obsidian-bases` skill using [bases-generation-spec.md](bases-generation-spec.md) |

## Optional Content Injection

| Target Candidate | Source Content |
|---|---|
| `AGENTS.md` or `CLAUDE.md` | [agents-lessons-section.md](agents-lessons-section.md) |

## Verification Checklist

- Required directories exist under `docs/notes/`.
- `docs/notes/00-INDEX.md` exists and follows index template structure.
- Optional `.base` files are created automatically via `obsidian-bases` delegation when available.
- Lessons section injection target is explicitly chosen when ambiguous.
- Initialization is idempotent: existing files are preserved unless explicit update is requested.
