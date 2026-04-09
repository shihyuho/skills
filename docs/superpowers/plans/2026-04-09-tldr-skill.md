# tldr Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a new `tldr` skill that produces a tldr.tech-style digest of any target — file, directory, git ref/range, URL, or GitHub PR/issue — so the reader grasps the whole picture in roughly two minutes.

**Architecture:** Pure prompt skill. No scripts, no bundled references, no evals. A single `SKILL.md` encodes output shape, voice, sentence-based budget, and error handling. Input acquisition is left to Claude's existing tools (Read, Bash, WebFetch, gh). A companion `commands/tldr.md` is the slash-command entry point.

**Tech Stack:** Markdown (skill and command files). No build, no runtime, no tests beyond a manual smoke test against the spec checklist.

**Spec reference:** `docs/superpowers/specs/2026-04-09-tldr-design.md` — the authoritative source for every rule below. If this plan and the spec disagree, the spec wins.

---

## File Structure

- **Create** `skills/tldr/SKILL.md` — main skill body, ~55 lines. Encodes intent, output shape, voice, language rule, budget, unreachable-target rule, empty-invocation rule.
- **Create** `skills/tldr/README.md` — repo-level summary per the "every published directory under `skills/` must include SKILL.md and README.md" rule in `CLAUDE.md`. ~30 lines: what it does, usage, output shape overview, when not to use.
- **Create** `commands/tldr.md` — slash-command entry point. ~10 lines. Loads the `tldr` skill with `$ARGUMENTS` passed through; handles empty-invocation by asking.
- **Modify** `README.md` (repo root) — add one row to the "Available Skills" bullet list so the README inventory stays in sync with `skills/`, as required by `CLAUDE.md`.

No tests. Skill quality is subjective and evals were explicitly declined during brainstorming (`docs/lessons/eval-coverage-and-discrimination-are-different.md`). Verification is a manual smoke test.

---

## Task 1: Create `skills/tldr/SKILL.md`

**Files:**
- Create: `skills/tldr/SKILL.md`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p skills/tldr
```

- [ ] **Step 2: Write `skills/tldr/SKILL.md` with exactly this content**

````markdown
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
- **Sections** use `##` H2, forming a natural `# TLDR:` / `## Section` hierarchy in any Markdown renderer. No emoji, no horizontal rules. Section names describe logical parts of the input ("What it does", "How it works", "Gotchas"), not newsletter-style topic categories. **Sections are optional** — skip them entirely when items don't cluster, and list items directly under the subtitle. When items cluster, use 2-5 sections.
- **Items are conceptual units, not physical ones.** Slice by what changed in the reader's mental model, not by file, commit, section, or paragraph. Three commits for one feature become one item. Three unrelated files in one PR become three items. Without this rule agents default to mechanical one-per-file slicing that preserves the format but loses the spirit.
- **Item headline** is a single bold line. No reading-time annotation (see Budget).
- **Item body** is a single prose paragraph: **1-3 sentences typical, 4 maximum**. No bullets within the body. No sub-headings. Rule taken verbatim from tldr.tech: "1-3 sentence description" and "2-4 sentences maximum". Language-agnostic.
- **Typical item count**: roughly 6-10. Fewer when the source is shorter than the budget. No fixed numeric ceiling; err on fewer-and-tighter over more-and-bloated.
- **When the source has more logical units than the budget allows** (e.g., a PR touching 15 subsystems), group related units into fewer items rather than dropping units. Each item can cover multiple related subsystems so every part gets mentioned at least in aggregate. Drop only as a last resort, and only when grouping would merge things so disparate that the resulting item becomes incoherent.

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
````

- [ ] **Step 3: Verify the file structure**

```bash
ls -la skills/tldr/
wc -l skills/tldr/SKILL.md
```

Expected: `SKILL.md` exists, length roughly 55-65 lines.

- [ ] **Step 4: Commit (bundled with spec + plan)**

Include the previously-uncommitted design spec and implementation plan in this first commit — they are the context for everything that follows, and committing them separately after the fact would break causal ordering.

```bash
git add \
  docs/superpowers/specs/2026-04-09-tldr-design.md \
  docs/superpowers/plans/2026-04-09-tldr-skill.md \
  skills/tldr/SKILL.md
git commit -m "feat(tldr): add skill with design spec and plan"
```

---

## Task 2: Create `skills/tldr/README.md`

**Files:**
- Create: `skills/tldr/README.md`

- [ ] **Step 1: Write `skills/tldr/README.md` with exactly this content**

````markdown
# tldr

Produce a tldr.tech-style digest of a given target so the reader grasps the whole picture in roughly two minutes.

Inspired by [tldr.tech](https://tldr.tech/)'s scannable daily newsletter format, adapted for single-target compression of files, PRs, URLs, and other inputs.

## Usage

```
/tldr <target>
```

`<target>` can be any of:

- A file or directory path — `/tldr README.md`, `/tldr skills/grill-diff/`
- A git ref or range — `/tldr HEAD~3..HEAD`, `/tldr main..feature-x`
- A URL — `/tldr https://tldr.tech/ai/2026-04-08`
- A GitHub PR or issue — `/tldr anthropics/claude-code#100`

Everything passed in one invocation is treated as a single aggregate target. Multi-path args are aggregated into one digest, not multiple.

## Output shape

A scannable Markdown digest with:

- `# TLDR: <title>` heading and a 1-3 highlight italic subtitle
- Optional `## Section` groupings (skipped when items don't cluster)
- Bold item headlines followed by a 1-3 sentence prose body — **no bullets within items, no emoji, no horizontal rules, no reading-time labels**
- Items sliced as conceptual units (one feature = one item, even across three commits)
- Output language matches the source's majority prose language; technical terms stay in their original form

## What it does not do

- **No short-circuit refusal**: if you invoke `/tldr`, it runs. It will not second-guess whether the source is "too short to tldr".
- **No fabrication**: if any part of the target cannot be read honestly (missing file, unreachable URL, binary content, context overflow), the skill reports the obstacle and asks rather than making up content.
- **No input-type routing**: the skill treats all targets with the same rules — no special behavior per file type, per git ref, per URL, etc.

## Notes

Very short sources are often faster to read directly than to tldr. The skill will still run if you ask it to — no refusal — but manage your expectations.
````

- [ ] **Step 2: Commit**

```bash
git add skills/tldr/README.md
git commit -m "docs(tldr): add README.md"
```

---

## Task 3: Create `commands/tldr.md`

**Files:**
- Create: `commands/tldr.md`

- [ ] **Step 1: Write `commands/tldr.md` with exactly this content**

````markdown
---
description: "Produce a tldr.tech-style digest of a target"
---

Use the `tldr` skill to produce a digest of the target specified in `$ARGUMENTS`.

If `$ARGUMENTS` is empty, ask the user what to tldr. Do not guess the current conversation context.

Otherwise, treat everything in `$ARGUMENTS` as a single aggregate target (file path, directory, git ref/range, URL, GitHub PR, or GitHub issue). Acquire the content using the appropriate built-in tool (Read for files, Bash with `git` for refs, WebFetch for URLs, `gh` for PRs/issues), then produce the digest according to the `tldr` skill's rules.

Execute only this flow for this invocation. Do not run unrelated actions unless the user explicitly asks.
````

- [ ] **Step 2: Commit**

```bash
git add commands/tldr.md
git commit -m "feat(tldr): add /tldr slash command"
```

---

## Task 4: Update root `README.md`

**Files:**
- Modify: `README.md` (repo root)

- [ ] **Step 1: Read the current Available Skills section**

```bash
sed -n '1,20p' README.md
```

Expected: existing bullet list of skills including `executing-plans-preflight`, `fanfuaji`, `lessons-learned`, `e04`, `writing-agents-md`, `promote-claude-settings`, `cover-branches`, `grill-diff`.

- [ ] **Step 2: Insert the tldr row into the Available Skills list**

Add this line to the Available Skills bullet list (alphabetical order would place it at the end since `t` > `g`, but the existing list is not alphabetical — place it after `grill-diff` to keep the "most recently added" convention the repo appears to follow):

```markdown
- **[tldr](skills/tldr/)** - Produce a tldr.tech-style digest of a file, directory, git ref, URL, or GitHub PR/issue so the reader grasps the whole picture in roughly two minutes.
```

- [ ] **Step 3: Verify the change**

```bash
grep -n "tldr" README.md
```

Expected: one line matching the inserted bullet.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add tldr to README skills list"
```

---

## Task 5: Smoke test the skill manually

The skill has no automated tests. Verification is a manual smoke test against the spec checklist, using the spec itself as a reference target (it's long enough to exercise grouping, short enough to verify coverage).

- [ ] **Step 1: Run the skill on the spec file**

In a fresh Claude Code session:

```
/tldr docs/superpowers/specs/2026-04-09-tldr-design.md
```

- [ ] **Step 2: Verify the output against this checklist**

The output must have **all** of:

- [x] Starts with `# TLDR: <title>` (title identifies the spec or its subject)
- [x] Has an italic subtitle with 1-3 comma-separated highlights
- [x] **No** reading-time annotation in the subtitle or anywhere else
- [x] Either uses `## Section` H2 headings or skips sections entirely (no `**Section**` inline bold as section dividers, no `###` H3 for sections)
- [x] **No** emoji in section headers or subtitles
- [x] Item headlines are **bold inline** (`**...**`)
- [x] Item bodies are **prose paragraphs with 1-3 sentences** (occasionally up to 4), with **no bullets** inside
- [x] Total digest body reads in roughly 2 minutes (vibes-check, not math)
- [x] Items represent **conceptual units**, not one-per-file or one-per-section mechanical slicing
- [x] Output language matches the spec's majority prose language (English, since the spec is English)
- [x] Technical terms like "tldr.tech", "SKILL.md", "H2" stay in original form
- [x] Does not fabricate content not present in the spec

- [ ] **Step 3: If any checklist item fails, open `skills/tldr/SKILL.md` and fix the rule that caused the miss**

Common failure modes and the rule to tighten:

- **Format drift** (wrong heading level, emoji appears, bullets inside items) → tighten the Output shape section.
- **Mechanical slicing** (one item per spec section regardless of concept overlap) → tighten the "Items are conceptual units" paragraph; strengthen the example.
- **Fabrication or over-padding** → tighten the Budget "ceiling, not a quota" rule or the Unreachable rule.
- **Reading-time label reappears** → tighten the Budget "No reading-time annotation" rule.

- [ ] **Step 4: Re-run step 1 and repeat until the checklist passes**

- [ ] **Step 5: Commit any `SKILL.md` fixes discovered during smoke testing**

```bash
git add skills/tldr/SKILL.md
git commit -m "fix(tldr): tighten <rule> based on smoke-test findings"
```

If no fixes were needed, skip this step.

---

## Task 6: Run a second-target smoke test

One-target smoke testing covers the "long English spec" case. Test a second target shape to catch rules that only break on a different input kind.

- [ ] **Step 1: Run the skill on a git diff target**

```
/tldr HEAD~3..HEAD
```

- [ ] **Step 2: Verify the same checklist from Task 5**

Additional checks specific to git-ref targets:

- [x] The digest describes **conceptual changes**, not "commit abc123 did X, commit def456 did Y" per-commit slicing
- [x] Multiple commits implementing one logical change appear as one item
- [x] Unrelated changes across files appear as separate items

- [ ] **Step 3: Fix any rule misses and commit**

```bash
git add skills/tldr/SKILL.md
git commit -m "fix(tldr): <rule> based on git-ref smoke-test findings"
```

Skip if no fixes.

---

## Self-Review Notes

- **Spec coverage**: every rule in `docs/superpowers/specs/2026-04-09-tldr-design.md` that applies to the agent's output has a corresponding line in the Task 1 SKILL.md content — Objective, aggregate target, output shape (top header, sections, items, conceptual slicing, count, grouping), voice, output language, budget, unreachable targets, empty invocation. The spec's "What the Skill Does Not Cover" and "Non-Goals" sections are deliberately absent from SKILL.md — they are rationale, not rules.
- **No placeholders**: all file content is shown inline. No TBDs, no "fill in later", no "similar to Task N".
- **Type consistency**: file paths (`skills/tldr/SKILL.md`, `skills/tldr/README.md`, `commands/tldr.md`, `README.md`), command name (`/tldr`), and cross-file references are consistent across tasks.
- **Repo rules followed**: `skills/tldr/` has both SKILL.md and README.md (CLAUDE.md requirement); no `_`-prefixed subdirectories; root README.md is updated to reflect the new skill (CLAUDE.md requirement); no test run is required for `skills/fanfuaji/scripts/` (no changes there).
