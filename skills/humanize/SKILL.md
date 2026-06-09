---
name: humanize
description: Rewrite a piece of text that reads as machine-generated so it sounds like a person wrote it — strip the telltale AI tics (throat-clearing openers, inflated diction, rule-of-three padding, em-dash drama, tacked-on participial clauses) while keeping every point intact. Use when the user explicitly asks to humanize, de-AI, make text sound human, or remove the AI / ChatGPT / Claude voice from a passage, document, or draft they point to, including text just produced in the conversation. Do not trigger as unprompted cleanup of text the user has not asked to change; when the problem is length rather than voice use the tighten or distil skill, and when the problem is specialist jargon rather than machine cadence use the plain skill.
license: MIT
---

# Humanize

Re-examine a passage that reads as machine-generated and rewrite it so it reads like a person wrote it. The points stay; the AI cadence goes. Humanizing is lossless on content — it changes voice, not substance.

## What to humanize

The user identifies the target — pasted text, a file path, or a passage in this conversation. If they invoke the skill without naming one, humanize the last substantial passage you wrote; needing your own output de-AI'd is the usual reason this skill is used. Ask only if the target is genuinely ambiguous.

## Approach

You cannot humanize by find-and-replacing tics one at a time. Swapping "utilize" for "use" leaves the underlying cadence — the relentless symmetry, the throat-clearing, the wind-down clauses — fully intact, and the text still reads as machine-made. Do not patch. Work out what the passage actually says, then re-express it the way a person would say it out loud: uneven sentence lengths, plain verbs, one idea at a time, willing to start a sentence with *And* or *But* and to stop when the point lands.

## Tics to cut

These are what make prose read as AI-generated. Cut them on sight:

- **Throat-clearing openers** — "It's important to note that", "It's worth noting", "At its core", "Needless to say".
- **Empty connective filler** — "Moreover", "Furthermore", "Additionally", "That said", used to glue sentences that need no glue.
- **Conclusion scaffolding** — "In conclusion", "In summary", "Ultimately", "All in all", "When it comes to".
- **Inflated diction** — delve, leverage, utilize, facilitate, foster, robust, comprehensive, seamless, pivotal, underscore, realm, landscape, tapestry, testament. Use the plain word.
- **Symmetric constructions** — "not only X but also Y", "it's not just X, it's Y", paragraphs where every sentence is the same shape.
- **Rule-of-three padding** — triples where one item carries the meaning ("fast, efficient, and scalable").
- **Em-dash drama** — "—" dropped in for a theatrical pause where a comma, full stop, or nothing belongs.
- **Hedge stacking** — "may potentially", "could possibly help to".
- **Tacked-on participial wind-downs** — clauses bolted to a sentence's end: ", ensuring X", ", allowing you to Y", ", making it Z".
- **Reflexive enthusiasm and meta-chatter** — "Great question!", "Absolutely!", "I hope this helps!", restating the prompt before answering.
- **Bold-label bullet soup** — bulleted lists with parallel **Label:** stems where flowing prose would read better.

This list is a guide, not a checklist to satisfy. The goal is prose a person would actually write, not prose with these specific strings removed.

## Preserve

- **Every point.** Humanizing is lossless: each claim, fact, and qualification survives — only voice and cadence change. If a point only existed to pad, that is a length problem; say so and point to the tighten skill rather than dropping it silently.
- **Meaning.** Assert nothing the original did not.
- **The author's intended register.** Formal-but-human stays formal; casual stays casual. You are breaking the machine cadence, not making everything chatty.
- **A professional voice.** Sounding human is not sounding careless. Breaking the cadence must not drag in slang, in-jokes, or throwaway flippancy to seem more relatable — even a casual register stays credible. Lose the AI tics without losing the author's authority.
- **Code, quotes, numbers, names, technical terms.** Reproduce verbatim.

## Output

Give the rewritten text, then a short report of which kinds of tics were cut — so the reader can confirm the voice changed while the substance held.
