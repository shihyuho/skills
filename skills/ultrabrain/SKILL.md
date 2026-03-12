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

- `maps/` stores MOCs, review lenses, and troubleshooting lenses
- `notes/` stores the canonical knowledge cards
- `sources/` stores minimal provenance notes (not archives)

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

### Self-consistency standard

Every card must meet these minimum standards:

- **Standalone comprehensible**: A reader can understand the card's core idea without reading the source. The card's main claim or insight should be complete within the card itself.
- **Self-contained premise**: Key definitions, context, and judgment criteria belong in the card, not in external context. If removing the source makes the card's primary point unclear, the card is not yet written.
- **No slogan-only content**: A card can be short, but not thin. "Short is OK, thin is not." A card that is only a conclusion without supporting reasoning, evidence, or context is too thin to be useful.

If a card's main comprehensibility depends on its source, the card has a writing problem, not a sourcing problem.

When a card is too thin, rewrite the card first. Do not propose a source note as the first fix for missing context.

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

Lens maps are different from domain MOCs. They are review tools, not primary recall entry points.

#### Review lenses

Use `by-source-moc` and `by-confidence-moc` for provenance review or uncertainty review, not as everyday navigation:

- `by-source-moc`: groups cards by `personal`, `inherited`, or `source-derived` origin. Useful when you need to audit where knowledge came from or verify provenance.
- `by-confidence-moc`: groups cards into human-readable confidence zones such as high-confidence vs tentative. Useful when assessing reliability or deciding how much to trust a constraint.

Do not treat review lenses as primary recall paths like `home`, domain MOCs, or `lessons-moc`.

#### Troubleshooting lenses

Create problem-oriented or troubleshooting-oriented lenses when a specific failure pattern or problem area recurs. These lenses are entry points for systematic diagnosis, not general navigation.

Examples of troubleshooting lens topics:

- `timeout-retry-idempotency-moc`: patterns for handling transient failures, retry logic, and idempotent operations
- `network-path-moc`: network connectivity, DNS, routing, firewall, and transport-layer issues
- `state-invalidation-moc`: cache invalidation, stale state, consistency models, and state recovery
- `workspace-locality-moc`: local vs remote state, workspace-specific configuration, environment isolation
- `compatibility-support-matrix-moc`: version compatibility, feature flags, support matrices, and migration paths

Create a troubleshooting lens when:

- a specific problem area has multiple related cards
- the problem is recurrent and worth systematic documentation
- readers would benefit from a checklist or pattern catalog rather than scattered notes

### Map filenames

Store maps in `docs/ultrabrain/maps/`.

Good examples:

- `docs/ultrabrain/maps/home.md`
- `docs/ultrabrain/maps/workflow-moc.md`
- `docs/ultrabrain/maps/by-source-moc.md`

Map filename rules:

- use lowercase `kebab-case`
- suffix all navigation maps (including domain MOCs, review lenses, and troubleshooting lenses) with `-moc`
- reserve `home.md` for the main entry page
- name maps by function or domain, not by temporary project context

## Recall Workflow

Use this workflow order:

```text
1. Seed map recall
2. Rough plan or problem framing
3. Gap-driven map recall loop
4. Planning convergence
5. High-value recall
6. Task execution
7. Capture
8. MOC grooming (manual trigger)
```

Use this mental model:

```text
seed recall
  ->
rough plan or brainstorming
  ->
[new critical gap, risk, or decision?]
  | yes
  v
gap-driven map recall
(budgeted, map-first)
  ->
update rough plan
  ->
[more critical gaps?] --yes--> repeat
  |
  no
  v
planning convergence
  ->
high-value recall
  ->
task execution
```

Recall should start before planning, but it does not need to be complete before planning. Use a small initial recall to orient the work, then pull in more knowledge only when planning exposes a real gap.

### 1. Seed map recall

Run before detailed planning:

1. Read `home`.
2. Identify the most relevant domain MOC or problem-oriented lens.
3. Read that map.
4. Load only the most relevant cards.

Seed recall is for orientation, not completeness. Its job is to give the plan an initial direction, not to find every relevant card before planning starts.

**Skip review lenses for normal recall.** Only consult `by-source-moc` or `by-confidence-moc` when:

- doing provenance review (checking where knowledge originated)
- doing uncertainty review (assessing reliability or confidence)

**Use troubleshooting lenses as entry points.** If a problem-oriented lens exists for the issue at hand (e.g., `timeout-retry-idempotency-moc`), use it as the troubleshooting entry instead of generic search.

Seed recall should give planning context, not full-vault search results.

When a relevant domain MOC or troubleshooting lens exists, prefer that map-first path over falling back to repo-wide search, unrelated skills, or general documentation. The point of map recall is to start from the navigation maps, not from whatever other files happen to mention similar topics.

### 2. Rough plan or problem framing

Use the initial recall to frame the problem:

- what the task appears to be about
- which domain or problem area is most likely central
- which risks, unknowns, or decision points still need clarification

At this stage, the plan is provisional. Its purpose is to expose recall gaps, not to freeze the final approach.

### 3. Gap-driven map recall loop

During planning or brainstorming, run another round of map-first recall only when a real gap appears.

Valid triggers include:

- a newly discovered domain or problem area
- a high-risk assumption that needs support or contradiction
- a decision fork where different prior lessons may matter
- a missing prerequisite or dependency that changes the plan

For each recall loop:

1. State the gap you are trying to answer.
2. Read at most 1-2 maps or lenses that directly address that gap.
3. Load only a small number of cards.
4. Update the rough plan with what changed.

Keep each loop budgeted and specific. Do not let gap-driven recall turn into broad vault exploration.

If file-based planning artifacts exist, record newly discovered gaps, risks, and decisions there while the plan evolves.

If a map-first path does not help within the current loop, treat that as a coverage gap or open assumption and continue planning. Do not silently fall back to full-text exploration as the default recall mode.

### 4. Planning convergence

Move on when the work is execution-ready:

- the main approach is clear
- the major risks or unknowns are named
- the next concrete steps are understandable

Planning convergence is not irreversible. Reopen the planning loop if later recall or execution reveals a material contradiction.

### 5. High-value recall

Run after planning convergence and before task execution, not before every planning step.

Use `lessons-moc` and strongly related cards as the default source of
high-value constraints. Load only a small number of cards that can constrain
the upcoming task and help avoid repeated mistakes.

Recommended high-value recall flow:

1. Check whether `docs/ultrabrain/maps/lessons-moc.md` exists.
2. If it exists, load only the most relevant lesson-oriented cards from that map.
3. If it does not exist, continue without lesson-specific recall.

High-value recall is a narrow pre-execution constraint pass. It is not a second broad brainstorming phase.

## Capture Workflow

Run capture after the task, not during every intermediate thought.

Use note-first capture:

1. Decide whether the new material is worth becoming a card.
2. Check whether the card is self-contained enough to stand on its own.
3. If it is too thin, rewrite the card before making any source-note decision.
4. Check whether a semantically similar card already exists.
5. Make the decision explicit as `decision=create` or `decision=update` before presenting the card result.
6. Update the card's `type`, `confidence`, `brief`, `related`, `updated`, and tags as needed.
7. Update the relevant MOC separately if the card should now appear in a map.
8. Create or update a source note only if later provenance is likely to matter after the card itself is already understandable.

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

Treat source notes as provenance notes, not archives. Their only job is to track where knowledge came from.

### Source note purpose

A source note records provenance, not context. If a card's main idea requires the source to make sense, the card is not yet self-contained. Source notes do not fill gaps in card comprehensibility.

Create a source note when:

- one source produced multiple cards
- the source may disappear later
- provenance is likely to matter for future verification
- the source would otherwise require duplicated provenance across cards

Skip source notes when the card is self-contained and the source has no future tracing value.

If a card is not yet self-contained, improve the card first. Do not create a source note as a substitute for missing rule, trigger, reasoning, definitions, or other core context.

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
- avoid treating source notes as background storage or archive bins

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

**Fill only the provenance fields.** Do not summarize the source's content, do not extract "key points", and do not explain why it matters. The card already contains the idea. The source note only records where the idea came from.

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
- heuristics that constrain future decisions

For decision rules and heuristics, include in the card:

- **Rule**: What to do or not do
- **Trigger**: When this rule applies (specific situation or condition)
- **Why**: The reasoning behind the rule, not just the rule itself

Do not reduce a decision rule to a template slogan. The card should explain the situation, the principle, and the reasoning. A card that says "always use X" without explaining when "always" applies is too thin to live in lessons-moc.

## Output Expectations

When asked to organize a knowledge base, produce concise outputs that make the next step obvious. Typical outputs include:

- which cards should be created or updated
- which source notes should be created or skipped
- which MOC should be updated, created, or split
- what the current recall constraints are

If the user asks you to edit files directly, make the note or MOC changes. If they ask for planning only, return the recommended changes without pretending the files already exist.
