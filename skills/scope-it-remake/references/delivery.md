# Conditional delivery

Use only for entry changes, saved/proposed Planning evidence, shared integration delivery, or an explicit delivery-verification request. Coordinate these contracts across sources; implementation, merges and closure remain the executor's work under its own authorization.

## Ownership and cleanup

Account for every entry change in a Change Proposal:

| Treatment | Evidence and effect |
| --- | --- |
| Carry | Proven scope-owned whole file or independently applicable exact patch that delivery must retain. |
| Remove | Proven scope-owned patch superseded by a durable artifact. |
| Preserve | Unrelated bytes kept unchanged. |
| Uncertain | Candidate path/range, ownership evidence gap and recommended treatment. |

Use session records, snapshots, exact patches or explicit user confirmation; semantic similarity only supports a recommendation. Include bounded uncertainties in the proposal. Preserve unbounded candidates; ask the smallest ownership question only when they prevent a verifiable proposal. Draft snapshots are not Carry without separate selection.

If no Carry or saved baseline needs delivery, use Planning `none`: only approved Remove cleanup, no Carrier, baseline branch/worktree/commit/push or pointer. An independently approved lane bootstrap remains possible.

For non-empty Carry, select one Carrier: the only ticket; an earliest executable-frontier ticket for independent multi-ticket delivery (document/foundation ownership breaks ties, no foundation-only restriction); or the final integrate-and-verify ticket for a shared lane. Direct delivery starts with its Carrier, replacing a provisional first choice; shared delivery starts with terminal tickets, not the final Carrier. Bundle approval fixes selection without another confirmation.

Apply exact approved Carry/Remove cleanup and verify:

- baseline diff = Carry, when a baseline exists;
- entry after = entry before minus Carry and Remove;
- Preserve byte-for-byte unchanged.

Retain recoverable evidence. Share only approved Carry/Remove payloads and non-disclosing Preserve hashes/receipts; full entry snapshots stay local or in explicitly approved controlled storage with access/retention recorded. Missing evidence, entry drift or a leftover patch prevents claiming the affected cleanup complete: recover/reconcile first, approve changed writes, and preserve successful results and new unrelated work.

## Baseline handoff

Perform only missing approved Git operations using available tools under repository/host rules. Bind each operation to the approved Carrier, exact branch/path, base or baseline SHA, isolated worktree, Carry scope and remote-publication choice. Verify branch/worktree ownership and collisions before mutation; an unrelated branch is not available for reuse, forcing or an unapproved alternate path. Optional skill assistance follows the environment's invocation rules; no Git skill is a prerequisite of this workflow. Missing tools, permissions or safety evidence pause the affected operation, not successful prior work. Read-only or pointer-only repairs introduce no Git mutation.

Initialize the Carrier's actual delivery path from the fetched remote default branch in an isolated worktree. Direct delivery uses its ticket-linked branch; shared delivery uses the canonical integration path. Commit only Carry as the immutable baseline before other path commits and retain its full SHA.

Persist this complete pointer on every related ticket, linked from the Map:

- Carrier URL; repository and exact branch/path; full baseline SHA; landing target;
- link to the approved Carry manifest with exact paths/patches and base SHA;
- executor must resume that same path with baseline ancestry; other tickets consume pointers, never duplicate Carry or parallel baselines;
- target must contain Carry, and after final landing so must main.

Read all pointers back before entry cleanup. On an interrupted publication, recover the approved manifest and bindings, verify existing branch/commit, baseline diff and same-path ancestry, then fill only missing approved pointers or cleanup. A clean entry or missing comment never warrants recreating existing Git work. For already completed landing, use the historical-evidence rule below.

## Shared lane

Disabled by default; enable only when multiple terminal tickets must land atomically to main. Verify canonical branch availability and applicable repository rules/checks for both terminal-to-integration and final-to-target edges. Any required capability bootstrap must be an exact approved write and verify before the lane is considered runnable.

Have the ticket source supply the final integrate-and-verify ticket, blocked by every terminal, before approval. Persist a lane contract linked from the Map and final ticket:

- canonical branch/target, capability or bootstrap evidence, terminal/final ticket identities and real blockers;
- optional baseline pointer, immutable full integration start SHA with capture point;
- umbrella PR URL, or the final executor's responsibility to bind it when created;
- the execution gates below.

Capture start at approved publication: empty Carry uses the established path's full SHA immediately, before later bootstrap; create the path from the approved base first if needed. Non-empty Carry initializes the baseline before other lane commits/terminal branches, completes approved bootstrap, then records start with baseline ancestry proved. Mutable integration HEAD/checks/PR receipts never rewrite immutable baseline/start evidence.

Persist these executor gates:

1. Terminals branch independently from the latest green integration HEAD. Their PRs use `Refs` or equivalent reference semantics, not automatic closing.
2. A terminal closes only after merge to integration, required checks on the exact resulting HEAD, and durable PR URL/full-SHA receipts.
3. The final ticket waits for all terminals and owns main-drift reconciliation, aggregate verification, umbrella synchronization and Map-home parent closure after the final gate.
4. Failed or unknown rules/checks/ancestry/exact-head evidence blocks new closure/finalization; retain artifacts and report the affected gate incomplete.

Initial publication records these contracts; it need not wait for implementation or landing and preserves the starting item's lifecycle.

## Requested verification

A later explicit resume/finalization check is read-only and does not modify the Map or repeat publication. Verify applicable ticket/relationship evidence plus:

With Carry/baseline, first verify Carrier availability, the recorded path/baseline binding and baseline diff for either stage.

| Evidence | Unfinished delivery | Completed landing |
| --- | --- | --- |
| Carry/baseline | Live same-path HEAD must descend from baseline. | Recover a readable immutable implementation/PR head bound to that Carrier/path and verify baseline ancestry there; a retired ref is not required. |
| Shared lane | Current branch/rules and required checks on the current exact integration HEAD. | Recover the bound final integration/umbrella PR head and applicable rule/check evidence for that exact head, even after ref retirement. |

For a lane, also verify immutable start, baseline ancestry when present, and relevant PR/full-SHA receipts. Another head's green checks never suffice; missing historical evidence requires recovery, not recreated refs. A cancelled Carrier leaves delivery incomplete until an approved Map amendment selects its replacement.

For Carry, read actual content from the target and, after final landing, main. Baseline existence, ancestry or a merged PR cannot excuse reverted content. Squash landing need not preserve baseline ancestry in target/main. Work may resume before Carry lands, but delivery is incomplete until its content gate passes.

Planning `none` skips Carrier/baseline/Carry-landing checks, not applicable shared-lane gates. Do not invent missing inapplicable fields. Retain successful publication when a delivery gate fails; corrective writes require separate exact approval.
