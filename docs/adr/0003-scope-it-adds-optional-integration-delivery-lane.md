# Scope-it adds optional Integration Delivery Lane

When a single planning session produces multiple implementation tickets that must land atomically, `scope-it` records an optional Integration Delivery Lane (IDL) separate from the Planning Baseline. The lane holds mutable delivery state: integration branch, canonical integration start SHA, bootstrap/state evidence, and final integration ticket ownership. When planning changes exist, that final ticket is the Planning Carrier; the immutable Planning Baseline initializes the canonical integration path, and the start SHA is recorded only after bootstrap with the baseline as an ancestor.

## Context

- Planning Baseline is a stable point-in-time baseline of repository documents produced by the settled scope.
- Multi-ticket delivery frequently needs shared integration and controlled verification before final main merge.
- The prior flow mixed baseline publication with delivery orchestration, creating ambiguity in child closure and parent-blocker semantics.

## Decision

- Add IDL as a distinct optional lane under `scope-it`'s delivery contract, enabled only when multi-ticket aggregation via integration branch is intended and repository CI/rulesets support exact integration branch validation.
- Keep child tickets tied to terminal implementation work only and native blocker release semantics from integration closure evidence.
- Keep the final ticket as the single owner for aggregate verification, main drift reconciliation, and umbrella PR finalization.
- Keep Planning Baseline immutable and independent; never encode evolving integration state into Planning Baseline artifacts.
- Require the integration start SHA to descend from the Planning Baseline before terminal ticket branches start, so the umbrella landing carries the planning changes once.

## Consequences

- Scope owners must classify and record two artifact families when IDL is enabled: the immutable Planning Baseline carried by the final ticket, and mutable IDL state.
- Child tickets should close only after referenceable merge evidence and green exact integration-head checks, avoiding direct closing keywords on non-default branch PRs.
- If integration checks, baseline ancestry, rulesets, head verification, or final `main` containment fail, finalization pauses and preserves completed artifacts until proof is repaired.
