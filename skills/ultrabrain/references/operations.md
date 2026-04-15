# Ultrabrain Operations

Detailed step-by-step for each operation. Read this when an operation triggers and you need the full procedure. SKILL.md dispatches to this file for the heavy details.

Vault location: `~/.ultrabrain/`.

Five operations:

- `bootstrap` — skill-side — create the vault on disk
- `capture` — skill-side — push session or file content into `raw/`
- `ingest` — delegates to vault `AGENTS.md` — integrate `raw/` into `wiki/`
- `query` — delegates to vault `AGENTS.md` — answer from the wiki
- `lint` — delegates to vault `AGENTS.md` — produce a health report

`bootstrap` and `capture` are owned by this skill and defined in full here. `ingest`, `query`, `lint` are owned by the vault's `AGENTS.md` — this file tells you how to *reach* them (load `AGENTS.md`, delegate), and the vault file tells you what to *do*.

---

## bootstrap

### Triggers

- User explicit: "bootstrap ultrabrain", "initialize vault", "設定 ultrabrain", "建立 vault"
- Implicit: when another operation runs and `~/.ultrabrain/` does not exist, ask the user to confirm bootstrap before proceeding.
- Force variant: "bootstrap --force", "wipe and rebuild", "reset vault". Used for the Methodology Swap workflow (replace `agents-template.md`, then force-bootstrap).

### Steps

1. **Check existence.** If `~/.ultrabrain/` already exists and the user did not request `--force`:
   - Report the current state in one line (e.g., "vault already exists at ~/.ultrabrain/ with N wiki pages, M raw files").
   - Exit without touching anything.
   - Tell the user to use `--force` if they want to rebuild.
2. **Force path.** If `--force` was requested, confirm in-session ("this will delete the existing `~/.ultrabrain/` including all wiki content. Proceed?") before deleting. Make sure the user has exported `raw/` and `raw/.processed/` elsewhere if they want to keep source material.
3. **Create directories**: `~/.ultrabrain/raw/` and `~/.ultrabrain/wiki/`.
4. **Copy the template**: copy this skill's `references/agents-template.md` to `~/.ultrabrain/AGENTS.md`. Do not modify contents during the copy.
5. **Write `~/.ultrabrain/CLAUDE.md`** with exactly one line: `@AGENTS.md`. This imports the canonical rules when Claude Code opens the vault directory.
6. **Write `~/.ultrabrain/index.md`** with a minimal skeleton:
   ```markdown
   # Wiki Index

   Last updated: YYYY-MM-DD

   No entries yet.
   ```
7. **Write an empty `~/.ultrabrain/log.md`** (zero bytes).
8. **Append** the bootstrap entry to `log.md`:
   ```
   2026-04-15T10:00:00Z BOOTSTRAP vault initialized from ultrabrain v1.0.0
   ```
9. **Report** to the user: "Vault ready at `~/.ultrabrain/`. Say 'install ultrabrain hooks' to enable the `SessionStart` + `PreCompact` reminders, or start capturing knowledge with 'capture X' or '記下來 X'."

---

## capture

### Triggers

- User explicit only. Natural-language phrases: "記下來 X", "capture this", "save to vault", "存進 vault", or pointing at an external file: "capture ~/Downloads/notes.md".

### Content boundary — three-layer resolution

Before writing anything, resolve *what* to capture:

1. **Explicit reference.** If the user names the content ("記下來上面那三點", "capture the Threads post I pasted", "save the decision about retry policy"), capture exactly that. Quote verbatim or near-verbatim; don't summarize aggressively.
2. **Ambiguous capture.** If the user says "記下來" or "capture this" without pointing at anything, **do not write silently**. Produce a short proposal:
   > "Preparing to capture: \<topic in 5-10 words\>, ~\<N\> chars from the last \<context window\>. Looks right?"
   Wait for confirmation or redirection. Only write after the user agrees or clarifies.
3. **Prefer small over large.** When in doubt, capture a smaller slice. A second supplementary capture is cheaper than cleaning up an over-stuffed raw file during ingest.

Record the user's capture instruction verbatim in the `origin:` frontmatter so ingest can later trace intent.

### Filename generation

Base pattern: `YYYY-MM-DD-<slug>.md`. Today's date plus a short kebab-case slug derived from content (5-8 words max, descriptive).

Examples:
- `2026-04-15-karpathy-three-layer-architecture.md`
- `2026-04-15-api-retry-policy-decision.md`
- `2026-04-15-threads-post-second-brain.md`

### Collision handling

Before writing to `raw/<filename>.md`:

1. Check if `raw/<filename>.md` exists. Also check `raw/.processed/<filename>.md`.
2. **If neither exists**, write and move on.
3. **If one exists**, offer the user a choice:
   > "A raw entry with the same name already exists (`raw/<filename>.md`). Options: (a) append to existing file with a `---` separator + timestamp, (b) create a new file with suffix `-2` (or `-3`, `-4`...). Pick, or I'll default to (b)."

   Default is option (b) — suffix. **Never silently overwrite.**
4. **If user picks (a) merge**: open the existing file, append:
   ```markdown

   ---

   ## Additional capture — 2026-04-15T10:32:11Z

   origin: "<user's instruction verbatim>"

   \<content\>
   ```
   Do not modify the existing content above the separator.
5. **If user picks (b) or defaults**: find the lowest unused suffix and write to `raw/<filename>-N.md`.

### Write format

```markdown
---
source: session | file | url
date: 2026-04-15
origin: "user said '記下來那個 Karpathy 三層架構'"
---

\<content — preserved in source language, near-verbatim>
```

`source` values:
- `session` — content pulled from the current session (user message, assistant message, or a stretch of dialog)
- `file` — contents of a file the user pointed to
- `url` — fetched from a URL the user provided (include the URL in the body)

### Steps

1. Ensure `~/.ultrabrain/` exists. If not, trigger bootstrap flow (ask user to confirm).
2. Resolve content boundary (section above).
3. Generate filename; handle collision.
4. Write to `raw/<filename>.md` with frontmatter and content.
5. **Do not touch** `wiki/`, `index.md`, or `raw/.processed/`.
6. Append to `log.md`:
   ```
   2026-04-15T10:32:11Z CAPTURE raw/2026-04-15-karpathy-three-layer-architecture.md
   ```
7. Report: path written, one-sentence preview, and a reminder that `ingest` integrates the raw file into the wiki.

---

## ingest

### Triggers

- User explicit: "ingest", "integrate raw", "sync vault", "整理 vault", "整合 raw"

### Skill-side steps

1. Verify `~/.ultrabrain/` exists and `AGENTS.md` is present. If `AGENTS.md` is missing, stop: tell the user to `bootstrap` or restore the file from `references/agents-template.md`.
2. List unprocessed files in `raw/` (exclude `raw/.processed/`). If empty, tell the user and exit.
3. **Read `~/.ultrabrain/AGENTS.md`** into context. Its `Operation: Ingest` section defines the actual integration procedure.
4. **Delegate** to the vault rules: follow the steps in `AGENTS.md`'s ingest section for each raw file.
5. After the vault-rules procedure completes, verify that each processed raw file has been moved to `raw/.processed/` and that `index.md` has been updated.
6. Append one `INGEST` entry to `log.md` per raw file processed.
7. Report back: files processed, pages created, pages updated, pages skipped with reasons.

---

## query

### Triggers

- **Description-driven** (primary). The skill's description surfaces this skill when the user asks factual, technical, or decision-oriented questions that plausibly concern retained knowledge.
- User explicit (backup): "查 vault", "ultrabrain 裡有沒有提過 X", "search the vault for Y".

### Skip clause (negative guardrail)

Before reading any vault file, verify the user's question plausibly concerns retained knowledge. **Skip the vault read** (fall through to normal answering) for:

- **Small talk** — greetings, thanks, meta-questions about the current session ("你會中文嗎", "what can you do").
- **Context-local questions** — answerable from the current session or open files: "what does this file do", "why is this line wrong", "what did you just change".
- **Execution requests** — tasks, not questions: "write a function", "run the tests", "refactor this", "add a button".

When classification is uncertain, **default to skipping** the vault read. Aggressive triggering is backed by this negative filter, not lifted by it.

### Skill-side steps

1. Apply the skip clause. If it applies, answer normally; do not read the vault.
2. Verify `~/.ultrabrain/` exists and `index.md` lists at least one wiki entry (beyond the "No entries yet." skeleton). If the vault is empty, fall back to a normal answer with a one-line note ("Vault is empty; answering from general knowledge").
3. **Read `~/.ultrabrain/AGENTS.md`** into context. Its `Operation: Query` section defines navigation rules.
4. **Read `~/.ultrabrain/index.md`** fully.
5. **Delegate** to the vault rules: follow the steps in `AGENTS.md`'s query section — locate candidate pages, Read them, follow cross-references.
6. Produce the answer with citations per the vault rules.
7. Append one `QUERY` entry to `log.md`.

Index-first strict. No Grep fallback on `wiki/` unless the vault rules explicitly call for it. If queries routinely miss, that's a signal the index is incomplete — surface it during `lint`, don't paper over with keyword search.

---

## lint

### Triggers

- User explicit: "lint", "check vault", "健檢 vault", "audit the wiki"

### Skill-side steps

1. Verify `~/.ultrabrain/` exists and `AGENTS.md` is present.
2. **Read `~/.ultrabrain/AGENTS.md`** into context. Its `Operation: Lint` section defines the checklist.
3. **Delegate** to the vault rules: scan `wiki/` and `index.md` for the checks listed in `AGENTS.md`.
4. Produce a markdown report. **Do not auto-fix.** At the end of the report, ask the user which findings they want addressed; work on them one at a time with confirmation.
5. Append one `LINT` entry to `log.md`.

---

## Global rules across operations

- **`log.md` entry format**: one line per entry, ISO-8601 prefix, uppercase operation keyword, no multi-line entries:
  ```
  2026-04-15T10:32:11Z CAPTURE raw/...
  2026-04-15T10:35:47Z INGEST raw/.processed/... → wiki/...
  2026-04-15T11:02:03Z QUERY "..." → wiki/...
  2026-04-15T18:00:00Z LINT N pages, C contradictions, ...
  ```
  Stable format — future log-rotation tooling can split by date or line count without migration.

- **Halt condition**: vault-side operations (`ingest`, `query`, `lint`) stop if `AGENTS.md` is missing. Ask the user to `bootstrap` or restore the file.

- **Scope of writes**: each operation writes only to the paths listed in its steps. Treat the rest of the vault as read-only.

- **No concurrency**: assume a single agent touches the vault at a time. No locking.
