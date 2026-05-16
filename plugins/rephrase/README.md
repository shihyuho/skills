# rephrase

Re-express verbose text more tightly — two skills, for two different intentions.

AI-drafted prose tends to run long, and revising it over a few rounds only makes it worse: each pass adds a caveat or a transition and removes nothing. Both skills here do a reset — they work out what the text means and re-express it from scratch, rather than patching what is already there.

## Skills

| Skill | What it does | Drops content? |
|---|---|---|
| [`tighten`](skills/tighten/) | Rewrite shorter with **every point kept** — same meaning, fewer words. | No — lossless |
| [`distil`](skills/distil/) | Rewrite down to the **core message**, cutting what is peripheral. | Yes — by design |

Reach for `tighten` when the text says the right things at the wrong length. Reach for `distil` when it also says too much.

Both are invoked explicitly — they act on a passage you point them at, not as unprompted cleanup. In Claude Code: `/rephrase:tighten` or `/rephrase:distil`.

## Installation

Install either skill on its own:

```bash
npx skills add shihyuho/skills --skill tighten -g
npx skills add shihyuho/skills --skill distil -g
```

Or install both as a Claude Code plugin:

```bash
/plugin marketplace add shihyuho/skills
/plugin install rephrase@shihyuho-skills
```
