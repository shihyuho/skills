# Environment details

## Project environments

Start at the workload directory and use the nearest `.sdkmanrc` inside its current Git worktree. Stop upward lookup at `git rev-parse --show-toplevel`; outside Git, use the selected directory as the boundary. A standalone query or default change does not inherit a project environment merely because one exists nearby.

Read `.sdkmanrc` as candidate/version data, never as shell code. Resolve malformed entries or conflicting duplicate candidates before activation. Check every applicable entry, including any explicit override; `sdk home <candidate> <exact-id>` verifies an installed location. This avoids `sdk env` changing one candidate before discovering another is missing.

Use `sdk env` from the file's directory when its full contents apply unchanged, then restore the workload cwd before running the command. Use individual `sdk use` operations for overrides or when a wrapper/toolchain owns some declarations. Keep unrelated files and candidate versions intact.

## Installed candidates and defaults

`sdk list <candidate>` distinguishes available, installed, and current versions; availability in the catalog is not proof of installation. `sdk current` and `sdk home` provide focused local evidence. Match exact IDs, including vendor suffixes, against installed tools.

SDKMAN can create a default when `sdk use` encounters a candidate without `current`. Before activation, check that candidate's `current` entry under `${SDKMAN_DIR:-$HOME/.sdkman}/candidates/`. If native activation would create a default, obtain authorization for that additional change before proceeding with the command. Resolve broken or unexpected links before proceeding.

For an authorized installation, check the CLI's default-selection behavior and preserve the prior default state, including having no default. Some versions automatically select the first installed version; if the CLI cannot keep the requested default state, resolve that additional change with the user before installation. Recheck installed state afterward.

## Offline work

SDKMAN startup and catalog queries may contact its services; availability/offline settings do not prove strict network isolation. For a strict no-network request, establish that the needed SDKMAN initialization and commands can run locally before using them. If that cannot be established, explain the constraint and leave the dependent workload unstarted.

Wrappers, dependencies, plugins, and toolchains have their own download behavior. Use their offline controls and cached inputs as required by the workload; an installed SDK alone does not make a build offline. Authorized SDKMAN installation may download and execute installation hooks.
