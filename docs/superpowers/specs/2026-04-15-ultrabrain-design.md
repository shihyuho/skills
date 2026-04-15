# Ultrabrain Design

Date: 2026-04-15
Author: Shihyu Ho
Status: Approved, ready for planning

## Summary

`ultrabrain` is a Claude Code skill that drives an LLM-maintained personal wiki stored at `~/.ultrabrain/`. The skill is a thin trigger layer: the vault is the self-contained knowledge artifact and all methodology rules live inside the vault's `AGENTS.md`, not inside the skill. Moving the vault to another agent (Cursor, Aider) or machine keeps the knowledge usable; losing the skill only removes convenience.

The skill is **methodology-agnostic**. It ships Karpathy's LLM-maintained-wiki pattern as the v1.0.0 default because that's the source inspiration, but the methodology (page types, ingest rules, query rules, lint rules) is fully swappable by replacing `references/agents-template.md` and re-bootstrapping the vault. See "Methodology Swap" section.

Default methodology source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## Goals

- Bootstrap a self-contained personal wiki with one command.
- Let users capture session content or external files into the vault with low friction and explicit disambiguation.
- Batch-integrate captured material into the wiki under explicit user control.
- Answer user questions from the vault using an index-first navigation strategy, with clear guardrails against low-value triggering.
- Audit vault health on demand.
- Install optional `SessionStart` (vault awareness on each session) and `PreCompact` (capture reminder before compaction) hooks.
- Keep the methodology (what goes in `AGENTS.md`) swappable without changing the skill itself.

## Non-Goals

- No evals in v1.0.0 (side-effectful behavior is hard to test; query accuracy has no ground truth).
- No automatic lint repair — lint produces reports only.
- No Grep fallback during query in v1.0.0 (index-first strict; hybrid may come later).
- No automatic hook installation — user must explicitly ask before the skill touches `settings.json`.
- No mandated `AGENTS.md` structure — the skill's contract is behavioral (defines ingest/query/lint), not structural.
- No explicit methodology-migration tooling in v1.0.0 — swap is supported implicitly via `rm -rf && bootstrap`.
- No `SessionEnd` hook in v1.0.0 — deferred because its `additionalContext` behavior wasn't conclusively verified (session is ending, so there may be no consumer for injected text).
- No concurrency control — assume single-user, one operation at a time.
- No `log.md` rotation in v1.0.0 — format is stable enough to add rotation later without migration.

## Architecture

Three layers. The skill owns the top layer; the vault (user-owned after bootstrap) owns the middle and bottom layers.

```
┌───────────────────────────────────────────────────┐
│  Skill Layer (plugin package)                     │
│  skills/ultrabrain/                               │
│    SKILL.md, README.md                            │
│    references/                                    │
│      karpathy-original.md                         │
│      agents-template.md                           │
│      operations.md                                │
│      setup.md                                     │
│      hooks/{session-start,pre-compact}.sh         │
└───────────────────────────────────────────────────┘
                        │ reads / writes
                        ▼
┌───────────────────────────────────────────────────┐
│  Schema Layer (vault, single source of truth)     │
│  ~/.ultrabrain/                                   │
│    AGENTS.md    — canonical rules                 │
│    CLAUDE.md    — one line: @AGENTS.md            │
└───────────────────────────────────────────────────┘
                        │ governs
                        ▼
┌───────────────────────────────────────────────────┐
│  Data Layer (vault)                               │
│    raw/             unprocessed capture inputs    │
│    wiki/            integrated knowledge pages    │
│    index.md         wiki catalog                  │
│    log.md           append-only operation history │
└───────────────────────────────────────────────────┘
```

Design rules:

- Skill Layer never restates rules that belong in `AGENTS.md` — no duplicated content, no drift.
- Skill Layer makes no structural assumptions about `AGENTS.md` content — only that it defines how to perform `ingest`, `query`, and `lint`.
- `AGENTS.md` is the sole definition of page types, naming, tagging, and integration/query/lint rules. Its internal structure is whatever the methodology author chose.
- `CLAUDE.md` is one line (`@AGENTS.md`) so Claude Code auto-picks up the rules when the user `cd`s into the vault. Cross-platform via import syntax, no symlink.

## Operations

Five operations, three layers of authorship:

| Operation | Authored by | Purpose |
|-----------|-------------|---------|
| `bootstrap` | Skill (skill-only) | Create the vault on disk |
| `capture` | Skill (skill-only) | Push session/file content into `raw/` |
| `ingest` | Vault rules (AGENTS.md) | Integrate `raw/` → `wiki/` in batch |
| `query` | Vault rules (AGENTS.md) | Answer questions using index-first navigation |
| `lint` | Vault rules (AGENTS.md) | Produce a health report |

Rename note: Karpathy's gist calls the raw→wiki step "ingest" and has no separate capture. We added `capture` to let users drop material quickly without paying integration cost. The `ingest` name is kept aligned with the original gist's terminology so `references/karpathy-original.md` remains intelligible.

### bootstrap

**Triggers**
- User explicit: "bootstrap ultrabrain", "initialize vault", "設定 ultrabrain"
- Implicit: when any other operation runs and `~/.ultrabrain/` does not exist, the skill asks the user to confirm before bootstrapping.

**Steps**
1. If `~/.ultrabrain/` already exists, **refuse and exit** with a one-line status ("vault already exists at ~/.ultrabrain/"). User must pass `--force` (or explicitly say "force bootstrap", "wipe and rebuild") to proceed. `--force` deletes the existing directory after confirming with the user in-session.
2. Create `raw/` and `wiki/` as empty directories.
3. Copy `references/agents-template.md` → `~/.ultrabrain/AGENTS.md`.
4. Write `~/.ultrabrain/CLAUDE.md` containing exactly `@AGENTS.md`.
5. Write empty skeleton `index.md` (header + "No entries yet.").
6. Write empty `log.md`.
7. Append one `BOOTSTRAP` line to `log.md`.

**Output**
Short confirmation plus a note that the `SessionStart` hook can be installed by asking explicitly.

**Notes**
- The `--force` path is the sanctioned route for "swap methodology" (see Methodology Swap section).
- Partial-existence cases (directory exists but files missing) are intentionally treated the same as "exists" — refuse unless `--force`. Keeps the surface minimal; users with weird state handle it manually or force-bootstrap.

### capture

**Triggers**
- User explicit only. Examples: "記下來 X", "capture this", "save to vault", "capture ~/Downloads/notes.md".

**Inputs**
- Session content the user points at (a specific message, a stretch of dialog, a decision).
- External files or URLs.

**Content boundary (three-layer resolution)**
The skill must resolve *what* to capture with this fallback:

1. **Explicit reference** — user names the content ("記下來上面那三點", "capture the Threads post", "save the decision about X"). Capture exactly that.
2. **Ambiguous capture** — user says "記下來" with no pointer. The skill **must not** write a file silently. It produces a short proposal ("preparing to capture: <topic>, ~<N> chars. OK?") and waits for confirmation before writing.
3. **Prefer small over large** — when in doubt, capture a smaller slice. A second supplementary `capture` is cheaper than cleaning up an over-stuffed raw file.

The `origin` frontmatter field records the user's capture instruction verbatim (e.g., `origin: "user said '記下來那個 Karpathy 三層架構'"`) so ingest can trace capture intent.

**Filename and collision handling**
1. Base filename: `YYYY-MM-DD-<slug>.md`. Slug generated from content.
2. Before writing, check if `raw/<filename>` or `raw/.processed/<filename>` already exists. If it does:
   - Offer the user a choice: (a) append to the existing raw file (separator `---` + timestamp, no overwrite), or (b) create a new file with suffix (`-2`, `-3`, etc.).
   - Never silently overwrite.
3. Default behavior if user doesn't choose: option (b) with suffix. Loud failure beats silent loss.

**Steps**
1. Ensure vault exists; otherwise trigger bootstrap flow.
2. Resolve content boundary per above.
3. Generate filename; check and resolve collision per above.
4. Write to `raw/<filename>` with frontmatter (`source`, `date`, `origin`) and near-verbatim material. Do not summarize aggressively — integration happens during `ingest`.
5. Do not touch `wiki/` or `index.md`.
6. Append one `CAPTURE` line to `log.md`.

**Output**
Path to the new raw file (or the updated one for merge case) and a reminder that `ingest` integrates it.

### ingest

**Triggers**
- User explicit: "ingest", "integrate raw", "sync vault", "整理一下 vault".

**Inputs**
- Every unprocessed file currently in `~/.ultrabrain/raw/`.

**Steps**
1. Verify vault exists and `AGENTS.md` is present. If `AGENTS.md` is missing, stop and ask the user to re-bootstrap or restore it.
2. Load `AGENTS.md` into context. Hand control to its `ingest` section for the actual integration logic.
3. For each raw file: read, extract, decide which wiki page to create or update, update cross-references, update `index.md`.
4. Move processed raw files to `raw/.processed/` as an audit trail (do not delete).
5. Append one `INGEST` line to `log.md` listing affected wiki pages.

**Output**
Summary: N files processed, pages created, pages updated, pages skipped (with reasons).

### query

**Triggers**
- Description-guided (primary). The skill's description makes Claude consider the vault whenever a user question might have been captured earlier.
- User explicit (backup): "查 vault", "ultrabrain 裡有沒有提過 X".

**Skip clause (negative guardrail)**
Before reading `index.md`, the skill MUST verify the user's question plausibly concerns retained knowledge. Skip the vault read for:

- **Small talk** — greetings, thanks, meta-questions about the session itself.
- **Context-local questions** — "what does this file do", "why is this line wrong", "what did you just change" — answerable from current session context, not vault.
- **Execution requests** — "write me a function", "run the tests", "refactor this" — the vault holds facts, not tasks.

If the classification is uncertain, default to skipping the vault read. Aggressive triggering is backed by this negative filter, not lifted by it.

**Steps**
1. Apply skip clause. If it applies, skip the vault entirely and answer normally.
2. Verify vault exists and `index.md` lists at least one wiki entry. If the vault was bootstrapped but never ingested, fall back to a normal answer with a note that the vault is empty.
3. Read `index.md` fully.
4. Hand control to `AGENTS.md`'s `query` section: locate relevant pages from the index, Read them, follow cross-references as the vault rules dictate.
5. Produce the answer with explicit citations to `wiki/path/page.md`.
6. Append one `QUERY` line to `log.md` with the pages consulted.

**Strictness**
Index-first strict. No Grep fallback in v1.0.0. If the user reports low hit rate, revisit with a hybrid approach in a later version.

### lint

**Triggers**
- User explicit: "lint", "檢查 vault", "健檢".

**Steps**
1. Load `AGENTS.md`'s `lint` section.
2. Scan `wiki/` for contradictions, orphaned pages (no inbound links), stale pages (not touched in >90 days), index/filesystem drift, and missing cross-references.
3. Produce a markdown report.
4. Do not repair automatically. Ask the user which findings to address interactively.
5. Append one `LINT` line to `log.md`.

**Output**
A markdown health report.

## Vault Contract (skill-enforced minimum)

The skill guarantees only this skeleton at bootstrap time:

```
~/.ultrabrain/
  AGENTS.md
  CLAUDE.md          # one line: @AGENTS.md
  index.md
  log.md
  raw/
  wiki/
```

**Contract with `AGENTS.md` is behavioral, not structural**: the skill requires only that `AGENTS.md` define — in any structure the methodology author prefers — how to perform `ingest`, `query`, and `lint` against the vault. No specific sections, headings, or formats are mandated. The skill loads `AGENTS.md` into context and delegates.

Everything else — subdirectory layout under `wiki/`, frontmatter schema, tag conventions, page types, cross-reference syntax — is defined inside `AGENTS.md` and fully owned by the user after bootstrap. The skill never overwrites `AGENTS.md` after bootstrap.

Global rules enforced by the skill at runtime:

- Vault-side operations (`ingest`, `query`, `lint`) halt if `AGENTS.md` is missing.
- Every operation appends exactly one entry to `log.md` in a stable format: `ISO-8601 OPERATION details` (uppercase operation keyword, single line, no multi-line entries). The format is stable enough that future log-rotation tooling can split by date or line count without migration.
- The skill treats the vault as read-only except for the specific paths each operation is defined to touch.

## Triggers and Description

The SKILL.md description is structured in two parts: a high-density semantic hint for the matcher, followed by explicit operation triggers and a skip clause for negative signal. Final text:

> Personal wiki at `~/.ultrabrain/` that accumulates knowledge across sessions using an LLM-maintained-wiki pattern. Use when the user asks factual, technical, or decision-oriented questions that may have been previously captured (check index.md before answering), or explicitly asks to capture/記下來/save session content, ingest/整合 raw entries into the wiki, lint/檢查 the vault, or bootstrap a new vault. Skip for small talk, current-file questions, or code-execution requests.

Design rationale:

- **~60 words**. Dense enough to teach the matcher the skill's scope without diluting the signal.
- **Query case surfaces first** because it's the highest-frequency trigger point.
- **Skip clause** gives the matcher explicit negative signal — not every user question should trigger a vault check.
- **Bilingual triggers** (`capture/記下來/save`, `ingest/整合`, `lint/檢查`) because users mix Chinese and English naturally.
- **No mention of Karpathy by name** — the skill is methodology-agnostic; the description describes the pattern, not the source.

## Hooks

**v1.0.0 ships `SessionStart` and `PreCompact`**. `SessionEnd` was considered but deferred — its `additionalContext` behavior wasn't conclusively verified (the session is ending, so there may be no consumer for injected text). It returns in a later version once behavior is verified on live Claude Code.

`Stop` is intentionally excluded: firing on every assistant turn is too noisy.

| Hook | Purpose | Output |
|------|---------|--------|
| `SessionStart` | Surface vault status so Claude knows it exists early | `vault: N wiki pages, M unprocessed raw, last ingest <date>` (dynamic, reads vault) |
| `PreCompact` | Remind to capture important content before compaction strips detail | Static reminder to use `capture X` before context is compacted |

Both hooks emit Claude Code hook JSON payloads (`hookSpecificOutput` with `hookEventName` and `additionalContext`). `SessionStart`'s payload is dynamic (counts wiki pages, raw files, reads last `INGEST` from `log.md`). `PreCompact`'s payload is static (no vault stats — the message is time-critical, not status-oriented).

**Installation model**

User must ask explicitly ("install ultrabrain hooks", "setup reminders"). The skill follows `references/setup.md` to:

1. Copy both hook scripts to `~/.claude/hooks/using-ultrabrain-session.sh` and `~/.claude/hooks/using-ultrabrain-precompact.sh`.
2. `chmod +x` the copied scripts.
3. Update `~/.claude/settings.json`:
   - **First** `Read` the file so Claude has the current content in context.
   - **Then** produce the proposed diff (covering both `SessionStart` and `PreCompact` entries) and show it to the user for confirmation.
   - **Only after user confirms**, use `Edit` to apply anchored changes that merge the new entries without disturbing other hooks.
   - Check per-hook for existing entries pointing at the same script path and skip any that are already installed (idempotent).
4. Confirm installation with the user.

Uninstall reverses step 1–3 with the same Read → diff → confirm → Edit discipline. The two hooks install as a bundle; individual uninstall is supported by the same flow applied to a single entry.

Scripts are minimal bash (no dependencies beyond a POSIX shell), exit silently if `~/.ultrabrain/` does not exist, and never fail the session.

## SKILL.md Structure

SKILL.md is short (~60–80 lines), following the `write-a-skill` convention:

- Frontmatter (`name`, `description`, `license`, `metadata.author`, `metadata.version: "1.0.0"`)
- One-line intro
- Trigger Contract section — five operations, when to trigger each; includes the query **skip clause** (small talk / context-local / execution requests bypass vault)
- Operations section — skill-side steps only; vault-side details delegated to `AGENTS.md`. Includes capture's content-boundary resolution and filename collision handling.
- Vault Contract section — location, `AGENTS.md` as sole behavioral source of truth, no structural mandate
- Hooks section — points to `references/setup.md` and the explicit-ask install model with Read → diff → confirm → Edit discipline
- References index

Step-by-step details for each operation live in `references/operations.md`, not in SKILL.md.

## Language Convention

- Skill-authored files (SKILL.md, README.md, references/*.md): English, per repo convention.
- Vault template (`agents-template.md`): English, because Claude follows English rule prompts most reliably.
- User content inside the vault (`raw/`, `wiki/`): user's language. Capture preserves source language verbatim; `AGENTS.md` explicitly instructs ingest to maintain the original language and not force translation.

## Marketplace Entry

Add to `.claude-plugin/marketplace.json`:

```json
{
  "name": "ultrabrain",
  "source": "./skills/ultrabrain",
  "version": "1.0.0",
  "description": "Karpathy-style LLM-maintained personal wiki at ~/.ultrabrain/"
}
```

Also update the top-level `README.md` skill list in the same change (per repo's global constraint).

## File Inventory (to be created)

```
skills/ultrabrain/
  SKILL.md
  README.md
  references/
    karpathy-original.md          # verbatim copy of the gist + attribution header; source of v1.0.0 methodology
    agents-template.md            # faithful rendering of Karpathy's logic as agent-readable rules; bootstrap copies this into the vault
    operations.md                 # full step-by-step for all five operations
    setup.md                      # SessionStart hook install/uninstall procedure
    hooks/
      session-start.sh
      pre-compact.sh
```

Plus updates to:
- `README.md` (top-level, add ultrabrain to skills list)
- `.claude-plugin/marketplace.json` (add entry)

## Methodology Swap

The skill is methodology-agnostic. The v1.0.0 default is Karpathy's LLM-maintained-wiki pattern, embodied by `references/agents-template.md`. A user who prefers a different methodology (Zettelkasten, Johnny Decimal, a custom taxonomy) can swap by:

1. Replacing the content of `references/agents-template.md` with rules for the new methodology. The only requirement is that the new template define `ingest`, `query`, and `lint` behaviors.
2. Running `bootstrap --force` to wipe the old vault and materialize a fresh one using the new template. **Destructive** — existing wiki content is lost. Users wanting to keep raw source material should copy `~/.ultrabrain/raw/` and `~/.ultrabrain/raw/.processed/` elsewhere first; they can re-`capture` and `ingest` them against the new methodology after.

v1.0.0 provides **implicit support only** — no dedicated operation for methodology migration, no export/import tooling. If real usage surfaces pain around this (e.g., users routinely losing knowledge during swaps), a later version can introduce a `repave` operation that exports/imports raw content across the swap.

`references/karpathy-original.md` documents the current default methodology's source. If a user permanently adopts a different methodology, they can also swap this file — it exists for provenance, not for the skill's operation.

## Open Decisions Recorded

These were decided during brainstorming (Q1–Q7) and grill-me (G1–G10). All are frozen for v1.0.0.

Brainstorming:
- Description-first for query, hooks for ingest reminders only. (Q1 → C)
- Two-phase capture/ingest rather than one-shot. (Q2 → B)
- Lint included from v1.0.0. (Q3 → B)
- Hooks are reminders only, not automatic actions. (Q4 → A)
- Vault owns its rules via `AGENTS.md`; skill owns flow only. (Q5 → C, plus `CLAUDE.md` → `@AGENTS.md` import)
- Index-first strict for query; no Grep fallback. (Q6 → A)
- Skill name: `ultrabrain`. (Q7 → A)
- Operation name alignment: keep Karpathy's `ingest` for raw→wiki; introduce `capture` for session→raw.
- `init` renamed to `bootstrap`.
- Aggressive query trigger in description (always check vault first if question might be covered).
- Short SKILL.md, details in `references/`.
- Version 1.0.0 from the start.
- No evals in v1.0.0.
- Vault content language follows the user.

Grill-me resolutions:
- Capture content boundary: three-layer resolution with proposal-then-confirm for ambiguous cases. (G1)
- `settings.json` editing: AI edits directly but with Read → diff → confirm → Edit discipline. (G2)
- Query skip clause: small talk, context-local questions, execution requests bypass the vault read. (G3)
- Bootstrap on existing directory: refuse unless `--force`; no partial-state detection. (G4)
- Capture filename collision: suffix by default, offer merge option, never silently overwrite. (G5)
- Karpathy source: ship verbatim with attribution header (not paraphrased). (G6, reversed)
- `AGENTS.md` structure: no mandated sections — contract is behavioral. (G7, reversed)
- `log.md`: no rotation in v1.0.0 but strict single-line format enables future rotation. (G8)
- Hooks: v1.0.0 ships `SessionStart` and `PreCompact`; `SessionEnd` deferred pending behavioral verification. (G9 + later reversal — PreCompact has explicit documentation for context preservation, making it a verified use case; SessionEnd's `additionalContext` destination remains unclear.)
- Description: 60-word two-part form with positive triggers + skip clause. (G10)
- Methodology swap: implicit support via `--force` bootstrap; no dedicated migration tooling.

## Risks and Mitigations

- **Description too aggressive, noisy query behavior.** Mitigation: skip clause filters small talk / local-context / execution requests before the vault is read. If noise still dominates, pull back description phrasing in a minor version.
- **Vault grows and `index.md` becomes unwieldy.** Mitigation: lint surfaces staleness; user can evolve index structure via `AGENTS.md` without touching the skill.
- **User edits `AGENTS.md` into an inconsistent state.** Mitigation: skill reads `AGENTS.md` literally; bad rules produce bad results but never corrupt vault data. `log.md` preserves history for recovery.
- **AI-driven `settings.json` editing corrupts the file.** Mitigation: mandatory Read → diff → user confirm → Edit flow. User sees every change before it's applied. Plus idempotency check for repeat installs.
- **Capture silently loses data due to filename collision.** Mitigation: never overwrite; suffix by default; offer explicit merge option.
- **`--force` bootstrap destroys unbacked knowledge.** Mitigation: `--force` requires explicit user invocation and in-session confirmation. Users are told to back up `raw/` before swapping methodology.
- **Hook output behaviour differs from expectation.** Mitigation: both `SessionStart` and `PreCompact` hooks skip-on-missing-vault, never fail the session; worst case is a missing reminder, not broken Claude Code. `SessionEnd` was deferred specifically because its output destination wasn't verified.
- **Karpathy methodology content attribution concerns.** Mitigation: ship with clear attribution header and source URL; file is trivially removable or swappable if the original author objects or the user adopts a different methodology.
- **`log.md` grows unbounded.** Mitigation: strict single-line format makes future rotation mechanical. Lint does not depend on `log.md` (uses page `updated:` frontmatter instead).

## Next Step

Invoke the `writing-plans` skill to turn this spec into an implementation plan.
