---
name: sdkman
description: Use when the task runs a Java/JDK, Maven/mvn, Gradle, Ant, Tomcat, Kotlin, or other SDKMAN-supported workload; applies .sdkmanrc; investigates an actual execution failure of such a workload; or queries or changes SDKMAN versions, installations, defaults, or configuration. For documentation-only edits, leave this skill unloaded.
license: MIT
---

# sdkman

Run Java, Maven, Gradle, and other SDKMAN-managed tools in the environment the project declares, and manage host tool versions through SDKMAN. An agent's shell carries no reliable SDKMAN state: auto-env may not fire, and an activation does not survive into the next tool call. So treat each run as a workload, with SDKMAN initialization, every activation, and the original command in one shell invocation, and apply an applicable declaration there even when the current environment looks compatible.

Before any activation or installation, read [Environment details](references/environment.md). It locates the applicable `.sdkmanrc`, checks installed IDs, catches native operations that change defaults, and covers offline limits.

## Choose versions

Preserve exact candidate IDs and vendors. For a broader version request, use the matching active/default or sole installed version, and ask when a meaningful choice remains. A missing version needs installation authorization rather than a substitute.

## Run a workload

1. **Resolve the environment.** Start from the applicable `.sdkmanrc` within the workload's worktree. An explicit candidate request overrides that candidate's declaration and keeps the rest. For Maven or Gradle, read [JVM build ownership](references/jvm-build-ownership.md): a wrapper, daemon criteria, or toolchain selects its own version, so SDKMAN supplies only the layers the shell selects.
2. **Confirm every required ID before applying any.** When SDKMAN cannot apply the environment, report that obstacle and leave the command unstarted. SDKMAN is this host's version manager: apply environments with `sdk use` or `sdk env`, since a hand-set home or `PATH` skips the checks above. `sdk home` locates an installation; it does not activate one.
3. **Run it as one shell.** Load `${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh` only when `sdk` is unavailable and initialization fits the network constraints, guarded as `source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh" || exit "$?"`. Chain each activation and the original command with `&&` or explicit status checks. Keep the command's cwd and exit status; a setup failure leaves it unstarted.

With no applicable declaration or request, the workload runs under the current configuration. When it fails, weigh tool-version and runtime compatibility alongside other causes, and resolve a version requirement at the layer that needs it. A failure after the workload starts belongs to the original task unless it identifies an SDKMAN-owned requirement.

## Change host state

A version query answers from SDKMAN evidence, with no activation or workload. Persistent changes, including installation, removal, defaults, global configuration such as auto-env, and project files, follow an explicit request for that action. Carry out that request without asking again, and keep unrelated settings intact.

Verify each persistent change with current CLI or file evidence, and recheck the environment before a dependent workload. For command details, use `sdk help <command>` or the [official usage guide](https://sdkman.io/usage/).
