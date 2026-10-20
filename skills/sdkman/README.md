# sdkman

Run Java, Maven, Gradle, and other SDKMAN-managed tools in the environment the project declares, and manage host tool versions through [SDKMAN](https://sdkman.io/).

Unlike running a command in whatever environment the agent's shell already has, it applies the declared environment, from `.sdkmanrc` or a version you name, in the same shell as each workload, even when the current JDK looks compatible: an agent's shell gets no reliable auto-env and keeps no activation between tool calls.

## When to use

- Running a build, test, server, or script on Java, Maven, Gradle, Ant, Tomcat, Kotlin, or another SDKMAN candidate, especially in a project with `.sdkmanrc`.
- Rerunning after a launcher or runtime failure such as `UnsupportedClassVersionError`.
- Asking which versions are installed, or installing, removing, or setting a default version through SDKMAN.

The agent uses it on its own when a task runs one of these tools or touches SDKMAN versions; you can also invoke it directly. For a project that pins its tools with mise, asdf, or jenv, use that manager instead, because this skill drives only SDKMAN.

## Before you start

SDKMAN is installed, either as the `sdk` command or at `${SDKMAN_DIR:-$HOME/.sdkman}`. The skill keeps no workspace and writes to SDKMAN or project files only when you ask for that change.

## Getting started

Ask for the run as you normally would:

```text
This project has a .sdkmanrc; run mvn test.
```

## The workload

A workload is one shell invocation: SDKMAN initialization when needed, each activation, then your original command, chained so a failed step leaves the command unstarted and its exit status reaches you unchanged. What the workload applies depends on what the project declares:

| Situation | What the workload does |
| --- | --- |
| `.sdkmanrc` applies to the command's worktree | Applies every entry through `sdk env` or `sdk use`, even when the current versions would also work |
| You name a version, such as "with Java 21" | Overrides that candidate and keeps the rest of `.sdkmanrc` |
| A wrapper, Gradle daemon criteria, or a toolchain selects a version | Leaves that layer to the build; SDKMAN supplies only what the shell selects, such as the launcher JDK |
| Nothing is declared | Runs under the current configuration, and looks at versions only after a failure points there |
| A declared version is missing, or the choice is ambiguous | Stops and asks before installing or choosing; it never substitutes another version |

## It's working if

- The command the agent runs for your build is a single shell line that activates versions and then runs your command, joined with `&&`.
- With a `.sdkmanrc`, the agent's report names the versions it applied, and `sdk current` in your own terminal shows the same defaults as before.
- A missing declared version ends with a question about installing it, not a build on a different JDK.
- When SDKMAN itself fails, the reported exit status is SDKMAN's and no build output appears.

## Common questions

**Why keep a local skill instead of adopting an external SDKMAN skill or MCP server?**
A survey in [#27](https://github.com/shihyuho/skills/issues/27) found no candidate that covers every SDKMAN candidate, worktree-scoped `.sdkmanrc`, exact versions and vendors, and explicit authorization for persistent changes. At the time, SDKMAN's official MCP server could not switch candidates or run workloads, and the community JDK switcher covered only Java under an unknown license. This skill is meant to be replaced once a published option passes those gates.

**Where did the bundled `inspect.py` inspector go?**
[#43](https://github.com/shihyuho/skills/pull/43) removed it. The native `sdk` CLI now provides the same evidence (`sdk current`, `sdk list`, `sdk home`), so the skill no longer needs Python or a custom resolver.

**Where did the session-start and build-error hooks go?**
They were removed when the skill was aligned with build toolchains (`62e050f`). The [research behind that change](../../docs/research/sdkman-skill-best-practices.md) found that a hook cannot see through wrappers or scripts, cannot make the agent load the skill, and fires on documentation or diffs that merely quote an error. The skill's description now carries those triggers: running a supported tool, or investigating an actual execution failure.

## Limitations

- Installing an SDK does not make a build offline: wrappers, dependencies, plugins, and toolchains download on their own terms.
- A failure after your command starts goes back to the original task unless it points at an SDKMAN-owned version.
