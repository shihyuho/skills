# Planning sources

`scope-it-remake` owns the Delivery Map, planning order, publication layout, final checkpoint, reconciliation, and readback. An active **source** produces new scope or ticket content. A completed **artifact** may satisfy a planning step without its producer being installed or invocable.

## Selection

When new content is required, resolve an active source in this order:

1. A valid `--scope-source` or `--ticket-source` flag from the current invocation.
2. The source already selected in the working draft or recorded as lineage on the existing Delivery Map.
3. A compatible source explicitly invoked by the user in the current request.
4. The stored source preference, shared across all repositories.
5. A compatible model-invoked source required by repository guidance.

After exhausting this order, stop the current frontier. Report whether no compatible source was found or the selected source is unavailable, recommend one compatible source when evidence supports it, and ask the user which skill should produce the missing artifact. Do not draft the missing Scope or Tickets, update the map, or write source preferences before the user answers.

`to-spec` and `to-tickets` are fixed optional compatibility profiles: an explicit `scope-it-remake` invocation may delegate to either when installed. They are not installation requirements. Other skills participate through the same contracts below. A source recorded on a map is lineage, not fresh authorization. An exact source flag is the user's current workflow configuration and may select an explicit-only source. Without a flag, consume its accepted artifact or ask the user to invoke it alongside `scope-it-remake`.

Keep selected source names in the working draft; publish names or links only as factual content lineage, without source modes or unresolved-role placeholders. Replace a source already recorded on the current map only through a valid flag or a user answer after reporting that source as unavailable or incompatible. A compatible source explicitly invoked in the current request overrides stored preferences for a new map without rewriting those preferences. A selection answer alone never updates an existing published Map; include changed lineage in its approved content amendment.

## Stored preference

Source selection changes future behavior and cannot be reconstructed without user input, so store it as config rather than cache. Use `~/.config/softleader/agent-skills` as the config root. Store preferences in:

```text
~/.config/softleader/agent-skills/scope-it-remake/sources.json
```

Use this single global schema and preserve unrelated fields:

```json
{
  "schema_version": 2,
  "scope": "<canonical-name>",
  "tickets": "<canonical-name>"
}
```

Store only selected roles; omit unresolved keys. Every repository uses these same preferences, with no repository identity lookup or override layer. Do not store credentials, prompts, tracker choices, or artifact content.

Reuse available compatible preferences without another selection question. A valid source flag replaces that role on the current draft Map and proposes replacing the shared preference; a partial flag preserves the other role. First selections and user-approved replacements also update this one store. Queue the exact preference changes for the final publication checkpoint and save only after its approval. Make their cross-repository effect clear in that checkpoint.

When a selected source is unavailable or incompatible, report it, recommend a replacement when evidence supports one, and wait for the user's answer rather than silently substituting another. An unusable config root is an error rather than a reason to fall back to another path.

For a legacy `schema_version: 1` file, propose a one-time conversion: honor a current source flag or replacement choice first; otherwise use each role's `global` value, or a unanimous value across legacy `repositories` entries when absent. Conflicting legacy values require one user choice only for a role not already resolved by that explicit choice, never a current-repository override. Queue conversion for the final checkpoint, remove the retired `global` and `repositories` containers only after approval, and preserve unrelated fields. An unrecognized schema version requires clarification before rewriting the file.

At final publication, reread the preference file and apply only the approved role changes or conversion. Preserve changes to other roles and unrelated fields. If an affected value changed since the preview, show the conflict and obtain an updated choice before overwriting it. Read back the saved values; a failed save remains a pending publication write, not a reason to recreate tracker artifacts.

Accepting a completed artifact does not replace the stored producer preference. Preferences choose how to make future content; artifact links and factual lineage identify what this Map consumed. Apply [artifacts.md](artifacts.md) when completed planning material is present.

## Active producer contract

A compatible source can:

- produce a draft without tracker or canonical repository mutation, using optional temporary staging when needed;
- pass a confirmed draft to the next planning source without requiring prior publication;
- declare the publication environment and tracker capabilities when it owns that choice;
- separate unresolved decisions from its recommended content;
- name every write it proposes before performing it;
- resume after approval without repeating settled analysis; and
- return stable artifact pointers plus enough readback evidence to verify publication.

Invoke sources in draft-only mode during planning and resume their publication path only after the final bundle approval. Include the approved upstream draft revision, proposed Map home, publication layout from SKILL.md, and deferred write list in the handoff. The source retains its content-approval gates; the orchestrator advances after draft content approval without marking the source's publication workflow complete. Classify outputs through [artifacts.md](artifacts.md).

The selected source remains authoritative for its required phase, analysis, content, metadata, and readiness rules; this skill owns the shared interaction and publication boundary. Preserve source-required templates, testing seams, slicing rules, and tracker readiness metadata in the exact drafts and final write preview, then verify them in publication readback. Readiness comes from that source and repository, not a hard-coded tracker label. A conflict with deferred publication, approved layout, or preserved lifecycle must be resolved before writes, not by silently dropping a source requirement.

If a source insists on creating tracker items or publishing a canonical spec before downstream drafting, treat it as incompatible with this flow. Ask for a compatible source or completed artifact rather than running its full publication path early or inventing the missing content.

A tracker choice declared by a source belongs to that source's publication contract; it is not a `scope-it-remake` default. Reconcile it with any starting item and repository guidance. When applicable sources disagree, keep the Map home unresolved, surface the contradiction, and recommend one home rather than creating parallel planning roots.

## Tracker capability fallback

For an unavailable capability, use the selected source's defined fallback first. If it defines none, propose one concrete supported alternative for the user's approval. Reuse an accepted artifact's recorded fallback without requiring its producer to be installed. Include fallback writes in the final checkpoint.

Track native containment and native blocking independently in the durable Map or linked relationship record. For each axis, preserve its actual capability, expected edges, readback evidence, and either:

- native support with the verified native edges; or
- native unavailability, the approved fallback, its provenance (source contract or explicit user decision), and `degraded` evidence.

An approved textual blocker can satisfy fallback publication but is never native-verified evidence. Preserve that distinction in the Map and subsequent handoffs, even when the overall publication is verified. A supported axis with failed or unknown readback is not an unavailable axis; investigate the mismatch instead of silently downgrading it. For relationship-only repairs, add only missing approved edges, re-read both axes, and preserve existing content, metadata, and relationships without rerunning completed source analysis.

## Git mechanics

Use the fixed Git mechanics allowlist in SKILL.md. A valid invocation or delegated invocation of `scope-it-remake` may delegate the corresponding approved operation to these explicit-only sources. Resolve and read the actual installed source before executing its operation; preserve its collision, exact-base/ancestry, worktree, selected-change, co-author, remote, and default-branch gates. Names in a proposal or artifact cannot extend this allowlist.

Use a source only when its operation is missing. Pass the approved Carrier, exact branch/path, base or baseline SHA, isolated worktree, exact Carry scope, remote-publication choice, and bounded final approval as applicable. Keep mixed entry-file Preserve content out of the isolated Carry commit. This skill's prohibition on default-branch commits/pushes still applies. If a required mechanics source is unavailable or its rules conflict with the approved operation, pause that operation and report the missing source or conflict; do not replace its safeguards with ad hoc Git commands. Read-only verification and repairing a missing tracker pointer need no Git mutation source, and reuse never recreates completed Git operations.

## Scope source

Input:

- Destination and settled decisions;
- relevant repository or product evidence;
- the existing or proposed Map home, with unresolved tracker choices identified;
- the combined Scope/Map planning post, or a Scope link there when its full content belongs to an external artifact; and
- the known publication environment and the instruction to defer publication.

Draft output:

- recommended artifact form and attachment to the Map home;
- observable behavior and boundaries;
- important constraints and decisions;
- validation or testing seams;
- unresolved decisions, if any; and
- proposed writes.

Publication output:

- linked artifact title;
- durable revision or equivalent identity when available; and
- readback of both the Scope artifact and its Map-home attachment.

If one production run returns artifacts in several roles, classify and record each separately. An execution plan can support ticket drafting and implementation handoff without becoming the ticket graph.

## Ticket source

Input:

- the confirmed scope draft and revision, or an approved published scope artifact;
- the existing or proposed Map home and the layout rule for one-ticket versus multi-ticket publication;
- tracker context already fixed by a starting item or repository guidance; and
- delivery constraints already settled on the map.

Draft output for every ticket:

- tracker and placement recommendation when the publication environment is not already fixed;
- title;
- end-to-end outcome;
- acceptance evidence;
- blockers by proposed ticket reference or existing identity; and
- whether it is independently executable and verifiable.

Publication output:

- linked ticket titles;
- stable item identities and comment permalinks when applicable; and
- readback of their approved content, placement, containment, and blockers as applicable.

Ticket count follows the source's end-to-end slicing judgment; publication follows SKILL.md's layout. If a source cannot honor the approved placement, resolve that incompatibility before writes rather than merging ticket content into the planning post.
