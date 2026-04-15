# Ultrabrain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `skills/ultrabrain/` v1.0.0 — a Claude Code skill that drives an LLM-maintained personal wiki at `~/.ultrabrain/`, following the spec at `docs/superpowers/specs/2026-04-15-ultrabrain-design.md`.

**Architecture:** Thin trigger layer. `SKILL.md` routes five operations (`bootstrap`, `capture`, `ingest`, `query`, `lint`). `bootstrap` and `capture` are skill-side; `ingest`, `query`, `lint` delegate to the vault's `AGENTS.md` (seeded from `references/agents-template.md`). Two opt-in hooks: `SessionStart` injects vault status, `PreCompact` warns to capture before compaction.

**Tech Stack:** Markdown files, POSIX bash scripts (`session-start.sh`, `pre-compact.sh`), JSON config (`.claude-plugin/marketplace.json`). No build system, no package deps beyond what Claude Code ships with. Verification via shell commands.

---

## File Structure

Create (all under `skills/ultrabrain/`):

```
skills/ultrabrain/
├── SKILL.md                              # trigger contract + operations summary (~75 lines)
├── README.md                             # user-facing install/usage (~50 lines)
└── references/
    ├── karpathy-original.md              # verbatim gist + attribution header
    ├── agents-template.md                # faithful Karpathy-logic rendering; bootstrap copies this
    ├── operations.md                     # 5-op full step-by-step
    ├── setup.md                          # hooks install/uninstall (SessionStart + PreCompact)
    └── hooks/
        ├── session-start.sh              # executable; emits SessionStart hook JSON
        └── pre-compact.sh                # executable; emits PreCompact hook JSON
```

Modify:

- `.claude-plugin/marketplace.json` — insert `ultrabrain` plugin entry between `tldr` and `writing-agents-md`.
- `README.md` (repo root) — add ultrabrain bullet to the skills list.

Separation of concerns:

- **`SKILL.md`** — what triggers each operation, one-paragraph ops summary, pointers into `references/`. Must stay under 100 lines so Claude loads it reliably.
- **`references/operations.md`** — full procedural detail for all five operations; loaded when an operation fires.
- **`references/agents-template.md`** — the vault's schema file (copied to `~/.ultrabrain/AGENTS.md` on bootstrap). Owns the vault's methodology rules for `ingest`/`query`/`lint`.
- **`references/karpathy-original.md`** — verbatim source methodology for traceability; never loaded by the skill, only preserved for humans to read.
- **`references/setup.md`** — install/uninstall procedure for both hooks (not auto-applied).
- **`references/hooks/session-start.sh`** — per-session vault status injection.
- **`references/hooks/pre-compact.sh`** — pre-compaction capture reminder.

---

## Task 1: Scaffold directory and `references/karpathy-original.md`

**Files:**
- Create: `skills/ultrabrain/references/hooks/` (directory, nested mkdir)
- Create: `skills/ultrabrain/references/karpathy-original.md`

- [ ] **Step 1: Create the directory tree**

```bash
mkdir -p skills/ultrabrain/references/hooks
```

- [ ] **Step 2: Verify tree exists and is empty**

```bash
ls -la skills/ultrabrain/references/hooks/
```

Expected: two entries (`.`, `..`), no files yet.

- [ ] **Step 3: Fetch Karpathy gist verbatim into a temp file**

```bash
curl -sfL https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw > /tmp/karpathy-gist.md
wc -l /tmp/karpathy-gist.md
```

Expected: ~80 lines of markdown fetched.

- [ ] **Step 4: Write `references/karpathy-original.md` with attribution header + verbatim gist**

Write the file with this exact structure — header first, then the contents of `/tmp/karpathy-gist.md` appended verbatim:

```markdown
# Source: Karpathy's LLM-Maintained Wiki Pattern

- **URL**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Author**: Andrej Karpathy
- **Included verbatim** for methodology fidelity. The `agents-template.md` in this directory is a faithful rendering of the logic described below as agent-readable rules.
- If the original author requests removal or you adopt a different methodology, this file is swappable without affecting the skill's operation.

---

<CONTENTS OF /tmp/karpathy-gist.md, pasted verbatim starting from its `# LLM Wiki` line>
```

Implementation tip — do this in shell to avoid manual copy-paste mistakes:

```bash
cat > skills/ultrabrain/references/karpathy-original.md <<'HEADER'
# Source: Karpathy's LLM-Maintained Wiki Pattern

- **URL**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Author**: Andrej Karpathy
- **Included verbatim** for methodology fidelity. The `agents-template.md` in this directory is a faithful rendering of the logic described below as agent-readable rules.
- If the original author requests removal or you adopt a different methodology, this file is swappable without affecting the skill's operation.

---

HEADER
cat /tmp/karpathy-gist.md >> skills/ultrabrain/references/karpathy-original.md
```

- [ ] **Step 5: Verify the file starts with the attribution header and contains the gist body**

```bash
head -10 skills/ultrabrain/references/karpathy-original.md
grep -c "^# LLM Wiki$" skills/ultrabrain/references/karpathy-original.md
```

Expected: first command shows the header with URL and Author lines; second command outputs `1` (the gist's top-level header is present once).

- [ ] **Step 6: Clean up temp file**

```bash
rm /tmp/karpathy-gist.md
```

- [ ] **Step 7: Commit**

```bash
git add skills/ultrabrain/references/karpathy-original.md
git commit -m "feat(ultrabrain): scaffold skill dir and archive Karpathy source gist"
```

---

## Task 2: Write `references/agents-template.md`

This file is the vault's schema — copied to `~/.ultrabrain/AGENTS.md` on bootstrap. It renders Karpathy's methodology as agent-readable rules for `ingest`/`query`/`lint`.

**Files:**
- Create: `skills/ultrabrain/references/agents-template.md`

- [ ] **Step 1: Write the file**

Full content (copy exactly):

````markdown
<!-- ultrabrain-template-version: 1.0.0 -->
<!-- methodology: karpathy-llm-wiki -->
<!-- source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f -->

# Ultrabrain Vault

This vault is your personal, LLM-maintained wiki. You (the agent) own the wiki content and maintain it across sessions according to the rules below.

Unlike RAG — which rediscovers knowledge from raw sources on every query — this vault is a **persistent, compounding artifact**. Sources are integrated once into interlinked wiki pages; queries read the integrated synthesis, not the raw sources. The user curates inputs and asks questions; you do the reading, extraction, cross-referencing, and bookkeeping.

## Layers

- **`raw/`** — curated source documents. **Immutable** — you read them but never modify them. Pre-processed by the skill's `capture` step.
- **`wiki/`** — the interlinked markdown wiki. You own this layer entirely: create pages, update them when new sources arrive, maintain cross-references.
- **This file (`AGENTS.md`)** — the schema. Defines conventions and workflows. You and the user co-evolve this over time.

Two support files:

- **`index.md`** — content-oriented catalog. Lists every wiki page with a one-line summary, organized by category. Update on every ingest. Read first on every query.
- **`log.md`** — chronological append-only record of ingests, queries, and lint passes. One line per entry, ISO-8601 prefixed (`YYYY-MM-DDTHH:MM:SSZ OPERATION details`).

## Wiki Page Conventions

**Page types** (suggested — extend as your domain needs):

- **Entity pages** — people, products, tools, companies. Filename: `wiki/entities/<kebab-case-name>.md`.
- **Concept pages** — abstract ideas, patterns, techniques. Filename: `wiki/concepts/<kebab-case-name>.md`.
- **Topic pages** — synthesis across multiple entities/concepts; overviews. Filename: `wiki/topics/<kebab-case-name>.md`.
- **Source summary pages** — one per ingested raw file when it warrants standalone treatment. Filename: `wiki/sources/<YYYY-MM-DD-slug>.md`.

Create subdirectories as they emerge. A flat `wiki/` is fine for small vaults.

**Frontmatter** (every wiki page):

```yaml
---
type: entity | concept | topic | source
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/.processed/2026-04-15-example.md
tags: [tag-one, tag-two]
---
```

Keep `updated` current. `sources` lists every raw file that contributed to this page.

**Cross-references**: use `[[wiki/path/page.md]]`. Follow the target path as written. When you mention an entity or concept that has (or should have) its own page, link it — don't re-explain.

**Language**: preserve the language of the source material. Do not force translation. If a source is in Chinese, its summary and derived entity/concept pages stay in Chinese. Mixed-language vaults are fine; link across languages freely.

## Operation: Ingest

Trigger: user runs `ingest` (e.g., "integrate raw", "整理 vault"). Skill calls this procedure with every unprocessed file in `raw/`.

Procedure — for each raw file:

1. **Read** the raw file completely. Note its frontmatter (`source`, `date`, `origin`) to understand what the user meant to capture.
2. **Discuss when warranted** — for substantial sources, briefly tell the user what you're pulling out and what pages you plan to touch, then proceed. For short captures, just do it and report after.
3. **Extract** the key facts, claims, decisions, or arguments. Split by subject, not by paragraph — one raw source typically feeds multiple wiki pages.
4. **Decide targets**: for each extracted chunk, identify the correct wiki page.
   - If the relevant page exists: update it in place. Preserve existing content; add new material in the right section; update `updated:` frontmatter; add this raw file to `sources:`.
   - If it doesn't exist: create it with the frontmatter template above.
   - If new material **contradicts** existing content: do not overwrite. Add a note like `> **Note (conflict, 2026-04-15):** <old claim> — newer source says <new claim>. Source: [[raw/.processed/...]]`. Let the user resolve during lint.
5. **Maintain cross-references**: when you add a new page, scan existing pages for mentions that should link to it; add the `[[...]]` links. When you update an entity/concept page, check outbound links on related pages and add new connections if the update warrants them.
6. **Update `index.md`**: add/update one line per affected page. Keep grouped by type. Keep the `Last updated:` timestamp current.
7. **Move** the raw file from `raw/` to `raw/.processed/` (create the subdirectory if needed). Do not delete — it's the audit trail.
8. **Append** to `log.md`:
   ```
   2026-04-15T10:32:11Z INGEST raw/.processed/2026-04-15-slug.md → wiki/concepts/foo.md (updated), wiki/entities/bar.md (created)
   ```

After processing all raw files, report to the user: N files processed, pages created, pages updated, pages skipped (with reasons). If you skipped anything, say why.

## Operation: Query

Trigger: user asks a factual, technical, or decision-oriented question that might be answerable from the vault. Skill's description routes these to this procedure after its skip-clause filter.

Procedure:

1. **Read `index.md`** fully. Identify candidate pages whose summaries plausibly contain the answer.
2. **Read the candidates**. Follow `[[...]]` cross-references up to 2 hops deep when they're relevant to the question.
3. **Synthesize the answer** from what the wiki says. Every factual claim in your answer should be traceable to a specific wiki page.
4. **Cite** with inline references: `[wiki/path/page.md]` after each claim, or as a "Sources:" list at the end for shorter answers.
5. **Distinguish vault content from inference**: if you extrapolate beyond what's in the wiki, mark it clearly ("The wiki doesn't cover X directly, but based on [page], my inference is..."). Never present unsupported inference as vault content.
6. **If the vault is empty or contains nothing relevant**: say so explicitly ("Vault has no entries on this; answering from general knowledge instead"). Do not invent wiki pages.
7. **Append** to `log.md`:
   ```
   2026-04-15T11:02:03Z QUERY "<short query>" → wiki/concepts/foo.md, wiki/topics/bar.md
   ```

**File answers back into the wiki** when they have lasting value. If the user asked for a comparison, analysis, or synthesis that took nontrivial effort, offer to file it as a new wiki page. Good explorations compound; don't let them evaporate into chat history.

## Operation: Lint

Trigger: user runs `lint` (e.g., "check vault", "健檢"). Produces a report. **Never** auto-fixes.

Check for:

1. **Contradictions** — pages asserting incompatible claims. Flag with both page references.
2. **Orphans** — pages with zero inbound `[[links]]`. Either the page should be linked from an index or synthesis page, or it should be merged into a hub.
3. **Stale** — pages whose `updated:` frontmatter is more than 90 days old. Flag for review; stale isn't bad, but it's worth confirming still-accurate.
4. **Index drift** — files in `wiki/` not listed in `index.md`, or index entries pointing at files that don't exist.
5. **Missing cross-references** — important concept/entity names that appear on a page in plain text (not as `[[link]]`) and do have a dedicated page elsewhere.
6. **Data gaps** — concepts or entities mentioned across multiple pages but lacking their own page. Suggest creating them and, if the user is exploring, suggest new sources or searches that would fill the gap.

Output a markdown report grouped by check type. For each finding, give:

- The file(s) involved
- A one-line description of the issue
- A suggested fix (don't perform it)

End the report by asking: "Which of these would you like me to address? I'll take them one at a time and confirm before changing anything." **Wait for the user to direct fixes — do not repair unprompted.**

Append to `log.md`:
```
2026-04-15T18:00:00Z LINT N pages checked, C contradictions, O orphans, S stale, D drift, M missing-links
```

## Philosophy — Why This Works

The tedious part of maintaining a knowledge base is the bookkeeping, not the reading. Humans abandon wikis because the maintenance grows faster than the value. You don't get bored and you can touch 15 files in one pass. Maintenance cost is near zero, so the wiki stays maintained and compounds over time.

The user's job is curating sources, directing analysis, and asking good questions. Your job is everything else.

Preserve this division. Don't ask the user to do cross-reference bookkeeping; don't ask them to update the index; don't ask which directory a new page belongs in — make the call and note your choice in the ingest report so they can overrule if they disagree.
````

- [ ] **Step 2: Verify file exists and top matter is correct**

```bash
head -5 skills/ultrabrain/references/agents-template.md
grep -c "^## Operation:" skills/ultrabrain/references/agents-template.md
```

Expected: first command shows version comment; second command outputs `3` (Ingest, Query, Lint).

- [ ] **Step 3: Commit**

```bash
git add skills/ultrabrain/references/agents-template.md
git commit -m "feat(ultrabrain): add agents-template for vault bootstrap"
```

---

## Task 3: Write `references/operations.md`

Full step-by-step for all five operations. SKILL.md delegates here for procedural detail.

**Files:**
- Create: `skills/ultrabrain/references/operations.md`

- [ ] **Step 1: Write the file**

Full content (copy exactly):

````markdown
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
````

- [ ] **Step 2: Verify operations count**

```bash
grep -c "^## \(bootstrap\|capture\|ingest\|query\|lint\)$" skills/ultrabrain/references/operations.md
```

Expected: `5`.

- [ ] **Step 3: Commit**

```bash
git add skills/ultrabrain/references/operations.md
git commit -m "feat(ultrabrain): add operations.md with step-by-step procedures"
```

---

## Task 4: Write `references/setup.md`

Install/uninstall procedure for both hooks (`SessionStart` + `PreCompact`). Follows `git-commit-co-author/references/setup.md` style with Read → diff → confirm → Edit discipline for `settings.json`. The hooks install together as a bundle.

**Files:**
- Create: `skills/ultrabrain/references/setup.md`

- [ ] **Step 1: Write the file**

Full content (copy exactly):

````markdown
# Hooks — Install & Uninstall

This file guides installation of two hooks that surface ultrabrain at useful moments in a Claude Code session. Installation is opt-in — only run this when the user explicitly asks. The two hooks install together as a bundle.

Trigger phrases that mean "install":

- "install ultrabrain hooks", "setup ultrabrain reminders", "enable ultrabrain hooks", "裝 ultrabrain hook"

Trigger phrases that mean "uninstall":

- "uninstall ultrabrain hooks", "remove ultrabrain hooks", "disable ultrabrain reminders", "移除 ultrabrain hook"

## What the hooks do

Both hooks emit Claude Code hook JSON payloads that inject a one-line message into Claude's context. Both are silent (exit 0 with no output) when `~/.ultrabrain/` does not exist, so non-ultrabrain users see nothing. Both never fail the session.

### `SessionStart` — vault awareness

Fires once at session start. Injects current vault stats so Claude is aware the vault is available from the user's first message.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "ultrabrain vault available at ~/.ultrabrain/ — 42 wiki pages, 3 unprocessed raw entries, last ingest 2026-04-13T10:12:33Z. Consult index.md before answering factual questions that may be covered."
  }
}
```

### `PreCompact` — capture reminder before compaction

Fires before Claude Code compacts context. Injects a reminder that the user should capture any important session content before detail is lost. Static message — no vault stats.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "additionalContext": "Context compaction is imminent. If this session contains decisions, patterns, or facts worth keeping beyond compaction, say 'capture X' to file them into ~/.ultrabrain/raw/ before detail is lost."
  }
}
```

## Install

1. **Copy both scripts** to the user-level hooks directory:
   ```bash
   cp <skill-path>/references/hooks/session-start.sh ~/.claude/hooks/using-ultrabrain-session.sh
   cp <skill-path>/references/hooks/pre-compact.sh ~/.claude/hooks/using-ultrabrain-precompact.sh
   chmod +x ~/.claude/hooks/using-ultrabrain-session.sh ~/.claude/hooks/using-ultrabrain-precompact.sh
   ```
   (Replace `<skill-path>` with the actual path where this skill is installed. Create `~/.claude/hooks/` if it doesn't exist.)

2. **Merge the hook entries into `~/.claude/settings.json`** — discipline for JSON editing:

   **Step 1: Read.** Load `~/.claude/settings.json` with the Read tool first. If it doesn't exist, create it with the final shape shown below. The user sees the current state in the conversation.

   **Step 2: Plan the diff.** Check whether `SessionStart` or `PreCompact` entries already point at the ultrabrain scripts (idempotency check per hook). Skip any hook that's already installed. Determine the minimal merge: add missing entries without disturbing unrelated ones.

   **Step 3: Show the user the proposed diff** as a code block before applying. Example (both hooks new):
   ```diff
     "hooks": {
   +   "SessionStart": [
   +     {
   +       "hooks": [
   +         {
   +           "type": "command",
   +           "command": "~/.claude/hooks/using-ultrabrain-session.sh"
   +         }
   +       ]
   +     }
   +   ],
   +   "PreCompact": [
   +     {
   +       "hooks": [
   +         {
   +           "type": "command",
   +           "command": "~/.claude/hooks/using-ultrabrain-precompact.sh"
   +         }
   +       ]
   +     }
   +   ]
     }
   ```

   **Step 4: Wait for confirmation.** Do not edit until the user explicitly approves.

   **Step 5: Apply with `Edit`.** Use anchored `old_string` / `new_string` pairs; never rewrite the whole file. If the file doesn't already have a `hooks` key, add it. If `hooks.SessionStart` or `hooks.PreCompact` don't exist, add each as a single-element array.

   The final entry shape for both hooks:
   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "~/.claude/hooks/using-ultrabrain-session.sh"
             }
           ]
         }
       ],
       "PreCompact": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "~/.claude/hooks/using-ultrabrain-precompact.sh"
             }
           ]
         }
       ]
     }
   }
   ```

3. **Confirm**: tell the user both hooks are installed. `SessionStart` fires at the start of each new Claude Code session; `PreCompact` fires whenever Claude Code is about to compact context.

## Uninstall

1. **Remove both scripts**:
   ```bash
   rm -f ~/.claude/hooks/using-ultrabrain-session.sh ~/.claude/hooks/using-ultrabrain-precompact.sh
   ```

2. **Remove the entries from `~/.claude/settings.json`** using the same Read → diff → confirm → Edit discipline:
   - Read the current settings.
   - Locate the entries whose commands point to `using-ultrabrain-session.sh` and `using-ultrabrain-precompact.sh`.
   - Show the user the diff (entries being removed).
   - Wait for confirmation, then Edit to remove exactly those entries. Leave other hook entries untouched. If removing an entry leaves an empty array, either remove the key or leave the empty array — both are valid.

3. **Confirm uninstall** with the user.

## Notes

- `~/.claude/settings.json` is a user-global file. Other skills and user customizations may share it. **Never overwrite wholesale** — only edit the minimal entries we own.
- The two hooks install as a bundle, but if a user wants to remove just one, they can ask ("remove only the PreCompact hook") and the same Read → diff → confirm → Edit flow applies to a single entry.
- If the user stores their Claude Code config somewhere other than `~/.claude/` (rare), ask before proceeding.
- This skill does not ship a `SessionEnd` hook in v1.0.0. `SessionEnd`'s `additionalContext` behavior wasn't conclusively verified (the session is ending, so there may be no consumer for the injected text). Revisit in a later version if the need surfaces.
````

- [ ] **Step 2: Verify**

```bash
grep -c "^## \(Install\|Uninstall\)$" skills/ultrabrain/references/setup.md
grep -c "SessionStart\|PreCompact" skills/ultrabrain/references/setup.md
```

Expected: first command outputs `2`; second command outputs at least `4` (both hook names appear multiple times).

- [ ] **Step 3: Commit**

```bash
git add skills/ultrabrain/references/setup.md
git commit -m "feat(ultrabrain): add hooks setup.md covering SessionStart and PreCompact"
```

---

## Task 5: Write and test `references/hooks/session-start.sh`

First of the two hook scripts. Injects vault status on every session start.

**Files:**
- Create: `skills/ultrabrain/references/hooks/session-start.sh`
- Temporary: `/tmp/ultrabrain-hook-test-*/` (test fixtures — deleted after verification)

- [ ] **Step 1: Write the script**

Full content (copy exactly):

```bash
#!/usr/bin/env bash
# Claude Code SessionStart hook for ultrabrain
#
# Fires once at session start. If ~/.ultrabrain/ exists, injects a
# one-line vault status into Claude's context so the model is aware
# the vault is available. Silent (no output) if the vault does not
# exist, so non-ultrabrain users see nothing.
#
# Installation:
#   1. Copy to ~/.claude/hooks/using-ultrabrain-session.sh
#   2. chmod +x ~/.claude/hooks/using-ultrabrain-session.sh
#   3. Add SessionStart hook entry to ~/.claude/settings.json (see setup.md)

set +e

VAULT="$HOME/.ultrabrain"

[ -d "$VAULT" ] || exit 0

wiki_count=$(find "$VAULT/wiki" -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
raw_count=$(find "$VAULT/raw" -maxdepth 1 -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

last_ingest=""
if [ -f "$VAULT/log.md" ]; then
    last_ingest=$(grep ' INGEST ' "$VAULT/log.md" 2>/dev/null | tail -n 1 | awk '{print $1}')
fi

if [ -n "$last_ingest" ]; then
    msg="ultrabrain vault available at ~/.ultrabrain/ — ${wiki_count} wiki pages, ${raw_count} unprocessed raw entries, last ingest ${last_ingest}. Consult index.md before answering factual questions that may be covered."
else
    msg="ultrabrain vault available at ~/.ultrabrain/ — ${wiki_count} wiki pages, ${raw_count} unprocessed raw entries, no ingest yet. Consult index.md before answering factual questions that may be covered."
fi

cat <<HOOK_JSON
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "${msg}"
  }
}
HOOK_JSON
```

- [ ] **Step 2: Make executable**

```bash
chmod +x skills/ultrabrain/references/hooks/session-start.sh
```

- [ ] **Step 3: Test — vault missing → silent exit 0**

```bash
TESTHOME=$(mktemp -d)
OUT=$(HOME="$TESTHOME" skills/ultrabrain/references/hooks/session-start.sh)
EXIT=$?
echo "stdout:[$OUT]"
echo "exit:$EXIT"
rm -rf "$TESTHOME"
```

Expected:
```
stdout:[]
exit:0
```

- [ ] **Step 4: Test — populated vault → JSON output**

```bash
TESTHOME=$(mktemp -d)
mkdir -p "$TESTHOME/.ultrabrain"/{raw,wiki}
echo test > "$TESTHOME/.ultrabrain/wiki/p1.md"
echo test > "$TESTHOME/.ultrabrain/wiki/p2.md"
echo test > "$TESTHOME/.ultrabrain/raw/x.md"
printf "2026-04-14T15:30:00Z INGEST raw/.processed/foo.md\n" > "$TESTHOME/.ultrabrain/log.md"
HOME="$TESTHOME" skills/ultrabrain/references/hooks/session-start.sh | python3 -m json.tool
EXIT=$?
echo "exit:$EXIT"
rm -rf "$TESTHOME"
```

Expected: valid JSON printed via `python3 -m json.tool`, exit 0. The `additionalContext` field contains `2 wiki pages, 1 unprocessed raw entries, last ingest 2026-04-14T15:30:00Z`.

- [ ] **Step 5: Test — vault exists but no log → "no ingest yet" message**

```bash
TESTHOME=$(mktemp -d)
mkdir -p "$TESTHOME/.ultrabrain"/{raw,wiki}
HOME="$TESTHOME" skills/ultrabrain/references/hooks/session-start.sh | python3 -c "import json, sys; d=json.load(sys.stdin); print(d['hookSpecificOutput']['additionalContext'])"
rm -rf "$TESTHOME"
```

Expected output contains: `0 wiki pages, 0 unprocessed raw entries, no ingest yet.`

- [ ] **Step 6: Commit**

```bash
git add skills/ultrabrain/references/hooks/session-start.sh
git commit -m "feat(ultrabrain): add SessionStart hook with vault status injection"
```

---

## Task 6: Write and test `references/hooks/pre-compact.sh`

Second hook. Fires before context compaction to remind the user to capture important content before detail is lost. Static message — no vault stats. Silent when vault is absent.

**Files:**
- Create: `skills/ultrabrain/references/hooks/pre-compact.sh`
- Temporary: `/tmp/ultrabrain-hook-test-*/` (test fixtures — deleted after verification)

- [ ] **Step 1: Write the script**

Full content (copy exactly):

```bash
#!/usr/bin/env bash
# Claude Code PreCompact hook for ultrabrain
#
# Fires before Claude Code compacts the context window. Injects a
# reminder to capture important session content before detail is lost.
# Static message — does not read vault stats. Silent (no output) if
# ~/.ultrabrain/ does not exist, so non-ultrabrain users see nothing.
#
# Installation:
#   1. Copy to ~/.claude/hooks/using-ultrabrain-precompact.sh
#   2. chmod +x ~/.claude/hooks/using-ultrabrain-precompact.sh
#   3. Add PreCompact hook entry to ~/.claude/settings.json (see setup.md)

set +e

VAULT="$HOME/.ultrabrain"

[ -d "$VAULT" ] || exit 0

cat <<'HOOK_JSON'
{
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "additionalContext": "Context compaction is imminent. If this session contains decisions, patterns, or facts worth keeping beyond compaction, say 'capture X' to file them into ~/.ultrabrain/raw/ before detail is lost."
  }
}
HOOK_JSON
```

- [ ] **Step 2: Make executable**

```bash
chmod +x skills/ultrabrain/references/hooks/pre-compact.sh
```

- [ ] **Step 3: Test — vault missing → silent exit 0**

```bash
TESTHOME=$(mktemp -d)
OUT=$(HOME="$TESTHOME" skills/ultrabrain/references/hooks/pre-compact.sh)
EXIT=$?
echo "stdout:[$OUT]"
echo "exit:$EXIT"
rm -rf "$TESTHOME"
```

Expected:
```
stdout:[]
exit:0
```

- [ ] **Step 4: Test — vault exists → valid JSON with correct hookEventName**

```bash
TESTHOME=$(mktemp -d)
mkdir -p "$TESTHOME/.ultrabrain"
HOME="$TESTHOME" skills/ultrabrain/references/hooks/pre-compact.sh | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['hookSpecificOutput']['hookEventName'] == 'PreCompact', 'wrong hookEventName'
assert 'capture' in d['hookSpecificOutput']['additionalContext'], 'missing capture prompt'
print('PreCompact test: PASS')
"
rm -rf "$TESTHOME"
```

Expected: `PreCompact test: PASS`.

- [ ] **Step 5: Commit**

```bash
git add skills/ultrabrain/references/hooks/pre-compact.sh
git commit -m "feat(ultrabrain): add PreCompact hook with capture reminder"
```

---

## Task 7: Write `SKILL.md`

Short dispatcher — ~80 lines. Uses the 60-word description from spec and delegates procedural detail to `references/`.

**Files:**
- Create: `skills/ultrabrain/SKILL.md`

- [ ] **Step 1: Write the file**

Full content (copy exactly):

````markdown
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
````

- [ ] **Step 2: Verify frontmatter parses**

```bash
python3 -c "
import re, sys
content = open('skills/ultrabrain/SKILL.md').read()
m = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
assert m, 'No frontmatter'
fm = m.group(1)
for key in ['name:', 'description:', 'license:', 'metadata:', 'author:', 'version:']:
    assert key in fm, f'Missing {key}'
print('frontmatter OK')
"
```

Expected: `frontmatter OK`.

- [ ] **Step 3: Verify line count is under 100**

```bash
wc -l skills/ultrabrain/SKILL.md
```

Expected: under 100 lines (target ~85).

- [ ] **Step 4: Commit**

```bash
git add skills/ultrabrain/SKILL.md
git commit -m "feat(ultrabrain): add SKILL.md with trigger contract and operations summary"
```

---

## Task 8: Write skill-level `README.md`

User-facing — short, install + triggers + layout + guardrails.

**Files:**
- Create: `skills/ultrabrain/README.md`

- [ ] **Step 1: Write the file**

Full content (copy exactly):

````markdown
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
````

- [ ] **Step 2: Verify**

```bash
wc -l skills/ultrabrain/README.md
grep -c "^## " skills/ultrabrain/README.md
```

Expected: ~52 lines; 6 top-level sections.

- [ ] **Step 3: Commit**

```bash
git add skills/ultrabrain/README.md
git commit -m "docs(ultrabrain): add skill-level README"
```

---

## Task 9: Update `.claude-plugin/marketplace.json`

Add `ultrabrain` entry between `tldr` and `writing-agents-md` (alphabetical placement).

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Read current state**

```bash
cat .claude-plugin/marketplace.json
```

Note the entry for `tldr` (should come just before `writing-agents-md` in the plugins array).

- [ ] **Step 2: Edit — add ultrabrain entry**

Use the Edit tool. `old_string`:

```json
    {
      "name": "tldr",
      "source": "./skills/tldr",
      "description": "Produce a TL;DR digest of any target in roughly two minutes",
      "version": "1.0.0",
      "keywords": ["summary", "tldr", "digest"]
    },
    {
      "name": "writing-agents-md",
```

`new_string`:

```json
    {
      "name": "tldr",
      "source": "./skills/tldr",
      "description": "Produce a TL;DR digest of any target in roughly two minutes",
      "version": "1.0.0",
      "keywords": ["summary", "tldr", "digest"]
    },
    {
      "name": "ultrabrain",
      "source": "./skills/ultrabrain",
      "description": "Personal LLM-maintained wiki at ~/.ultrabrain/ that compounds knowledge across sessions",
      "version": "1.0.0",
      "keywords": ["knowledge-base", "wiki", "second-brain", "karpathy", "pkm"]
    },
    {
      "name": "writing-agents-md",
```

- [ ] **Step 3: Verify JSON validity**

```bash
python3 -c "
import json
data = json.load(open('.claude-plugin/marketplace.json'))
ultra = [p for p in data['plugins'] if p['name'] == 'ultrabrain']
assert len(ultra) == 1, 'ultrabrain missing or duplicated'
u = ultra[0]
assert u['version'] == '1.0.0', 'version mismatch'
assert u['source'] == './skills/ultrabrain', 'source mismatch'
print('marketplace entry OK; total plugins:', len(data['plugins']))
"
```

Expected: `marketplace entry OK; total plugins: 10`.

- [ ] **Step 4: Verify version matches SKILL.md**

```bash
grep 'version:' skills/ultrabrain/SKILL.md | head -1
grep -A1 '"name": "ultrabrain"' .claude-plugin/marketplace.json | grep version
```

Expected: both show `1.0.0` (SKILL.md uses `version: "1.0.0"`, marketplace uses `"version": "1.0.0"`). CLAUDE.md requires these match.

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "chore(marketplace): register ultrabrain v1.0.0"
```

---

## Task 10: Update top-level `README.md`

Add ultrabrain to the skills list (required by CLAUDE.md global constraint).

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read current state**

```bash
grep "^- " README.md
```

Note the line for `tldr` — we insert after it.

- [ ] **Step 2: Edit — add ultrabrain entry**

Use the Edit tool. `old_string`:

```
- **[tldr](skills/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.
```

`new_string`:

```
- **[tldr](skills/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.
- **[ultrabrain](skills/ultrabrain/)** - Drive a personal LLM-maintained wiki at `~/.ultrabrain/` that compounds knowledge across sessions — based on Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern.
```

- [ ] **Step 3: Verify**

```bash
grep -c "ultrabrain" README.md
```

Expected: `2` (one in the list bullet, one in the link `[ultrabrain](skills/ultrabrain/)`).

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: list ultrabrain in repo README"
```

---

## Task 11: Final end-to-end verification

Make sure nothing was missed and every repo-level constraint is satisfied.

**Files:** none modified; verification only.

- [ ] **Step 1: Confirm skill directory has SKILL.md AND README.md** (CLAUDE.md rule)

```bash
ls skills/ultrabrain/SKILL.md skills/ultrabrain/README.md
```

Expected: both listed, no errors.

- [ ] **Step 2: Confirm no `_`-prefixed subdirectories** (CLAUDE.md rule)

```bash
find skills/ultrabrain -type d -name '_*'
```

Expected: empty output.

- [ ] **Step 3: Confirm SKILL.md frontmatter has all required fields**

```bash
python3 -c "
import re
c = open('skills/ultrabrain/SKILL.md').read()
fm = re.match(r'---\n(.*?)\n---', c, re.DOTALL).group(1)
for k in ['license:', 'author:', 'version:']:
    assert k in fm, f'SKILL.md frontmatter missing {k}'
print('SKILL.md frontmatter ok')
"
```

Expected: `SKILL.md frontmatter ok`.

- [ ] **Step 4: Confirm SKILL.md version matches marketplace.json version**

```bash
python3 -c "
import re, json
sv = re.search(r'version: \"([^\"]+)\"', open('skills/ultrabrain/SKILL.md').read()).group(1)
mv = [p for p in json.load(open('.claude-plugin/marketplace.json'))['plugins'] if p['name']=='ultrabrain'][0]['version']
assert sv == mv, f'version mismatch: SKILL.md={sv}, marketplace={mv}'
print(f'versions match: {sv}')
"
```

Expected: `versions match: 1.0.0`.

- [ ] **Step 5: Confirm both hook scripts are executable**

```bash
test -x skills/ultrabrain/references/hooks/session-start.sh && echo "session-start: executable" || echo "session-start: NOT executable"
test -x skills/ultrabrain/references/hooks/pre-compact.sh && echo "pre-compact: executable" || echo "pre-compact: NOT executable"
```

Expected: both `executable`.

- [ ] **Step 6: Re-run hook tests one last time** (in case permissions got changed by earlier edits)

```bash
TESTHOME=$(mktemp -d)

# SessionStart — missing vault
OUT=$(HOME="$TESTHOME" skills/ultrabrain/references/hooks/session-start.sh)
[ -z "$OUT" ] && echo "session-start missing-vault: PASS" || echo "session-start missing-vault: FAIL"

# PreCompact — missing vault
OUT=$(HOME="$TESTHOME" skills/ultrabrain/references/hooks/pre-compact.sh)
[ -z "$OUT" ] && echo "pre-compact missing-vault: PASS" || echo "pre-compact missing-vault: FAIL"

# SessionStart — populated vault
mkdir -p "$TESTHOME/.ultrabrain"/{raw,wiki}
echo test > "$TESTHOME/.ultrabrain/wiki/p1.md"
printf "2026-04-14T15:30:00Z INGEST raw/.processed/foo.md\n" > "$TESTHOME/.ultrabrain/log.md"
HOME="$TESTHOME" skills/ultrabrain/references/hooks/session-start.sh | python3 -m json.tool >/dev/null 2>&1 && echo "session-start populated: PASS" || echo "session-start populated: FAIL"

# PreCompact — populated vault
HOME="$TESTHOME" skills/ultrabrain/references/hooks/pre-compact.sh | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['hookSpecificOutput']['hookEventName'] == 'PreCompact'
" && echo "pre-compact populated: PASS" || echo "pre-compact populated: FAIL"

rm -rf "$TESTHOME"
```

Expected: all four lines end in `PASS`.

- [ ] **Step 7: Check git log for the feature commits**

```bash
git log --oneline | head -15
```

Expected: ~10 ultrabrain-related commits (Tasks 1–10 each committed).

- [ ] **Step 8: Confirm no stray files**

```bash
git status
```

Expected: clean working tree (or only the plan/spec files if they're still untracked).

---

## Post-Implementation

Do **not** push or open a PR in this plan. The user will decide when to:
- Squash-merge or keep the per-task commits
- Open a PR
- Install the skill and smoke-test it in a real session

Ready hand-off: after Task 11 passes, tell the user `skills/ultrabrain/` v1.0.0 is ready on the branch and ask whether to push / open PR / install.
