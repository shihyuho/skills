---
name: artifact-anatomy
description: Defines where spec-driven working artifacts (the spec, plan, and task list) live on disk and how they are numbered, scoped, and resolved, so multiple specs can run in parallel without overwriting one another. Use when a spec/plan/build workflow needs to create, locate, or update these artifacts, when more than one spec or feature is in progress at once, or when a draft spec gets an issue number assigned. Governs only where artifacts live and how they are addressed, not what goes in them.
license: MIT
---

# Artifact Anatomy

## Overview

Spec-driven workflows produce working artifacts — a spec, a plan, and a task list — that are living documents kept in version control as the shared source of truth between the human and the agent. This skill defines their on-disk layout, numbering namespace, and resolution rules so that several specs can be worked **in parallel**, each scoped to its own numbered feature directory, instead of overwriting a single global spec file at the repo root.

It governs the *where* and the *naming*. It does not govern the *what*: writing the spec content and breaking work into tasks are separate concerns handled by your spec and planning workflows.

> **Workflow-agnostic.** Examples use the common `SPEC.md` + `tasks/plan.md` + `tasks/todo.md` artifact set, but the same layout applies to whatever spec/plan/task files your toolchain produces — substitute your own filenames.

## When to Use

- A new spec is created → decide the feature directory and its number
- A plan or build step needs to locate the artifacts for the feature being worked on
- More than one spec or feature is in progress at the same time
- A draft spec later gets an issue-tracker number and needs to be linked

**When NOT to use:** Deciding what content goes in the spec, plan, or task list. This skill only decides *where* artifacts live and *how* they are addressed.

## Layout

One feature per numbered directory under `docs/specs/`. The directory contents are **unchanged** from a single-spec layout — same filenames, same content — only their location moves:

```
docs/specs/
  142-payment-retry/
    SPEC.md
    tasks/
      plan.md
      todo.md
  draft-search-revamp/
    SPEC.md
    tasks/
      plan.md
      todo.md
```

The artifact filenames keep their exact names and structure. The only new thing is the `docs/specs/<id>-<slug>/` wrapper that scopes them to one feature.

## Numbering namespace

The `<id>` prefix marks where the work is tracked, and the two forms are kept strictly separate so a glance at `docs/specs/` is unambiguous:

- **Bare number** (`142-payment-retry`) — a real issue-tracker issue number. Reserved **exclusively** for issue numbers.
- **`draft-` prefix** (`draft-search-revamp`) — no issue yet; a local draft. Never give a local-only spec a bare number.

When a draft later gets an issue number, rename the directory in one step:

```
git mv docs/specs/draft-search-revamp docs/specs/160-search-revamp
```

This keeps the guarantee that **a bare number always maps to a tracker issue**, while letting work start before any issue exists.

## Assigning the id (when a spec is created)

Resolve `<id>` in order, stopping at the first that applies:

1. **An issue reference is supplied** — passed as an argument, or `#142` mentioned in context → use that number: `docs/specs/142-payment-retry/`.
2. **No reference** — ask the user once: *"Does this spec have a tracker issue? Give me the number, or I'll start it as a draft."*
3. **User has none or declines** → `docs/specs/draft-<slug>/`.

Do **not** auto-detect the issue tracker (scanning branch names, running `gh issue list`). That is out of scope — rely on the supplied reference plus the single question.

## Resolving the target directory (when planning or building)

1. **An id or slug is supplied** → use `docs/specs/<that>/`.
2. **Nothing supplied** → scan `docs/specs/*/`:
   - exactly one feature directory → use it
   - multiple → list them and ask which feature to act on (never guess)
   - none → fall back to a legacy root spec file + `tasks/` if the project still uses one (see Backward compatibility)

## Backward compatibility

A root spec file (e.g. `SPEC.md`) with its `tasks/` directory is treated as the single, unnumbered default feature. Projects that have only ever had one spec keep working with no change; the numbered `docs/specs/<id>-<slug>/` layout is opt-in and only needed once a second spec enters progress.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "There's only one spec, a root spec file is fine." | Today there's one. The moment a second spec starts, the root spec collides and one overwrites the other. The numbered directory costs nothing now and prevents the collision later. |
| "I'll just give the local spec a number, close enough." | Bare numbers are reserved for real issue numbers. A fake number breaks the one guarantee the namespace provides — that a number maps to a tracker issue. Use `draft-`. |
| "I can tell which feature they mean." | When multiple `docs/specs/*` directories exist, guessing risks editing the wrong feature's artifacts. List them and ask. |
| "I'll auto-detect the issue from the branch name." | Auto-detection is explicitly out of scope and adds fragile coupling. Ask the one question instead. |

## Red Flags

- Writing the spec / `tasks/` to the repo root while another spec is already in progress
- A bare-number directory (`docs/specs/3-foo/`) that has no corresponding tracker issue
- Planning or building against a guessed feature directory when several exist instead of asking
- Renaming or moving files *inside* the feature directory (the filenames are fixed)

## Verification

After resolving artifact locations, confirm:

- [ ] Each in-progress spec has its own `docs/specs/<id>-<slug>/` directory
- [ ] Bare-number prefixes map to real issue numbers; local drafts use `draft-`
- [ ] Planning and building operated on the intended feature directory (asked when ambiguous)
- [ ] Filenames inside the directory are unchanged
