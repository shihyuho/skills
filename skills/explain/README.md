# Explain

Explain any subject top-down so you actually understand it — the whole picture first, then drill into the parts you pick.

A learning explainer, not an answer dump. The aim is that you come away understanding — holding a working mental model — not that a polished explanation gets delivered. It starts from what you already know, opens with what the subject is and why it matters, and anchors each new idea to something familiar — then maps the subject into a handful of parts and lets you choose what to open and how deep to go. Detail arrives on demand, never front-loaded; and if a part doesn't land, it comes at it from another angle rather than repeating itself.

## Usage

Invoke it on whatever you want explained — a concept, a passage, a file, code, a paper:

- *"explain monads top-down"*
- *"give me the whole-game view of this codebase, then let me drill in"*
- `/skills:explain <topic, text, or file path>` — explicit invocation in Claude Code

It runs top-down: you get the overview and a map of the parts. For a large or deep subject it then lets you pick which part to open, each drill-down itself top-down; a small one it just explains in a single pass. It stays a single-subject explainer — for a one-shot factual answer, just ask normally.

## Installation

```bash
npx skills add shihyuho/skills --skill explain -g
```
