---
name: create-worktree
description: "Start the work in its own Git worktree under ~/code/worktrees and continue there."
license: MIT
disable-model-invocation: true
---

# create-worktree

Start the work in its own Git worktree under `~/code/worktrees` and continue there.

Treat every run as a possible **resume**. The work may already have its worktree, or its branch may already exist; resume those rather than adding a second. A new worktree always lives at the fixed path `~/code/worktrees/<repo>/<name>` outside the repository and, by default, branches from a freshly fetched `origin/<default-branch>` rather than whatever local `HEAD` happens to be.

## Invocation input

`$ARGUMENTS` is the trigger. It may carry a description of the work or an existing branch name, and a base. Treat it as a description, not a literal name, unless it already reads like a branch slug.

Work from the current branch, status and `git worktree list` already in context, reading only what is missing.

## Name

Derive `<name>` from `$ARGUMENTS`; without it, from the task this session is about to start: what the user just asked for, the plan under discussion, or the uncommitted changes. Keep it short, ASCII and valid for `git check-ref-format --branch`, e.g. `feat/create-worktree-command`, `fix/null-deref`. If neither says what the work is, ask one short question.

`<repo>` is the directory name of the repository's main working tree, not of the worktree you may be in. A `/` in `<name>` nests another level.

## Resume or create

Fetch `origin`, then take the first path that matches:

1. **Registered worktree** — a worktree already checks out `<name>`: resume it at its path, keeping any uncommitted work there. A branch lives in one worktree at a time; when that is the main working tree, report it there rather than forcing a second checkout.
2. **Existing branch** — `<name>` exists with no worktree. It is this work's branch when `$ARGUMENTS` named it or its commits match the work; otherwise report it as a collision and stop. Attach a local branch with `git worktree add <path> <name>`, fast-forwarding it first with `git branch -f <name> origin/<name>` only when it is strictly behind; when only `origin/<name>` exists, use `git worktree add --track -b <name> <path> origin/<name>`. Diverged local and remote refs stop the operation.
3. **New branch** — `git worktree add --no-track -b <name> <path> <base>`, in one step so branch and worktree cannot drift apart; `--no-track` keeps the base from becoming the branch's upstream.

**Base** for a new branch is the one the trigger names, otherwise `origin/<default-branch>`. Use current `HEAD` when the task depends on commits that exist only there, or another existing branch when the task's requirements give a concrete reason; verify it resolves after the fetch and report the reason. When requirements point equally at several bases, ask which one. Uncommitted changes stay where they are; report any the task depends on before creating anything.

**Path collision** — a non-empty target directory that is not the registered worktree for `<name>` stops the operation; report it rather than choosing a variant path.

## Continue there

Switch the session into the worktree when the host can; in Claude Code, call `EnterWorktree` with its `path`. Report the path, branch, base and reason for a new branch, and whether the worktree was `created` or `reused`. Then pick up the task that prompted it.
