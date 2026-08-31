# Manual read-only inspection

Use this fallback only when `python3` or the bundled inspector is unavailable. Preserve the same outcomes: one complete environment plan, no network, and no persistent mutation.

## Boundary

Start from the workload directory. In Git, resolve `git -C <workload> rev-parse --show-toplevel` and stop every upward lookup at that worktree root. Outside Git, use the explicitly selected workload directory as the boundary. The first `.sdkmanrc` found within that boundary is the only applicable file.

Keep the original workload cwd. Do not inspect a sibling worktree, originating checkout, or parent repository.

## Applicable declarations

Read `.sdkmanrc` as `candidate=exact-id` data after removing comments and whitespace; never source it as shell. Reject malformed or duplicate declarations.

Apply the ownership mental model before validation:

- delegate Maven or Gradle to the project wrapper that launches it;
- delegate compile or test Java to a configured build toolchain;
- retain only candidates that SDKMAN must provide to the next command.

An explicit user constraint replaces the same candidate declaration and leaves the other applicable declarations intact.

## Installed evidence

For each applicable candidate, inspect only `${SDKMAN_DIR:-$HOME/.sdkman}/candidates/<candidate>/`:

- an exact ID must name an installed directory;
- a version or vendor constraint may select an active or `current` matching ID, or the sole matching installed ID;
- multiple matches require one user choice;
- a missing exact ID requires installation approval;
- a non-exact constraint with no match requires the user to choose an exact ID before installation.

Preserve the candidate ID and vendor suffix exactly. Validate all applicable candidates before activating any of them.

## Activation plan

Use `sdk use` only when the candidate already has a `current` entry that resolves inside its candidate directory. Treat a broken or escaping entry as an inspection error. If `current` is missing, plan direct environment activation with `<CANDIDATE>_HOME`, the exact installed candidate directory, and its `bin` directory on `PATH`.

The fallback ends when it has the equivalent of one verdict:

- ready complete plan;
- no SDKMAN-owned candidate;
- one consolidated choice;
- one consolidated persistent-action approval;
- inspection error.

Return to the main skill for interaction and execution.
