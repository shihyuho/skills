---
name: splitoff
description: "Hand the current conversation to a fresh background agent using a self-contained handoff summary; use a named Claude Code agent or a native Codex subagent."
license: MIT
disable-model-invocation: true
---

## Invocation input

`$ARGUMENTS` below means the arguments supplied with the user's explicit invocation. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.

Create a self-contained handoff prompt for a fresh agent. Include the goal, completed work, decisions, relevant paths and repository state, validation performed, outstanding work, and constraints. Preserve the user's explicit request and any model preference. Do not make the user read or assemble the handoff.

## Claude Code

Write the handoff prompt to a temporary file. Launch a named background agent with `claude --bg --name "<descriptive name>" --model "<model>" -- "$(cat <handoff-file>)"`. Keep `--` so a handoff beginning with `-` is not parsed as a flag. On successful launch, delete the temporary file; keep it on failure for retry. The user manages the agent with `claude agents`.

Always pass `--name`: derive a short descriptive name from `ARGUMENTS`, or from the handed-off work. Always pass `--model`: use the model named in `ARGUMENTS`, otherwise the current session model. Do not silently fall back to a default model.

## Codex

Delegate the complete handoff prompt to one fresh native Codex subagent in the current project. Start it as background delegated work; do not create a user-owned chat/task and do not invoke `codex exec` as a fallback. If the current Codex host supports subagent naming, use the descriptive name; otherwise preserve it in the subagent prompt.

Honor a user-specified model or reasoning setting only when the current host exposes a compatible override. Otherwise inherit the parent configuration and state that limitation when reporting the launch. Do not invent CLI flags or host tool names.

After delegation, report that the subagent owns the handed-off work and where the current host exposes its progress. Do not duplicate its work. Wait for and synthesize its result only when the user asks to continue or report the delegated outcome.

ARGUMENTS: $ARGUMENTS
