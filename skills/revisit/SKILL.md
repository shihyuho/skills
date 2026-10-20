---
name: revisit
description: Recover why a ticket or PR exists and what changed, reassess it against the current version, and discuss the smallest complete change if one is still needed.
license: MIT
disable-model-invocation: true
---

# revisit

Recover why a ticket or PR exists and what changed, reassess it against the current version, and discuss the smallest complete change if one is still needed.

Write for a **returning reader**: someone who has forgotten the ticket's background unless the conversation shows otherwise. A reassessment counts only once the returning reader can tell why the ticket was opened, so restore that context before assessing, and make the first assessment's final response stand alone.

## Phases

Resolve the ticket or PR from the supplied number, link, or conversation; when it cannot be read, report that and stop. Then run these phases in order. Each phase follows its skill's own instructions within the boundary given here.

1. **Restore** with `productivity:explain`. Show the returning reader why the ticket or PR exists through one concrete situation: what someone was trying to do, the reported behavior or missing capability, why it mattered, and the intended outcome. Prefer a source-backed example; label an illustrative one as such. Include prior decisions or fixes that explain why it remains open. The phase is complete once the explanation is delivered; move on without waiting for the reader to confirm understanding.
2. **Reassess** against the current version, naming the version checked. For a defect, performance, or security concern, use `mattpocock-skills:diagnosing-bugs`, scoped to investigation: necessary verification tests and their cleanup. For an enhancement or other non-defect concern, check whether the current version already delivers what it asks for. Implementation follows the discussion, with separate user authorization.
3. **Decide**. When the concern still applies and needs a change, discuss the smallest complete change with `skills:grill-minimal`. Otherwise report why action is no longer needed, or what remains unverified; a missing confirmation leaves the concern unverified rather than resolved.

Use `productivity:resolving-user-invoke-skills` when needed and available to load these skills. When a phase's skill is unavailable, run that phase directly within the same boundary.

## First assessment response

The returning reader may read only this final response, so carry forward the essential context and concrete example even when they already appeared in progress messages. Lead with that context, then current-version findings, then the next decision, including when the result is resolved or unverified. Let the concern set the shape and length.

Keep three layers distinct: the original report or proposal, current evidence, and proposed changes. A reproduced behavior may still need a business decision about the desired behavior. Introduce adjacent findings after the original concern is clear, identifying any proposed expansion of scope.

Before sending, check that the returning reader could explain from this response alone why the ticket was opened, what changed since, and what remains to address or decide. State missing history or evidence as a limit. On follow-ups, build on the established context and add only the background the current question needs.
