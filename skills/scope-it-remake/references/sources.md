# Planning sources

`scope-it-remake` owns the Delivery Map, frontier order, mutation boundary, reconciliation, and readback. An active **source** produces new scope or ticket content. A completed **artifact** may satisfy a frontier without its producer being installed or invocable.

## Selection

When new content is required, resolve an active source in this order:

1. A valid `--scope-source` or `--ticket-source` flag from the current invocation.
2. The source already recorded on the current Delivery Map.
3. The repository's stored source preference.
4. A compatible source explicitly invoked by the user in the current request.
5. A compatible model-invoked source required by repository guidance.

After exhausting this order, stop the current frontier. Report whether no compatible source was found or the selected source is unavailable, recommend one compatible source when evidence supports it, and ask the user which skill should produce the missing artifact. Do not draft the missing Scope or Tickets, update the map, or write source preferences before the user answers.

`to-spec` and `to-tickets` are fixed optional compatibility profiles: an explicit `scope-it-remake` invocation may delegate to either when installed. They are not installation requirements. Other skills participate through the same contracts below. A source recorded on a map is lineage, not fresh authorization. An exact source flag is the user's current workflow configuration and may select an explicit-only source. Without a flag, consume its accepted artifact or ask the user to invoke it alongside `scope-it-remake`.

Record the selected source names on the map so later sessions preserve the content lineage. Replace a selected source only through a valid flag or a user answer after reporting that the stored source is unavailable or incompatible.

## Stored preference

Source selection changes future behavior and cannot be reconstructed without user input, so store it as config rather than cache. Resolve the agent-skills config root from active user-level instructions; otherwise use `~/.config/agent-skills`. Store preferences in:

```text
<resolved-config-root>/scope-it-remake/sources.json
```

Use this minimal schema and preserve unknown fields:

```json
{
  "schema_version": 1,
  "repositories": {
    "<repository-identity>": {
      "scope": "<canonical-name>",
      "tickets": "<canonical-name>"
    }
  }
}
```

Store only roles whose source the user has selected; omit an unresolved `scope` or `tickets` key until its frontier resolves it.

Prefer the normalized `origin` repository identity so worktrees share one preference: retain only host and repository path, removing scheme, user info, query, fragment, and a trailing `.git`. When no remote identity exists, use the absolute repository root. Do not store credentials, prompts, or artifact content.

On first selection, include the preference-file write in the frontier's **Writes** and persist it only after approval. On later invocations, reuse the map or stored preference without asking. A valid source flag overrides the corresponding role for the current map and updates the stored preference after approval; a partial override preserves the other role. If the chosen source cannot be resolved or fails the compatibility contract, show one replacement recommendation, wait for the user's answer, then update both map and preference. An unusable explicitly configured config root is an error rather than a reason to fall back to another path.

Accepting a completed artifact does not replace the stored producer preference. Preference state chooses how to make future content; artifact state records what this map actually consumed. Apply [artifacts.md](artifacts.md) when completed planning material is present.

## Active producer contract

A compatible source can:

- produce a draft without tracker or repository mutation;
- separate unresolved decisions from its recommended content;
- name every write it proposes before performing it;
- resume after approval without repeating settled analysis; and
- return stable artifact pointers plus enough readback evidence to verify publication.

The source retains every content-approval gate in its own workflow. `scope-it-remake` owns mutation approval for the exact writes shown in the current checkpoint. Classify its outputs and complete the frontier through [artifacts.md](artifacts.md).

## Scope source

Input:

- Destination and settled decisions;
- relevant repository or product evidence;
- the Map home or its approved proposed identity;
- whether the Scope belongs in a Map-home section or remains in its own artifact with a Map pointer; and
- the intended publication environment.

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

- the approved scope artifact;
- the Map home;
- tracker capabilities; and
- delivery constraints already settled on the map.

Draft output for every ticket:

- title;
- end-to-end outcome;
- acceptance evidence;
- native blockers; and
- whether it is independently executable and verifiable.

Publication output:

- linked ticket titles;
- stable identities; and
- readback of their approved content and Map-home containment.

Ticket count follows the source's end-to-end slicing judgment. One cohesive ticket stays on the Delivery Map home; multiple tickets become children of the Map home when the tracker supports native containment.
