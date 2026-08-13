---
name: sdkman
description: Switch an SDKMAN-managed JDK, Kotlin, Gradle, Maven, or other candidate for a command. Use for a requested version or vendor, `.sdkmanrc`, or an actual Java version failure (`UnsupportedClassVersionError`, invalid target release, class-file version errors); diagnose the failing layer because compiler targets and healthy build toolchains do not require a shell-JDK switch.
license: MIT
---

# sdkman

SDKMAN exposes `sdk` as a shell function. A version selected with `sdk use` affects only that shell, while agent shell tool calls normally start fresh shells. Keep the switch and the command that needs it in the same shell invocation.

## Resolve the workload context

Before each workload invocation, resolve the directory where the command must run. In Git, treat its current worktree as the environment boundary: from the workload directory, look upward for the nearest `.sdkmanrc`, stopping at that worktree's root. Outside Git, stop at the explicitly selected project directory. Re-check the current filesystem; a prior shell, another checkout, or pre-compaction context is not evidence that this project has the file.

Follow these invariants:

- Invoke `sdk env` only after confirming the selected `.sdkmanrc` exists inside the workload's environment boundary.
- Do not read or copy `.sdkmanrc` from a sibling checkout, the originating checkout, or another worktree.
- Preserve the workload's original directory; environment discovery must not change the command's cwd.

## Choose the execution path

Use the first matching row:

| Evidence | Action |
| --- | --- |
| The user requested an exact SDKMAN id | Use that exact installed id with `sdk use`. |
| The user requested a candidate, version, or vendor constraint | Resolve one installed id with the evidence order below, then use `sdk use`. |
| The current worktree contains an applicable `.sdkmanrc` | Follow its exact declarations with `sdk env`. |
| No `.sdkmanrc`; the repository has `mvnw` or `gradlew` and its launcher works | Run the wrapper and let the build select its toolchains. |
| A wrapper launcher probe cannot start because the shell JDK is missing or incompatible | Select an evidence-backed installed JDK for the launcher, then run the unchanged workload command. |
| A compile, test, daemon, toolchain, or application runtime reports a mismatch | Diagnose that failing layer; switch the shell candidate only when that layer depends on it. |

The absence of `.sdkmanrc` is a normal branch, not an `sdk env` failure. Use the wrapper or diagnose the launcher instead of invoking `sdk env` speculatively.

## Select an installed candidate

An exact id from the user or `.sdkmanrc`, including its vendor suffix, is a reproducibility contract. If it is unavailable, stop and ask whether to install the exact id; do not substitute the same major, another patch, or another vendor. Mention installed alternatives only as information, not as a way to bypass the contract; using one requires the user to explicitly override the requested environment.

When a shell JDK is actually required but the project provides only a major-version constraint, select with this evidence order:

1. A compatible JDK already active in the workload shell.
2. SDKMAN's current or configured default selection, only when it resolves to one exact installed id matching the constraint.
3. The sole compatible installed candidate.
4. If multiple candidates remain, ask for the vendor or exact id.

If no compatible candidate is installed, ask the user to choose an exact id and vendor before installation. Use `sdk list <candidate>` only when remote options are needed; do not infer a remote vendor from a major-version constraint.

Treat tracked `.java-version` and vendor or runtime constraints as project intent, but respect the version manager that owns them. Do not turn compiler compatibility settings into a vendor choice or proof that SDKMAN owns the environment.

## Diagnose Java builds

Do not infer a shell-JDK switch merely from compiler compatibility settings such as Maven's `maven.compiler.release`, `source`/`target`, or Gradle's `options.release`／`sourceCompatibility`. A newer JDK can compile an older release. Let a configured Maven or Gradle toolchain select its own JDK unless the failure is in the launcher or the build proves the required toolchain is unavailable.

When Java availability or launcher compatibility is unknown, use a non-workload launcher probe such as `./mvnw -version` or `./gradlew --version`. A failed probe means environment setup failed; it is not a failed test or build. Start the user's original workload only after the launcher is ready.

For Gradle, distinguish the Client JVM, Daemon JVM, and task toolchain. A shell switch changes the Client launch environment but does not necessarily override Daemon JVM criteria or the JDK selected for compile／test tasks.

## Confirm SDKMAN and installed candidates

Only perform these checks when a switch is needed:

```bash
[ -s "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh" ]
ls "${SDKMAN_DIR:-$HOME/.sdkman}/candidates/<candidate>/"
```

If SDKMAN is absent, report that the requested switch cannot be performed through SDKMAN and inspect the project's existing version-manager setup before proposing an alternative.

## Run with an ephemeral version

For a one-command switch, load SDKMAN only when necessary and run the workload in the same invocation:

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
sdk use java <installed-jdk-id> && <command>
```

This is the default because it validates the id and SDKMAN defines `use` as a current-shell switch. Replace `java` with another SDKMAN candidate when requested. SDKMAN may create a missing candidate `current` link on first use; when preserving the absence of that link matters, use the validated direct-environment fallback instead.

For `.sdkmanrc`, validate the file, load it from its directory, return to the workload directory, and run the command in the same shell:

```bash
workload_dir=$PWD
sdkmanrc_dir=/validated/path/inside/current/worktree
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
test -f "$sdkmanrc_dir/.sdkmanrc" &&
  cd "$sdkmanrc_dir" &&
  sdk env &&
  cd "$workload_dir" &&
  <command>
```

If `.sdkmanrc` names an uninstalled candidate, stop and ask before installing it.

## Persistent changes and installs

Use `sdk default <candidate> <id>` only when the user explicitly asks to change future shells. Use `sdk install <candidate> <id>` or `sdk env install` only after the user approves the persistent download and every exact candidate id, including vendor when applicable. Leave the user's auto-env setting unchanged.

Create, copy, or commit `.sdkmanrc` only when the user explicitly asks to establish a persistent project contract. Compiler settings alone cannot determine its exact SDKMAN ids.

When a non-exact requested constraint has no installed match:

1. Show compatible installed ids.
2. Ask the user to choose an exact id without silently choosing a vendor.
3. Ask before running `sdk install`; use `sdk list <candidate>` only when remote options are needed.

## Direct environment fallback

Use direct environment variables only when the `sdk` function cannot be loaded or a detached process specifically requires them. Validate the candidate directory first, then set both the home variable and `PATH` in the same invocation:

```bash
sdkman_candidate_home="${SDKMAN_DIR:-$HOME/.sdkman}/candidates/java/<installed-jdk-id>"
test -d "$sdkman_candidate_home" &&
  export JAVA_HOME="$sdkman_candidate_home" &&
  export PATH="$JAVA_HOME/bin:$PATH" &&
  <command>
```

For other candidates, use the corresponding home variable: `GRADLE_HOME`, `MAVEN_HOME`, or `KOTLIN_HOME`.

## Completion check

The requested workload must start only after environment initialization and candidate validation succeed in the same shell invocation. Preserve the original workload command, cwd, and exit status.

Report which boundary failed:

- If discovery, `sdk env`, `sdk use`, or candidate validation fails, state that environment initialization failed and the workload did not start.
- If initialization succeeds and the workload fails, report the workload failure and its status without relabeling it as setup failure.

Leave the user's explicit default, installed candidates, project files, and auto-env setting unchanged unless the user authorized that persistent change.
