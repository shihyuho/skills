---
name: lgtm
description: Before acting on an approval, re-read from disk every file that was under review — the user may have edited them while reviewing, leaving your in-context copy stale. Use when the user signals go-ahead on something you put up for review — "lgtm", "looks good", "looks good to me", "approved", "go ahead" — before you start the next step. Applies to any reviewed artifact — spec, plan, diff, edited code, proposal.
license: MIT
---

# LGTM

The user reviewed something you put up — a spec, plan, diff, edited code, a proposal — and approved it. While reviewing, they may have edited the files themselves, so whatever you hold in context is now possibly stale.

## On approval

Before the next step, re-read from disk every file that was under review. Build on what is on disk now, not on what you remember writing there — and do this even when you are sure nothing changed, since you cannot see edits made outside the conversation.

- Can't tell which files were under review? Ask.
- Nothing under review was a file — it lived only in chat? Nothing to re-read; just proceed.

Don't make a ceremony of it — re-read, then continue.
