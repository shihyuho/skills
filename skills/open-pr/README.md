# open-pr

Get the current work into a verified pull request, changing only what does not yet match the work. Unlike `gh pr create`, it reconciles a feature branch, a commit, a push and the pull request against your work: each one that is missing or no longer matches is brought in line, and each one that already matches is reused, an open PR and its description included.

```text
$open-pr
├─ on the default branch with uncommitted work     → create a feature branch
├─ the selection has uncommitted changes           → commit
├─ the remote branch is not at HEAD or not tracked → push
├─ no open PR matches repository/head/base         → gh pr create
└─ the PR's title or body misses part of the diff  → gh pr edit
```

## When to use

- Your work is anywhere between uncommitted and pushed, and it should end in a pull request.
- A previous run stopped partway, for example after a failed push or a PR creation timeout, and you want it finished without duplicate commits or PRs.
- A PR may already exist for the branch, and you want its URL verified rather than a second PR.
- You added commits to a branch whose PR is open, and its title and body should describe them too.

This skill must be invoked explicitly. Use `push` instead when the work should reach a remote branch without a pull request, because `open-pr` always ends in one.

## Before you start

You need a logged-in `gh` that can open and edit pull requests on the target repository, and write access to the branch's remote. To install this skill on its own:

```bash
npx skills add shihyuho/skills --skill open-pr -g
```

## Getting started

```text
$open-pr
```

### Options

| Invocation | Effect |
|---|---|
| `$open-pr` | Opens the PR against the target repository's default branch |
| `$open-pr into <base>` | Uses `<base>` as the base |
| `$open-pr <path>...` | Commits only those paths if they are still uncommitted |

## Reconciling the target

The target is one exact repository/head/base triple. Each prerequisite is read back and compared with your work, and only a mismatch is acted on:

| Step | Matches the work when | Otherwise |
|---|---|---|
| Feature branch | You are on a feature branch | On the default branch with uncommitted work: a new local branch named for the work, started from the base, carrying the work |
| Commit | Nothing in the selection is uncommitted | A commit of only the selection; every other change stays as it was |
| Push | The remote branch holds HEAD, and your branch tracks it | A push of HEAD, read back from the remote, with your branch set to track it |
| Pull request | Exactly one open PR matches the target, with the pushed SHA as its head and a title and body that cover the diff against the base | No match: `gh pr create`, following the repository's PR template. A match whose title or body misses part of the diff: `gh pr edit`, changing only what the diff contradicts or leaves out |

A description covers the diff when its title summarizes the change as a whole and its body accounts for each change, in the PR template's sections. A revision starts from the title and body as they read back from GitHub, so text that is still true stays, whoever wrote it and whenever: your notes, checked boxes and linked issues included.

The URL comes back only after the PR reads back with the target's repository, head and base, the pushed SHA as its head, and the title and body this run left.

## It's working if

- The report lists each step as created, updated or reused, and running it again right after a success reuses all of them.
- The PR's head commit on GitHub is the SHA the report names.
- The PR's title and body describe every commit on the branch, including commits pushed after the PR was opened.
- What you wrote in the PR body, checked boxes and linked issues included, is still there after a revision.
- Starting on the default branch with uncommitted work leaves the default branch untouched and puts the PR on a new feature branch.
- Changes outside the selection are still in your working tree, staged or unstaged as before.
- No second PR appears for the same branch and base.

## Common questions

**Does `open-pr` commit and push for me?**
Yes, but only what does not already match: committed work is pushed as it is, and work already on the remote goes straight to the PR.

**Does it update the description of a PR it reuses?**
Yes, when the branch has commits the title and body do not cover: it revises them with `gh pr edit`. A description that already covers the diff is left untouched.

**Does it still need `create-branch`, `push` and `commit`?**
No. It reconciles each step itself, so it installs and runs alone. For what only those skills do, such as a branch linked to an issue or a commit split by concern, run that skill first; `open-pr` reuses the branch or commit it leaves.

**Where did `pr` and `commit-push-pr` go?**
Both changed in #47. `pr` was renamed `open-pr` because its name collided with other skill packs' `pr` skill. `commit-push-pr` was retired because `open-pr` now creates the branch, commits and pushes whatever is missing.

## Limitations

- It stops on the default branch when that branch already holds commits not on the remote: moving those commits to a feature branch is left to you.
- It stops for a question when several open PRs match the target.
- It checks that the title and body cover the diff, not how well they read; when a PR-writing skill is installed, it writes a new PR's title and body with that skill, inside the repository's PR template when there is one.
- It does not merge, request reviewers, or wait for CI.
