# kickoff

Two go-signals for handing reviewed work back to Claude — one light, one heavy.

When you finish reviewing something Claude proposed, the risk is the same both times: Claude carries on from the version in its context, not the version on disk — and during review you may have edited that version yourself. Both skills here re-sync from disk at that handoff. `lgtm` is the bare gesture; `kickoff` is the full plan-to-build ritual.

## Skills

| Skill | What it does | Scope |
|---|---|---|
| [`lgtm`](skills/lgtm/) | Re-read from disk every file that was under review, then continue with the next step. | Any approval, any artifact |
| [`kickoff`](skills/kickoff/) | Re-read a reviewed SPEC/PLAN, then build it while keeping a running implementation-notes file (Markdown or HTML) of design decisions, deviations, tradeoffs, and open questions. | One reviewed plan, a full build |

Reach for `lgtm` to approve any single step and keep going. Say `開工` to trigger `kickoff` when the thing approved is a whole plan you want built.

## Installation

Install either skill on its own:

```bash
npx skills add shihyuho/skills --skill lgtm -g
npx skills add shihyuho/skills --skill kickoff -g
```

Or install both as a Claude Code plugin:

```bash
/plugin marketplace add shihyuho/skills
/plugin install kickoff@shihyuho-skills
```
