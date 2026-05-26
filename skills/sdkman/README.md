# sdkman

Teach the agent to switch JDK (or any SDKMAN-managed candidate) correctly on a machine configured with [SDKMAN](https://sdkman.io/).

The short version: `sdk` is a shell function, not a binary, and every Bash tool call starts a fresh shell — so naively running `sdk use java 21-tem` and then another command in a later call silently does nothing. This skill hands the agent the right patterns instead:

- **Primary — one-shot `sdk use`** — `source sdkman-init.sh && sdk use … && <cmd>` in a single Bash call. Validates the version, gives clear errors, leaves no global state behind.
- **Fallback — direct `JAVA_HOME`** — point at `$SDKMAN_DIR/candidates/java/<jdk-id>` when a tool needs `JAVA_HOME` in a detached process.
- **Project-scoped — `.sdkmanrc`** — auto-follow the repo's declared version via `sdk env`, no confirmation needed.
- **Global default — `sdk default`** — only when the user explicitly asks for a permanent change.

**Default policy**: ephemeral (this task only). The skill never runs `sdk default` or `sdk install` without explicit user confirmation; when a version isn't installed it stops and asks rather than auto-downloading hundreds of megabytes.

The skill checks `$SDKMAN_DIR` (default `~/.sdkman`) up front and steps aside if SDKMAN isn't installed. Native Windows `cmd`/PowerShell is not supported — SDKMAN requires a POSIX shell (macOS, Linux, WSL, Git Bash, Cygwin, MSYS).

## When it triggers

User says "switch to Java 17" / "run with JDK 21" / "use Gradle 8.x", a build fails with `UnsupportedClassVersionError` or "class file has wrong version", or the repo contains a `.sdkmanrc`.

## Install

```bash
npx skills add shihyuho/skills --skill sdkman -g
```

## License

MIT
