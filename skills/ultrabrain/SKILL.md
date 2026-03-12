---
name: ultrabrain
description: Use when working with a second-brain or PKM system built from linked notes, MOCs, knowledge cards, and source notes. Use when the user mentions Obsidian, LYT, MOCs, note recall, note capture, knowledge-base restructuring, map cleanup, source-note design, or wants AI to organize, retrieve, and evolve a personal knowledge system over time, even if they do not explicitly ask for "PKM" or "second brain."
license: MIT
metadata:
  author: shihyuho
  version: "0.1.0"
---

# UltraBrain

## Overview

Use this skill to maintain a linked-note knowledge system where notes are the
canonical units, MOCs are navigation maps, source notes preserve minimal
provenance, and recall, capture, and MOC grooming happen at different times.

## When to Use

Use this skill when the user wants to:

- design or maintain a LYT-style or MOC-driven note system
- organize knowledge in Obsidian, Markdown vaults, or a second-brain workflow
- recall relevant knowledge before planning work
- capture reusable knowledge after work
- create or update MOCs, source notes, or atomic knowledge cards
- keep AI-curated maps stable while cards continue to evolve

Do not use this skill for:

- one-off factual Q&A with no note-taking or knowledge-organization goal
- task management or execution planning systems unrelated to knowledge organization
- raw full-text archiving where the user wants a document repository instead of a linked-note system

## Core Model

Use this structure as the default model:

```text
docs/ultrabrain/
  maps/
  notes/
  sources/
```

- `maps/` stores MOCs and entry pages
- `notes/` stores the canonical knowledge cards
- `sources/` stores minimal provenance or evidence notes when source context matters later

Use lowercase `kebab-case` for directories and filenames. Do not use spaces.

Examples:

- `docs/ultrabrain/maps/home.md`
- `docs/ultrabrain/notes/avoid-storing-volatile-relationships-in-card-metadata.md`
- `docs/ultrabrain/sources/2026-03-12-ai-conversation-moc-churn.md`

This system uses maps as its navigation layer. Do not force abstract system words into card titles or MOC names. Prefer concrete lowercase names like `workflow-moc` or `debugging-moc`.

## MOC Rules

- Treat a MOC as a map, not a category bucket.
- Let one note appear in multiple MOCs when that improves navigation.
- Keep card content stable and let maps evolve around it.
- Do not store frequently changing MOC relationships as canonical card metadata.
- Prefer updating maps over rewriting cards when only the navigation structure changes.

## Card Rules

Use cards as the canonical knowledge unit.

### Card filenames

Store cards in `docs/ultrabrain/notes/` using semantic lowercase `kebab-case` slugs.

Good examples:

- `docs/ultrabrain/notes/avoid-storing-volatile-relationships-in-card-metadata.md`
- `docs/ultrabrain/notes/source-notes-are-provenance-not-archives.md`

Filename rules:

- use lowercase only
- use `-` instead of spaces
- make the filename describe the knowledge itself, not the tool session that created it
- keep one atomic idea per file
- prefer stable semantic names over timestamps for cards

### Card frontmatter

Use this default frontmatter:

```yaml
---
title: <note title>
type: statement
confidence: 0.7
brief: "<one-sentence summary of the card's core idea>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - tag1
  - tag2
---
```

### Field meanings

- `type`: the card role; use `statement | thing | question | quote | person`
- `confidence`: numeric confidence in the `0.0-0.9` range
- `brief`: one-sentence summary for preview and recall
- `related`: optional high-value horizontal links to other cards only
- `created` and `updated`: temporal tracking for evolution
- `tags`: lightweight search aids

Do not use card frontmatter for volatile relationships such as current MOC membership or current source grouping. Those belong in maps and source notes.

Do not put MOCs, source notes, folders, or other navigation pages in `related`. `related` is only for card-to-card links.

Default to omitting `related`.

Add `related` only when the target is a real existing card, the link adds real
retrieval value, and the target is not a MOC, source note, folder, or
placeholder concept.

If you do not know any clearly related cards, omit `related` rather than inventing placeholders, synthetic card names, or links to maps.

## Map Structure

Use these maps as the default navigation layer:

- `home`
- `code-style-moc`
- `testing-moc`
- `git-moc`
- `debugging-moc`
- `workflow-moc`
- `general-moc`
- `lessons-moc`
- `by-source-moc`
- `by-confidence-moc`

Use domain maps as follows:

- `code-style-moc`: naming, structure, readability, abstraction choices
- `testing-moc`: testing methods, validation patterns, regression strategy
- `git-moc`: commit practices, branching, review patterns, version-control principles
- `debugging-moc`: diagnosis paths, failure patterns, verification tactics
- `workflow-moc`: research flow, AI collaboration flow, execution order, process heuristics
- `general-moc`: cross-domain or meta-level ideas that do not fit one domain cleanly
- `lessons-moc`: high-value lessons, decision rules, and reusable hard-won insights

### Lens maps

- `by-source-moc`: groups cards by `personal`, `inherited`, or `source-derived` origin
- `by-confidence-moc`: groups cards into human-readable confidence zones such as high-confidence vs tentative

### Map filenames

Store maps in `docs/ultrabrain/maps/`.

Good examples:

- `docs/ultrabrain/maps/home.md`
- `docs/ultrabrain/maps/workflow-moc.md`
- `docs/ultrabrain/maps/by-source-moc.md`

Map filename rules:

- use lowercase `kebab-case`
- suffix map files with `-moc` when they are actual MOCs
- reserve `home.md` for the main entry page
- name maps by function or domain, not by temporary project context

## Recall Workflow

Use this workflow order:

```text
1. Map recall
2. Plan
3. High-value recall
4. Task execution
5. Capture
6. MOC grooming (manual trigger)
```

### 1. Map recall

Run before planning:

1. Read `home`.
2. Identify the most relevant domain MOC.
3. Read that MOC.
4. If useful, read `by-source-moc` or `by-confidence-moc`.
5. Load only the most relevant cards.

Map recall should give planning context, not full-vault search results.

When a relevant domain MOC exists, prefer that map-first path over falling back to repo-wide search, unrelated skills, or general documentation. The point of map recall is to start from the navigation maps, not from whatever other files happen to mention similar topics.

### 2. High-value recall

Run before task execution, not before every planning step.

Use `lessons-moc` and strongly related cards as the default source of
high-value constraints. Load only a small number of cards that can constrain
the upcoming task and help avoid repeated mistakes.

Recommended high-value recall flow:

1. Check whether `docs/ultrabrain/maps/lessons-moc.md` exists.
2. If it exists, load only the most relevant lesson-oriented cards from that map.
3. If it does not exist, continue without lesson-specific recall.

## Capture Workflow

Run capture after the task, not during every intermediate thought.

Use note-first capture:

1. Decide whether the new material is worth becoming a card.
2. Check whether a semantically similar card already exists.
3. Make the decision explicit as `decision=create` or `decision=update` before presenting the card result.
4. Update the card's `type`, `confidence`, `brief`, `related`, `updated`, and tags as needed.
5. Update the relevant MOC separately if the card should now appear in a map.
6. Create or update a source note only if later provenance is likely to matter.

Capture only when the knowledge is reusable, non-obvious, or likely to matter again.

Keep the layers separate during capture:

- card content belongs in the card
- navigation belongs in MOCs
- provenance belongs in source notes

Do not solve a card update by stuffing map membership or source grouping back into the card metadata.

When reporting capture results, do not jump straight to a heading like
`Card Created`. First state `decision=create` or `decision=update` and why,
then present the card change itself.

If you recommend updating a MOC after capture, present that as a separate follow-up action. Do not mix MOC placement into the card's canonical fields.

During capture, do not phrase navigation updates as if they are part of the card itself. Avoid lines like `add to lessons-moc` inside the card result. If map maintenance matters, say it separately as a later grooming or follow-up action.

## Source Notes

Treat source notes as provenance notes, not archives.

### Source note filenames

Store source notes in `docs/ultrabrain/sources/` using a date prefix plus a short topic slug.

Good examples:

- `docs/ultrabrain/sources/2026-03-12-ai-conversation-moc-churn.md`
- `docs/ultrabrain/sources/2026-03-12-directory-scan-linked-notes.md`
- `docs/ultrabrain/sources/2026-03-12-lyt-framework-guide.md`

Source filename rules:

- use lowercase `kebab-case`
- prefix with `YYYY-MM-DD-`
- describe the source context, not the conclusion card
- keep source filenames distinct from note card filenames

Create a source note when one source produced multiple cards, may disappear
later, is likely to matter for future verification, or would otherwise require
duplicated provenance across cards.

Skip source notes when the card is already self-contained and the source has no future tracing value.

Use this source-note structure:

```md
# <source-title>

## Metadata
- Type: conversation | directory-scan | article | book | meeting
- Date: YYYY-MM-DD
- Origin: <URL / path / conversation topic / directory>
- Status: ephemeral | available | archived

## Summary
- What this source covered
- Why it is worth keeping

## Key Extracts
- Key point 1
- Key point 2
- Key point 3

## Derived Notes
- [[card-one]]
- [[card-two]]

## Why It Matters
- Why this provenance is worth retaining
```

## MOC Grooming

Do not automatically reorganize MOCs after every capture. Groom them only when manually triggered or when the user explicitly asks.

### Create a new MOC when

- a stable cluster of notes exists but has no good entry point
- the cluster is large enough to need navigation
- a reader would understand the area better from a map than from flat links

### Update an existing MOC when

- a new card clearly belongs to an existing section
- the structure is still good and only needs small changes
- section order or summaries need minor refinement

### Split a MOC when

- it reads like a list instead of a map
- multiple clear sub-clusters have formed
- readers or AI have to search repeatedly inside one oversized page

When splitting, keep the old MOC as an upper-level map of maps instead of deleting it.

## Boundary Rules

### general-moc

Use `general-moc` for:

- cross-domain principles
- meta knowledge about the system itself
- cards that are clearly valuable but not yet stable in one domain

Do not use `general-moc` as a dump for unprocessed material.

### lessons-moc

Use `lessons-moc` for:

- reusable lessons
- high-value decision rules
- hard-won constraints or prerequisites worth remembering

Do not put generic definitions, weak observations, or raw source summaries in `lessons-moc`.

## Output Expectations

When asked to organize a knowledge base, produce concise outputs that make the next step obvious. Typical outputs include:

- which cards should be created or updated
- which source notes should be created or skipped
- which MOC should be updated, created, or split
- what the current recall constraints are

If the user asks you to edit files directly, make the note or MOC changes. If they ask for planning only, return the recommended changes without pretending the files already exist.
