# Scope-it adds optional Integration Delivery Lane

When a single planning session produces multiple implementation tickets that must land atomically, `scope-it` records an optional Integration Delivery Lane (IDL) separate from the Planning Baseline. The lane holds mutable delivery state: integration branch, canonical integration start SHA, bootstrap/state evidence, and final integration ticket ownership. Planning Baseline remains immutable planning evidence for repository documents and remains unchanged by lane movement.

## Context

- Planning Baseline is a stable point-in-time baseline of repository documents produced by the settled scope.
- Multi-ticket delivery frequently needs shared integration and controlled verification before final main merge.
- The prior flow mixed baseline publication with delivery orchestration, creating ambiguity in child closure and parent-blocker semantics.

## Decision

- Add IDL as a distinct optional lane under `scope-it`'s delivery contract, enabled only when multi-ticket aggregation via integration branch is intended and repository CI/rulesets support exact integration branch validation.
- Keep child tickets tied to terminal implementation work only and native blocker release semantics from integration closure evidence.
- Keep the final ticket as the single owner for aggregate verification, main drift reconciliation, and umbrella PR finalization.
- Keep Planning Baseline immutable and independent; never encode evolving integration state into Planning Baseline artifacts.
- Require explicit user confirmation before IDL enablement, even when conditions/capability checks are already satisfied, to avoid unintended delivery-mode activation.

## Consequences

- Scope owners must classify and record two artifact families when IDL is enabled: Planning Baseline and IDL state.
- Child tickets should close only after referenceable merge evidence and green exact integration-head checks, avoiding direct closing keywords on non-default branch PRs.
- If integration checks, rulesets, ancestry, or head verification fail, finalization pauses and preserves completed artifacts until proof is repaired.
