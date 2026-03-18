# UltraBrain

Give your AI a knowledge system it can actually learn from.

`ultrabrain` helps AI recall the right context before acting, capture reusable lessons after work, and avoid repeating the same mistakes as your knowledge base grows.

## Why UltraBrain

Most AI workflows lose important learning in chat history, scattered notes, or unstable metadata. UltraBrain gives agents a cleaner long-term memory model:

- recall relevant knowledge before planning or execution
- capture reusable lessons instead of rediscovering them later
- keep stable knowledge separate from changing navigation structure
- preserve provenance without making cards depend on the source to make sense
- let AI improve the vault over time without turning it into a folder dump

## What It Helps AI Do

### Recall before acting

UltraBrain starts with a small map-first recall to orient the work, loops back only when planning reveals a real gap, risk, or decision, then runs a narrow lessons pass before execution.

### Learn from finished work

After a task, AI can decide whether a lesson should be skipped, rewritten first, added as a new note, or used to update an existing one.

### Avoid repeating mistakes

Past decisions, debugging lessons, and proven heuristics stay available for the next plan, refactor, or risky change.

### Keep knowledge clean as the vault evolves

Cards stay self-contained, maps stay focused on navigation, and source notes stay minimal. That separation keeps the system usable even when structure changes.

## How It Works

UltraBrain keeps a simple file layout:

```text
docs/ultrabrain/
  maps/
  notes/
  sources/
```

- `maps/` contains entry pages, default recall maps, and optional review lenses for provenance or uncertainty review
- `notes/` contains self-contained canonical knowledge cards
- `sources/` contains minimal provenance notes, not archives or missing card context

The workflow is simple:

- start with a small map recall, then pull in more only when planning exposes a real gap
- capture reusable knowledge only when it is worth keeping, and rewrite thin lessons before turning them into notes
- keep navigation changes in maps instead of stuffing them into note metadata
- keep source notes for provenance only, and treat broader MOC grooming as a separate manual pass

### Obsidian Integration

`docs/ultrabrain/` is plain Markdown. If you use Obsidian, you can open `docs/ultrabrain/` directly as a vault and work with the same files your AI uses.

## Example Prompts

```text
Recall the most relevant ultrabrain maps before planning this refactor.

We just finished a debugging session. Capture the reusable lesson into ultrabrain so we do not repeat this mistake.

Before touching this migration, use ultrabrain to load any prior lessons about retries, rollback risk, and deployment failures.

Reorganize my messy docs/ultrabrain vault into maps, notes, and sources so AI can navigate it more reliably.
```

## Get Started

Install the skill:

```bash
npx skills add shihyuho/skills --skill=ultrabrain
```

You can then open `docs/ultrabrain/` directly in Obsidian if you want a visual vault on top of the same Markdown files.

If you want the reminder block that nudges agents to consider UltraBrain automatically, use `ultrabrain-init`.

For the full workflow rules, recall model, and capture behavior, see [SKILL.md](SKILL.md).

## Learn More

- [SKILL.md](SKILL.md) - canonical workflow and operational rules
- [../../commands/ultrabrain-init.md](../../commands/ultrabrain-init.md) - install the reminder block in `AGENTS.md` or `CLAUDE.md`
- [../../commands/ultrabrain-recall.md](../../commands/ultrabrain-recall.md) - manual recall entrypoint
- [../../commands/ultrabrain-capture.md](../../commands/ultrabrain-capture.md) - manual capture entrypoint
- [../../commands/ultrabrain-groom.md](../../commands/ultrabrain-groom.md) - manual MOC grooming entrypoint

## License

MIT
