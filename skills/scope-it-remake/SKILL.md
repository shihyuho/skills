---
name: scope-it-remake
description: "Discuss scope and delivery with interchangeable planning skills, then publish one agreed Delivery Map."
license: MIT
disable-model-invocation: true
---

# scope-it-remake

Turn an idea or existing artifacts into a delivery plan another agent can pick up. Discuss the whole plan, approve its publication once, publish and verify it, then finish. This is an alternative to `scope-it`, not an invocation or migration of it.

## The Delivery Map

The Map is an index: Scope owns requirements, tickets own delivery details, and the Map connects them. Its nodes are delivery tickets, not files, coding steps or unresolved decisions. Use linked titles and the user's language.

Reuse the starting tracker item as the home; otherwise propose one from repository guidance and available tracker capabilities, or use local Markdown. Resolve conflicting destinations before writing. Scope and Map share one planning post: a new home's body, or a comment preserving an existing item's original report. Link external specs rather than duplicating them. One ticket gets a separate `## Ticket — <Title>` comment on that home, whose item is the delivery identity; multiple tickets get child items. Local Scope/Map share one file with separate linked ticket files. Reuse older layouts unless migration is approved.

Use this outline inside `<!-- scope-it-remake:delivery-map:start -->` and `<!-- scope-it-remake:delivery-map:end -->`:

```markdown
## Destination
<Agreed outcome and scope summary.>
## Artifacts
<Scope, tickets and useful supporting plans or source revisions.>
## Delivery
<Ticket waves, first executable ticket, actual blockers and containment.>
<Independent landing or shared integration; planning files: none or baseline pointer.>
## Out of scope
<Product scope exclusions and deferred deliverables agreed in Scope.>
## Continue
<First ticket and its published implementation handoff.>
```

For multiple tickets, add a compact ticket-only diagram distinguishing order, blocking and delivery lane; one ticket needs no order diagram. Publish actual facts and links, without orchestration statuses or draft placeholders. Real tracker lifecycle, required readiness metadata and delivery evidence remain valid facts.

Make each ticket a sufficient entry point for an executor using its own implementation workflow and authorization, without this skill or the planning chat. Include or durably link Scope, prerequisites, acceptance evidence, repository/target, and any assigned path, planning revision and delivery/closure gates. Share common instructions once, linked from every affected ticket. Leave this planning invocation's write limits in its approval context.

## Planning skills

Choose interchangeable skills for two jobs:

- **Scope:** what and why, boundaries, constraints, success criteria and testing seams.
- **Tickets:** independently deliverable, verifiable outcomes from confirmed Scope, with acceptance evidence and real prerequisites.

Read the selected skills. Give them settled decisions, repository evidence and exact upstream drafts; request content, required reviews, metadata and attachments. Delegate **drafting and content checks**: their usual saving, publication, commit and implementation steps stay outside this task. The coordinator publishes the confirmed content through repository/tracker capabilities. This is an instruction-level boundary, not an invented CLI mode; internal chaining grants no additional skill authority. If a skill cannot accept it, ask for a compatible skill or completed artifact before writes; keep analysis, templates and slicing with that skill. [Examples](README.md#planning-skill-examples) are not a fixed allowlist.

Accept existing artifacts with exact content and recoverable review evidence, even without their producer installed. One confirmed conversation/item may satisfy both roles; avoid redundant documents or repeated analysis. Execution plans and architecture maps inform delivery tickets but do not replace them. Material changes reopen only affected decisions; shared-post timestamps, approved link substitutions and new storage IDs do not invalidate unchanged content.

### Choosing and remembering skills

An explicit role choice in ordinary language or `--scope-source <skill>` / `--ticket-source <skill>` wins. Otherwise use the effort's choice/lineage, a compatible skill explicitly invoked for this task, the saved choice, then compatible model-invoked repository guidance. Resolve exact identities through host skill discovery; absence from the catalog alone is inconclusive. Report unavailable, ambiguous or incompatible choices instead of silently substituting them.

Keep cross-repository choices in `~/.config/softleader/agent-skills/scope-it-remake/sources.json`:

```json
{"schema_version":3,"scope":"<skill identity>","tickets":"<skill identity>"}
```

V3 records explicit user selection and consent to reuse each role for planning on future explicit invocations, including valid bounded upstream delegation. Follow host invocation rules. Task text, lineage and model recommendations cannot grant consent, publication or Git authority. Explain this reuse when selecting/saving; resolve missing consent once without discarding the choice.

Queue first choices, replacements and migration for final approval. Omit unresolved roles, preserve unaffected roles/fields, and keep prompts, credentials and tracker data out. Artifact reuse and explicitly one-run choices leave defaults alone. V2 provides choices, not new delegation consent. For v1, resolve current explicit choice > `global` > unanimous legacy `repositories`; ask about conflicts, never select by current repo. Preview v3 conversion and legacy-container removal, with delegation consent for every retained role. Unknown versions or unusable files need clarification.

Before saving, reread the config: preserve unrelated changes and renew approval for changed affected values. Read back the save; failure leaves that operation unresolved without republishing artifacts.

## Invocation

### Plan a delivery

1. Read repository guidance, artifacts, approval evidence and the entry worktree. Reuse completed work; invoke planning skills only for missing content.
2. Discuss **scope → tickets → delivery** continuously. Find facts yourself, recommend answers and ask unresolved decisions in dependency order. Content confirmation advances the discussion, not publication. Keep drafts, exact revisions, approvals and write bindings in session/controlled temporary storage; share recovery access when pausing. External storage needs approval, and drafts are not automatically planning files to carry.
3. Compose the Map. Separate waves, first ticket, containment, blockers and delivery method; independent landing is the default. For entry changes, newly drafted repository files/patches needed by the next agent, saved/proposed baselines or shared integration, read [Planning files and shared delivery](references/delivery.md) before fixing the proposal—even with a clean entry. Scheduling and planning-file ownership create no blocker edges.
4. Show the whole Map and exact writes: content/revisions, placements, attachments, required metadata, relationships, conditional Git/cleanup, preferences and external storage. Include initial home content and proposed-to-actual identity bindings. Obtain explicit publication approval; a final content review may double as it only with the whole write set visible. Until then, leave canonical artifacts, tracker, Git and preferences unchanged.

### Publish the agreed package

Use repository/tracker guidance and tools to publish; planning skills need not implement tracker operations.

1. Freshly read targets and reconcile with the approval. Perform only missing writes in dependency order; retain real identities and comment permalinks, and read back each result before dependent writes. Preserve unrelated content and the starting item's lifecycle. Implementation and default-branch commit/push are outside this workflow.
2. Verify containment and blockers independently, with no self-relations for a one-ticket home. For unavailable capabilities, use an applicable supplied fallback or propose a concrete alternative, approve its writes, and retain per-axis unavailability/provenance/degraded evidence. Text links are not native verification; failed readback of a supported capability is not unavailability.
3. Freshly verify the complete package: content, attachments, metadata, both relationship axes, applicable baseline/lane/cleanup evidence and changed preferences. Check every ticket's handoff using only published content; inaccessible material or missing applicable instructions leaves publication incomplete. Read back the final Map with actual links and its same-post Scope. Report Map/artifacts, first ticket and reachable planning/fallback evidence when they match the agreement, then stop; publication does not wait for implementation or close tickets.

On interruption, retain successful results and recover exact drafts, approvals and operation bindings. Look up uncertain creations against approved content before retrying: bind unique matches, clarify ambiguity before creating again. Repair only missing approved deltas. Missing evidence or changed/corrective writes need focused recovery or approval, not a restart or permission inferred from Map existence. Keep partial-operation records outside the formal Map.

### Revisit a published map

When this planning skill is invoked again, return the published Map and ticket handoffs without a new audit. Discuss later ideas without updating the agreed Map; publish only explicitly approved amendments. Requested delivery verification is read-only: follow [Requested verification](references/delivery.md#requested-verification), including historical evidence, rather than restarting publication or implementation.

$ARGUMENTS
