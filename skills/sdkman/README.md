# sdkman

Teach an agent to run commands under an explicitly requested or project-selected [SDKMAN](https://sdkman.io/) candidate without leaking shell-local state across tool calls.

The skill keeps `sdk use` or `sdk env` and the workload in one shell invocation, prefers project wrappers and build toolchains, preserves an explicitly requested vendor, and asks before installing a candidate or changing the user's default.

It distinguishes launcher, build toolchain, compile／test, and application runtime failures: Maven `release`／`source`／`target` and Gradle `options.release`／compatibility settings do not by themselves require changing the shell JDK.

## When it triggers

- The user requests a JDK, Kotlin, Gradle, Maven, or other SDKMAN candidate version or vendor.
- A repository has `.sdkmanrc`.
- A build reports an actual Java runtime or toolchain mismatch.
- A task depends on SDKMAN-managed `JAVA_HOME` behavior.

## Install

```bash
npx skills add shihyuho/skills --skill sdkman -g
```

## License

MIT
