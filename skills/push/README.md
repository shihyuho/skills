# push

Push the current work to one verified destination, committing it first only if it is still uncommitted. Unlike `git push`, it commits missing work through `commit`, resolves the repository behind the remote's effective push URL and that repository's live default ref, asks before a default-branch push, and reports success only after the destination ref reads back as the intended SHA.

This skill must be invoked explicitly. It requires the `commit` skill.

## Installation

```bash
npx skills add shihyuho/skills --skill push --skill commit -g
```
