---
name: create-worktree
description: "Create or resume isolated work in a descriptive Git worktree, including an existing Planning Baseline branch."
license: MIT
disable-model-invocation: true
---

# create-worktree

## Invocation input

`$ARGUMENTS` below means the arguments supplied with the user's explicit invocation. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.


## Context

- Current branch: !`git branch --show-current`
- Current git status: !`git status --short`
- Existing worktrees: !`git worktree list`
- Recent commits: !`git log --oneline -10`

## Your task

Create or resume a worktree for the work at hand and continue in it. `$ARGUMENTS` may include a Baseline Pointer: an exact branch and full commit SHA that the caller already verified against its ticket.

**Name.** A Planning Baseline branch is the exact `<name>`; never derive a replacement. Otherwise derive `<name>` from what `$ARGUMENTS` describes — treat it as a description of the work, not as a literal name, unless it already reads like a slug. Without one, derive it from the task this session is about to start: what the user just asked for, the plan under discussion, or the uncommitted changes in Context. Keep `<name>` short, ASCII, and valid as a branch name (`git check-ref-format --branch <name>`), e.g. `feat/create-worktree-command`, `fix/null-deref`. If neither the arguments nor the session says what the work is, ask the user one short question.

**Where.** Always `~/code/worktrees/<repo>/<name>`, where `<repo>` is the repository name — the directory name of its main working tree, not of the worktree you may currently be in. A `/` in `<name>` just nests another level. Never place a worktree inside the repository's own working tree.

**Select the source.** Fetch `origin`, then choose exactly one path:

1. **Matching registered worktree** — when one registered worktree already checks out `<name>`, verify its branch and, when supplied, that the Planning Baseline SHA is an ancestor of its HEAD. Reuse that path. A different registered branch at the target path is a collision.
2. **Planning Baseline branch** — require the full SHA to exist and be an ancestor of the selected branch HEAD. If the local branch exists and is free, attach it with `git worktree add <path> <name>`. If only `origin/<name>` exists, create it with `git worktree add --track -b <name> <path> origin/<name>`. When both refs exist, fast-forward a free local branch with `git branch -f <name> origin/<name>` only when it is strictly behind the remote; keep unpushed local commits when the remote is its ancestor; divergent refs stop the operation.
3. **New branch** — default to `origin/<default-branch>`. Use current `HEAD` when the task depends on commits that exist only there. Use another existing base when the task requirements provide a concrete reason; verify that base resolves to a commit after the fetch, then report the selected base and reason. Uncommitted changes do not cross this boundary; report the dependency before creating anything.

**Before creating.** Read Context first:
- **Path collision** — if a non-empty target directory is not the matching registered worktree, stop. Do not choose a variant path.
- **Branch already checked out** — a branch can live in only one worktree at a time. If `<name>` is checked out elsewhere, say where; don't force it.
- **Baseline conflict** — a missing SHA, failed ancestry check, or divergent local/remote branch stops the operation. Do not choose another base or branch.
- **Base conflict** — conflicting requirements or several equally plausible bases stop the operation. Do not pick one arbitrarily.

Create a new branch and worktree in one step with `git worktree add -b <name> <path> <base>` so they cannot drift apart. Attach or track existing branches with the exact commands in the source-selection rules above.

Once it exists, switch into it if the session can, and report the path, branch, source (`<base>` and reason, `Planning Baseline <full SHA>`, or matching registered worktree), and whether the worktree was created or reused. Then pick up the task that prompted it.

$ARGUMENTS
