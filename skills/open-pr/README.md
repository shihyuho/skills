# open-pr

Get the current work into a verified pull request, doing only the steps still missing. Unlike `gh pr create`, it treats branch, commit, push and pull request as prerequisites: each missing one runs through the skill that owns it, and each one already present, including a matching open PR, is verified and reused.

This skill must be invoked explicitly. It requires the `create-branch`, `push`, and `commit` skills.

## Installation

```bash
npx skills add shihyuho/skills --skill open-pr --skill push --skill commit --skill create-branch -g
```
