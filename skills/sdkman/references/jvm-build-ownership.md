# JVM build ownership

Choose the environment for the actual command. Preserve a user- or repository-selected `mvn`, `gradle`, wrapper, or higher-level entrypoint such as `make test`; prefer a project wrapper when choosing an otherwise unspecified build command.

| Layer | What selects its version |
| --- | --- |
| Maven or Gradle executable | A wrapper's configuration, or the selected executable for direct `mvn` / `gradle` commands |
| Launcher/client JVM | The environment that starts the command; SDKMAN can supply this JDK |
| Gradle daemon JVM | Daemon criteria when configured, otherwise Gradle's launcher rules |
| Compile/test JVM | An available configured toolchain, otherwise the build's defaults |

A wrapper-owned Maven or Gradle declaration needs no SDKMAN activation. A task toolchain does not itself supply a missing launcher JVM, and changing shell `JAVA_HOME` does not override daemon criteria or task toolchains. Resolve the requirement at the layer that needs it.

Compiler `release`, `source`, `target`, and Gradle compatibility settings describe source/output compatibility. They alone establish neither a shell-JDK requirement nor a vendor choice. Error strings quoted in documentation are not execution evidence.

When launcher compatibility is uncertain, use the selected command's version probe, such as `mvn -version`, `./mvnw -version`, or `./gradlew --version`. A startup failure leaves the build unstarted; a failure after the build starts needs diagnosis at that later layer.
