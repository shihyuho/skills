# UltraBrain

Build a second brain your AI can actually navigate.

`ultrabrain` helps turn a pile of notes into a living knowledge system built from linked notes, MOCs, source notes, and reusable knowledge cards.

## Core Principles

### Cards are self-contained

Every knowledge card must be understandable on its own. The card's main idea should be complete within the card itself—not depending on reading the source to understand the point.

- Short is OK. Thin is not.
- Key definitions and context belong in the card.
- If removing the source makes the card unclear, the card needs work—not the source.

### Maps are for navigation, not storage

- Domain MOCs (`code-style-moc`, `testing-moc`, etc.), `lessons-moc`, and `general-moc` form the default recall layer.
- Review lenses (`by-source-moc`, `by-confidence-moc`) are for provenance or confidence review only.

### Source notes track provenance only

A source note records where knowledge came from. It does not fill gaps in card comprehensibility. If a card needs its source to make sense, rewrite the card.

- Fix thin cards first.
- Do not use a source note as the first remedy for missing context.

## Why Use This Skill

Your notes probably already contain useful ideas. The hard part is not writing them down. The hard part is finding the right note later, keeping structure stable as the vault grows, and letting AI help without turning everything into a messy folder dump.

UltraBrain gives your AI a cleaner way to work with knowledge:

- recall the right maps before planning
- capture reusable ideas as stable notes
- keep navigation in MOCs instead of stuffing structure into note metadata
- preserve provenance when a source still matters later
- groom maps over time without constantly rewriting your cards

## Think While Recalling

Most knowledge systems assume you already know the exact domain before you start planning. Real work does not feel like that.

Usually you begin with a vague issue, a half-formed idea, or a broad theme. The useful domains and problem frames only become visible while you are thinking through the task.

UltraBrain is built for that reality.

It starts with a small map recall, just enough to orient the work. Then, as planning or brainstorming exposes a new gap, risk, or decision, it pulls in more of your prior knowledge through maps and cards.

That makes UltraBrain feel less like a static archive and more like a knowledge partner:

- start with one map, not the whole vault
- think in public while the plan is still forming
- use new questions to trigger better recall
- keep old knowledge flowing into the plan without drowning in search results

If you also use file-based planning, the fit is especially strong:

- planning files hold the new discoveries from this session
- UltraBrain supplies the old knowledge that becomes relevant as those discoveries appear

In other words: planning surfaces the gaps, and UltraBrain fills them map-first.

## What AI Can Do With It

### Recall before acting

When you ask AI to plan, write, or research, UltraBrain starts from your knowledge maps. It uses a small map recall first, then follows the planning process as new domains, risks, and decision points become clear.

That means recall is not a one-shot ritual before planning. It is a map-first loop that keeps feeding the plan as the problem gets sharper.

### Review provenance and confidence when needed

AI uses `by-source-moc` and `by-confidence-moc` only for audit work—not for everyday recall. This keeps navigation clean.

### Capture without chaos

When a useful idea appears, UltraBrain helps decide whether it should become a new note, update an existing one, or stay out of the system.

### Keep maps and notes separate

Your knowledge cards stay focused on ideas. Your MOCs stay focused on navigation. That separation makes the system easier to grow without constant cleanup.

### Preserve where ideas came from

Source notes track provenance, not context. The card itself contains the idea; the source note only remembers the origin.

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

- `maps/` holds your entry pages, MOCs, and review lenses
- `notes/` holds canonical knowledge cards
- `sources/` holds lightweight provenance notes

The default philosophy is simple: notes store knowledge, maps store navigation, and source notes store origin—not context.

In that navigation layer, `home` is the entry page, `domain maps`, `lessons-moc`, and `general-moc` act as the default recall maps, and `review lenses` stay secondary so they help with provenance or confidence review without becoming the main home for knowledge.

## How To Start

1. Install the skill.

```bash
npx skills add shihyuho/skills --skill=ultrabrain
```

2. Optionally install the reminder block with `ultrabrain-init`. This inserts a mandatory prompt block in your `AGENTS.md` or `CLAUDE.md` that forces agents to consider using UltraBrain when you mention PKM-related keywords.

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

## Related Files

- [SKILL.md](SKILL.md) - Canonical workflow and operational rules
- [../../commands/ultrabrain-init.md](../../commands/ultrabrain-init.md) - Install the reminder block in `AGENTS.md` or `CLAUDE.md`
- [../../commands/ultrabrain-recall.md](../../commands/ultrabrain-recall.md) - Manual recall entrypoint
- [../../commands/ultrabrain-capture.md](../../commands/ultrabrain-capture.md) - Manual capture entrypoint
- [../../commands/ultrabrain-groom.md](../../commands/ultrabrain-groom.md) - Manual MOC grooming entrypoint

## License

MIT
