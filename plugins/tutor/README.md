# tutor

Turn Claude into a learning on-ramp accelerator instead of an answer machine — two skills, for two depths of learning.

A cold textbook is too steep and ad-hoc Q&A drifts. What gets a learner into a new domain is *scaffolding*: a frame rough enough to build on fast, honest enough to point back at the real source. Both skills here generate that scaffold — one sized to a single subject, one to a whole domain.

## Skills

| Skill | What it does | Scope |
|---|---|---|
| [`explain`](skills/explain/) | Explain one subject top-down — whole picture, a working model, a map of its parts, then drill in wherever the learner points. | One subject, one sitting |
| [`course`](skills/course/) | Run a full guided course — consultative diagnosis, a custom syllabus, unit-by-unit lessons, progress kept in a course vault. | A whole domain, many sessions |

Reach for `explain` to understand *one thing* fast. Reach for `course` to study *a domain* over time.

Both rest on the same two-stage philosophy: Stage 1 is low-friction exploration *with* the skill; Stage 2 is high-rigor verification against authoritative sources, *away* from it. The skill always names the Stage 2 target — scaffolding is for getting started, not for citing.

## Installation

Install either skill on its own:

```bash
npx skills add shihyuho/skills --skill explain -g
npx skills add shihyuho/skills --skill course -g
```

Or install both as a Claude Code plugin:

```bash
/plugin marketplace add shihyuho/skills
/plugin install tutor@shihyuho-skills
```

## Credits

Concept and philosophy distilled from `docs/ideas/tutor/` — the *learning onramp accelerator* framing and the two-stage model (low-friction exploration → high-rigor verification).
