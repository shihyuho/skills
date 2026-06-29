---
name: lgtm
description: Before acting on an approval, re-read from disk every file that was under review — the user may have edited them while reviewing, leaving your in-context copy stale. Use when the user signals go-ahead on something you put up for review — "lgtm", "looks good", "looks good to me", "approved", "go ahead" — before you start the next step. Applies to any reviewed artifact — spec, plan, diff, edited code, proposal.
license: MIT
---

# LGTM

You can't see edits the user made outside the conversation. So before the next step, act on **evidence** of what's on disk now — not on **belief** about what you wrote there. Your in-context copy is belief; so is your certainty that nothing changed. Neither earns the right to skip a re-read — re-reading from disk does.

A cheap, objective check of *which* files changed can narrow that work, but it counts as evidence only when it's real. It must be **fresh** — run now, after the user finished reviewing; a `git status` you remember from earlier predates their edits, so it's belief, not evidence. And it speaks only for what it tracks: use `git status` (a bare `git diff` misses staged and untracked changes), and read its silence about a file — new, untracked, gitignored, or outside the repo — as "unseen," not "unchanged."

So skip a reviewed file only where a fresh check positively vouches it's unchanged; re-read every other one — and with no such check, re-read them all. For just a file or two, skip the check — re-reading them outright is cheaper.

- Can't tell which files were under review? Ask.
- Nothing under review was a file — it lived only in chat? Nothing to re-read; just proceed.

Don't make a ceremony of it — re-read what the evidence points to, then continue.
