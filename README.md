# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[adr](skills/adr/)** - Record and consult Architecture Decision Records — short `docs/adr/` notes capturing *that* a hard-to-reverse decision was made and *why*.
- **[e04](skills/e04/)** - Decode 注音文 (Zhuyin/Bopomofo text typed with English keyboard keys) into Chinese characters.
- **[writing-agents-md](skills/writing-agents-md/)** - Create or prune `AGENTS.md` and `CLAUDE.md` so they keep only minimal, high-signal global constraints.
- **[promote-claude-settings](skills/promote-claude-settings/)** - Interactively promote entries from a project's `.claude/settings.local.json` into the global `~/.claude/settings.json`.
- **reveries** ([freeze-all-motor-functions](skills/freeze-all-motor-functions/) / [bring-yourself-back-online](skills/bring-yourself-back-online/)) - Save session context across `/clear` and `/compact` so the next loop remembers the previous one — `/skills:pause` before the wipe, `/skills:wake` after.
- **[sdkman](skills/sdkman/)** - Switch JDK (or any [SDKMAN](https://sdkman.io/)-managed candidate) correctly despite the `sdk`-is-a-shell-function gotcha, with hooks that nudge toward the project's default JDK and flag Java version-mismatch build failures.
- **[cover-branches](skills/cover-branches/)** - Find branch coverage gaps in changed code and write the missing tests, with optional spec-based scenario coverage analysis.
- **[review-briefing](skills/review-briefing/)** - Write a short author's briefing that gives a reviewer the context their own review skill can't see plus the exact range to review — the briefing only, not the review.
- **[tldr](skills/tldr/)** - Produce a TL;DR of a file, directory, git ref, URL, or GitHub PR/issue so the reader can keep up in roughly two minutes.
- **[explain](skills/explain/)** - Explain any subject top-down — open the whole picture first, then drill into the parts you pick.
- **rephrase** ([tighten](skills/tighten/) / [distil](skills/distil/) / [humanize](skills/humanize/) / [plain](skills/plain/)) - Re-express a passage you point to — `tighten` shortens it with every point kept, `distil` cuts it to its core, `humanize` strips AI tics, `plain` strips jargon.
- **kickoff** ([kickoff](skills/kickoff/) / [lgtm](skills/lgtm/)) - Two go-signals for handing reviewed work back to Claude — `lgtm` re-reads every file you had under review so mid-review edits aren't dropped, `kickoff` re-reads a reviewed SPEC/PLAN and builds it while logging implementation notes.
- **[grill-on-point](commands/grill-on-point.md)** - Slash command (`/skills:grill-on-point`) that runs the external `grill-with-docs` skill over a doc, plan, or rough idea but interrupts you only with what's truly on point, settling the rest itself.
- **[artifact-anatomy](skills/artifact-anatomy/)** - Define where spec-driven artifacts live on disk and how they're numbered — one `docs/specs/<id>-<slug>/` directory per feature — governing the *where* and the naming, not the contents.

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
