# Tutor

Turn Claude into a learning onramp accelerator instead of an answer machine.

A skill for sustained, structured learning: state a goal, get a course; walk through one unit at a time; let the learner's questions and stuck points feed back into pace and depth. The boundary is honest — what the skill produces is *low-friction scaffolding* that gets the learner reading the authoritative source, not a substitute for it.

## When It Triggers

- **"I want to systematically learn X" / "teach me Y" / "be my tutor for Z"** — the canonical goal-anchored prompt.
- **"Plan a course / make a syllabus on X"** — explicit course-design request.
- **"I have <duration> until <exam>, help me prep"** — time-boxed study plan.
- **Upload of study material with a request for guided reading** — PDF / EPUB / notes anchored learning.
- **Mentions of *tutor*, *syllabus*, *curriculum*, *coursework*, *家教*, *學習路徑*** — explicit cue.

Skipped for one-shot factual Q&A, code-context explanations, or task automation.

## Why This Exists

Two failure modes most AI learning sessions fall into:

1. **Cold textbook.** The learner faces a domain authority before they have any semantic grounding — too steep, and they bounce.
2. **Ad-hoc Q&A drift.** The learner asks isolated questions, forgets them, and never builds a structured map of the domain.

Tutor mode aims at the gap: AI as a *scaffolding generator* that lets the learner reach concepts in their Zone of Proximal Development, then nominates authoritative sources for them to pressure-test against on their own.

## Installation

```bash
npx skills add shihyuho/skills --skill tutor -g
```

Then in any Claude Code session, state a learning goal — Tutor mode activates and runs the consultative interview.

## Lifecycle

```text
Stage 1: Consult & anchor   → diagnose goal, time budget, level, format, sources
Stage 2: Generate syllabus  → ordered units the learner edits and approves
Stage 3: Run a unit         → read in chunks → capture highlights → recap
Stage 4: Adjust & verify    → update profile, nominate authoritative sources, update dashboard
```

Each course gets its own vault — `./<course-slug>/` by default — with `syllabus.md`, `learner-profile.md`, `whiteboard.md`, an `index.md` dashboard, and one `lessons/lesson-NN.md` per unit. The vault is read at the start of every session so the course adapts as it goes.

## Course Vault

```text
<course-slug>/
├── index.md             # one-screen dashboard: goal, current unit, next action
├── syllabus.md          # negotiated course outline
├── learner-profile.md   # background, preferences, stuck points
├── whiteboard.md        # learner-flagged snippets, verbatim
└── lessons/
    └── lesson-NN.md     # one file per unit (reading + Q&A + recap)
```

## Teaching Patterns

- **Scaffold via the familiar.** Abstract concepts get framed through cultural texts the learner already knows (film, novels, daily-used systems), then the frame is removed.
- **Two-stage learning.** Stage 1 is low-friction exploration with the skill. Stage 2 is high-rigor verification *away* from the skill, against authoritative sources — always nominated explicitly.
- **ZPD pacing.** Gap too wide → insert a stepping stone. Too narrow → raise depth.

## Boundaries

- **Hypothesis-grade output.** Every unit closes with a verification reminder pointing at authoritative sources. Tutor output is for getting started, not for citing.
- **Deep-water domains.** Frontier research and very recent regulation are flagged explicitly; the skill nominates Stage 2 sources rather than fabricating coverage.
- **Not a Q&A bot.** If the user just wants a single answer, Tutor mode steps aside.

## Credits

Concept and philosophy distilled from `docs/ideas/tutor/` — particularly the *learning onramp accelerator* framing and the two-stage learning model (low-friction exploration → high-rigor verification).
