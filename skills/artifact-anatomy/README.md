# Artifact Anatomy

Defines **where** spec-driven working artifacts — the spec, the plan, and the task list — live on disk, and how they are numbered, scoped, and resolved, so several specs can be worked in parallel without overwriting a single root file.

It governs only the layout and the naming, never the contents:

- **Layout** — one feature per numbered directory under `specs/<id>-<slug>/`; the artifact filenames inside are unchanged from a single-spec setup, only their location moves.
- **Numbering** — a bare number (`142-payment-retry`) is reserved exclusively for a real issue-tracker number; a `draft-` prefix (`draft-search-revamp`) marks a local-only spec with no issue yet. A draft is promoted with a single `git mv` once its issue exists.
- **Assigning** — resolve the id from a supplied issue reference, else ask once, else fall back to `draft-`. No auto-detecting the tracker.
- **Resolving** — locate the target directory from a supplied id/slug, else the lone `specs/*` directory, else ask which feature when several exist; never guess.
- **Backward compatible** — a legacy root spec file with its `tasks/` keeps working as the single default feature; the numbered layout is opt-in once a second spec starts.

Pairs with whatever spec/plan/task workflow your toolchain uses — substitute your own filenames; the addressing rules stay the same.

## Installation

```bash
npx skills add shihyuho/skills --skill artifact-anatomy -g
```
