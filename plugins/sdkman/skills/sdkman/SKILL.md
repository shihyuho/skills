---
name: sdkman
description: Switch JDK, Kotlin, Gradle, Maven, or any SDKMAN-managed candidate when the user or a project demands a different version. Use when the user says "switch to Java 17", "run with JDK 21", "use Gradle 8.x", asks about JAVA_HOME, a build fails with UnsupportedClassVersionError or "class file has wrong version", or the repo has a `.sdkmanrc`. Also consult this proactively before compiling or running a Maven/Gradle/Kotlin project: check that the current `java -version` matches the JDK the project declares as its default (pom.xml `maven.compiler.release`, a Gradle toolchain, `.sdkmanrc`, `.java-version`) and align to it before building — while honoring any version the user explicitly asks for over that default. Operates on machines configured with SDKMAN (`$SDKMAN_DIR`, default `~/.sdkman`).
license: MIT
---

# SDKMAN Version Switching

[SDKMAN](https://sdkman.io/) manages parallel installs of JDKs and related tools under `$SDKMAN_DIR/candidates/<tool>/<version>/` (default `$SDKMAN_DIR` is `~/.sdkman`). This skill explains how to switch versions **correctly** from Bash tool calls — the naive approach silently does nothing.

> Throughout this document `$SDKMAN_DIR` means `${SDKMAN_DIR:-$HOME/.sdkman}`. Users may relocate the install via that env var; never hard-code `~/.sdkman`.

## Precondition

Before assuming this skill applies, confirm SDKMAN actually exists:

```bash
SDKMAN_DIR="${SDKMAN_DIR:-$HOME/.sdkman}"
[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ] && echo "sdkman ok" || echo "no sdkman"
```

If absent, say so and stop — don't invent paths. The machine may use system packages (`apt`, `brew`), `asdf`, `mise`, `jenv`, or a manual `JAVA_HOME` instead; ask the user which. SDKMAN itself runs on macOS, Linux, WSL, and POSIX shells on Windows (Git Bash, Cygwin, MSYS) — **not** native `cmd`/PowerShell.

## Quick Decision Guide

| Situation | Pattern |
|---|---|
| About to build/run a project — verify the JDK matches first | Check Before Building → A/D |
| Run one build/test under a specific JDK | A |
| Repo has `.sdkmanrc` | D (auto-follow) |
| Tool reads `JAVA_HOME` in a detached process | B |
| User asked for a permanent default change | C |
| Target version isn't installed | Stop, list options, ask |

## Default Policy

Unless the user **explicitly** asks otherwise:

- **Ephemeral, not persistent.** Use Pattern A (preferred) or B. They affect only the current Bash invocation. Never run `sdk default` (Pattern C) just because a user said "switch to Java 17" — that changes every future shell the user opens.
- **Check, don't blindly switch.** Before building, compare the project's target JDK with the current `java` (see *Check Before Building*); switch only on a real mismatch. If they already match, do nothing.
- **Install with confirmation only.** If a version isn't installed, stop and ask — do not auto-run `sdk install`. JDK downloads are hundreds of MB, persistent, and vendor-specific.
- **Follow `.sdkmanrc` without asking.** A `.sdkmanrc` is the repo author's explicit intent for anyone entering the repo. Honor it via Pattern D; only pause to ask if the declared version is missing.

## Aligning to the Project's Default JDK

A project's declared JDK is a **default, not a mandate**. When the user hasn't asked for a specific version, align the active `java` to that default before building so an unfamiliar repo builds as its author intended. But an explicit user request always wins — if the user says "test this under 21" while the project declares 17, run 21. Never force the project default over a version the user asked for.

To find the default, see what the build would use right now and compare it against what the project declares:

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
java -version    # the JDK the build would launch with
```

Where the project states its target JDK:

- **`.sdkmanrc`** — authoritative; follow it (Pattern D) and skip the rest.
- **`pom.xml`** — `<maven.compiler.release>`, `<maven.compiler.source>`/`<target>`, or a `<java.version>` property.
- **`build.gradle[.kts]`** — `languageVersion = JavaLanguageVersion.of(N)` (toolchain) or `sourceCompatibility`.
- **`.java-version`** — a bare version line (jenv/asdf convention).

If the current `java` already satisfies the default (or the user asked for the version that's active), **do nothing** — switching adds no value. Only when they differ and the user hasn't chosen otherwise, switch for that build via Pattern A (or D when a `.sdkmanrc` exists). Note a Gradle toolchain can locate or provision its own JDK, so a shell switch is only needed when that toolchain version isn't otherwise available to Gradle.

## Hooks (optional)

This skill ships two hooks. **Neither enforces a version** — a project default is overridable, so blocking a build would be wrong:

- **SessionStart (advisory nudge)** — in a JVM project on an SDKMAN machine, injects a one-line reminder to prefer `sdk` for version changes and to treat project-declared versions as defaults the user can override. Pure preference, never coercive.
- **PostToolUse (reactive, catch-all)** — scans build output for Java version-mismatch errors (`UnsupportedClassVersionError`, `invalid target release`, …) and prompts a switch + retry. Because it keys off the error, it covers builds wrapped in `make`, `just`, npm scripts, or custom shell scripts too — and only fires on a genuine failure, so it never second-guesses an intentional version choice.

If you installed the `sdkman` **plugin** in Claude Code, these hooks are already active (bundled in `hooks/hooks.json`). Otherwise — an `npx skills add` style install, or running under **Codex** (whose hook schema is the same) — follow [references/setup.md](references/setup.md) to wire them in. The same two scripts work unchanged on both runtimes.

## The One Thing That Trips Agents Up

`sdk` is a **shell function** exported by `$SDKMAN_DIR/bin/sdkman-init.sh`, not a binary on `PATH`. Two consequences:

1. **Every Bash tool call starts a fresh shell.** Running `sdk use java <id>` in one call does not affect the next — the function isn't defined there unless you re-source it.
2. **`sdk use` is shell-local.** Even interactively it only changes the current shell; nothing persists across shells.

So: do not run `sdk use` and expect the next tool call to inherit it. Pick a pattern below.

## Loading `sdk` Idempotently

Some agent runtimes pre-define `sdk` in each shell (Claude Code replays a shell snapshot that includes `.zshrc`/`.bashrc`-sourced SDKMAN init; login shells behave similarly). Plain non-interactive bash does not. The portable idiom that works in both cases — check first, source only if missing:

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
```

Re-sourcing when already loaded is safe but wasteful. Patterns A / C / D below use this check-first form.

## Pattern A — One-Shot Command (primary)

The default choice for running something under a specific version. `sdk use` validates the version exists, gives clear errors when it doesn't, and sets the full SDKMAN-managed environment (not just `JAVA_HOME`). Everything stays in a single Bash invocation so shell state persists across the statements:

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
sdk use java <jdk-id> && mvn test
```

Replace `<jdk-id>` with a value that is actually installed (see *Discovering What's Installed*). Self-contained, no global state left behind.

## Pattern B — Set JAVA_HOME Directly (fallback)

Every installed JDK lives at `$SDKMAN_DIR/candidates/java/<jdk-id>/`. Use this fallback when a tool reads `JAVA_HOME` in a detached way (long-running background daemon, a subprocess Pattern A's shell won't reach) or when the environment genuinely cannot load the `sdk` function:

```bash
export JAVA_HOME="${SDKMAN_DIR:-$HOME/.sdkman}/candidates/java/<jdk-id>"
export PATH="$JAVA_HOME/bin:$PATH"
java -version
```

Skips `sdk`'s validation — if you typo the id, this silently points at a nonexistent directory. Prefer A whenever possible.

## Pattern C — Change the User's Default (explicit request only)

`sdk default java <jdk-id>` rewrites `$SDKMAN_DIR/candidates/java/current` and affects every future shell the user opens — shared state beyond this task. **Do not use this pattern just because a user said "switch to Java 17".** Only use it when the user explicitly asks for a permanent change (e.g., "set Java 21 as my default", "change the system default").

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
sdk default java <jdk-id>
```

## Pattern D — Project-Scoped with `.sdkmanrc` (auto-follow)

If the repo has a `.sdkmanrc`, follow it without asking — this is the repo author's explicit instruction to anyone entering the project:

```bash
type sdk >/dev/null 2>&1 || source "${SDKMAN_DIR:-$HOME/.sdkman}/bin/sdkman-init.sh"
cd /path/to/project && sdk env && ./gradlew build
```

If `sdk env` reports a version in `.sdkmanrc` is not installed, **stop** and ask the user whether to install it (see *When a Version Isn't Installed* below). Do not run `sdk env install` unprompted.

## Discovering What's Installed

Version strings include a **vendor suffix** (`-tem` Temurin, `-zulu` Azul, `-amzn` Corretto, `-graal`/`-graalce` GraalVM, `-librca` Liberica, `-oracle`, …) — guessing produces `Stop! java <x> is not available.` Always check first:

```bash
SDKMAN_DIR="${SDKMAN_DIR:-$HOME/.sdkman}"
ls "$SDKMAN_DIR/candidates/java/"               # installed <jdk-id> values
readlink "$SDKMAN_DIR/candidates/java/current"  # current default
```

## When a Version Isn't Installed

If the target version isn't under `$SDKMAN_DIR/candidates/<tool>/`:

1. List what IS installed (the `ls` above).
2. If the user wants to see remote options: `sdk list java` (requires network).
3. **Stop and ask.** Either pick a compatible installed version, or confirm `sdk install java <jdk-id>` with the user — specifying vendor, since the user may have a policy (`-tem`, `-amzn`, `-graalce`, …). Do not run `sdk install` autonomously.

## Other Candidates

The patterns above work for every SDKMAN candidate — swap `java` for the candidate name and use the matching env var when Pattern B is needed:

| Candidate | Env var |
|---|---|
| `java` | `JAVA_HOME` |
| `gradle` | `GRADLE_HOME` |
| `maven` | `MAVEN_HOME` (some tools also honor `M2_HOME`) |
| `kotlin` | `KOTLIN_HOME` |

Other candidates (`ant`, `scala`, `groovy`, `springboot`, …) follow the same convention: `<CANDIDATE>_HOME` points at `$SDKMAN_DIR/candidates/<candidate>/<version>/`.
