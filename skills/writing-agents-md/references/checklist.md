# Writing Agents MD Audit Checklist

Use this checklist for a line-by-line review after discovering the active instruction chain.

## Evidence

For each rule, record:

1. **Authority** — Is it user or organization policy, checked-in configuration, current implementation, or an unsupported claim?
2. **Behavior delta** — What costly mistake, repeated correction, or wrong default does it prevent? If target models behave the same without it, it is a no-op.
3. **Currentness** — Does current code, CI, documentation, or recent operational evidence support it?
4. **Conflict** — Does another active instruction disagree? Resolve by scope and authority; do not silently choose the most convenient source.

Treat an existing instruction file as a contract under review. Repository evidence can reveal stale implementation facts, but it cannot reconstruct every safety, release, compliance, or external-system policy.

## Routing

Apply the [Routing Interface](../SKILL.md#routing-interface). Record exactly one action and its destination for each rule so no candidate disappears between review and rewrite.

## Content Quality

Retained instructions should be:

- **scope-correct** — loaded only where they apply
- **decision-changing** — meaningfully alter behavior from the target model's default
- **specific** — name the action, condition, or safe path
- **verifiable** — allow the agent or reviewer to determine compliance
- **stable enough** — unlikely to rot faster than maintainers can update it
- **single-source** — not a cache of easy repository lookups or another instruction file

Discoverability lowers the value of repetition but does not decide by itself. Keep a concise canonical command when it prevents repeated wrong validation; defer a branched protocol to a skill. A one- or two-sentence repository purpose can orient the agent; a directory tour does not earn always-on load.

## Completion

- The target host, directory scope, and requested mutation mode are explicit.
- Ancestor, override, nested, imported, and path-scoped instructions relevant to the target are accounted for.
- Every candidate has one routing action and supporting evidence.
- Unresolved safety, production, release, legal, or external-system rules remain visible for owner confirmation.
- Retained rules do not conflict or duplicate another active source.
- Changed files validate, and review-only or output-only boundaries were honored.
