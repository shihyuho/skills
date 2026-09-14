# Public fixture comparison after review

The reviewed skill completes the tested tours with source navigation and saved-document provenance. Both conditions explain the synthetic program correctly; the observed difference is the saved artifact's source identity and snapshot information.

## Results

Three cases ran once with and once without the skill at each effort: 12 executions. All exited successfully.

| Case | Medium with skill | Medium without skill | High with skill | High without skill |
| --- | --- | --- | --- | --- |
| 1: dispatch and effects before failure | 6/6 | 6/6 | 6/6 | 6/6 |
| 2: class relationships and unused marker | 4/4 | 4/4 | 4/4 | 4/4 |
| 3: saved preview tour | 5/5 | 4/5 | 5/5 | 4/5 |
| Total | 15/15 | 14/15 | 15/15 | 14/15 |

The no-skill documents omit the synthetic source identity, exact content snapshot and statement that no Git revision is supplied. Their code explanations and relative source links are otherwise correct. With-skill documents retain that provenance. Every source file remains byte-identical; case 3 alone creates the requested `docs/preview-tour.md`.

## Review changes

The review shortened the explicit-only skill's description to a human-facing purpose statement and made completion depend on checkable tour content rather than an assumption that the reader understands. Its purpose, invocation markers and authorization boundaries remain unchanged.

The earlier exploratory trial used private production source. Its detailed outputs were moved outside this public repository, and private-repository links were removed from the research narrative. This suite uses independently authored, distributable Python fixtures instead. The two trials use different source and prompts, so their scores are not combined or used to claim a before/after improvement.

## Method and evidence

- Input: [report-demo](../../files/report-demo/), five small Python files and [content-snapshot metadata](../../files/report-demo/source-info.json). The source is a toy in-memory publisher, not a production-code excerpt or a Git checkout.
- Executor: `codex-cli 0.154.0-alpha.6.2`, explicitly configured with `gpt-6-astra` and medium or high effort. The event stream does not independently echo provider-effective settings; these are verified invocation settings.
- Isolation: fresh ephemeral process and source copy per condition; other skills, user configuration, project instructions, memory, plugins and subagents disabled. Executors received the prompt, fixture and, for the with-skill condition, the skill text. Assertions were withheld. Built-in host instructions still apply.
- Grading: a Sol medium grader read all twelve anonymized outputs, tool actions and the fixture, with condition labels withheld. The parent independently checked fixture outcomes, input preservation and saved-artifact scope. No grading overrides were applied.
- Evidence: [results.json](results.json) preserves prompts, configured commands, skill and fixture hashes, normalized outputs and their hashes, completed tool actions, per-assertion grades, usage and file changes. It contains only public synthetic data. Local evaluation paths are normalized to placeholders.
- Review pages: standard `skill-creator` aggregation and static viewers were generated for both efforts, with metadata corrected to the configured resources and one run per condition.

The evaluated skill hash matches the reviewed `SKILL.md`. Repository frontmatter validation, metadata/invocation checks, fixture execution, snapshot verification and local document-link checks passed.

## Limits

This is one sample per condition on a small Python fixture. Case 2 tests class-diagram correctness after an explicit diagram request, not autonomous selection. The suite does not establish behavior on large repositories, missing dependencies, real multi-turn dialogue, or human learning and reading speed. Diagram semantics were checked against source; Mermaid rendering was not executed. Timing includes concurrent work and usage includes cached input, so neither supports a general cost claim.
