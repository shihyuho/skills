---
name: sdkman
description: Manage development tools and runtimes with SDKMAN. Use for SDKMAN version queries, installation, removal, defaults, project environments, or a command whose applicable .sdkmanrc or diagnosed runtime requirement needs SDKMAN.
license: MIT
---

# sdkman

Manage development tools and execution environments with SDKMAN according to the task's needs.

## Choose the operation

Use the native CLI; `sdk help <command>` and the [official usage guide](https://sdkman.io/usage/) supply command details. Before activation, installation, project-environment work, or offline operations, read [Environment details](references/environment.md). Load `${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh` only when `sdk` is unavailable and initialization fits the network constraints.

| Need | Commands |
| --- | --- |
| Inspect versions and installed locations | `sdk current [candidate]`, `sdk list <candidate>`, `sdk home <candidate> <id>` |
| Select an environment for a command | `sdk use <candidate> <id>`, `sdk env` |
| Change installed tools or defaults | `sdk install`, `sdk uninstall`, `sdk default` |
| Maintain project environments | `sdk env init`, `sdk env install` |
| Change global SDKMAN configuration | `sdk config` |

Match the operation to the request: a version query needs no switch or workload; a one-command switch stays local to that shell. Persistent changes, including installation, removal, defaults, global configuration such as auto-env, and project-file edits, require an explicit request for that action. Apply existing authorization without asking again, keeping unrelated settings intact.

Preserve exact candidate IDs and vendor choices. For a broader version request, use a matching active/default or sole installed version; ask when a meaningful choice remains. A missing requested version needs installation authorization rather than an unrequested substitute.

## Resolve the environment

For a command, preserve its directory and resolve the complete applicable environment before activation. An explicit candidate request overrides that candidate's project declaration while retaining the other applicable declarations.

Before choosing versions for a Maven or Gradle command, read [JVM build ownership](references/jvm-build-ownership.md). The actual launcher and configured toolchains determine which requirements belong to SDKMAN; compiler compatibility settings alone do not require a shell switch.

## Apply the requested change

For a workload, keep initialization, every activation, and the original command in one shell. Gate each step on the previous step's success, including initialization: guard a needed `source` with `source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh" || exit "$?"`, then chain activations and the original command with `&&` or explicit status checks. Preserve the command's cwd and exit status; a setup failure leaves it unstarted.

For a persistent change, verify the requested installation, default, or configuration with current CLI or file evidence. Recheck the environment before any dependent workload. Leave build/test diagnosis to the original task unless the failure identifies an SDKMAN-owned requirement.
