# create-worktree

Start the work in its own Git worktree under `~/code/worktrees` and continue there.

Unlike `git worktree add` from local `HEAD`, or Claude Code's `EnterWorktree` under `.claude/worktrees/`, it puts the worktree at the fixed path `~/code/worktrees/<repo>/<name>` outside the repository, branches from a freshly fetched `origin/<default-branch>`, and resumes the work's existing worktree or branch instead of adding a second.

## When to use

- You want to start a task without disturbing the current checkout, for example while other changes or other agent sessions live there.
- You want to pick up a branch or worktree you started earlier.

This skill must be invoked explicitly. When switching the current checkout is enough, use `create-branch`, because it also links the branch to a GitHub issue and can publish it.

## Before you start

It writes each worktree to `~/code/worktrees/<repo>/<name>`, where `<repo>` is the directory name of the repository's main checkout; a `/` in the branch name nests a folder. Removing a finished worktree is up to you, with `git worktree remove <path>`.

## Getting started

```text
create-worktree add rate limiting to the login endpoint
```

Describe the work to have it name the branch, or pass an existing branch name such as `feat/42-handoff` to resume it. Name a base when the work belongs on another branch, such as a maintained `3.x`.

## Resume or create

It takes the first row that matches:

| What it finds | What it does |
|---|---|
| A worktree already has the branch checked out | Resumes that worktree and keeps its uncommitted work |
| The branch exists locally or on `origin`, with no worktree | Attaches it at the conventional path; stops if local and remote have diverged |
| Nothing | Creates the branch and worktree in one step from `origin/<default-branch>` |

A non-empty directory at the target path that belongs to anything else stops the run rather than sending it to a variant path.

## It's working if

- Every worktree it made sits under `~/code/worktrees/<repo>/`, and `git worktree list` shows one entry per branch.
- Running it again for the same branch reports `reused` and lands in the same directory.
- A new branch starts at the latest `origin/<default-branch>`, or at the base it reported with a reason, and `git rev-parse --abbrev-ref @{upstream}` does not show that base.
- In Claude Code, the session continues inside the worktree.

## Common questions

**I have a branch name and a commit SHA to continue from. What do I pass?** The branch name. `create-worktree` resumes that branch, or the worktree that already has it checked out; it takes no SHA.

## Limitations

- Uncommitted changes in the current checkout stay there; it does not move them into the new worktree.
- It does not remove worktrees.
- The location is fixed to `~/code/worktrees`.
