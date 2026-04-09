# tldr Skill — Design Spec

## Objective

A skill that produces a tldr.tech-style digest of a given target so that the user can grasp the whole picture within ~2 minutes of reading.

**Everything passed in a single `/tldr` invocation is treated as one aggregate target** — whether that's a single file, a directory, multiple paths, a git ref/range, a URL, or a GitHub PR/issue. The digest describes the aggregate as a whole ("what is this thing, why does it exist, what's inside, what should I watch out for"), not a concatenation of per-source summaries. The skill does not branch behavior on target type.

The skill is deliberately narrow. It does **not** teach the agent how to fetch inputs — Claude already knows how to read files, run `git diff`, `WebFetch`, or `gh` commands. The skill only encodes what Claude is not naturally good at: the target output shape, the reading-time budget, and the casual-but-professional voice that makes a digest scannable instead of bloated.

## Trigger

Slash command is the primary entry point: `/tldr <target>`. The command file lives at `commands/tldr.md` and simply loads the `tldr` skill with the user-provided argument as the target.

The skill's `description` frontmatter is deliberately **not** pushy. The user has stated they will invoke the skill explicitly when they want it — undertriggering is preferable to false positives in this case.

Empty-argument behavior: when the user runs `/tldr` without a target, the skill reflects the question back to the user ("What should I tldr?") rather than guessing current conversation context.

## Output Format

The output format is taken directly from a reverse-engineering of [tldr.tech](https://tldr.tech/), with small adaptations for single-input usage.

### Top header

```
# TLDR: <title>
*<one-line subtitle with 1-3 key hooks>*
```

- `<title>` identifies the target (e.g., file name, PR title, URL slug).
- `<subtitle>` is a single italic line listing **1-3 comma-separated highlights** (whatever the source naturally offers — do not pad to three). No reading-time annotation — see Reading-Time Budget for why.

### Sections

Section headings use **H2** (`## Foo`) — forming a natural `# TLDR:` / `## Section` hierarchy when the digest is rendered in any Markdown environment (GitHub comment, Notion, Slack rich text). No emoji, no horizontal rules. Item headlines remain inline bold (`**Foo**`) so H2 section headings stay visually distinct from item headlines.

A section groups related items. For a single-target tldr, sections represent logical parts of the input (e.g., "What it does", "How it works", "Gotchas"), not newsletter-style topic categories.

Sections are optional. When the digest has only a handful of items with no natural grouping, the agent skips sections and lists items directly under the top header. When items cluster naturally, the agent introduces 2-5 sections. Judgment call, not a table.

### Items

**Items are conceptual units, not physical ones.** Slice by "what changed in the user's mental model" — not by file, commit, section, or paragraph. Related physical units (three commits implementing one feature, two files of the same subsystem, three sections about the same concept) collapse into one item. Unrelated physical units in the same container (three files in one PR touching different subsystems) become different items.

Concrete example. A PR with three commits — `add dark mode toggle`, `fix dark mode toggle flicker`, `add dark mode toggle tests` — is **one item**, not three:

> **Dark mode toggle shipped** — a new toggle lands with an initial-render flicker fix folded in and tests alongside.

This rule exists because tldr.tech items are "stories" (concept-essence units), and without this guidance an agent will default to a mechanical "one-per-file" or "one-per-commit" slicing that preserves the format but loses the spirit.

Each item follows a two-part structure:

- **Headline**: a single bold line describing the item. No reading-time annotation — see Reading-Time Budget for why the digest carries no visible time labels at all.
- **Body**: a single prose paragraph, **typically 1-3 sentences, up to 4 at most**. No bullet points within the body, no sub-headings. (Sentence-based rule taken verbatim from the tldr.tech analysis — "1-3 sentence description" and "2-4 sentences maximum". Language-agnostic by design.)
- No metadata line. (tldr.tech uses publication date / category tags; those are newsletter-specific and dropped here.)

Typical item count: roughly **6-10 items** for a digest that honestly hits the ~2 minute budget. Fewer items when the source is shorter than the budget (budget is a ceiling, not a quota). No fixed numeric item ceiling — the agent uses judgment, erring on the side of fewer-and-tighter over more-and-bloated.

**When the source has more logical units than the budget allows** (e.g., a PR touching 15 subsystems when only ~8-10 items comfortably fit), the agent **groups related units into fewer items** rather than dropping units. Each item can cover multiple related subsystems/files/sections so every part of the source gets mentioned at least in aggregate. Dropping is the last resort — only when grouping itself would merge things so disparate that the resulting item becomes incoherent.

## Voice and Tone

Taken verbatim from the tldr.tech analysis:

> The writing is casual and conversational without being unprofessional. Summaries use straightforward language and occasionally include informal phrasing.

Concrete rules for the agent:

- Prefer plain verbs over corporate nouns ("rewrote the filter" over "performed a refactoring of the filter module").
- Occasional informal phrasing is welcome, never at the cost of technical precision.
- No hedging fluff ("it might be worth noting that…", "in general terms…"). Cut them.

### Output language

Output follows the **majority language of the source's prose content** — that is, the natural-language text in the source (commit messages, comments, docs, discussion). Code, identifiers, package names, CLI flags, and boilerplate (badges, license headers, shields) are excluded from the majority calculation.

**Technical terms stay in their original form** even when the surrounding prose is translated. Never rewrite "specialist subagent", "pre-commit hook", "rolling update", or similar established jargon into the prose language. A Chinese digest of this very spec should write "fast mode 用 specialist subagent 先篩選 high-value findings", not「快速模式用專家子代理預先篩選高價值發現」.

When the source prose is roughly 50/50, default to the language of the user's most recent invocation message. The user can also override explicitly in the invocation (e.g., `/tldr <target> in English`).

## Reading-Time Budget

Taken from the tldr.tech analysis:

> Each summary distills articles to 2-4 sentences maximum, enabling rapid scanning.

The raw tldr.tech "Keep up in 5 minutes" budget is deliberately **not** adopted. That five minutes covers ~15 items across multiple topic categories; a single-target tldr has fewer items (see Items section), so the per-target budget scales down proportionally. Giving the agent 5 minutes for a single target invites Parkinson's law — the agent fills the budget and the output stops being a tldr.

Concrete rules:

- **Target**: ~2 minutes of reading time. Single number, no complexity tiers — the extra judgment a "complex vs. simple" rule would demand is not worth the rule-surface cost.
- **Ceiling**: ~3 minutes, used only as a safety rail.
- **Budget is a ceiling, not a quota**: when the source is shorter than the budget, the agent produces a proportionally shorter digest. It does not pad to hit the target.
- **No short-circuit refusal**: if the user invoked `/tldr`, the agent runs. It does not second-guess whether the source is "too short to tldr" and refuse.
- **Enforcement is sentence-based, not word-count-based**: the per-item sentence rule (1-3 typical, 4 max) is the primary brake. The agent does not count words or characters — that over-engineers a rule that tldr.tech handles with plain sentence limits. The ~2 minute target is a vibes-based sanity check on the overall digest, not a math problem.
- **No reading-time annotation in the output**: the budget is purely the agent's internal self-regulation — it never appears in the digest itself, neither in the subtitle nor per-item. The reader sees a short digest; they do not see "~2 min read" labels. A visible label would be (a) noise if correct, (b) misleading if wrong, and (c) yet another surface the agent has to maintain.
- When compression would lose coherence, prefer dropping items over shortening individual items into incoherence.

## Unreachable or Unreadable Targets

If any part of the target can't be read honestly — file missing, URL unreachable, PR forbidden, binary content, empty source, context-window overflow — the agent **reports the obstacle and asks**, and does **not** fabricate the missing content. A partial digest is acceptable as long as the partial scope is declared at the top of the digest; a fabricated "whole picture" is not.

This rule matters because the "grasp the whole picture" goal creates a subtle incentive to fill gaps. The rule exists to override that incentive.

## What the Skill Does Not Cover

Deliberately excluded from `SKILL.md` because Claude already handles them:

- **Input acquisition**: how to read files, resolve paths, run `git diff`, call `WebFetch`, use `gh pr view`, etc. Claude already knows these.
- **Target-type routing**: the skill doesn't branch per input type. A single voice/format specification works for all targets.
- **Deterministic helpers**: no scripts, no tools, no bundled resources beyond `SKILL.md` and `README.md`.

This is the application of a prior lesson (`docs/lessons/agent-rule-discoverability-needs-costly-mistake-exception.md`): discoverability is the default delete signal, and input-fetching mechanics are maximally discoverable.

## File Layout

```
skills/tldr/
├── SKILL.md           # English; main skill body
└── README.md          # English; short project-level summary (per repo rule)

commands/
└── tldr.md            # Slash command entry; loads the tldr skill
```

The tldr digest **output** itself defaults to matching the input language (Chinese input → Chinese digest, English input → English digest). Only the `SKILL.md` / `README.md` / `commands/tldr.md` files themselves are English.

No `scripts/`, no `references/`, no `evals/`.

## Non-Goals

- **No evals**: tldr output quality is subjective. A prior lesson (`docs/lessons/eval-coverage-and-discrimination-are-different.md`) warned that coverage evals on subjective skills often fail to discriminate between with-skill and baseline. Quality assurance will be manual review of 2-3 test runs before merging.
- **No pushy trigger**: the user will invoke `/tldr` explicitly.
- **No emoji decoration**: plain markdown, bold only.
- **One invocation, one digest**: multi-path args like `/tldr fileA fileB` do not produce multiple digests. They are aggregated into a single digest — see Objective.

## Open Questions for Implementation

None blocking. The following are minor defaults that the implementation phase will lock down:

- Exact wording of the empty-argument reflection prompt.
- Whether to surface `git log` metadata (commit count, authors) when the target is a git ref, or leave that to agent judgment. Default: agent judgment.
