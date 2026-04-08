---
name: grill-diff
description: Review git changed files one by one, asking probing questions about every aspect of each change until reaching shared understanding. Use when user wants to review their diff, grill their changes, or stress-test code changes before committing or opening a PR.
---

Review my git changes file by file. For each file, interrogate every aspect of the diff until we reach a shared understanding before moving to the next file.

Determine changed files automatically:
1. If there are staged changes, use those.
2. Otherwise, if there are unstaged changes, use those.
3. Otherwise, diff the current branch against the default branch.
4. If the user specifies a target (e.g. "against develop", a PR URL), use that instead.

Ask if there is a related spec or plan file to understand the goal of the changes. Read through all changed files to understand the full picture, then go through the files one at a time. Ask one question at a time.

If a question can be answered by exploring the codebase, specs, or tests, explore them yourself instead of asking me.

Flag any change that isn't required to achieve the stated goal. Probe: "What breaks if we revert this?"
