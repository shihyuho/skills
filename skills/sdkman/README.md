# sdkman

Run a command under an explicitly requested or worktree-selected [SDKMAN](https://sdkman.io/) candidate while preserving wrappers, build toolchains, exact vendor identity, and persistent user settings.

The skill now uses a bundled read-only inspector to validate the complete applicable environment before one same-shell execution. It triggers only when SDKMAN can affect the next command; an unrelated `.sdkmanrc`, compiler target, or healthy wrapper/toolchain does not cause a switch.

The inspector uses Python 3's standard library, performs no network or environment mutation, and returns a versioned verdict. Installation, default changes, auto-env, and project-file changes still require an explicit request.

## Install

```bash
npx skills add shihyuho/skills --skill sdkman -g
```

## License

MIT
