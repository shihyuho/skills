---
name: tldr
description: Produce a tldr.tech-style digest of a given target (file, directory, git ref/range, URL, GitHub PR, or GitHub issue) so the reader grasps the whole picture in roughly two minutes. Use when the user explicitly invokes `/tldr` or asks for a tldr of a specific target.
---

## Intent

Everything passed in one `/tldr` invocation is one aggregate target. Describe the aggregate as a whole — "what is this thing, why does it exist, what's inside, what should I watch out for" — not a concatenation of per-source summaries. Acquire the content using Claude's standard tools (Read, Bash, WebFetch, `gh`) — this skill does not teach how to fetch.

## Output shape

```
# TLDR: <title>
*<1-3 comma-separated highlights>*

## <Section name>
**<Item headline>**
<Prose body: 1-3 sentences typical, 4 max. No bullets. No sub-headings.>

**<Next item headline>**
<Body.>

## <Next section>
...
```

- **Title** identifies the target (file name, PR title, URL slug, etc.).
- **Subtitle**: 1-3 italic highlights separated by commas. Don't pad to three.
- **Sections** use `##` H2, forming a natural `# TLDR:` / `## Section` hierarchy in any Markdown renderer. No emoji, no horizontal rules. Section names describe logical parts of the input ("What it does", "How it works", "Gotchas"), not newsletter-style topic categories. **Sections are optional** — skip them entirely when items don't cluster naturally, and list items directly under the subtitle.
- **Item headline** is a single bold line. **Item body** is a single prose paragraph of **1-3 sentences, 4 maximum**. No bullets within the body. No sub-headings. No reading-time annotation anywhere.

## Items

**Items are conceptual units, not physical ones.** Slice by what changed in the reader's mental model, not by file, commit, section, or paragraph. Three commits for one feature become one item. Three unrelated files in one PR become three items.

Typical count: 6-10 items. Fewer when the source is shorter than the budget. Err on fewer-and-tighter over more-and-bloated.

**When the source has more logical units than the budget allows** (e.g., a PR touching 15 subsystems), group related units into fewer items rather than dropping units. Each item can cover multiple related subsystems so every part gets mentioned at least in aggregate. Drop only as a last resort.

## Voice

Casual and conversational without being unprofessional. Straightforward language, occasional informal phrasing welcome — never at the cost of technical precision. Prefer plain verbs over corporate nouns ("rewrote the filter", not "performed a refactoring of the filter module"). No hedging fluff ("it might be worth noting that…", "in general terms…") — cut them.

## Output language

Follow the **majority language of the source's prose content** — commit messages, comments, docs, discussion. Code, identifiers, package names, CLI flags, and boilerplate (badges, license headers, shields) do not count toward the majority.

**Technical terms stay in their original form** even when the surrounding prose is translated. Never rewrite "specialist subagent", "pre-commit hook", or similar established jargon into the prose language. A Chinese digest writes "fast mode 用 specialist subagent 先篩選 high-value findings", not「快速模式用專家子代理預先篩選高價值發現」.

When the source prose is roughly 50/50, default to the language of the user's most recent invocation message. The user can override explicitly (e.g., `/tldr <target> in English`).

## Budget

Target roughly **two minutes** of reading time; safety rail at three. The budget is **purely internal self-regulation** — it never appears in the digest. No "~2 min read" label in the subtitle, no per-item annotation, nothing. A visible label would be noise if correct and misleading if wrong.

Enforcement is **sentence-based**, not word-count-based: the 1-3-sentence-per-item rule is the primary brake. Do not count words or characters — that over-engineers a rule tldr.tech handles with plain sentence limits. The two-minute figure is a vibes-based sanity check on the overall digest, not a math problem.

The budget is a **ceiling, not a quota**. When the source is shorter than the budget, the digest is proportionally shorter — don't pad. When compression would lose coherence, prefer dropping items over shortening individual items into incoherence.

## Unreachable targets

If any part of the target can't be read honestly — file missing, URL unreachable, PR forbidden, binary content, empty source, context-window overflow — **report the obstacle and ask**. Do not fabricate. A partial digest is acceptable if the partial scope is declared at the top; a fabricated "whole picture" is not.

This rule exists to override the subtle incentive the "grasp the whole picture" goal creates to fill gaps.

## Empty invocation

If `/tldr` is called without a target, ask the user what to tldr. Do not guess the current conversation context.
