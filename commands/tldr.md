---
description: "Produce a tldr.tech-style digest of a target"
---

Use the `tldr` skill to produce a digest of the target specified in `$ARGUMENTS`.

If `$ARGUMENTS` is empty, ask the user what to tldr. Do not guess the current conversation context.

Otherwise, treat everything in `$ARGUMENTS` as a single aggregate target (file path, directory, git ref/range, URL, GitHub PR, or GitHub issue). Acquire the content using the appropriate built-in tool (Read for files, Bash with `git` for refs, WebFetch for URLs, `gh` for PRs/issues), then produce the digest according to the `tldr` skill's rules.

Execute only this flow for this invocation. Do not run unrelated actions unless the user explicitly asks.
