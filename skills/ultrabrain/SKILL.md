---
name: ultrabrain
description: Personal wiki at ~/.ultrabrain/ that accumulates knowledge across sessions using an LLM-maintained-wiki pattern. Use when the user asks factual, technical, or decision-oriented questions that may have been previously captured (check index.md before answering), or explicitly asks to capture/記下來/save session content, ingest/整合 raw entries into the wiki, lint/檢查 the vault, or bootstrap a new vault. Skip for small talk, current-file questions, or code-execution requests.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Ultrabrain

Drive a personal, LLM-maintained wiki at `~/.ultrabrain/`. This skill is a thin trigger layer — the vault is self-contained and methodology rules live in `~/.ultrabrain/AGENTS.md`, not here.

## Trigger Contract

Five operations. The first two are skill-side; the last three delegate to vault rules.

| Operation | Trigger examples |
|-----------|------------------|
| `bootstrap` | "bootstrap ultrabrain", "initialize vault", "設定 ultrabrain", or any other operation fires with no vault present |
| `capture` | "記下來 X", "capture this", "save to vault", "存進 vault", or "capture <path-or-url>" |
| `ingest` | "ingest", "integrate raw", "整合 raw", "整理 vault" |
| `query` | description-driven for factual/technical/decision questions, or explicit: "查 vault", "search ultrabrain" |
| `lint` | "lint vault", "健檢 vault", "check wiki" |

### Query skip clause

Before reading any vault file for `query`, verify the user's question plausibly concerns retained knowledge. **Skip the vault** (answer normally) when the question is:

- **Small talk** — greetings, thanks, session meta-questions.
- **Context-local** — answerable from the current session or open files ("what does this file do", "why did that fail").
- **Execution requests** — "write this", "run that", "refactor X". Vault holds facts, not tasks.

When classification is uncertain, default to skipping. Aggressive description triggering is balanced by this negative filter, not overridden.

## Operations

Full step-by-step lives in `references/operations.md`. Summary:

- **`bootstrap`** creates `~/.ultrabrain/` with `AGENTS.md` (copied from `references/agents-template.md`), `CLAUDE.md` (one line: `@AGENTS.md`), empty `index.md` and `log.md`, and `raw/` / `wiki/` directories. Refuses if the vault exists unless `--force` is passed.
- **`capture`** writes session or file content to `raw/YYYY-MM-DD-<slug>.md` with frontmatter. Resolves ambiguous "記下來" requests by proposing a scope and waiting for user confirmation. Never silently overwrites — collisions go to suffixed filenames or a user-chosen append.
- **`ingest`** loads `~/.ultrabrain/AGENTS.md` and follows its `Operation: Ingest` section to integrate unprocessed `raw/` files into `wiki/`, moving processed raw to `raw/.processed/`.
- **`query`** loads `AGENTS.md`, reads `index.md` first, then follows the vault's query rules (index-first strict; no Grep fallback). Answers cite specific wiki pages. Falls back to general knowledge if the vault is empty, with an explicit note.
- **`lint`** loads `AGENTS.md` and produces a health report (contradictions, orphans, stale pages, index drift, missing cross-references). Never auto-fixes; asks the user which findings to address.

Every operation appends one line to `log.md` in the format `ISO-8601 OPERATION details`.

## Vault Contract

Vault location: `~/.ultrabrain/`.

**`AGENTS.md` is the single source of truth for methodology.** The skill's contract with it is **behavioral, not structural** — `AGENTS.md` must define how to perform `ingest`, `query`, and `lint`, in whatever structure the methodology author prefers. The skill makes no assumptions about section headings, page types, tag schemas, or cross-reference syntax.

`~/.ultrabrain/CLAUDE.md` is exactly one line: `@AGENTS.md`. This makes the vault rules auto-load if the user `cd`s into the vault inside Claude Code; `AGENTS.md` stays canonical for cross-tool compatibility.

Vault-side operations (`ingest`, `query`, `lint`) halt if `AGENTS.md` is missing. Ask the user to `bootstrap` or restore the file.

The skill treats the vault as read-only except for paths each operation is defined to touch (see `references/operations.md`).

## Methodology Swap

The v1.0.0 default methodology is Karpathy's LLM-maintained-wiki pattern (see `references/karpathy-original.md` for the source and `references/agents-template.md` for the agent-readable rendering). To swap:

1. Replace `references/agents-template.md` with rules for a different methodology. Only requirement: the new template must define `ingest`, `query`, and `lint` behaviors.
2. Run `bootstrap --force` to wipe and rebuild the vault. Destructive — back up `~/.ultrabrain/raw/` first if you want to preserve source material for re-capture.

## Hooks

Two hooks are available but **not auto-installed**:

- `SessionStart` — injects vault status (wiki count, unprocessed raw, last ingest) at session start so Claude is aware the vault is available.
- `PreCompact` — injects a reminder before context compaction to capture important session content before detail is lost.

On explicit user request ("install ultrabrain hooks"), follow `references/setup.md` to copy both hook scripts and merge the entries into `~/.claude/settings.json` using Read → diff → confirm → Edit discipline. Both hooks install as a bundle; either can be uninstalled individually later.

## References

- `references/karpathy-original.md` — verbatim source methodology + attribution
- `references/agents-template.md` — bootstrap copies this to `~/.ultrabrain/AGENTS.md`
- `references/operations.md` — full step-by-step for all five operations
- `references/setup.md` — hook install/uninstall (SessionStart + PreCompact)
- `references/hooks/session-start.sh` — vault status injection on session start
- `references/hooks/pre-compact.sh` — capture reminder before compaction
