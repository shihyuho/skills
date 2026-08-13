# go-for-it

Run or resume a settled design through scoping, implementation, and pull request, with an optional bounded peer review-and-fix loop.

This skill must be invoked explicitly.

It uses `resolve-user-invoke-skill` to load `scope-it`, `create-worktree`, `implement`, `commit`, `push`, and `pr` from the active agent environment. It carries any verified Planning Baseline from scope into the delivery worktree. The default path still stops after opening the pull request.

Use `--loop` to load the fixed `get-pr-ready` phase after the pull request exists:

```text
go-for-it --loop [--review-session <handle>] [--max-fix-rounds N]
```

The `--review-session` and `--max-fix-rounds` options are invalid without `--loop`.

The optional loop requires `get-pr-ready` and its required dependencies to be installed in the active agent environment.

## Installation

```bash
npx skills add shihyuho/skills --skill go-for-it -g
```
