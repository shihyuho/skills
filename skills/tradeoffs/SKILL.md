---
name: tradeoffs
description: "Recommend a discussed option by weighing its added value against cost, risk, and complexity, with evidence that would change the recommendation."
license: MIT
disable-model-invocation: true
---

# tradeoffs

Recommend which option in the conversation is most worth choosing for the user's goal, constraints, and priorities. `$ARGUMENTS` narrows the discussion or supplies a save path; otherwise consider the whole discussion. Ask for the decision question only when it cannot be inferred from context.

## Recommendation

Compare the options against a common baseline, including keeping the current approach when viable. Weigh incremental value against implementation and ongoing cost, risk, and complexity. Prefer the simplest sufficient, reversible option; broader coverage earns its place through added value. Identify a useful new alternative as a proposal rather than a previously discussed option.

Resolve only unknowns that could change the recommendation, using proportionate read-only checks of supplied artifacts or primary sources. When resolution needs new authority, writes, or disproportionate work, carry the unknown as an explicit assumption and recommend under that uncertainty, or propose the smallest useful validation step. Distinguish evidence from inference; use numeric estimates only when supported and cite researched claims beside their sources.

Lead with the recommendation and decisive reason. Include the comparison and assumptions needed to assess it, then the evidence or threshold that would reverse it. Scale detail and structure to the decision; preserve code, paths, and `file:line` references verbatim.

## Saving

Without a save request, the recommendation completes the task in chat. When saving is requested, use the supplied path or `docs/decisions/<slug>.md` in the current project. Create parent directories as needed and preserve existing files by adding an unused `-2`, `-3`, … suffix before the extension. Report the saved path.
