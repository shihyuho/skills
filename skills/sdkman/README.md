# sdkman

Run development tools in the environment the task requires, and manage host tool versions through [SDKMAN](https://sdkman.io/).

Applies project environment declarations before running Java, Maven, Gradle, Ant, Tomcat, Kotlin, and other supported tools. Otherwise, uses the current configuration and investigates compatibility when a command fails. Version changes use SDKMAN; wrappers and toolchains retain their project-owned settings.

Also handles version queries, installation, removal, defaults, and project environments through the native CLI. Persistent changes follow the user's explicit request.

## Install

```bash
npx skills add shihyuho/skills --skill sdkman -g
```

## License

MIT
