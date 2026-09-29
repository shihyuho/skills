---
name: revisit
description: Recover the context of a ticket or PR, assess what still applies to the current version, and discuss the smallest complete change if needed.
license: MIT
disable-model-invocation: true
---

# revisit

Help a returning reader recover why a ticket or PR exists, how it reached its current state, and what remains to address or decide. Assume its background has been forgotten unless the conversation establishes otherwise.

Resolve the ticket or PR from the supplied number, link, or conversation, then invoke these skills in order:

1. `productivity:explain` to restore that context before reassessment. Give the reader a brief explanation tracing one concrete situation: what someone was trying to do, the reported behavior or missing capability, why it mattered, and the intended outcome. Explain the terms needed to follow that trace. Include prior decisions or fixes when they explain why this ticket remains open. Prefer a source-backed example; label illustrative examples and gaps in the available history. This step is complete when the explanation has been delivered, without requiring a separate acknowledgment of understanding.
2. `mattpocock-skills:diagnosing-bugs` to reassess that concern against the current version, identifying the version checked. Choose verification appropriate to the ticket's nature (such as a defect, performance, security, or enhancement), explicitly justifying any inapplicable diagnosis phases. Scope this invocation to investigation, including necessary verification tests and cleanup; implementation follows the discussion, with separate user authorization.
3. If the concern remains applicable and requires a change, `skills:grill-minimal` to discuss the smallest complete change, including its call to `grill-with-docs` for that discussion. Otherwise, report why action is no longer needed or what remains unverified; lack of confirming evidence alone does not establish resolution.

Use each skill's own instructions within these phase boundaries. If a required skill cannot be resolved, report the missing dependency and stop the affected phase.

## First assessment response

Make the first assessment's final response stand alone: carry forward the essential context and concrete example even if they appeared in progress messages. Present that explanation before current-version findings and the next decision, including when the result is resolved or unverified. Use the shape and length the concern needs rather than a fixed report template.

Keep the original report or proposal, current evidence, and proposed changes distinct. A reproduced behavior may still need a business decision about the desired behavior. Introduce adjacent findings after the original concern is clear, identifying any proposed expansion of scope.

Before sending, check whether a reader of only this response can explain why the ticket was opened, what changed since then, and what remains to address or decide. State missing history or evidence as a limit rather than filling it in. On follow-ups, build on the established context and add only the background needed for the current question.
