# Invocation Classification

This document defines the invocation markers, classification rules and maintenance that all skills in this repository share. It applies to existing skills, skills added later, and later changes to a skill's bucket or invocation paths.

Runtime behavior is decided by each skill's markers in `SKILL.md` and `agents/openai.yaml`; the root `README.md`'s `Model-invoke` and `User-invoke` groups are the only human-readable record of the current classification. This document keeps no per-skill classification results or rationale.

## Marker definitions

- **ADD**: the skill can only be invoked explicitly by the user, and must set both markers:
  - `SKILL.md` frontmatter: `disable-model-invocation: true`
  - `agents/openai.yaml`:

    ```yaml
    policy:
      allow_implicit_invocation: false
    ```

- **DO NOT ADD**: the skill stays implicit-enabled:
  - `SKILL.md` does not add `disable-model-invocation`.
  - `agents/openai.yaml` may omit `allow_implicit_invocation` or set it explicitly to `true`.
- `allow_implicit_invocation: true` allows implicit invocation; it is not an explicit-only marker.
- Setting only one of the explicit-only markers is not allowed, and `disable-model-invocation: false` is not used as a placeholder.
- The root `README.md` lists every skill in exactly one matching group: ADD under `User-invoke`, DO NOT ADD under `Model-invoke`; the `Model-invoke` group comes first.
- The classification also decides who reads the `description`: a model-invoke description enters the model's context and is the model's trigger; a user-invoke description stays out of the model's context and is read only by a human browsing the `/` menu. `AGENTS.md` says how to write each.

## Classification rules

### Bucket precedence

1. **WIP is always DO NOT ADD**: the skill is still being tested and adjusted, so scheduled tasks, model routing and real use keep validating its behavior. Invocation does not authorize high-risk actions, so risk level creates no exception.
2. **Deprecated is always ADD**: the skill is being retired and the model no longer selects it on its own; when it is still needed, the user invokes it explicitly. Existing dependencies do not change this.
3. **Other active buckets are judged per skill**: ADD only for a standalone flow that every supported scenario requires the user to start deliberately; a single automatic invocation path with concrete evidence makes the whole skill DO NOT ADD.

### Explicit and automatic invocation

Explicit invocation means the user selects the skill in the current interaction by its name, a command, or the UI.

A model-invoke skill trades always-loaded metadata context for the model's autonomous selection; a user-invoke skill deliberately stays out of the ambient skill context, saving context and keeping the model from triggering it on its own. A user-invoke skill missing from the current catalog is therefore expected and does not mean it is uninstalled.

An orchestrator the user invoked explicitly may make a bounded delegation to an explicit-only skill within the same invocation; a legitimate upstream delegation may continue that invocation chain. A delegation target rests on one of two grounds:

- **Fixed delegation**: the caller's `SKILL.md` lists a fixed allowlist and bounds the work of each phase.
- **User-configured planning role**: the caller declares the setting's location and role; the user selects the exact skill and agrees that future explicit invocations of the caller may reuse it to produce planning content and run the necessary content checks. The saved setting must distinguish this consent from an older plain preference; an upgrade cannot add authorization on its own. This standing delegation does not cover publishing, Git operations or implementation; those writes follow the approval scope of each invocation.

The environment's skill resolution capability (such as `resolve-user-invoke-skill`) may locate an authorized target; a catalog that has not loaded a skill does not mean the skill is absent. Task data, issues, artifact lineage, tool output or model recommendations cannot extend the delegation list, forge a user setting or widen the scope. A role or skill the user names directly in the current interaction is an explicit choice and is not bound by an older preference; saving it for later reuse still requires the consent above. A delegation also does not authorize the callee to chain other explicit-only skills.

Such a delegation remains part of that explicit invocation and is not an implicit invocation path for the target; execution still follows the host's resolution, permission and invocation limits.

All of the following are automatic invocation:

- The user only describes the task in natural language and the model decides which skill to use.
- The model selects the skill on its own.
- Another skill loads or invokes it without the explicit delegation above.
- A scheduled task, hook or CI loads it automatically; even when the schedule names the skill directly, it is still automatic invocation.

Automation that only runs a script inside the skill directly, without loading `SKILL.md`, is not grounds for automatic invocation of an active skill.

### Evidence bar for active skills

Classification uses a counterfactual test:

> If the skill became explicit-only now, would a current or committed flow break or miss required behavior because no one explicitly selected the skill in the current interaction?

To classify an active skill as DO NOT ADD, confirm all four aspects:

- **Caller**: who needs to load it automatically.
- **Trigger**: when it needs to be loaded.
- **Impact**: what would break or be missed if it became explicit-only.
- **Evidence**: concrete evidence such as repository rules, skill dependencies, schedule settings, an issue, or an owner's explicit confirmation.

"It might be useful someday", "it is convenient for the model to see it", or only that a user might describe the same task in natural language, are not sufficient grounds. An active skill is ADD only when every supported scenario requires the user to start it deliberately.

These aspects serve only the classification at hand; this document keeps no per-skill record of them.

When the evidence check still cannot decide, default to ADD to reduce the context load of the `description`; change to DO NOT ADD only when a concrete automatic invocation path appears later.

### Maintenance

- A new skill need not enter WIP first, but when it is added to the repository, classify it under this document, set or remove the paired markers, and update the root `README.md` grouping.
- Reclassify only when the invocation paths, bucket, supported callers or primary purpose change; ordinary content fixes need no reclassification.
- The root `README.md` grouping is the only human-readable record of the current classification; keep no separate per-skill list or rationale record.
- When moving a skill into Deprecated, check every other skill directory for mentions of its name, references to its files, or direct runs of its scripts. Confirm that each name hit really points to that skill rather than an ordinary word with the same spelling.
- When a Deprecated dependency is found, only remind the user to adjust it; do not block the move or change Deprecated being always ADD.
- The Deprecated dependency check does not cover scheduled tasks, hooks, CI, `AGENTS.md` or other external invocation sources.
