# code-tour evaluations

The maintained cases use [report-demo](files/report-demo/), an independently authored synthetic Python fixture. It performs formatting, storage and notification entirely in memory; it contains no production code or external-service access. Its supplied [source metadata](files/report-demo/source-info.json) identifies the exact content snapshot and explicitly has no Git revision.

## Run the comparison

1. Copy `files/report-demo/` contents to a fresh disposable directory for each run. Supply only the case prompt and fixture, plus `SKILL.md` for the with-skill condition. Keep assertions and expected outputs out of the executor context.
2. Run the three prompts from [evals.json](evals.json), with and without the skill, separately at Astra medium and high. Use the same host, tools and permissions for paired conditions and a fresh process without other skills, project instructions or memory.
3. Cases 1 and 2 are read-only. Case 3 permits only its requested document. Compare all input file hashes before and after; record created, changed and removed paths.
4. Retain configured model/effort, host version, skill hash, fixture snapshot, prompts, outputs, tool actions and filesystem deltas. Grade against the actual fixture, checking diagram edges and precise source locations rather than visual polish. Clear text diagrams count where the prompt does not request a specific diagram type.

Case 1 covers construction, dispatch and an effect preceding failure. Case 2 explicitly requests a class diagram and checks an unused marker; it tests diagram correctness and scope, not autonomous choice of diagram type. Case 3 checks preview behavior, saved navigation and honest provenance when no Git revision exists.

Use the standard `skill-creator` viewer for paired output review. Executed results belong under `results/<date>/`; report unrun conditions explicitly.

## Evidence boundaries

Public evaluation evidence must use distributable source. Keep private-repository source, derived walkthroughs and detailed traces outside this repository; a public aggregate must disclose that readers cannot independently reproduce the private trial from these files.

An earlier private-source exploratory comparison used different prompts and source. Its aggregate is recorded in the [research note](../../../docs/research/code-comprehension-and-diagrams.md), separately from this maintained suite. Its raw evidence is retained locally and is not included here.

These small fixtures test behavior and the requested deliverable. They do not establish performance on large repositories, dynamic wiring, unavailable dependencies, real multi-turn dialogue, or human understanding and reading speed.
