# Skill Design

A skill's model is its job, its defining constraint and its leading word. Settle it with the user before writing, then open the skill's files with it. This complements `skill-creator` and `writing-for-agents`, which own how the rest of the skill is written.

## Settle the model before the first line

Before writing a `SKILL.md`, or changing what one does, agree four things with the user:

- **Job**: what the skill does, in one sentence.
- **Defining constraint**: the one fact that makes the skill, or the change, behave differently from the obvious default.
- **Leading word**: the term the agent thinks with while running it, such as _tracer bullet_ or _seam_.
- **Composability**: whether skills in this repo, or others already available to the agent, cover the behavior.

A skill with no defining constraint, or one that composes from existing skills, is a workflow or a prompt rather than a skill; keep it as a prompt or an `AGENTS.md` rule.

## Where the model lands

The agreed model has no document of its own in the repo. It opens the files the skill already has:

- `SKILL.md` opens, right under the H1, with the job and the defining constraint as prose in the leading word's terms.
- `README.md` opens with the job sentence and the defining constraint, as [writing-readme.md](writing-readme.md) lays out.
- When an issue tracks the work, it carries the four answers labeled, under a title that opens with `<skill>: `, so a search by skill name finds it.
