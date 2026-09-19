---
name: sdkman
description: Use when the requested action runs Java/JDK, Maven/mvn, Gradle, Ant, Tomcat, Kotlin, or another SDKMAN-supported tool; applies .sdkmanrc; investigates an actual execution failure involving those tools; or queries or changes SDKMAN versions, installations, defaults, or configuration. For documentation-only edits, leave this skill unloaded.
license: MIT
---

# sdkman

Use the development-tool environment required by the task, and manage host tool versions through SDKMAN.

## Run or troubleshoot a tool

Before a workload, read [Environment details](references/environment.md) to find applicable declarations, including `.sdkmanrc`, within its worktree. Apply them through SDKMAN before execution, even if the current environment appears compatible. An explicit candidate request overrides that candidate's project declaration while retaining the other applicable declarations.

Otherwise, run the requested command with the current configuration. If it fails, consider tool-version or runtime compatibility alongside other causes; use the failing process and its requirements to decide whether a version change is needed.

For Maven or Gradle, read [JVM build ownership](references/jvm-build-ownership.md) to distinguish the launcher, wrapper, daemon, and task toolchains. Compiler compatibility settings alone do not require a shell switch.

## Manage versions with SDKMAN

SDKMAN is this host's version manager for its supported tools. Apply a required command environment with `sdk use` or `sdk env`; `sdk home` only locates an installation. Use the native CLI for installed versions and defaults as well. If SDKMAN cannot apply the required environment, resolve that obstacle before starting the dependent command.

Use `sdk help <command>` and the [official usage guide](https://sdkman.io/usage/) for command details. For activation, installation, project-environment work, or offline operations, read [Environment details](references/environment.md). Load `${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh` only when `sdk` is unavailable and initialization fits the network constraints.

| Need | Commands |
| --- | --- |
| Inspect versions and installed locations | `sdk current [candidate]`, `sdk list <candidate>`, `sdk home <candidate> <id>` |
| Select an environment for a command | `sdk use <candidate> <id>`, `sdk env` |
| Change installed tools or defaults | `sdk install`, `sdk uninstall`, `sdk default` |
| Maintain project environments | `sdk env init`, `sdk env install` |
| Change global SDKMAN configuration | `sdk config` |

Match the operation to the request: a version query needs no switch or workload. Persistent changes, including installation, removal, defaults, global configuration such as auto-env, and project-file edits, require an explicit request for that action. Apply existing authorization without asking again, keeping unrelated settings intact.

Preserve exact candidate IDs and vendor choices. For a broader version request, use a matching active/default or sole installed version; ask when a meaningful choice remains. A missing requested version needs installation authorization rather than an unrequested substitute.

## Apply the requested change

For a workload, keep initialization, every activation, and the original command in one shell. Gate each step on the previous step's success, including initialization: guard a needed `source` with `source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh" || exit "$?"`, then chain activations and the original command with `&&` or explicit status checks. Preserve the command's cwd and exit status; a setup failure leaves it unstarted.

For a persistent change, verify the requested installation, default, or configuration with current CLI or file evidence. Recheck the environment before any dependent workload. Leave build/test diagnosis to the original task unless the failure identifies an SDKMAN-owned requirement.
