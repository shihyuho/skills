# UltraBrain Templates And Conventions

Use this file when you need exact naming rules, frontmatter, or source-note formats.

## Card filenames

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

## Card frontmatter

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

## Map filenames

Store maps in `docs/ultrabrain/maps/`.

Good examples:

- `docs/ultrabrain/maps/home.md`
- `docs/ultrabrain/maps/workflow-moc.md`
- `docs/ultrabrain/maps/by-source-moc.md`

Map filename rules:

- use lowercase `kebab-case`
- suffix all navigation maps other than `home.md` with `-moc`
- reserve `home.md` for the main entry page
- name maps by function or domain, not by temporary project context

## Source note filenames

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
- avoid treating source notes as background storage or archive bins

## Source note structure

Use this source-note structure:

```md
# <source-title>

## Metadata
- Type: conversation | directory-scan | article | book | meeting
- Date: YYYY-MM-DD
- Origin: <URL / path / conversation topic / directory>
- Status: ephemeral | available | archived

## Produced Cards
- [[card-one]]
- [[card-two]]

## Provenance Notes
- <any specific detail needed to re-locate or verify this source>
- <do not repeat the card content here>
```

Fill only the provenance fields. Do not summarize the source's content, do not extract "key points", and do not explain why it matters.
