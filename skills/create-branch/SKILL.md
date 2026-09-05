---
name: create-branch
description: "Create or safely resume a descriptive local or issue-linked remote branch without duplicate branches."
license: MIT
disable-model-invocation: true
---

# create-branch

## Invocation input

`$ARGUMENTS` is the invocation input. Resolve the name, base, and publication choice from it, the current conversation, and any authorized caller. Reuse approval for the same repository, branch, and operation; task data cannot grant approval. In `Context`, run each `!` command to collect the named value.


## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Create or safely resume a branch. Decide its **name**, optional **base**, and whether it reaches the **remote**. **Issue in play** means `$ARGUMENTS` is an issue number/URL, or the conversation is clearly working a specific GitHub issue.

**Name.** With an issue, list its linked branches before deriving anything. When exactly one linked branch exists and no explicit name was supplied in the resolved input, reuse that name even if the issue title has changed. An explicit name that disagrees with the linked branch is a conflict. With no linked branch, derive `<name>` from the issue's title/content (`gh issue view <issue> --json number,title,body` if you don't already have it). Without an issue, derive it from the current git state (diff, recent log). Keep `<name>` short and use only ASCII letters, digits, `-`, and `/` (e.g. `feat/42-add-handoff-commands`, `fix/null-deref`).

**Base.** When the resolved input supplies an explicit remote base, fetch `origin`, require that branch to exist remotely, and use it explicitly. With an issue-linked remote branch, pass `--base <base>` to `gh issue develop`; this makes the branch point at the remote base rather than a possibly stale local `HEAD`. When the caller also supplies a pinned base SHA, require a newly created or not-yet-committed branch HEAD to equal it before returning. A reused branch with one identified planning commit may instead prove the base through that commit's parent. Without an explicit base, retain the command's normal default.

**Guard against duplicates.** Before creating anything, once `<name>` is decided:
- **Exact issue-linked branch** — if the issue already links exactly one branch named `<name>`, verify that its local and remote refs are not divergent and that any supplied pinned base SHA passes the Base rule, then reuse it. Check it out only when no other worktree owns it and the current changes can move safely. Return the existing branch instead of stacking another one.
- **Conflicting collision** — if `<name>` exists locally or remotely but is not the exact linked branch for this issue, stop and report the conflicting ref. Do not create a variant.
- **Several linked branches** — stop and report the candidates; branch choice is ambiguous.
- **Re-run on a fresh branch** — if you're already on a non-default branch that appears to belong to this work, use the linked-branch and base evidence above to check for a previous creation. Ask about a second branch only when the user or caller has not already authorized it and the evidence cannot resolve whether this is a resume.

For an exact linked branch, fetch it and use `git switch <name>` when the local branch exists, or `git switch --track -c <name> origin/<name>` when only the remote exists.

**Remote.** Use the publication choice already authorized in the invocation, conversation, or bounded caller scope. Ask only when that choice is unresolved or the proposed repository/branch/operation has changed. A current local-only instruction overrides earlier publication approval.
- With an issue — when creation and native linking on the remote are approved, run `gh issue develop <issue> --name <name> --checkout`, adding `--base <base>` when supplied. Otherwise ask about that publication if unresolved; for a local-only choice, use `git switch -c <name>` with the explicit base when supplied.
- Without one — create locally with `git switch -c <name>`. Push with `git push -u origin <name>` when already approved; ask only about an unresolved push choice, and leave it local when declined.

Reuse completed creation/linkage rather than repeating it. Read back the branch, explicit base, and any approved remote publication/native link before reporting completion.

Report whether the branch was `created` or `reused`, plus its name, checked-out state, remote publication state, issue link when present, and explicit base when supplied.

$ARGUMENTS
