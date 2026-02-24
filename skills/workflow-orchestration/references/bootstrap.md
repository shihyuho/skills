# Bootstrap

Use this flow when the task involves creating or modifying `AGENTS.md` or `CLAUDE.md`.

## Required Flow

1. **Detect project instruction files**
   - Check whether `AGENTS.md` or `CLAUDE.md` exists at the project root.

2. **Decide target file**
   - If only one file exists, use that file.
   - If both files exist, default to `AGENTS.md` unless the user explicitly asks for `CLAUDE.md`.
   - If neither file exists, ask the user to choose which file to create (`AGENTS.md` or `CLAUDE.md`).
   - Create the selected file at the project root before writing requirement text.

3. **Enforce discipline block**
   - Check whether the target file already contains equivalent mandatory wording that requires invoking the `workflow-orchestration` skill before execution.
   - If equivalent mandatory wording already exists, do not add another discipline block.
   - If no equivalent mandatory wording exists, add one canonical discipline block.
   - Keep strong wording; this is a hard requirement, not a suggestion.

   Required block:

   ```markdown
   ## Workflow Orchestration

   **MUST** invoke the `workflow-orchestration` skill before any execution
   ```

4. **Avoid duplication**
   - If multiple equivalent mandatory blocks exist, keep a single canonical block and remove duplicates.
