# Skill Design

Design skills around a clear mental model, a goal, and observable completion conditions. These principles complement `skill-creator` and `writing-for-agents`: give the model enough direction to integrate different tools and workflows while preserving the user's expected outcome.

## Principles

1. **Lead with the outcome.** State what the skill accomplishes, who owns each responsibility, and what counts as complete or blocked. Use these expectations to integrate existing progress and interchangeable dependencies. Let the model choose routine operations that satisfy them.

2. **Put precision at consequential boundaries.** Specify authorization, interfaces, required state transitions, and ordering dependencies. Keep exact commands or formats where correctness or interoperability depends on them. For ordinary implementation choices, give the model the purpose and constraints needed to adapt to its environment.

3. **Disclose references by need.** Keep the framework and shared completion conditions in the main file; load specialized rules when their branch applies. Moving text to a file every path immediately reads saves no context. Refer to a dependency's own contract instead of reproducing its procedure.

4. **Preserve capabilities when simplifying.** Before removing a rule, reference, or helper, identify the supported behavior it carries and where that behavior will live. Preserve fallbacks and existing verification coverage. Retiring a supported capability is a separate scope decision that needs the user's agreement.

5. **Reuse evidence while it applies.** Refresh when evidence is missing, conflicts, or no longer matches the relevant execution context, or when the decision requires a fresh observation. A skill invocation or pass boundary alone does not invalidate evidence. Use established context without adding a routine proof that nothing changed.

6. **Leave no tombstones.** When an edit retires a behavior, remove its mentions with it, in the skill and its README alike. A sentence that denies what only the edit history contains, such as "does not rewrite the PR body" after body maintenance was dropped, an example citing a retired rule, or "once" stressing a frequency no reader expected otherwise, puts the retired idea back into the reader's context. Keep a negation that guards a behavior the reader or model would otherwise default to. Development history belongs in issues and PRs.

7. **Judge improvements by behavior.** Check completion, meaningful boundaries, and preserved capabilities. Retain deterministic helpers where they provide reliable, testable behavior; expose their necessary interface. Use focused behavioral evaluations and existing relevant tests to assess changes. Compare token and runtime costs across the actual execution path, including loaded references and repeated work.

8. **Settle the model before the first line.** Before writing a `SKILL.md`, or changing what one does, agree four things with the user:

   - **Job**: what the skill does, in one sentence, answering a real situation where its absence stalled the work: what was asked, what the agent did, and what was expected instead. "It would be nicer with it" is not one.
   - **Defining constraint**: the one fact that makes the skill, or the change, behave differently from the obvious default.
   - **Leading word**: the term the agent thinks with while running it, such as _tracer bullet_ or _seam_.
   - **Composability**: whether skills in this repo, or others already available to the agent, cover the behavior.

   A skill with no defining constraint, or one that composes from existing skills, is a workflow or a prompt rather than a skill; keep it as a prompt or an `AGENTS.md` rule.

   The agreed model has no document of its own in the repo. `SKILL.md` opens, right under the H1, with the job and the defining constraint as prose in the leading word's terms; `README.md` opens with them as [writing-readme.md](writing-readme.md) lays out. When an issue tracks the work, it carries the four answers labeled, under a title that opens with `<skill>: `, so a search by skill name finds it.

9. **Point at a dependency only where its absence makes output wrong.** A hard dependency, one the output is wrong without (a tracker to publish to, a label vocabulary to apply), gets one explicit line that names it and says what to do when it is missing. A soft dependency, one the output is only duller without (a glossary, ADRs in the area), is referenced in plain prose that assumes it may be absent, and the skill runs the same way either way. The pointer runs one way: a skill names what it loads, never what loads it. A standard that other skills read (a test-design standard a design guide pulls in) says nothing about those consumers in its `SKILL.md` or `README.md`; each consumer names the standard from its own side. A neighbour the README's `When to use` offers as the thing to use instead is an alternative for the reader, not a consumer pointer.
