# JVM build ownership

Use this reference to decide which layer owns a Maven or Gradle requirement. The shell JDK, build launcher, daemon, compile toolchain, test JVM, and application runtime are separate control planes.

## Wrappers own build-tool versions

Prefer `./mvnw` and `./gradlew` when the repository provides them. Their wrapper configuration selects Maven or Gradle; an SDKMAN `maven` or `gradle` declaration is not applicable to that wrapper command unless the user explicitly requested the SDKMAN executable instead.

A wrapper may download its declared distribution. That is a network and supply-chain boundary, not an SDKMAN candidate switch; use the failure and supply-chain reference when downloads matter.

## Compiler targets are compatibility settings

Maven `maven.compiler.release`, `source`, and `target`, plus Gradle `options.release`, `sourceCompatibility`, and `targetCompatibility`, describe source or output compatibility. They do not alone prove that the shell must run the same JDK version. A newer launcher JDK can often compile an older release.

Treat quoted errors in docs, source, or diffs as content rather than runtime evidence.

## Toolchains own compile and test JDKs

Maven Toolchains can give toolchain-aware plugins a JDK different from the Maven launcher. Gradle Java Toolchains select compile and test JDKs independently of the shell. Delegate Java to the toolchain when it is configured and available.

If a required toolchain is unavailable, report that build-toolchain failure. Do not hide it by changing the shell JDK unless the project explicitly makes the shell its toolchain source.

## Launchers own startup failures

Use a non-workload probe such as `./mvnw -version` or `./gradlew --version` only when launcher compatibility is unknown. A failed probe means the launcher did not start; it is not a failed test or build.

For Gradle, distinguish:

- Client JVM: starts the wrapper and client;
- Daemon JVM: selected by daemon criteria or launcher behavior;
- task JVM/toolchain: runs compile, test, or other toolchain-aware tasks.

A shell `JAVA_HOME` change affects the client launch environment. It does not necessarily override daemon criteria or task toolchains.

## Ownership outcomes

- Healthy wrapper plus healthy toolchain: run the wrapper without an SDKMAN switch.
- Wrapper launcher needs Java: SDKMAN may own only the launcher JDK.
- User explicitly requests an SDKMAN Maven or Gradle executable: SDKMAN owns that requested candidate instead of a wrapper.
- Build runtime or toolchain reports a mismatch: diagnose that layer before changing the shell.
