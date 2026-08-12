---
name: sdkman
description: Switch an SDKMAN-managed JDK, Kotlin, Gradle, Maven, or other candidate for a command. Use for a requested version or vendor, `.sdkmanrc`, or an actual Java version failure (`UnsupportedClassVersionError`, invalid target release, class-file version errors); diagnose the failing layer because compiler targets and healthy build toolchains do not require a shell-JDK switch.
license: MIT
---

# sdkman

SDKMAN exposes `sdk` as a shell function. A version selected with `sdk use` affects only that shell, while agent shell tool calls normally start fresh shells. Keep the switch and the command that needs it in the same shell invocation.

## Choose whether to switch

Use this decision order:

1. Honor the candidate, version, and vendor the user requested.
2. If the repository has `.sdkmanrc`, follow it with `sdk env`.
3. Otherwise, prefer the repository's `mvnw` or `gradlew` so the project selects its build-tool version.
4. On a version-mismatch failure, identify whether it comes from the Maven／Gradle launcher, a build toolchain, a compile／test task, or the application runtime. Switch the shell JDK only when the launcher or a legacy path actually depends on it.

Do not infer an exact shell JDK merely from compiler compatibility settings such as Maven's `maven.compiler.release`, `source`/`target`, or Gradle's `options.release`／`sourceCompatibility`. A newer JDK can compile an older release. Likewise, let a configured Maven or Gradle toolchain select its own JDK unless the failure is in the launcher or the build proves the required toolchain is unavailable.

For Gradle, distinguish the Client JVM, Daemon JVM, and task toolchain. A shell switch changes the Client launch environment but does not necessarily override Daemon JVM criteria or the JDK selected for compile／test tasks.

Treat `.java-version` as evidence of project intent, not proof that SDKMAN owns the environment; respect another configured version manager.

## Confirm SDKMAN and installed candidates

Only perform these checks when a switch is needed:

```bash
[ -s "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh" ]
ls "${SDKMAN_DIR:-$HOME/.sdkman}/candidates/<candidate>/"
```

Use an exact installed id, including its vendor suffix. If SDKMAN is absent, report that the requested switch cannot be performed through SDKMAN and inspect the project's existing version-manager setup before proposing an alternative.

## Run with an ephemeral version

For a one-command switch, load SDKMAN only when necessary and run the workload in the same invocation:

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
sdk use java <installed-jdk-id> && <command>
```

This is the default because it validates the id and SDKMAN defines `use` as a current-shell switch. Replace `java` with another SDKMAN candidate when requested. SDKMAN may create a missing candidate `current` link on first use; when preserving the absence of a default matters, use the validated direct-environment fallback instead.

For `.sdkmanrc`, enter the project and keep `sdk env` with the workload:

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
cd /path/to/project && sdk env && <command>
```

If `.sdkmanrc` names an uninstalled candidate, stop and ask before installing it.

## Persistent changes and installs

Use `sdk default <candidate> <id>` only when the user explicitly asks to change future shells. Use `sdk install <candidate> <id>` or `sdk env install` only after the user approves the persistent download and every exact candidate id, including vendor when applicable. Leave the user's auto-env setting unchanged.

When the requested id is missing:

1. Show compatible installed ids.
2. Offer those as alternatives without silently changing vendors.
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

The requested workload must start only after the selected candidate succeeds in the same shell invocation. Preserve the original workload command and its exit status. Leave the user's explicit default, installed candidates, and auto-env setting unchanged unless the user authorized that persistent change.
