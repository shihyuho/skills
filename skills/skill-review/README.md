# skill-review

Review a skill using writing-for-agents and skill-creator, and optionally apply fixes.

This skill must be invoked explicitly.

`/writing-for-agents` and `/skill-creator:skill-creator` are the sources of truth for review criteria. This skill coordinates the target, review mode and result without maintaining another rubric.

Review is read-only by default. With `--fix`, it applies corrections within the requested scope, preserves unrelated work, and reports verification and unresolved findings. Missing source coverage remains explicit.

Eval scenarios in `evals/evals.json` cover coordination and scope; the source skills own the authoring criteria.

## Installation

```bash
npx skills add shihyuho/skills --skill skill-review -g
```
