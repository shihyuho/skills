# create-branch

Put the current work on its own descriptive branch, linked to its issue when there is one.

Unlike `git switch -c`, it treats every run as a possible resume: it finds the work's existing branch, the issue's linked branch or a ref of the same name, and switches to it, and it stops on a name that belongs to other work instead of creating a variant.

## When to use

- You are starting work on a GitHub issue and want its branch created and linked to the issue, or picked up again if it already exists.
- You have changes on the default branch and want them on a descriptively named feature branch.

This skill must be invoked explicitly. When you want the work in its own directory instead of switching the current checkout, use `create-worktree`, because it leaves the current checkout alone and puts the branch in a separate worktree.

## Before you start

Issue-linked branches need a logged-in `gh` with write access to the repository; without an issue, plain `git` is enough.

## Getting started

```text
create-branch 42
```

Pass an issue number or URL to link the branch to that issue, or describe the work to get a branch without one. Say "local only" to keep it off the remote, or name a base such as `release/3.x` to start from a remote branch other than the default.

## Resume or create

Each run first asks whether the work already has its branch:

| What it finds | What it does |
|---|---|
| The issue links exactly one branch | Resumes it under its existing name, even if the issue title has changed since |
| The issue links several branches | Stops and lists them for you to pick |
| The name exists but belongs to other work | Stops and reports the conflicting ref |
| You are already on this work's branch | Reports it as reused |
| Nothing matches | Creates it: on the remote and linked to the issue when you approved publishing, otherwise local |

A branch started from a remote base does not take that base as its upstream, so a later bare `git push` or `git pull` never targets `main` by accident.

## It's working if

- Running it again for the same issue reports `reused` and leaves you on the same branch.
- When you approved publishing, the issue's Development section on GitHub lists the branch.
- `git rev-parse --abbrev-ref @{upstream}` shows nothing, or `origin/<branch>` once published, never the base.
- It asks about publishing only when you have not already said.

## Limitations

- It carries uncommitted changes but does not move commits already on the default branch.
- It stops at the branch: committing, pushing beyond the branch's own publication, and opening a pull request belong to other skills.
- Issue linking needs GitHub.
