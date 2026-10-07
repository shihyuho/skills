# Handoff inputs

Read this for repository planning files or planning worktree creation or transfer, including when accepting existing Tickets. This coordinator settles what must land and prepares the handoff inputs; `to-afk-agent` decides how it lands under its current workflow.

## Prepare landing obligations

Reconcile all planning artifacts against the settled scope and current repository state. Distinguish repository content with a landing obligation from content supplied only for Issue-comment publication. For ADRs, `CONTEXT.md` changes or other required repository content, establish exact scope-owned files/patches, their index/worktree versions, ownership evidence, repository and landing target (the branch the content must finally reach, such as `main`; the path there belongs to the handoff). Preserve unrelated bytes and keep uncertain ownership unresolved.

Carry confirmed planning patches still needed for delivery even when Ticket acceptance quotes them or assigns later recreation. An Issue comment can preserve a supplied document, but does not discharge a repository patch's landing obligation. A clean worktree or semantic similarity does not establish ownership or eliminate an existing delivery obligation. Carry ownership creates no blocker.

Pass verified existing Carrier and delivery-path bindings, remote artifacts and preservation evidence for reuse, and unverified or unlinked branches only as evidence, together with explicit retention/cleanup choices or unresolved legacy source-choice questions. The handoff selects any missing Carrier, preserves what still needs preservation and records the Carry; reuse its verified results on resume. Keep required drafts and continuation paths available until the handoff verifies their replacements.

A change to the carried files, patch bounds or landing target returns to this coordinator for approval. Carrier and delivery-path changes are amendments under the handoff's own workflow.

## Transfer planning worktrees

Account for temporary worktrees created by this planning run and its invoked workflows, including when nothing needs carrying. Record creation or transfer evidence and current repository/path/ref/HEAD identities. Explicitly entrust the eligible worktrees to `to-afk-agent` within the handoff's cleanup scope, carrying forward retention choices and any continuing use or required local paths.

The delegate verifies preservation, source disposition, worktree eligibility and removal under its own cleanup rules. Existing, unrelated or ownership-uncertain worktrees stay outside the transfer. Retaining a source at an agreed worktree path can require retaining that worktree too. Keep successful publication and removal evidence on interruption; unresolved required disposition leaves the handoff incomplete.
