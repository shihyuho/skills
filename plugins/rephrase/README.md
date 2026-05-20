# rephrase

Re-express a passage from scratch — four skills, for four different intentions, along two axes: how long it is, and how it reads.

AI-drafted prose tends to run long and read like a machine wrote it, and revising it over a few rounds only makes it worse: each pass adds a caveat or a transition and removes nothing. Every skill here does a reset — it works out what the text means and re-expresses it from scratch, rather than patching what is already there.

## Skills

**Length** — change how much there is:

| Skill | What it does | Drops content? |
|---|---|---|
| [`tighten`](skills/tighten/) | Rewrite shorter with **every point kept** — same meaning, fewer words. | No — lossless |
| [`distil`](skills/distil/) | Rewrite down to the **core message**, cutting what is peripheral. | Yes — by design |

**Readability** — change how it reads, not how long it is:

| Skill | What it does | Drops content? |
|---|---|---|
| [`humanize`](skills/humanize/) | Strip the telltale **AI tics** so it reads like a person wrote it. | No — lossless |
| [`plain`](skills/plain/) | Strip **jargon** and untangle syntax so a non-specialist can follow. | No — lossless |

Reach for `tighten` when the text says the right things at the wrong length, `distil` when it also says too much, `humanize` when it sounds machine-made, and `plain` when it is right but hard to follow.

All are invoked explicitly — they act on a passage you point them at, not as unprompted cleanup. In Claude Code: `/rephrase:tighten`, `/rephrase:distil`, `/rephrase:humanize`, or `/rephrase:plain`.

## Installation

Install either skill on its own:

```bash
npx skills add shihyuho/skills --skill tighten -g
npx skills add shihyuho/skills --skill distil -g
npx skills add shihyuho/skills --skill humanize -g
npx skills add shihyuho/skills --skill plain -g
```

Or install both as a Claude Code plugin:

```bash
/plugin marketplace add shihyuho/skills
/plugin install rephrase@shihyuho-skills
```
