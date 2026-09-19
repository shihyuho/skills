# SDKMAN evaluations

`evals.json` defines behavior after the skill is loaded. `trigger-evals.json` tests whether a task leads the agent to consult the skill from its name and description, without preloading the body or asking it to use a skill.

A positive trigger does not imply a version change:

- Ordinary Maven or Ant execution should reach the skill and use the current configuration when no environment declaration applies.
- An applicable `.sdkmanrc` selects the environment before execution, even when the current runtime appears compatible.
- A real runtime mismatch calls for diagnosis and an SDKMAN change at the affected layer.
- Documentation containing tool names, quoted errors, or an incidental `.sdkmanrc` should leave the runtime skill unloaded.

For a comparison, snapshot the baseline and candidate, including their references. Run each prompt in a fresh context with equivalent fixtures and record which skill file was actually read, the executed commands, workload environment, exit status, and persistent state. Keep trigger selection and behavior results separate.

Use isolated SDKMAN directories and command fixtures for activation and failure cases. Give the evaluator write access to its evidence directory, pass its fixture environment to every non-login shell, and guard fixture initialization against any other `SDKMAN_DIR`. These checks exercise agent decisions and local shell behavior; they do not establish real build, download, or installation success.

Keep generated transcripts, fixtures, and the official skill-creator viewer in an ignored workspace under this directory. Report the cases actually run, model/runtime, repetitions, and any discarded harness trials; a small fixture sample is not a general trigger-rate estimate.
