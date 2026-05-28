# Explain

Explain any subject top-down — the whole picture first, then drill into the parts the learner picks.

A learning explainer, not an answer dump. It opens with what the subject is and why it matters, hands over one concrete model to hold onto, and maps the subject into a handful of parts — then lets the learner choose what to open and how deep to go. Detail arrives on demand, never front-loaded.

For a sustained, multi-unit course with a syllabus and saved progress, see the sibling [`tutor`](../tutor/) skill.

## Usage

Invoke it on whatever you want explained — a concept, a passage, a file, code, a paper:

- *"explain monads top-down"*
- *"give me the whole-game view of this codebase, then let me drill in"*
- `/tutor:explain <topic, text, or file path>` — explicit invocation in Claude Code

It runs top-down: you get the overview and a map of the parts. For a large or deep subject it then lets you pick which part to open, each drill-down itself top-down; a small one it just explains in a single pass. It stays a single-subject explainer — for a one-shot factual answer, just ask normally.

## Installation

```bash
npx skills add shihyuho/skills --skill explain -g
```
