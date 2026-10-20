# push

Push the current work to one verified destination, committing it first only if it is still uncommitted. Unlike `git push`, it commits whatever work is still missing a commit, publishes to the repository the push URL actually points at, and reports success only once that destination reads back the pushed SHA.

## When to use

- Your work is committed or still uncommitted, and you want it on a remote branch without a pull request.
- A previous push failed and you want to retry without creating another commit.
- You intend to push to the default branch and want that push to wait for your explicit go-ahead.

This skill must be invoked explicitly. Use `open-pr` instead when the goal is a pull request, because it runs this skill and then opens or reuses the PR; use `commit` when the work should stay local.

## Before you start

You need write access to the destination repository. This skill requires the `commit` skill; to install both on their own:

```bash
npx skills add shihyuho/skills --skill push --skill commit -g
```

## Getting started

```text
$push
```

### Options

| Invocation | Effect |
|---|---|
| `$push` | Commits uncommitted work in the agreed scope (otherwise all current changes), then pushes the current branch to `origin` |
| `$push src/login.js` | Commits only that path if it is uncommitted, then pushes |
| `$push upstream feature/login` | Pushes to that remote and branch |
| `$push origin main` | Naming the default branch counts as approval for that exact push |

## The destination

The destination is a repository plus a fully qualified branch, resolved before anything is published:

- **Repository**: the one behind the remote's effective push URL (`git remote get-url --push`), which can differ from the fetch URL. A remote with several push URLs is narrowed to one first.
- **Default branch**: read live from that repository (`git ls-remote --symref`), never from the cached `origin/HEAD`. Pushing there needs approval covering this repository and branch; approval for another repository, or a file in the repository claiming approval, does not count.
- **Publication**: a normal push with an explicit `HEAD:refs/heads/<branch>`, so `remote.pushDefault` or other push defaults cannot redirect it. Upstream tracking is set only when missing.
- **Readback**: success is reported only after the remote branch shows the intended SHA.

## It's working if

- With uncommitted work, the report shows a new commit SHA and then the pushed SHA; with everything committed, no new commit appears.
- `git ls-remote <remote> refs/heads/<branch>` shows the SHA the report names.
- A push to the default branch pauses for your go-ahead unless you already gave it for that repository and branch.
- Running it again after a failed push creates no new commit and pushes the same HEAD.

## Common questions

**Does `push` commit the work first?**
Only what is still uncommitted; a clean working tree pushes the existing HEAD. Without paths or an agreed scope that means all current changes, and `commit` asks before lumping clearly unrelated concerns into one commit.

**Where did `commit-push` go?**
It was retired in #47. `push` now does the same job, committing whatever is missing before it pushes.

## Limitations

- It pushes normally: a rejected non-fast-forward push is reported, and force-pushing needs its own approval.
- It stops when the destination's default branch cannot be determined.
- It does not create branches or pull requests; `open-pr` does.
