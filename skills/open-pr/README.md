# open-pr

Get the current work into a verified pull request, doing only the steps still missing. Unlike `gh pr create`, it treats branch, commit, push and pull request as prerequisites of the target, running each missing one through the skill that owns it and reusing each one already present, a matching open PR included.

```text
$open-pr
├─ on the default branch with uncommitted work   → create-branch
├─ uncommitted work, or HEAD not on the remote   → push (→ commit)
└─ no open PR matches repository/head/base       → gh pr create
```

## When to use

- Your work is anywhere between uncommitted and pushed, and it should end in a pull request.
- A previous run stopped partway, for example after a failed push or a PR creation timeout, and you want it finished without duplicate commits or PRs.
- A PR may already exist for the branch, and you want its URL verified rather than a second PR.

This skill must be invoked explicitly. Use `push` instead when the work should reach a remote branch without a pull request, because `open-pr` always ends in one.

## Before you start

You need a logged-in `gh` that can open pull requests on the target repository, and write access to the branch's remote. This skill requires the `create-branch`, `push` and `commit` skills; to install them on their own:

```bash
npx skills add shihyuho/skills --skill open-pr --skill push --skill commit --skill create-branch -g
```

## Getting started

```text
$open-pr
```

### Options

| Invocation | Effect |
|---|---|
| `$open-pr` | Opens the PR against the target repository's default branch |
| `$open-pr into 3.x` | Uses `3.x` as the base |
| `$open-pr src/login.js` | Commits only that path if it is still uncommitted |

## Prerequisites of the target

The target is one exact repository/head/base triple. Each prerequisite is checked against it:

| Step | Missing when | Runs through | Reused when |
|---|---|---|---|
| Feature branch | You are on the target repository's default branch with uncommitted work | `create-branch`, as a local branch | You are already on a feature branch |
| Commit | The selection still has uncommitted changes | `push`, which invokes `commit` | Nothing in the selection is uncommitted |
| Push | The remote branch is not at HEAD | `push` | The remote branch already holds HEAD |
| Pull request | No open PR matches the target | `gh pr create`, following the repository's PR template | Exactly one open PR matches the target |

On the default branch with commits not yet on the remote, it stops: moving those commits to a feature branch is left to you. Several matching PRs also stop it for a question. The URL comes back only after the PR reads back with the target's repository, head and base, and with the pushed SHA as its head.

## It's working if

- The report lists each step as completed or reused, and running it again right after a success reuses all of them.
- The PR's head commit on GitHub is the SHA the report names.
- Starting on `main` with uncommitted work leaves `main` untouched and puts the PR on a new feature branch.
- No second PR appears for the same branch and base.

## Common questions

**Does `open-pr` commit and push for me?**
Yes, but only what is missing: committed work is pushed as it is, and work already on the remote goes straight to the PR.

**Where did `pr` and `commit-push-pr` go?**
Both changed in #47. `pr` was renamed `open-pr` because its name collided with other skill packs' `pr` skill. `commit-push-pr` was retired because `open-pr` now creates the branch, commits and pushes whatever is missing.

## Limitations

- It stops on the default branch when that branch already holds commits not on the remote.
- An existing matching PR is reused as it is; its title and body are not rewritten.
- It does not merge, request reviewers, or wait for CI.
