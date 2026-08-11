---
name: create-branch
description: "Create or safely resume a descriptive local or issue-linked remote branch without duplicate branches."
license: MIT
disable-model-invocation: true
---

# create-branch

## Invocation input

`$ARGUMENTS` below means the arguments supplied with the user's explicit invocation. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.


## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Create or safely resume a branch. Decide its **name**, optional **base**, and whether it reaches the **remote**. **Issue in play** means `$ARGUMENTS` is an issue number/URL, or the conversation is clearly working a specific GitHub issue.

**Name.** With an issue, list its linked branches before deriving anything. When exactly one linked branch exists and `$ARGUMENTS` supplies no explicit name, reuse that name even if the issue title has changed. An explicit name that disagrees with the linked branch is a conflict. With no linked branch, derive `<name>` from the issue's title/content (`gh issue view <issue> --json number,title,body` if you don't already have it). Without an issue, derive it from the current git state (diff, recent log). Keep `<name>` short and use only ASCII letters, digits, `-`, and `/` (e.g. `feat/42-add-handoff-commands`, `fix/null-deref`).

**Base.** When `$ARGUMENTS` supplies a remote base, fetch `origin`, require that branch to exist remotely, and use it explicitly. With an issue-linked remote branch, pass `--base <base>` to `gh issue develop`; this makes the branch point at the remote base rather than a possibly stale local `HEAD`. When the caller also supplies a pinned base SHA, require a newly created or not-yet-committed branch HEAD to equal it before returning. A reused branch with one identified planning commit may instead prove the base through that commit's parent. Without an explicit base, retain the command's normal default.

**Guard against duplicates.** Before creating anything, once `<name>` is decided:
- **Exact issue-linked branch** — if the issue already links exactly one branch named `<name>`, verify that its local and remote refs are not divergent and that any supplied pinned base SHA passes the Base rule, then reuse it. Check it out only when no other worktree owns it and the current changes can move safely. Return the existing branch instead of stacking another one.
- **Conflicting collision** — if `<name>` exists locally or remotely but is not the exact linked branch for this issue, stop and report the conflicting ref. Do not create a variant.
- **Several linked branches** — stop and report the candidates; branch choice is ambiguous.
- **Re-run on a fresh branch** — if you're already on a non-default branch that looks freshly created with nothing committed yet (a likely leftover from a previous run), confirm the user actually wants a second branch before proceeding.

For an exact linked branch, fetch it and use `git switch <name>` when the local branch exists, or `git switch --track -c <name> origin/<name>` when only the remote exists.

**Remote.** Take the choice from `$ARGUMENTS` if it states one; otherwise ask the user.
- With an issue — ask whether to create and link the branch on the remote. Approved: run `gh issue develop <issue> --name <name> --checkout`, adding `--base <base>` when an explicit base was supplied. Declined: create a local branch with `git switch -c <name>`, adding `<base>` as the final argument when supplied.
- Without one — create locally with `git switch -c <name>`, then ask whether to push it. Approved: `git push -u origin <name>`. Declined: leave it local.

Report whether the branch was `created` or `reused`, plus its name, checked-out state, remote publication state, issue link when present, and explicit base when supplied.

$ARGUMENTS
