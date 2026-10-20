# commit

Commit the selected changes, leaving everything outside the selection as found. Unlike `git add -A && git commit`, it treats the selection as the whole commit: a requested path with no change stops the run instead of widening the selection, and staged or unstaged work outside the selection ends exactly as it started.

## When to use

- You want part of a dirty working tree committed (a few paths, the fix just discussed, or what is already staged) without disturbing the rest.
- You want the whole working tree committed as one cohesive commit, with a question first when it mixes clearly unrelated concerns.

This skill must be invoked explicitly. When the work should also reach a remote branch or a pull request, use `push` or `open-pr` instead, because they commit whatever is still uncommitted and then publish it.

## Before you start

To install this skill on its own:

```bash
npx skills add shihyuho/skills --skill commit -g
```

Where the `git-commit-co-author` skill from [softleader/agent-skills](https://github.com/softleader/agent-skills) is installed, commits also carry its AI attribution trailer.

## Getting started

```text
$commit
```

### Options

| Invocation | What gets committed |
|---|---|
| `$commit` | The scope already agreed in the conversation, otherwise all current changes |
| `$commit <path>...` | Exactly those paths |
| `$commit staged only` | The current index, without restaging working-tree edits |
| `$commit split by concern` | One commit per concern in the selection, without asking first |

## The selection

The selection is decided once, in this order:

1. Paths named in the invocation, taken literally: `:(glob)*.txt` is a filename, not a pattern.
2. The scope already agreed in the conversation, such as "only the login fix".
3. All current changes.

Everything outside the selection stays out of the commit and stays as it was, including changes that were already staged. Cohesion is judged inside the selection only: one concern becomes one commit even across many files, and clearly unrelated concerns get a question about splitting.

## It's working if

- `git status` after the commit shows the same unrelated staged and unstaged changes as before.
- `git show --stat` on the new commit lists only the selected paths.
- A mistyped or unchanged path stops the run before anything is staged.
- The report names the commit SHA and the selection it committed.

## Limitations

- It commits on the current branch, the default branch included.
- A hunk-level selection whose ownership is unclear stops for a question rather than widening to whole files.
- When a commit hook fails, it reports the failure and leaves the work uncommitted.
