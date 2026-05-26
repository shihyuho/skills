---
name: tighten
description: Rewrite a piece of verbose text so it conveys exactly the same meaning in fewer words — every point in the original survives, and the result replaces the text rather than summarising it. Use when the user explicitly asks to tighten, shorten, condense, or compress a passage, document, message, or draft they point to, including text just produced in the conversation, and wants nothing dropped. Do not trigger as unprompted cleanup of text the user has not asked to change; when the user is willing to drop peripheral content to reach a core message, use the distil skill instead.
license: MIT
---

# Tighten

Re-examine a passage and rewrite it to carry the same meaning in fewer words. Nothing is dropped — tightening is lossless.

## What to tighten

The user identifies the target — pasted text, a file path, or a passage in this conversation. If they invoke the skill without naming one, tighten the last substantial passage you wrote; needing your own output tightened is the usual reason this skill is used. Ask only if the target is genuinely ambiguous.

## Approach

A verbose passage does not get tighter by editing in place. Each editing pass tends to add a caveat or a transition and remove nothing, so length compounds. Do not patch the existing wording. Work out what the passage actually says, then re-express that from scratch in the fewest words that still land it.

## Preserve

- **Every point.** Tightening is lossless: each distinct claim, fact, and qualification the original made must survive — only wording and structure change. If a point cannot stay without bloat, that is a sign the user wants the distil skill instead; say so rather than dropping it silently.
- **Meaning.** Assert nothing the original did not.
- **Register and tone.** Formal stays formal, casual stays casual; only the padding goes.
- **Code, quotes, numbers, names, technical terms.** Reproduce verbatim.

Do not chase a percentage. "As tight as it can be" is the target; a fixed ratio just trades padding for over-cutting.

When the rewrite is done, read the original once more and confirm no point was lost or altered. Adjust if it was.

## Output

Give the rewritten text, then a short report of what kinds of filler were cut — it lets the reader confirm that only padding went, nothing of substance.
