# skill-review

Review a skill against writing-for-agents, skill-creator and its repository's guidance, applying the warranted corrections with `--fix`. Unlike running an authoring skill's review directly, which tends to act on every finding it raises, it gives each finding a verdict against the skill's own evidence and fixes only what earns a fix.

## When to use

- A skill was just written or changed, and you want it checked before it ships.
- An existing skill predates the repository's current guidance and needs to catch up.
- You want an authoring guide's opinion on a skill without letting the agent reshape the skill to fit it.

This skill must be invoked explicitly. To build a skill or iterate on one with eval runs, use `skill-creator` directly instead, because skill-review takes only its criteria.

## Before you start

The criteria come from two skills installed in the same agent:

- `writing-for-agents`: `claude plugin install mattpocock-skills@claude-plugins-official`
- `skill-creator`: `claude plugin install skill-creator@claude-plugins-official`

With either missing, the review still runs and is reported as partial.

## Getting started

```text
/skill-review skills/<skill>
```

In Codex, use `$skill-review skills/<skill>`. With no target, it reviews the skill the conversation is about.

### Options

| Option | Effect |
| --- | --- |
| `--fix` | Apply the fix verdicts to the skill and to whatever the repository requires to change with it, such as the root `README.md` catalog line. |

## Verdicts

An authoring guide is written to shape a skill, so its findings read as orders: applied wholesale, they delete the "redundant" exception that was the point of a paragraph, or push every skill toward the same template. skill-review treats each finding as a claim and settles it against the skill's own files, the repository's guidance and the environment:

| Verdict | When | With `--fix` |
| --- | --- | --- |
| fix | The evidence confirms the problem. | Applied. |
| reject | The evidence contradicts it. | Left as is, with the reason. |
| defer | The evidence can't settle it, the sources disagree with nothing in the repository to decide, or it would change the skill's job, invocation mode or what it may do and you haven't authorized that change. | Left for you to decide. |

## It's working if

- Every finding in the report carries a verdict and the evidence behind it, rejected and deferred ones included.
- A review without `--fix` leaves `git status` unchanged.
- Unless you authorized it, a finding that would change what the skill does appears as a defer, not as an edit in the diff.
- A report missing a source names it and says the review is partial.

## Common questions

**Why load two external skills instead of carrying its own rubric?**

[#35](https://github.com/shihyuho/skills/issues/35) proposed a standalone review contract instead. The criteria stayed in the source skills so they improve where they are maintained; the cost is loading both on every run. What skill-review adds is the verdict.

## Limitations

- It reads the skill against criteria; it doesn't run the skill or its evals, so behavior stays untested until you do.
- A criterion that neither source nor the repository's guidance carries goes unchecked.
- With `--fix`, the changes stay uncommitted.
