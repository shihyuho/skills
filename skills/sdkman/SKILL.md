---
name: sdkman
description: Switch an SDKMAN-managed candidate for the next command when the user requests a candidate/version/vendor, a worktree-contained `.sdkmanrc` applies, or a diagnosed launcher/runtime mismatch belongs to SDKMAN. Leave compiler targets and wrapper- or toolchain-owned runtimes to their owning layer.
license: MIT
---

# sdkman

Treat SDKMAN as one environment layer, not as the owner of every Java build setting. A project wrapper owns its Maven or Gradle version, and a configured build toolchain owns compile and test JDK selection. SDKMAN owns only the candidate that affects the next command's launcher or runtime.

## Form one environment plan

Resolve the workload directory first. Preserve it as the command's cwd.

Translate evidence into structured inspector inputs:

- Pass an immutable candidate identity as `--exact CANDIDATE=ID`.
- Pass a non-exact request as `--version-prefix CANDIDATE=PREFIX`; add `--vendor-suffix CANDIDATE=SUFFIX` only when the SDKMAN suffix is evidence-backed.
- Pass `--delegate CANDIDATE=wrapper|toolchain` when that layer owns a `.sdkmanrc` declaration.

An explicit constraint overrides the same candidate in `.sdkmanrc`; other applicable declarations remain. Exact IDs and vendor suffixes are reproducibility contracts, so preserve them byte-for-byte and ask only when the installed evidence is genuinely ambiguous.

Run the bundled read-only inspector once:

```text
python3 <skill-directory>/scripts/inspect.py \
  --workload-dir <directory> \
  [--exact <candidate>=<id>]... \
  [--version-prefix <candidate>=<prefix>]... \
  [--vendor-suffix <candidate>=<suffix>]... \
  [--delegate <candidate>=wrapper|toolchain]...
```

The inspector returns `schema_version: 1` JSON. It reads only the current worktree, its applicable `.sdkmanrc`, and relevant installed candidates. It does not source SDKMAN, run a workload, use the network, or mutate state.

If `python3` is unavailable or the script cannot start and therefore emits no verdict, read [references/manual-inspection.md](references/manual-inspection.md) and perform the same read-only decision manually.

## Follow the verdict

- `ready`: apply the complete plan and run the command without another confirmation.
- `no_switch`: run the unchanged command directly; make no further SDKMAN probe.
- `choice_required`: ask one consolidated question for every unresolved exact ID.
- `approval_required`: ask once before installing the listed exact IDs; installation is a separate persistent action.
- `error`: report the inspection boundary that failed and leave the workload unstarted.

Never apply a partial plan. If a later answer or approved installation changes the environment, inspect the current state again before execution.

## Execute in one shell

Apply every `ready` plan item before starting the workload:

- For `activation: sdk_use`, load `sdkman-init.sh` only when `sdk` is unavailable, then run `sdk use <candidate> <exact_id>`.
- For `activation: direct_environment`, export the returned `home_variable` to `candidate_home` and prepend `bin_directory` to `PATH`.

Keep all activation steps and the original command in one shell invocation. Do not evaluate inspector output as shell code. Preserve the original cwd, command, and exit status.

The default lane is task-local. Run `sdk install`, `sdk env install`, `sdk default`, auto-env changes, or create or modify `.sdkmanrc` only when the user explicitly requests that persistent action and the exact candidate identity is known.

## Diagnose the owning layer

Load [references/jvm-build-ownership.md](references/jvm-build-ownership.md) when Maven or Gradle launchers, daemons, compiler targets, or toolchains determine ownership.

Load [references/failure-network-supply-chain.md](references/failure-network-supply-chain.md) for failure attribution, offline constraints, installation, wrapper downloads, or supply-chain questions.

Report failures at the layer that failed:

1. environment inspection or activation;
2. wrapper or launcher;
3. build runtime or toolchain;
4. requested workload.

State whether the original command and real workload started, and preserve the failing exit status. Diagnose an execution failure before considering a retry; do not switch candidates or rerun automatically.

## Completion check

Completion means the complete validated environment was applied before the unchanged workload started, or the agent truthfully reported why it did not start. User defaults, installed candidates, auto-env, and project files remain unchanged unless that exact persistent action was authorized.
