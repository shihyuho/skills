# Review Briefing

Write a short author's briefing to hand to a code reviewer — it does not run the review here.

Meant to ride **alongside** the reviewer's own code-review skill rather than replace it: the reviewer's agent already knows how to review, grade, and format output, so this adds only what that skill can't see — the author's knowledge of where the change is subtle, uncertain, or deliberately odd, plus the exact commit range to review. It works best right after you've done the work, drawing on this session (and any [`kickoff`](../kickoff/) implementation-notes) rather than re-analyzing the diff. On start it asks whether to save the briefing to `review-briefing.md` or print it inline.

What it deliberately leaves out: how to review, severity tiers, output format — that's the reviewer's own skill's job.

## Usage

Ask for it right after finishing a piece of work, or invoke it explicitly:

- *"write a briefing I can hand to a teammate's reviewer agent — flag the tricky bits and what I'm unsure about"*
- *"package my last commit as a heads-up note for whoever reviews it"*
- `/skills:review-briefing` — explicit invocation in Claude Code

## Installation

```bash
npx skills add shihyuho/skills --skill review-briefing -g
```
