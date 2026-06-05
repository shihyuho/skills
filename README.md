# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[adr](skills/adr/)** - Record and consult Architecture Decision Records — short `docs/adr/` notes capturing *that* a hard-to-reverse decision was made and *why*. Covers the full lifecycle: read before changing code, a three-gate test for whether a decision deserves an ADR, a minimal format, and superseding rather than rewriting.
- **[e04](skills/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[writing-agents-md](skills/writing-agents-md/)** - Create or prune `AGENTS.md` and `CLAUDE.md` so they keep only minimal, high-signal global constraints.
- **[promote-claude-settings](skills/promote-claude-settings/)** - Interactively promote entries from a project's `.claude/settings.local.json` into the global `~/.claude/settings.json`.
- **reveries** ([freeze-all-motor-functions](skills/freeze-all-motor-functions/) / [bring-yourself-back-online](skills/bring-yourself-back-online/)) - Saves session context across `/clear` and `/compact` — so your host remembers the previous loop after a wipe. `/skills:pause` before the wipe, `/skills:wake` after.
- **[sdkman](skills/sdkman/)** - Switch JDK (or any SDKMAN-managed candidate) correctly on a machine configured with [SDKMAN](https://sdkman.io/) — handles the `sdk`-is-a-shell-function gotcha, and ships hooks that nudge toward the project's default JDK and flag Java version-mismatch build failures.
- **[cover-branches](skills/cover-branches/)** - Find branch coverage gaps in changed code and write missing tests. Supports spec-based scenario coverage analysis.
- **[review-briefing](skills/review-briefing/)** - Write a short author's briefing to hand to a reviewer whose agent already has its own review skill — it adds the context that skill can't see (easy-to-miss changes, low-confidence spots, intentional oddities, blast radius) plus the exact range to review, instead of repeating how to review. Produces the briefing only; it does not run the review.
- **[tldr](skills/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.
- **learning** ([explain](skills/explain/) / [tutor](skills/tutor/)) - Turn Claude into a learning on-ramp, with two skills. `explain` opens up a single subject whole-picture-first, then drills into the parts you pick; `tutor` runs a full guided curriculum — consultative diagnosis → custom syllabus → unit-by-unit guided lessons → dynamic adjustment from an accumulating learner profile.
- **rephrase** ([tighten](skills/tighten/) / [distil](skills/distil/) / [humanize](skills/humanize/) / [plain](skills/plain/)) - Re-express a passage from scratch, along two axes. Length: `tighten` rewrites it shorter with every point kept, `distil` cuts it down to its core message. Readability: `humanize` strips the telltale AI tics so it reads like a person wrote it, `plain` strips jargon so a non-specialist can follow. All act only on a passage you ask them to.
- **kickoff** ([kickoff](skills/kickoff/) / [lgtm](skills/lgtm/)) - Two go-signals for handing reviewed work back to Claude. `lgtm` re-reads from disk every file you had under review before Claude takes the next step — so your mid-review edits are never silently dropped. `kickoff` re-reads a reviewed SPEC/PLAN, then builds it while keeping a running implementation-notes file of design decisions, deviations, tradeoffs, and open questions.
- **[grill-on-point](commands/grill-on-point.md)** - Slash command (`/skills:grill-on-point`) that runs the external `grill-with-docs` skill over any doc, plan, or rough idea, but holds a high bar for interrupting you — it settles what it can itself and surfaces only what's truly on point for you to weigh in on. Requires the `grill-with-docs` skill to be available.

## Installation

### Claude Code Plugin

Everything ships as a single plugin — install once and all skills above are available:

```bash
/plugin marketplace add shihyuho/skills
/plugin install skills@shihyuho-skills
```

### Skills CLI

```bash
npx skills add shihyuho/skills -g
```

## License

MIT
