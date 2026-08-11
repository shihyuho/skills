# get-pr-ready

Raise one completed, self-authored pull request to the `engineering:pr-review` quality bar through a bounded peer review-and-fix loop without merging it.

This skill must be invoked explicitly. It requires durable peer-task start/send/wait/read coordination and an authenticated GitHub identity that both owns and can update the pull request.

## Usage

```text
get-pr-ready <PR URL> [--review-session <handle>] [--max-fix-rounds N]
```

When no review task is supplied, the skill creates a dedicated peer task after validating the pull request. Labels under `loop:` expose progress but never drive the loop.

## Installation

```bash
npx skills add shihyuho/skills --skill get-pr-ready -g
```
