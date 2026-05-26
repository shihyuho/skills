---
name: distil
description: Rewrite a piece of text down to its core message, dropping whatever is peripheral to it — the result is the text itself rewritten shorter, not a summary written about it. Use when the user explicitly asks to distil, cut to the essentials, trim the fat, or strip a passage, document, or draft down to what matters, and is willing to lose secondary detail. Do not trigger as unprompted cleanup of text the user has not asked to change; when the user wants the text shorter but every point kept, use the tighten skill instead.
license: MIT
---

# Distil

Re-examine a passage and rewrite it down to its core message. Peripheral content is dropped on purpose — distilling is lossy by design.

## What to distil

The user identifies the target — pasted text, a file path, or a passage in this conversation. If they invoke the skill without naming one, distil the last substantial passage you wrote. Ask only if the target is genuinely ambiguous.

## Approach

A verbose passage does not get tighter by editing in place. Each editing pass tends to add a caveat or a transition and remove nothing, so length compounds. Do not patch the existing wording. Work out what the passage actually says, separate the core message from what merely supports or decorates it, then re-express the core from scratch in the fewest words that still land it.

Decide what counts as peripheral yourself and cut it directly, without pausing to confirm each cut — being trusted with that judgement is the point of this skill. Peripheral means secondary examples, asides, caveats that do not change the conclusion, and background the reader does not need; the core is what the passage would be useless without.

## Preserve

- **The core message.** Whatever the passage fundamentally exists to say must survive intact and unweakened.
- **Meaning.** What you keep must mean what the original meant — assert nothing it did not.
- **Register and tone.** Formal stays formal, casual stays casual.
- **Code, quotes, numbers, names, technical terms.** Reproduce verbatim wherever kept.

Do not chase a percentage. Distil to what matters and stop; a fixed ratio just forces arbitrary cuts or padding.

When the rewrite is done, read the original once more and confirm the core survived and nothing kept was distorted. Adjust if so.

## Output

Give the rewritten text, then a short report:

- what kinds of filler were cut;
- which actual points were dropped as peripheral — one line each, so the reader can catch a cut that went too deep.
