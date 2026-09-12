# skill-review

Review a skill using writing-for-agents and skill-creator, and optionally apply fixes.

This skill must be invoked explicitly.

`/writing-for-agents` and `/skill-creator:skill-creator` are the sources of truth for review criteria. This skill coordinates the target, review mode and result without maintaining another rubric.

Review is read-only by default. With `--fix`, it assesses each finding and fixes the points it agrees are warranted within the requested scope, explaining rejected or deferred findings and reporting verification. Missing source coverage remains explicit.

Eval scenarios in `evals/evals.json` cover coordination and scope; the source skills own the authoring criteria.

## Installation

```bash
npx skills add shihyuho/skills --skill skill-review -g
```
