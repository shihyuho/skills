# Bootstrap

Use this flow when the task involves adding or enforcing requirement/constraint text in `AGENTS.md` or `CLAUDE.md`.

## Required Flow

1. **Detect project instruction files**
   - Check `AGENTS.md` and `CLAUDE.md` at the project root.
   - Treat every existing file as a target file.
   - If neither file exists, ask the user which file to create, create it at the project root, and treat it as a target file.

2. **Enforce required block**
   - For each target file found, check whether it already contains equivalent mandatory wording that requires invoking the `workflow-orchestration` skill before execution.
   - If equivalent mandatory wording already exists in a file, do not add another discipline block to that file.
   - If no equivalent mandatory wording exists in a file, add one canonical discipline block to that file.
   - Keep strong wording; this is a hard requirement, not a suggestion.

   Required block:

   ```markdown
   ## Workflow Orchestration

   **MUST** invoke the `workflow-orchestration` skill before any execution
   ```

3. **Avoid duplication**
   - In each target file, if multiple equivalent mandatory blocks exist, keep a single canonical block and remove duplicates.
