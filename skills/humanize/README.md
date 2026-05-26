# Humanize

Rewrite text that reads as machine-generated so it reads like a person wrote it — strip the telltale AI tics while keeping every point. Lossless on content; it changes voice, not substance.

The problem here is voice, not length. To shorten instead, see [`tighten`](../tighten/) (keep every point) or [`distil`](../distil/) (cut to the core); when the problem is specialist jargon rather than machine cadence, see [`plain`](../plain/).

## Usage

Ask explicitly to humanize a passage, a file, or text just written:

- *"humanize this, it sounds like ChatGPT wrote it: …"*
- *"make what you just wrote sound less AI"*
- `/rephrase:humanize <text or file path>` — explicit invocation in Claude Code

It acts only on text you point it at, not as unprompted cleanup. The output is the rewritten text followed by a short report of which tics were cut.

## Installation

```bash
npx skills add shihyuho/skills --skill humanize -g
```
