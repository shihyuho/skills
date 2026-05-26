---
name: plain
description: Rewrite a piece of jargon-heavy or convoluted text into plain language a non-specialist can follow — unpack the jargon, break up tangled sentences, and cut academese and business-speak while keeping every point and staying precise. Use when the user explicitly asks to put something in plain language, simplify the wording, make a passage accessible, explain it like a human, or strip jargon from a document or draft they point to, including text just produced in the conversation. Do not trigger as unprompted cleanup of text the user has not asked to change; when the problem is length use the tighten or distil skill, and when the problem is machine-generated cadence rather than specialist jargon use the humanize skill.
license: MIT
---

# Plain

Re-examine a passage that is hard to follow and rewrite it in plain language a non-specialist can read. Every point stays; what goes is the jargon, the abstraction, and the tangled syntax that hid the meaning. Plain language is meaning-preserving, not meaning-losing — clear is not the same as vague.

## What to put in plain language

The user identifies the target — pasted text, a file path, or a passage in this conversation. If they invoke the skill without naming one, work on the last substantial passage you wrote. Ask only if the target is genuinely ambiguous.

Aim for a smart reader who is *not* in this field. If the user names a specific audience, write for that one instead.

## Approach

A convoluted passage does not get clearer by softening a word here and there — the tangled sentence structure and buried actors survive the edit. Do not patch. Work out what the passage is actually saying underneath the jargon, then say it the way you would explain it to a sharp colleague from outside the field.

Concretely:

- **Unpack jargon and acronyms** — name the thing in ordinary words; expand an acronym on first use. Keep a technical term only when it is load-bearing, and define it briefly the first time.
- **Undo nominalizations** — "make a decision" → "decide", "the implementation of X" → "implementing X".
- **Name the actor** — turn hidden-subject passives ("a review was conducted") into who did what ("we reviewed it").
- **Shorten the words** — pick the short common word over the long Latinate one where it carries the same meaning.
- **Split tangled sentences** — break a sentence with stacked subordinate clauses into two or three plain ones.
- **Ground the abstract** — replace an abstract noun with the concrete thing it stands for where that lands better.

## Preserve

- **Every point.** This is not distilling: keep all the content. Unpacking a term may cost a few extra words, and that is fine — plain is not measured by word count.
- **Precision.** Plain is not vague. Do not trade away technical accuracy or necessary caveats to sound simpler.
- **Necessary technical terms.** Define them, do not delete them; some terms are the precise word and have no plain equivalent.
- **Register.** Plain is not the same as casual — keep the formality the context calls for.
- **Code, quotes, numbers, names.** Reproduce verbatim.

## Output

Give the rewritten text, then a short report: which jargon and tangled structures were simplified, and any technical term you kept and defined rather than replaced.
