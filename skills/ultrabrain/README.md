# UltraBrain

Build a second brain your AI can actually navigate.

`ultrabrain` helps turn a pile of notes into a living knowledge system built from linked notes, MOCs, source notes, and reusable knowledge cards.

## Why Use This Skill

Your notes probably already contain useful ideas. The hard part is not writing them down. The hard part is finding the right note later, keeping structure stable as the vault grows, and letting AI help without turning everything into a messy folder dump.

UltraBrain gives your AI a cleaner way to work with knowledge:

- recall the right maps before planning
- capture reusable ideas as stable notes
- keep navigation in MOCs instead of stuffing structure into note metadata
- preserve provenance when a source still matters later
- groom maps over time without constantly rewriting your cards

## What AI Can Do With It

### Recall before acting

When you ask AI to plan, write, or research, UltraBrain can start from your knowledge maps instead of a blind repo-wide search.

### Capture without chaos

When a useful idea appears, UltraBrain helps decide whether it should become a new note, update an existing one, or stay out of the system.

### Keep maps and notes separate

Your knowledge cards stay focused on ideas. Your MOCs stay focused on navigation. That separation makes the system easier to grow without constant cleanup.

### Preserve where ideas came from

When provenance matters, UltraBrain uses lightweight source notes so you can keep context without turning the whole vault into an archive.

## Typical Use Cases

### 1. Build a cleaner Obsidian knowledge base

You have dozens or hundreds of Markdown notes, but no reliable way to organize them. UltraBrain helps shape them into maps, notes, and sources that AI can work with more deliberately.

### 2. Recall the right context before planning work

Before starting a project, you want AI to load the most relevant knowledge maps and a small set of high-value notes instead of rediscovering everything from scratch.

### 3. Capture lessons without bloating metadata

You learned something reusable, but you do not want every note to carry fragile relationship fields. UltraBrain keeps canonical knowledge in notes and navigation in maps.

### 4. Clean up a messy PKM structure over time

Your note system evolved organically and now feels inconsistent. UltraBrain helps reorganize the navigation layer without rewriting every note whenever the structure changes.

## How It Works

UltraBrain uses a simple default layout:

```text
docs/ultrabrain/
  maps/
  notes/
  sources/
```

- `maps/` holds your MOCs and entry pages
- `notes/` holds canonical knowledge cards
- `sources/` holds lightweight provenance notes

The default philosophy is simple: notes store knowledge, maps store navigation, and source notes store context.

## How To Start

1. Install the skill.

```bash
npx skills add shihyuho/skills --skill=ultrabrain
```

2. Optionally install the reminder block with `ultrabrain-init` so your agent gets nudged to use the skill in PKM or second-brain workflows.

3. Start with prompts like:

```text
Use ultrabrain to reorganize my Obsidian vault into maps, notes, and source notes.
Recall the most relevant ultrabrain maps before planning this refactor.
Capture the reusable insight from this debugging session into my ultrabrain notes.
```

## Guardrails

- It is not a general task manager or project planner.
- It is not for one-off factual Q&A with no knowledge-base goal.
- It does not treat MOCs as category buckets or replace notes with folder structure.
- It keeps human-readable structure in files, so your vault stays inspectable.

## License

MIT
