# Plain

Rewrite jargon-heavy or convoluted text into plain language a non-specialist can follow — unpack the jargon, untangle the sentences, keep every point, and stay precise. Clear is not the same as vague.

The problem here is readability, not length. To shorten instead, see [`tighten`](../tighten/) (keep every point) or [`distil`](../distil/) (cut to the core); when the problem is machine-generated cadence rather than specialist jargon, see [`humanize`](../humanize/).

## Usage

Ask explicitly to put a passage, a file, or text just written into plain language:

- *"put this in plain language: …"*
- *"explain what you just wrote without the jargon"*
- `/rephrase:plain <text or file path>` — explicit invocation in Claude Code

It acts only on text you point it at, not as unprompted cleanup. The output is the rewritten text followed by a short report of what was simplified and which terms were kept and defined.

## Installation

```bash
npx skills add shihyuho/skills --skill plain -g
```
