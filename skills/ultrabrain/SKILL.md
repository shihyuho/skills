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
canonical units, maps are the navigation layer, source notes preserve minimal
provenance, and recall, capture, and MOC grooming happen at different times.

`SKILL.md` defines the primary rules. Use `references/` for exact formats,
templates, and grooming procedures when those details are needed.

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

- `maps/` stores entry pages, MOCs, and review lenses
- `notes/` stores the canonical knowledge cards
- `sources/` stores minimal provenance notes, not archives

Use lowercase `kebab-case` for directories and filenames. Do not use spaces.

Examples:

- `docs/ultrabrain/maps/home.md`
- `docs/ultrabrain/notes/avoid-storing-volatile-relationships-in-card-metadata.md`
- `docs/ultrabrain/sources/2026-03-12-ai-conversation-moc-churn.md`

This system uses maps as its navigation layer. Do not force abstract system words into card titles or MOC names. Prefer concrete lowercase names like `workflow-moc` or `debugging-moc`.

### Map Classes

Use these map classes in the navigation layer:

- `home`: the entry page and top-level orientation map
- `domain maps`: the default recall maps for concrete areas such as code style, testing, git, debugging, or workflow
- `lessons-moc`: the default recall map for high-value lessons, decision rules, and reusable hard-won constraints
- `general-moc`: the default recall map for cross-domain or meta-level ideas that do not fit one domain cleanly
- `review lenses`: conditional review views such as `by-source-moc` and `by-confidence-moc`

`home` is the entry page, not the parent class of every other map.

`domain maps`, `lessons-moc`, and `general-moc` form the default recall maps. `review lenses` are views over existing knowledge, not canonical homes for it.

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

- **Standalone comprehensible**: A reader can understand the card's core idea without reading the source.
- **Self-contained premise**: Key definitions, context, and judgment criteria belong in the card, not in external context.
- **No slogan-only content**: A card can be short, but not thin. "Short is OK, thin is not."

A card that is only a conclusion without reasoning, context, or trigger conditions is too thin.

For rule-like, lesson-like, or heuristic cards, self-contained means the card can state:

- **Rule**: what to do or not do
- **Trigger**: when it applies
- **Why**: the reasoning behind it

If a card's main comprehensibility depends on its source, the card has a writing problem, not a sourcing problem.

When a card is too thin, rewrite the card first. Do not propose a source note as the first fix for missing context.

### Card metadata rules

- Use `type: statement | thing | question | quote | person`
- Keep `confidence` in the `0.0-0.9` range
- Use `brief` as the one-sentence preview for recall
- Use `related` only for high-value card-to-card links
- Do not put MOCs, source notes, folders, or placeholder concepts in `related`
- Omit `related` when there is no clearly useful target

Do not use card frontmatter for volatile relationships such as current MOC membership or current source grouping. Those belong in maps and source notes.

For exact filename rules, frontmatter, map naming, and source-note templates, read `references/templates-and-conventions.md`.

## Map Structure

Use this navigation model by default:

- start at `home`
- move to the most relevant default recall map
- load only the cards needed for the current task

Default recall maps include:

- domain maps such as `code-style-moc`, `testing-moc`, `git-moc`, `debugging-moc`, and `workflow-moc`
- `lessons-moc`
- `general-moc`

Review lenses are different from default recall maps. They are review tools, not everyday navigation entry points.

Use `by-source-moc` and `by-confidence-moc` for provenance review or uncertainty review, not as everyday navigation.

Do not treat review lenses as default recall maps like `domain maps`, `lessons-moc`, or `general-moc`.

### Boundary Rules

Use `general-moc` for:

- cross-domain principles
- meta knowledge about the system itself
- cards that are clearly valuable but not yet stable in one domain

Do not use `general-moc` as a dump for unprocessed material.

Use `lessons-moc` for:

- reusable lessons
- high-value decision rules
- hard-won constraints or prerequisites worth remembering
- heuristics that constrain future decisions

For decision rules and heuristics, include in the card:

- **Rule**: what to do or not do
- **Trigger**: when this rule applies
- **Why**: the reasoning behind the rule

Do not reduce a decision rule to a slogan. If a card says "always use X" without explaining when it applies, it is too thin for `lessons-moc`.

## Recall Workflow

Use this workflow order:

```text
1. Map recall
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
map recall
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

### 1. Map recall

Run before detailed planning:

1. Read `home`.
2. Identify the most relevant default recall map. In most cases, this should be a domain MOC.
3. Read that map.
4. Load only the most relevant cards.

Map recall is for orientation, not completeness.

Skip review lenses for normal recall. Only consult `by-source-moc` or `by-confidence-moc` when:

- doing provenance review
- doing uncertainty review

When a relevant domain MOC, `lessons-moc`, or `general-moc` exists, prefer that map-first path over falling back to repo-wide search, unrelated skills, or general documentation.

### 2. Rough plan or problem framing

Use the initial recall to frame the problem:

- what the task appears to be about
- which domain or knowledge area is most likely central
- which risks, unknowns, or decision points still need clarification

At this stage, the plan is provisional. Its purpose is to expose recall gaps, not to freeze the final approach.

### 3. Gap-driven map recall loop

During planning or brainstorming, run another round of map-first recall only when a real gap appears.

Valid triggers include:

- a newly discovered domain or knowledge area
- a high-risk assumption that needs support or contradiction
- a decision fork where different prior lessons may matter
- a missing prerequisite or dependency that changes the plan

For each recall loop:

1. State the gap you are trying to answer.
2. Read at most 1-2 default recall maps or review lenses that directly address that gap.
3. Load only a small number of cards.
4. Update the rough plan with what changed.

Keep each loop budgeted and specific. Do not let gap-driven recall turn into broad vault exploration.

If file-based planning artifacts exist, record newly discovered gaps, risks, and decisions there while the plan evolves.

If a map-first path does not help within the current loop, treat that as a coverage gap or open assumption and continue planning.

### 4. Planning convergence

Move on when the work is execution-ready:

- the main approach is clear
- the major risks or unknowns are named
- the next concrete steps are understandable

Planning convergence is not irreversible. Reopen the planning loop if later recall or execution reveals a material contradiction.

### 5. High-value recall

Run after planning convergence and before task execution, not before every planning step.

Use `lessons-moc` and strongly related cards as the default source of high-value constraints. Load only a small number of cards that can constrain the upcoming task and help avoid repeated mistakes.

Recommended high-value recall flow:

1. Check whether `docs/ultrabrain/maps/lessons-moc.md` exists.
2. If it exists, load only the most relevant lesson-oriented cards from that map.
3. If it does not exist, continue without lesson-specific recall.

High-value recall is a narrow pre-execution constraint pass. It is not a second broad brainstorming phase.

## Capture Workflow

Run capture after the task, not during every intermediate thought.

Use note-first capture:

1. Decide whether the new material is worth becoming a card at all.
2. If it is too generic, redundant, or not worth preserving as reusable knowledge, return `decision=skip` and explain why.
3. Check whether the card is self-contained enough to stand on its own.
4. If it is too thin, stop there and return `decision=rewrite-first`.
5. Only after the card is self-contained, check whether a semantically similar card already exists.
6. Make the decision explicit as `decision=create` or `decision=update` before presenting the card result.
7. Update the card's key fields as needed.
8. Update the relevant MOC separately if the card should now appear in a map.
9. Create or update a source note only if later provenance is likely to matter after the card itself is already understandable.

Capture only when the knowledge is reusable, non-obvious, or likely to matter again.

If the proposed lesson is too generic, already covered, or not worth preserving as a reusable card, return `decision=skip` instead of forcing a create or update.

`decision=skip` and `decision=rewrite-first` are different outcomes:

- `decision=skip`: do not capture this item as a card
- `decision=rewrite-first`: the idea may be worth capturing, but the card is still too thin

When a proposed card is too thin, the correct immediate outcome is to rewrite the card, not to jump straight to `decision=create`, `decision=update`, or source-note handling.

If a proposed card is only a conclusion without reasoning, context, or trigger conditions, do not output `decision=create` or `decision=update` yet; return `decision=rewrite-first` until the card is self-contained.

If the card is a lesson, rule, or heuristic and cannot yet state `Rule`, `Trigger`, and `Why`, it is still too thin.

For a thin-card result, do not draft frontmatter, do not pick a filename, do not assign a MOC, and do not decide whether to create a source note yet.

For thin-card cases, use this output shape:

```text
decision=rewrite-first

Why the card is too thin:
- <missing reasoning / context / trigger>

Rewrite target:
- Rule: <what to do>
- Trigger: <when it applies>
- Why: <why it matters>

Only after that rewrite should you decide whether the final result is `create` or `update`.
```

For thin-card prompts, any answer that jumps straight to a finished card, filename, frontmatter, MOC placement, or source-note decision is incorrect.

Keep the layers separate during capture:

- card content belongs in the card
- navigation belongs in MOCs
- provenance belongs in source notes

Do not solve a card update by stuffing map membership or source grouping back into the card metadata.

When reporting capture results, do not jump straight to a heading like `Card Created`. First state `decision=create`, `decision=update`, or `decision=skip` and why, then present the card change itself when there is one.

If you recommend updating a MOC after capture, present that as a separate follow-up action. Do not mix MOC placement into the card's canonical fields.

During capture, do not phrase navigation updates as if they are part of the card itself. If map maintenance matters, say it separately as a later grooming or follow-up action.

## Source Notes

Treat source notes as provenance notes, not archives. Their only job is to track where knowledge came from.

A source note records provenance, not context. If a card's main idea requires the source to make sense, the card is not yet self-contained.

Create a source note when:

- one source produced multiple cards
- the source may disappear later
- provenance is likely to matter for future verification
- the source would otherwise require duplicated provenance across cards

Skip source notes when the card is self-contained and the source has no future tracing value.

If a card is not yet self-contained, improve the card first. Do not create a source note as a substitute for missing rule, trigger, reasoning, definitions, or other core context.

For exact source-note filename rules and the source-note template, read `references/templates-and-conventions.md`.

## MOC Grooming

Do not automatically reorganize MOCs after every capture. Groom them only when manually triggered or when the user explicitly asks.

For create, update, split, prune, and class-specific grooming guidance, read `references/map-grooming.md`.

## Output Expectations

When asked to organize a knowledge base, produce concise outputs that make the next step obvious. Typical outputs include:

- which cards should be created or updated
- which source notes should be created or skipped
- which MOC should be updated, created, or split
- what the current recall constraints are

If the user asks you to edit files directly, make the note or MOC changes. If they ask for planning only, return the recommended changes without pretending the files already exist.
