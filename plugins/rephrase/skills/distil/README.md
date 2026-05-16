# Distil

Rewrite text down to its core message, dropping whatever is peripheral. Lossy by design — secondary detail is cut on purpose.

To shorten a passage without losing any of its content, see the sibling [`tighten`](../tighten/) skill.

## Usage

Ask explicitly to distil a passage, a file, or text just written:

- *"distil this down to what matters: …"*
- *"cut the fat from what you just wrote"*
- `/rephrase:distil <text or file path>` — explicit invocation in Claude Code

It acts only on text you point it at, not as unprompted cleanup. The output is the rewritten text followed by a short report of what was cut, including which points were dropped.

## Installation

```bash
npx skills add shihyuho/skills --skill distil -g
```
