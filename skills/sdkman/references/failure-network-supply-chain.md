# Failure, network, and supply-chain boundaries

## Failure layers

Classify the first failing boundary and state what actually started.

| Layer | Typical evidence | Honest report |
| --- | --- | --- |
| Environment inspection or activation | invalid `.sdkmanrc`, missing exact candidate, inspector error, `sdk use` failure | Environment setup failed; original command did not start. |
| Wrapper or launcher | wrapper script or client JVM cannot start | Launcher failed; build or tests did not start. |
| Build runtime or toolchain | Gradle daemon criteria, Maven or Gradle toolchain resolution, compile/test JVM setup | Build started, but its runtime or toolchain failed before the requested workload completed. |
| Requested workload | compilation, tests, application, or requested command after setup | Workload started and failed with its original exit status. |

Do not label an unstarted test red or failed. Preserve the original non-zero status when the process produced one.

An execution failure is diagnosis evidence, not permission to substitute a candidate or retry. Retry only when the correction and retry are within the user's request.

## Network modes

SDKMAN availability or offline mode is not proof of strict no-network execution. SDKMAN initialization may perform availability or upgrade checks, and Maven or Gradle wrappers, plugins, dependencies, and toolchains may use their own network paths.

When the user requires no network:

- prefer direct-environment activation for an already installed candidate so SDKMAN initialization is unnecessary;
- use the build tool's documented offline mode when applicable;
- verify that required wrapper distributions, dependencies, plugins, and toolchains already exist locally;
- report unknown network behavior instead of claiming isolation from an SDKMAN setting alone.

## Persistent and executable downloads

`sdk install` and `sdk env install` download and persist candidate content and may execute candidate installation hooks. A wrapper may download and execute its declared Maven or Gradle distribution. Dependency and plugin resolution extends the supply-chain surface further.

Before a persistent SDKMAN install:

1. establish every exact candidate ID and vendor;
2. obtain explicit authorization for the download and persistent installation;
3. keep default and auto-env unchanged unless separately requested;
4. re-inspect installed state before executing the workload.

Creating or modifying `.sdkmanrc` establishes a persistent project contract and also requires an explicit request. Compiler settings cannot determine a vendor or exact SDKMAN ID by themselves.
