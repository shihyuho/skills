# Harvest Auto Capture on SOT Changes

## Overview

This document records the design baseline after moving capture rules into the Harvest skill contract.

Current scope is **OpenCode only**.

Target SOT files:

- `task_plan.md`
- `findings.md`
- `progress.md`

Manual commands remain valid:

- `commands/harvest.md`
- `commands/harvest-capture.md`

## Contract-First Architecture

Canonical contract location:

- `skills/harvest/SKILL.md`

Trigger entrypoint guidance:

- `skills/harvest/SKILL.md`
- `commands/harvest-capture.md` (optional convenience entrypoint)

Plugin runtime:

Single-file plugin runtime:

- Plugin entry + logic: `.opencode/plugins/harvest.js`

Install doc:

- `.opencode/INSTALL.md`

Core rule:

- `harvest:harvest` skill contract is the canonical execution source.
- All entrypoints MUST share one capture contract.

## Trigger Model

Primary trigger (proactive):

- OpenCode events `file.edited` and `file.watcher.updated`
- Only reacts when changed file is one of the three SOT files

Convergence trigger:

- OpenCode event `session.idle`
- If in-memory pending flag is true, plugin runs capture flow on idle

Manual reconciliation:

- Plugin does not rely on command events.
- Manual command usage is optional and independent from plugin-triggered capture.
- Plugin uses notes-output file events as success signal (`docs/notes/**`) for observability.

## Dedupe and Idempotency

Canonical fingerprint strategy:

- `sha256(normalized(task_plan.md + findings.md + progress.md))`
- Normalization: LF line endings + trim trailing whitespace

Plugin runtime gates:

- Debounce: `12000ms`
- Cooldown: `45000ms` between capture prompts

Canonical dedupe source:

- Timeline metadata `sot_fingerprint` (defined by Harvest skill contract)

## Stateless Capture Baseline

Defined by capture flow implementation and command guidance:

- `.opencode/plugins/harvest.js`
- `commands/harvest-capture.md`

- Compute `sot_fingerprint` from normalized SOT files only.
- Check timeline metadata for existing `sot_fingerprint` before appending.
- No-op if same `sot_fingerprint` is already captured.
- Include `sot_fingerprint` in new timeline snapshot metadata.
- Do not create runtime dedupe state files under project.

This applies to all trigger methods, including optional command entrypoints.

## Runtime State Policy

Plugin runtime is stateless on disk.

- No `.harvest/auto-capture/*` runtime dedupe files are written.
- Debounce and cooldown live in process memory only.
- Cross-session dedupe memory is timeline metadata (`sot_fingerprint`) as defined by the Harvest skill contract.

## Capture Execution Strategy

When capture is needed:

1. Plugin sends `client.session.prompt` with concise instructions to invoke `harvest:harvest` and force key-update snapshot capture.
2. Plugin retries prompt dispatch once on failure (total 2 attempts).
3. On successful dispatch, plugin clears pending trigger state and waits for notes-output success signal.
4. Plugin confirms success signal when `docs/notes/**` file events are observed.
5. On dispatch failure, plugin keeps in-memory pending trigger state for next idle convergence.

## Safety and Boundaries

- Input boundary is strict SOT allowlist only.
- `docs/notes/**` is never used as input in plugin logic.
- Failures are non-blocking to session progression.
- No runtime dedupe state write is used.

## Files Changed in This Iteration

- Updated `skills/harvest/SKILL.md` with entrypoint consistency contract.
- Updated `commands/harvest-capture.md` as optional convenience entrypoint with shared capture contract wording.
- Updated `.opencode/plugins/harvest.js` to remove runtime state file writes and remove direct dependency on `harvest-capture` command.

## Verification Notes

Completed checks:

- Content-level consistency checks between `skills/harvest/SKILL.md` and `commands/harvest-capture.md`.
- `node --check .opencode/plugins/harvest.js`
- LSP diagnostics clean for `.opencode/plugins/harvest.js`

Runtime checks (manual):

1. Edit any SOT file.
2. Confirm plugin-triggered capture path follows `harvest:harvest` contract without requiring command wrappers.
3. Validate no duplicate snapshot when `sot_fingerprint` already exists.
4. Confirm `.harvest/auto-capture` is not created.

## Deferred Items

- Claude Code plugin support is intentionally removed.
- Timeline metadata parsing and lookup behavior should be validated against real timeline note variants.
