# LGTM

When you approve something Claude put up for review — a spec, a plan, a diff, edited code — by saying **lgtm** (or "looks good", "go ahead"), Claude re-reads those files from disk before taking the next step.

Why it matters: while you were reviewing, you may have edited the files yourself. Without re-reading, Claude builds the next step on a stale in-context copy and silently drops your edits. `lgtm` closes that gap.

## Installation

```bash
npx skills add shihyuho/skills --skill lgtm -g
```
