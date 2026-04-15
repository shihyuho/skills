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
