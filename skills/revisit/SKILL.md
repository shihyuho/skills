---
name: revisit
description: Revisit a ticket or PR, assess its concern against the current version, and discuss the smallest complete change if still needed.
license: MIT
disable-model-invocation: true
---

# revisit

Resolve the ticket or PR from the supplied number, link, or conversation, then invoke these skills in order:

1. `productivity:explain` to explain the ticket's original concern, intended outcome, and discussion.
2. `mattpocock-skills:diagnosing-bugs` to reassess that concern against the current version, identifying the version checked. Choose verification appropriate to the ticket's nature (such as a defect, performance, security, or enhancement), explicitly justifying any inapplicable diagnosis phases. Scope this invocation to investigation, including necessary verification tests and cleanup; implementation follows the discussion, with separate user authorization.
3. If the concern remains applicable and requires a change, `skills:grill-minimal` to discuss the smallest complete change, including its call to `grill-with-docs` for that discussion. Otherwise, report why action is no longer needed or what remains unverified; lack of confirming evidence alone does not establish resolution.

Use each skill's own instructions within these phase boundaries. If a required skill cannot be resolved, report the missing dependency and stop the affected phase.
