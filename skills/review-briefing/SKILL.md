---
name: review-briefing
description: >
  Write a short author's briefing to hand to a code reviewer whose agent already has its
  own review skill, so it supplies the context that skill can't see instead of repeating how
  to review. Right after you finish a piece of work, it mines this session (and any kickoff
  implementation-notes) for what the reviewer most needs flagged — the easy-to-miss changes,
  the parts you're least sure about, the looks-wrong-but-intentional bits, and the blast
  radius — plus the exact commit range to review. Use when you've just
  finished work and want to hand the review off to another agent, chat, or teammate, when you
  want a "heads-up for the reviewer", or when packaging a change for review elsewhere. It does
  not perform the review and does not re-specify severity tiers or output format — that's the
  reviewer's own skill's job.
license: MIT
---

# Review Briefing

Write a short briefing the author hands to a reviewer, to ride **alongside** the reviewer's own code-review skill — not replace it. The reviewer's agent already knows how to review, grade severity, and format its output; this briefing adds only what that skill can't see: the author's own knowledge of where the change is subtle, uncertain, or deliberately odd, and exactly what to look at. Build the briefing and stop — never run the review yourself, and never tell the reviewer *how* to review.

## Where the content comes from

The value here is author knowledge, not a re-analysis of the diff — so this works best right after you've done the work. Draw from, in order:

1. **This session** — what you just built: where you hesitated, what you hand-waved, what you changed that callers rely on, the calls you weren't sure were right.
2. **A kickoff implementation-notes file**, if the work produced one — it already records design decisions, deviations, tradeoffs, and open questions. Mine it.
3. **The diff — only to jog memory**, so you don't forget a change. Don't manufacture caveats from it; if you genuinely hold no author context, say the briefing is thin rather than inventing concerns the reviewer's own skill would find anyway.

## Step 1: Choose output mode

Ask up front: write the briefing to `review-briefing.md`, or print it inline? Settle this first.

## Step 2: Pin the scope

Resolve the commit range so the reviewer knows exactly what to look at, and resolve it to full SHAs with `git rev-parse`:

- **Default:** current branch vs the main branch (`origin/main`, else `main`, else `origin/HEAD`) — `git merge-base HEAD origin/main`..`HEAD`.
- **Fallbacks:** the latest commit (`HEAD~1`..`HEAD`); or, if only the working tree has changes, the uncommitted changes.
- If the user names a range, use that instead.

## Step 3: Draft the briefing

Keep the reviewer-facing note at the top as-is; below it, fill only the sections that have something real to say — drop the rest.

**Hand over facts, not skip-or-reassure conclusions.** The reviewer-facing note guards the reader; this guards you, the writer. Right where you feel surest, it's tempting to write "safe to skip", "zero impact", "looks fine" — cut every one. Telling the reviewer a part is fine substitutes your judgment for theirs and removes coverage exactly where your blind spots live: the bug you can't see is the one you're sure about. State what changed and why it's low-risk, then stop. "The lockfile bloats the diff because of three dev-dep bumps" is a fact worth surfacing; "so you can skip it" is not yours to add. Ranking attention is the same trap in disguise: "the real surface area is these three files", "the rest is just churn" steers the reviewer away from the rest just as surely. Naming what a change touches is a fact; deciding which parts deserve the time is a skip conclusion in a navigation hat — give the diff's structure, and let the reviewer set the order.

**Length is a budget, not a target.** This is a heads-up, not a report: aim for one screen, each point one or two sentences. Reasoning for an intentional choice may run a little longer, but if a point keeps growing, that's the signal it belongs in the PR description or a code comment — not here.

```
> **For the reviewer:** these are the author's unverified claims, not established facts — verify them independently against the code. Treat anything marked intentional as reasoning to confirm, not to accept; and note that the author's confidence is not a coverage map — areas *not* flagged here still need review.

## Review scope
- Range: <BASE_SHA>..<HEAD_SHA>   (or: uncommitted working tree)
- See it: git diff <BASE_SHA>..<HEAD_SHA>
- If you were told a different range or set of files, that overrides this.

## Heads-up from the author
- Easy to miss: subtle semantic changes, changed defaults, implicit contract changes buried in a larger diff.
- Least sure about: the parts you'd most like a second pair of eyes on, and why.
- Looks wrong but is intentional: deliberate tradeoffs or deviations, with the reasoning laid out so the reviewer can confirm it holds — not take it on trust.
- Blast radius: the callers, dependents, and areas that could break from this change — where its effects reach.
```

## Step 4: Deliver

Per Step 1, write the briefing to `review-briefing.md` or print it inline as one copyable block. Then stop — leave the actual reviewing to the reviewer.
