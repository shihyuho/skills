# Ultrabrain

Drive a personal, LLM-maintained wiki at `~/.ultrabrain/` that compounds knowledge across sessions.

Based on [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): three layers (raw sources / LLM-maintained wiki / schema), three operations (ingest / query / lint). This skill adds `bootstrap` to create the vault and `capture` to split source intake from integration so you can drop material quickly.

## When It Triggers

- **Factual / technical / decision questions** — description-driven; Claude checks `index.md` before answering.
- **"記下來 X" / "capture this"** — push content into `raw/`.
- **"ingest" / "整合 raw"** — integrate unprocessed raw entries into the wiki.
- **"lint vault"** — health-check report (contradictions, orphans, stale pages).
- **"bootstrap ultrabrain"** — create the vault on first use.

Skipped for small talk, current-file questions, and code-execution requests.

## Installation

```bash
npx skills add shihyuho/skills --skill ultrabrain -g
```

Then run `bootstrap ultrabrain` in any Claude Code session. Optionally `install ultrabrain hooks` to enable the `SessionStart` (vault status on every session) and `PreCompact` (capture reminder before compaction) hooks.

## Vault Layout

```text
~/.ultrabrain/
├── AGENTS.md          # methodology rules (bootstrap-seeded, user-owned)
├── CLAUDE.md          # one line: @AGENTS.md
├── index.md           # wiki catalog
├── log.md             # append-only operation history
├── raw/               # unprocessed captures
│   └── .processed/    # audit trail after ingest
└── wiki/              # integrated knowledge pages
```

## Methodology Swap

The skill is methodology-agnostic. Replace `references/agents-template.md` with any rules that define `ingest`, `query`, and `lint` behaviors, then `bootstrap --force` to rebuild. Destructive — back up `~/.ultrabrain/raw/` first.

## Guardrails

- Vault-side operations halt if `AGENTS.md` is missing.
- `capture` never silently overwrites; collisions go to suffixed names or a user-chosen merge.
- `lint` reports only — you direct every repair.
- Hook installer uses Read → diff → confirm → Edit on `~/.claude/settings.json`.
- Both hooks (`SessionStart`, `PreCompact`) exit silently if the vault is absent.

## Credits

Methodology: [Andrej Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Verbatim source in `references/karpathy-original.md`.
