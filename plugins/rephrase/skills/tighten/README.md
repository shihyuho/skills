# Tighten

Rewrite verbose text so it carries the same meaning in fewer words — losslessly. Every point in the original survives; only wording and structure change.

To cut a passage down to a core message instead, dropping the peripheral, see the sibling [`distil`](../distil/) skill.

## Usage

Ask explicitly to tighten a passage, a file, or text just written:

- *"tighten this paragraph, keep every point: …"*
- *"shorten what you just wrote without losing anything"*
- `/rephrase:tighten <text or file path>` — explicit invocation in Claude Code

It acts only on text you point it at, not as unprompted cleanup. The output is the rewritten text followed by a short report of what filler was cut.

## Installation

```bash
npx skills add shihyuho/skills --skill tighten -g
```
