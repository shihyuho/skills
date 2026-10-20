# commit

Commit the selected changes, leaving everything outside the selection as found. Unlike `git add -A && git commit`, it treats the selection (an exact path list, the scope settled in the conversation, or the index) as the whole commit, and stops on a requested path with no change instead of widening the selection.

This skill must be invoked explicitly. It writes commit messages with the external `git-commit-co-author` skill.

## Installation

```bash
npx skills add shihyuho/skills --skill commit -g
```
