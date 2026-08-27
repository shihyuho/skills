# Planning sources

`scope-it-remake` owns the Delivery Map, frontier order, mutation boundary, reconciliation, and readback. An active **source** produces new scope or ticket content. A completed **artifact** may satisfy a frontier without its producer being installed or invocable.

## Selection

When new content is required, resolve an active source in this order:

1. A valid `--scope-source` or `--ticket-source` flag from the current invocation.
2. The source already recorded on the current Delivery Map.
3. A compatible source explicitly invoked by the user in the current request.
4. The repository's stored source preference.
5. The stored global source preference.
6. A compatible model-invoked source required by repository guidance.

After exhausting this order, stop the current frontier. Report whether no compatible source was found or the selected source is unavailable, recommend one compatible source when evidence supports it, and ask the user which skill should produce the missing artifact. Do not draft the missing Scope or Tickets, update the map, or write source preferences before the user answers.

`to-spec` and `to-tickets` are fixed optional compatibility profiles: an explicit `scope-it-remake` invocation may delegate to either when installed. They are not installation requirements. Other skills participate through the same contracts below. A source recorded on a map is lineage, not fresh authorization. An exact source flag is the user's current workflow configuration and may select an explicit-only source. Without a flag, consume its accepted artifact or ask the user to invoke it alongside `scope-it-remake`.

Record the selected source names on the map so later sessions preserve the content lineage. Replace a source already recorded on the current map only through a valid flag or a user answer after reporting that source as unavailable or incompatible. A compatible source explicitly invoked in the current request overrides stored preferences for a new map without rewriting those preferences.

## Stored preference

Source selection changes future behavior and cannot be reconstructed without user input, so store it as config rather than cache. Use `~/.config/softleader/agent-skills` as the config root. Store preferences in:

```text
~/.config/softleader/agent-skills/scope-it-remake/sources.json
```

Use this minimal schema and preserve unknown fields:

```json
{
  "schema_version": 1,
  "global": {
    "scope": "<canonical-name>",
    "tickets": "<canonical-name>"
  },
  "repositories": {
    "<repository-identity>": {
      "scope": "<canonical-name>",
      "tickets": "<canonical-name>"
    }
  }
}
```

Store only roles whose source the user has selected; omit an unresolved `scope` or `tickets` key until its frontier resolves it. Treat `global` as the reusable default and `repositories` as sparse overrides.

Prefer the normalized `origin` repository identity so worktrees share one preference: retain only host and repository path, removing scheme, user info, query, fragment, and a trailing `.git`. When no remote identity exists, use the absolute repository root. Do not store credentials, prompts, or artifact content.

When a role has no repository or global preference, include writing the user's first approved selection to `global` in the frontier's **Writes**. On later invocations, reuse the map, repository override, or global preference without asking. A valid source flag overrides the corresponding role for the current map and writes a repository override after approval; a partial override preserves the other role and the global defaults. Update `global` instead only when the user explicitly changes the default for future repositories. A configured repository preference shadows `global`; when the selected repository or global source is unavailable or incompatible, report it, show one replacement recommendation, and wait for the user's answer rather than silently falling through. After approval, update the map and the applicable preference level. An unusable config root is an error rather than a reason to fall back to another path.

Accepting a completed artifact does not replace the stored producer preference. Preference state chooses how to make future content; artifact state records what this map actually consumed. Apply [artifacts.md](artifacts.md) when completed planning material is present.

## Active producer contract

A compatible source can:

- produce a draft without tracker or repository mutation;
- declare the publication environment and tracker capabilities when it owns that choice;
- separate unresolved decisions from its recommended content;
- name every write it proposes before performing it;
- resume after approval without repeating settled analysis; and
- return stable artifact pointers plus enough readback evidence to verify publication.

The source retains every content-approval gate in its own workflow. `scope-it-remake` owns mutation approval for the exact writes shown in the current checkpoint. Classify its outputs and complete the frontier through [artifacts.md](artifacts.md).

A tracker choice declared by a source belongs to that source's publication contract; it is not a `scope-it-remake` default. Reconcile it with any starting item and repository guidance. When applicable sources disagree, keep the Map home unresolved, surface the contradiction, and recommend one home rather than creating parallel planning roots.

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
- the Map home or its approved proposed identity;
- tracker context already fixed by a starting item or repository guidance; and
- delivery constraints already settled on the map.

Draft output for every ticket:

- tracker and placement recommendation when the publication environment is not already fixed;
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
