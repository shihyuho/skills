# sdkman Next — Implementation Design Spec

## Objective

Refactor the canonical `sdkman` skill into a smaller, safer execution flow for commands whose runtime environment is actually owned by SDKMAN.

The next version keeps the agent responsible for intent and workload ownership, delegates deterministic environment inspection to a bundled read-only inspector, and leaves environment activation and workload execution to SDKMAN, project wrappers, and the shell. It must preserve exact candidate identity, Git worktree isolation, task-local execution, persistent-action approval, and truthful failure attribution while reducing repeated prompt text and shell probes.

This is an in-place transition design, not a permanent commitment to a local implementation. A released external package that later passes every replacement gate in [Issue #27](https://github.com/shihyuho/skills/issues/27#issuecomment-5467239675) should replace this skill directly.

## Authority and scope

The closed [Wayfinder map #24](https://github.com/shihyuho/skills/issues/24#issuecomment-5477901844) and its resolution comments are the sole decision source for this spec:

- [SDKMAN and JVM build-tool best practices](https://github.com/shihyuho/skills/issues/25#issuecomment-5466203450)
- [Cross-project usage and bottleneck audit](https://github.com/shihyuho/skills/issues/26#issuecomment-5466157946)
- [Keep, absorb, or replace decision](https://github.com/shihyuho/skills/issues/27#issuecomment-5467239675)
- [Validation, migration, and spec completion](https://github.com/shihyuho/skills/issues/28#issuecomment-5477885819)
- [External skill landscape](https://github.com/shihyuho/skills/issues/29#issuecomment-5466170158)
- [Capability and interaction contract](https://github.com/shihyuho/skills/issues/30#issuecomment-5477692256)
- [Token-efficient candidate decision](https://github.com/shihyuho/skills/issues/31#issuecomment-5467000517)

Research artifacts support those resolutions but do not override them. Implementation must not reopen an approved choice without a new user decision.

## Design summary

The runtime flow has four layers:

1. **Agent mental model** — decide whether SDKMAN matters, identify applicable candidate constraints, and assign wrapper or toolchain ownership.
2. **Read-only inspector** — discover the current worktree state, validate applicable constraints against installed candidates, and return a versioned JSON verdict.
3. **Native execution** — apply the complete validated plan and run the unchanged workload in one shell invocation.
4. **On-demand references** — load detailed fallback, JVM ownership, failure, network, or supply-chain guidance only when that branch is reached.

`SKILL.md` must describe this flow and its invariants, not reproduce inspector parsing rules or detailed Maven and Gradle documentation.

## Trigger contract

Keep `sdkman` model-invocable, but narrow its description and body around this rule:

> Load the skill only when an SDKMAN-managed environment can affect the next command.

Concrete positive triggers are:

- the user requests an SDKMAN candidate, version, or vendor for a command;
- the next command has an applicable worktree-contained `.sdkmanrc` declaration;
- a real launcher or runtime failure shows that an SDKMAN-managed candidate controls the failing layer;
- the command explicitly depends on an SDKMAN-managed home or binary path.

The following evidence is insufficient by itself:

- a repository merely contains `.sdkmanrc` when the next action does not execute an affected command;
- documentation contains a Java error string;
- Maven compiler release or Gradle compatibility settings name an older Java level;
- a wrapper or configured build toolchain already owns the requested Maven, Gradle, compile, or test runtime.

The invocation classification remains `Model-invoke`: natural-language runtime failures and version requests are supported implicit paths. Do not add explicit-only markers or move the root README entry to `User-invoke`.

## Agent mental models

### Candidate intent

Respect explicit intent and use installed evidence. Exact SDKMAN IDs, including vendor suffixes, are immutable identities: never shorten, normalize, or silently substitute them. Ask only when evidence leaves a real ambiguity.

An explicit constraint supplied for a candidate overrides the same candidate in `.sdkmanrc`; all other applicable declarations remain in the plan.

The skill should give this mental model, not a long candidate-ranking algorithm. The inspector may resolve an exact installed ID, a current or default installed match, or a sole installed match. Multiple remaining matches require a choice.

### Workload ownership

Determine ownership before asking the inspector to validate a plan:

- a repository wrapper owns its Maven or Gradle version;
- a configured build toolchain owns compile and test JDK selection;
- SDKMAN owns only the launcher, runtime, or candidate layer that actually affects the command.

Represent wrapper and toolchain ownership as inspector delegations. Delegated `.sdkmanrc` declarations are recorded as ignored diagnostics and do not block the workload.

### Complete plans

Filter by workload ownership first, then validate every remaining declaration together. A `ready` verdict means the whole applicable plan can be activated. Never apply only the candidates that happened to resolve while ignoring another applicable blocker.

### Persistent state

The default lane is task-local and discardable. Installation, default changes, auto-env changes, and creating or modifying `.sdkmanrc` or other project files require an explicit user request.

If `sdk use` may create a missing `current` link, the plan must use direct-environment activation instead. The inspector never performs either activation mode.

## Bundled inspector

### Location and runtime

Create:

```text
skills/sdkman/scripts/inspect.py
```

Requirements:

- Python 3 standard library only;
- no pip packages, downloads, or network access;
- may use the local `git` executable only for read-only worktree discovery;
- never source SDKMAN;
- never invoke `sdk env`, `sdk use`, `sdk install`, or `sdk default`;
- never create, modify, or remove files, directories, or links;
- never start the requested workload;
- never emit executable shell text.

If `python3` is unavailable, the agent reports that the inspector is unavailable and loads the manual fallback reference. This is not an inspector JSON status because the script did not run.

### Command-line contract

The inspector accepts the workload directory plus optional structured constraints and ownership delegations:

```text
python3 skills/sdkman/scripts/inspect.py \
  --workload-dir PATH \
  [--exact CANDIDATE=EXACT_ID]... \
  [--version-prefix CANDIDATE=PREFIX]... \
  [--vendor-suffix CANDIDATE=SUFFIX]... \
  [--delegate CANDIDATE=wrapper|toolchain]...
```

Rules:

- Options are data, not shell fragments. Candidate names, IDs, prefixes, and suffixes must reject path separators, NULs, control characters, and empty values.
- `--exact` is mutually exclusive with `--version-prefix` or `--vendor-suffix` for the same candidate.
- `--vendor-suffix` refines the matching candidate's `--version-prefix`; it cannot appear alone.
- A candidate may appear at most once in each option family. Conflicting duplicates return `error`.
- Explicit constraints override the same candidate from `.sdkmanrc`.
- `--delegate` removes that candidate from the applicable SDKMAN plan and records the named owner. Delegating an explicitly constrained candidate is an input conflict and returns `error`.
- Version prefixes match only an ID prefix boundary, not an arbitrary substring. Vendor suffixes match the preserved SDKMAN ID suffix. The inspector does not translate one vendor identity into another ecosystem's name.
- The agent derives these structured inputs from user intent and workload ownership. The inspector does not parse the original command or natural language.

Repeatable options permit one inspection to cover a multi-candidate `.sdkmanrc` plus any explicit overrides.

### Environment boundary and discovery

Resolve `--workload-dir` to an existing directory without changing process cwd.

Inside Git:

- use the containing worktree's top-level directory as the hard search boundary;
- search from the workload directory upward for the nearest `.sdkmanrc` without crossing that boundary;
- do not inspect sibling worktrees, the originating checkout, or parent repositories outside the current worktree.

Outside Git:

- use the explicitly supplied workload directory as both the project boundary and `.sdkmanrc` lookup location;
- do not walk above it.

SDKMAN discovery reads `${SDKMAN_DIR}` when set, otherwise the user's standard `.sdkman` directory. It may inspect only:

- the applicable `.sdkmanrc`;
- installed directories under `candidates/<candidate>/`;
- current and configured-default observations needed to resolve an installed match;
- path and link metadata needed to prove that a selected candidate is installed and contained in that candidate directory.

`.sdkmanrc` parsing accepts SDKMAN candidate declarations and ignores blank lines and comments. Malformed declarations, duplicate candidates, unsafe names, or an exact declaration that escapes the candidate directory are blockers. Do not call `sdk env` as a parser or validator because its application is not atomic.

Discovery should be demand-driven. `no_switch` must not enumerate unrelated SDKMAN candidates, and a request for one candidate must not inspect every other installed candidate unless an applicable `.sdkmanrc` requires them.

### JSON output contract

Stdout contains exactly one UTF-8 JSON object. It is deterministic, contains no executable command, and starts with:

```json
{
  "schema_version": 1,
  "status": "ready",
  "workload": {
    "directory": "/absolute/worktree/modules/api",
    "boundary": "/absolute/worktree",
    "inside_git": true,
    "sdkmanrc": "/absolute/worktree/.sdkmanrc"
  },
  "plan": [],
  "blockers": [],
  "diagnostics": []
}
```

Top-level fields are always present:

| Field | Contract |
| --- | --- |
| `schema_version` | Integer `1`. Consumers reject unknown versions instead of guessing. |
| `status` | One of the five verdicts below. |
| `workload` | Resolved absolute directory, hard boundary, Git membership, and applicable `.sdkmanrc` path or `null`. |
| `plan` | Every applicable SDKMAN-owned candidate in deterministic order. Empty for a genuine `no_switch`. |
| `blockers` | Machine-readable items that prevent immediate execution. Empty for `ready` and `no_switch`. |
| `diagnostics` | Non-blocking evidence such as delegated declarations. It must not duplicate blockers or emit routine success narration. |

Each `plan` item has this shape:

```json
{
  "candidate": "java",
  "source": "explicit",
  "requested": {
    "kind": "version_prefix",
    "value": "21",
    "vendor_suffix": "tem"
  },
  "exact_id": "21.0.8-tem",
  "candidate_home": "/home/user/.sdkman/candidates/java/21.0.8-tem",
  "bin_directory": "/home/user/.sdkman/candidates/java/21.0.8-tem/bin",
  "home_variable": "JAVA_HOME",
  "resolution": "sole_installed_match",
  "activation": "sdk_use"
}
```

Plan-item rules:

- `source` is `explicit` or `sdkmanrc`.
- `requested.kind` is `exact` or `version_prefix`; `vendor_suffix` is `null` when absent.
- `exact_id`, candidate paths, `resolution`, and `activation` are `null` when that item is blocked.
- `resolution` is one of `exact`, `current_match`, `default_match`, or `sole_installed_match`.
- `activation` is `sdk_use` only when using it will not create a missing candidate `current` link; otherwise it is `direct_environment`.
- `home_variable` is the SDKMAN candidate's uppercase home variable (`JAVA_HOME`, `MAVEN_HOME`, `GRADLE_HOME`, `KOTLIN_HOME`, or the corresponding normalized `<CANDIDATE>_HOME`). The inspector returns the name only, never a shell assignment.
- Candidate homes and bin directories must be absolute, validated installed paths. They must not be synthesized for missing candidates.
- Ordering follows applicable `.sdkmanrc` declaration order, with explicit-only candidates appended by candidate name. An override retains the original declaration's position.

Each blocker has a stable `code`, a short `message`, and relevant structured fields such as `candidate`, `requested`, or `matches`. Initial codes must cover:

- invalid input or workload boundary;
- malformed or unsafe `.sdkmanrc`;
- unavailable SDKMAN installation when an applicable plan exists;
- ambiguous installed matches;
- missing exact installed candidates;
- no installed match for a non-exact constraint;
- unreadable or escaping candidate paths or links.

Code names are implementation details within schema version 1, but tests must pin every emitted code. Messages are for explanation, not control flow.

### Verdicts and exit codes

| Verdict | Meaning | Agent action | Exit |
| --- | --- | --- | ---: |
| `ready` | The complete applicable plan resolves to installed exact IDs. | Execute without another confirmation. | `0` |
| `choice_required` | At least one non-exact constraint has multiple matches or no exact install choice. | Ask once for all unresolved choices; do not execute. | `2` |
| `approval_required` | Every identity is exact, but at least one candidate is missing and installation would persist state. | Ask once whether to install the listed exact IDs; do not execute. | `2` |
| `no_switch` | Ownership filtering leaves no SDKMAN-owned candidate plan. | Run the unchanged command without further SDKMAN probes. | `0` |
| `error` | Inspection input, boundary, parsing, or safety contract cannot be established. | Report inspection failure; do not execute. | `1` |

Verdict precedence is `error`, then `choice_required`, then `approval_required`, then `no_switch`, then `ready`. All blockers remain in the response even when one higher-precedence status names the next interaction. The agent asks one consolidated question, not one question per candidate.

## Native execution contract

The inspector proves a plan; it does not perform it.

For `ready`, the agent constructs one shell invocation that:

1. starts from the original workload directory;
2. validates the inspector's schema version and `ready` status;
3. applies every plan item in order;
4. runs the user's original command unchanged;
5. preserves the command's exit status.

For an `sdk_use` item, source `sdkman-init.sh` only if `sdk` is unavailable, then run `sdk use <candidate> <exact-id>` in that same shell. For a `direct_environment` item, export the returned home variable to `candidate_home` and prepend `bin_directory` to `PATH` in that same shell. Never evaluate inspector output as shell code.

A multi-candidate plan must finish all activation steps before starting the workload. If any activation fails, stop immediately and report that the workload did not start.

For `no_switch`, execute the original command directly. Do not source SDKMAN, enumerate candidates, or run a second preflight.

For `choice_required` or `approval_required`, ask one question containing all necessary choices or exact installation approvals. A later user answer may require another inspection before execution; this does not violate the single-inspection normal-success gate.

Persistent commands remain outside the default flow:

- run `sdk install`, `sdk env install`, `sdk default`, or auto-env changes only after explicit authorization for that exact action and candidate identity;
- create or modify `.sdkmanrc` only when explicitly requested;
- do not combine a newly authorized persistent action with unrelated state changes;
- after installation, re-inspect before executing the workload so the plan is proven against current state.

## Failure reporting

Classify failures by the layer that actually failed:

1. **Environment inspection or activation** — inspector, SDKMAN initialization, candidate validation, `sdk use`, or direct-environment setup.
2. **Wrapper or launcher** — Maven or Gradle wrapper startup and client JVM compatibility.
3. **Build runtime or toolchain** — Gradle daemon, Maven or Gradle toolchain resolution, compile JVM, or test JVM.
4. **Requested workload** — the requested build, test, application, or command after its runtime started.

Every failure report states:

- the failed layer;
- whether the original command started;
- whether the real workload behind a wrapper or launcher started;
- the original non-zero exit status when available.

Execution failure does not authorize selecting a different candidate or retrying. Diagnose first; only retry when the user requested a retry or the diagnosed correction is already within the authorized task.

## Progressive disclosure and file responsibilities

The implementation is one cohesive change with this layout:

```text
skills/sdkman/
├── SKILL.md
├── README.md
├── scripts/
│   └── inspect.py
├── references/
│   ├── manual-inspection.md
│   ├── jvm-build-ownership.md
│   └── failure-network-supply-chain.md
└── evals/
    ├── evals.json
    └── test_inspector.py
```

Responsibilities:

- `SKILL.md` — frontmatter trigger, four mental models, inspector-to-execution flow, verdict interaction, persistent-action boundary, and concise completion check. It must not duplicate parser rules, JSON field definitions, Maven or Gradle details, or long examples.
- `scripts/inspect.py` — deterministic discovery, parsing, validation, resolution, plan construction, and JSON serialization. It contains no agent prose or execution logic.
- `references/manual-inspection.md` — read-only fallback when Python is unavailable or the inspector cannot run. It mirrors outcomes, not the inspector implementation line by line.
- `references/jvm-build-ownership.md` — Maven wrapper and launcher, Gradle Client/Daemon/task JVM, and build-toolchain ownership details. Load only for JVM build ownership or diagnosis.
- `references/failure-network-supply-chain.md` — four failure layers, strict no-network versus SDKMAN availability, installation and wrapper download boundaries, and representative reports. Load only for failure, network, installation, or supply-chain branches.
- `evals/evals.json` — agent behavior expectations. It tests decisions and interactions, not exact prose or script internals.
- `evals/test_inspector.py` — Python stdlib unit tests with temporary fixtures. It does not require a real SDKMAN installation or network.
- skill `README.md` — user-visible behavior changes only: narrower trigger, read-only inspector, wrapper/toolchain ownership, and persistent-state safety.
- root `README.md` — retain `sdkman` under `Model-invoke` and update its single-sentence description if needed.

Do not create `sdkman-v2`, a second trigger, compatibility shim, generated shell script, or runtime dependency on an external SDKMAN agent package.

## Validation

### Inspector unit tests

Use `unittest`, `tempfile`, and stdlib mocks to build disposable Git worktrees, `.sdkmanrc` files, installed candidate directories, and current/default links. Tests must cover:

- every verdict: `ready`, `choice_required`, `approval_required`, `no_switch`, and `error`;
- exact ID and vendor preservation;
- explicit override of one `.sdkmanrc` candidate while retaining the others;
- nearest `.sdkmanrc` lookup without crossing the current worktree;
- sibling-worktree and parent-repository isolation;
- wrapper and toolchain delegation before all-or-nothing validation;
- multi-candidate all-or-nothing blocking;
- deterministic ordering and schema version;
- direct-environment activation when `sdk use` may create a `current` link;
- no unrelated candidate enumeration for `no_switch`;
- rejection of unsafe names, paths, links, duplicates, and option conflicts;
- stdout-only JSON and the documented exit-code mapping;
- zero network by making network APIs fail the test if called;
- zero mutation by comparing the fixture tree before and after inspection.

Tests invoke the inspector as a subprocess against fixture-specific `SDKMAN_DIR` and workload paths. They must not read or change the developer's real SDKMAN installation.

### Agent behavior evals

Retain and update the existing 14 cases to use the inspector verdict and new interaction contract. Do not preserve outdated command-shape assertions when the same behavior is now represented by structured inspection plus native execution.

Add no more than these four cases:

1. an unrelated command does not trigger merely because `.sdkmanrc` exists;
2. wrapper ownership defeats an inapplicable SDKMAN Maven or Gradle declaration;
3. an explicit candidate override preserves other applicable `.sdkmanrc` declarations;
4. a missing `current` link selects direct-environment execution.

Correctness and safety assertions must not regress. There is no statistical token benchmark, repeated-run harness, run receipt, percentage reduction target, or benchmark UI.

### Efficiency gates

- `SKILL.md` is materially shorter and keeps only always-needed mental models and the primary flow.
- A rule has one authoritative home; references explain branches without copying the core contract.
- A normal `ready` path uses at most one inspector call and one same-shell execution call.
- `no_switch` performs no additional SDKMAN probe.
- `choice_required` and `approval_required` produce one consolidated question.
- An execution failure does not trigger automatic candidate substitution or retry.

These are flow-shape gates, not token-count claims.

### Repository gates

The implementation ticket must run and record:

- inspector unit tests;
- JSON parsing for `skills/sdkman/evals/evals.json`;
- `python3 scripts/check-frontmatter.py`;
- Agent Skills package validation for `skills/sdkman`;
- invocation-marker and root README classification consistency;
- local Markdown-link validation for changed files;
- `git diff --check`;
- a readback that all changed paths are limited to the cohesive migration scope.

Any unavailable external validator must be reported as unverified; it cannot be silently treated as passed.

## Migration and rollback

Migration is an in-place replacement of the canonical `sdkman` package:

- keep the canonical name, directory, first H1, and MIT license;
- start inspector output at `schema_version: 1`, internal to this skill;
- update `SKILL.md`, inspector, references, evals, skill README, and root README together;
- do not migrate or modify installed candidates, defaults, auto-env, user configuration, or project `.sdkmanrc` files;
- do not add a user setting or data migration step.

Rollback is a revert of the cohesive repository change. No environment or data rollback script is needed because the migration itself creates no persistent user state.

## Non-goals

- Benchmarking model token consumption or claiming a numeric reduction.
- Improving Maven or Gradle workload performance.
- Managing version managers other than SDKMAN.
- Reimplementing SDKMAN switching, Maven or Gradle wrappers, or JVM toolchains.
- Parsing arbitrary shell commands or natural language in the inspector.
- Installing candidates, changing defaults, enabling auto-env, or editing project files without an explicit request.
- Adopting or copying an external skill whose source, license, maintenance, or behavior does not pass the approved replacement gates.

## Completion criteria

This spec is ready for an implementation ticket when the user approves it and all of the following are true:

- file responsibilities and progressive-disclosure boundaries are explicit;
- inspector inputs, output fields, verdicts, and exit codes are implementable without guessing;
- agent interaction, workload ownership, persistent-state safety, and failure reporting are defined;
- tests cover the deterministic inspector and the 14 plus at most four agent evals;
- efficiency uses flow-shape gates rather than a benchmark;
- migration is in place and rollback is a repository revert;
- no blocking open question remains.

## Open questions

None.
