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
