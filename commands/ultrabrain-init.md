---
description: "Initialize ultrabrain trigger reminder"
---

Run setup for project instruction files.

1. **Detect project instruction files**
   - Check `AGENTS.md` and `CLAUDE.md` at the project root.
   - Treat every existing file as a target file.
   - If neither file exists, ask which file to create, create it at project
     root, and treat it as target.

2. **Enforce canonical ultrabrain block**
   - For each target file, check whether equivalent mandatory wording already
     exists.
   - If equivalent wording exists, do not add another block.
   - If equivalent wording does not exist, add this canonical block:

    ```markdown
    ## UltraBrain

    **MUST** use the `ultrabrain` skill for ultrabrain-relevant work only:
    knowledge recall/capture, second-brain or PKM workflows, and
    notes/MOC/linked-note organization.
    For relevant work, follow the visible trace rules in the `ultrabrain`
    skill's `SKILL.md`.
    ```

3. **Avoid duplication**
   - If multiple equivalent mandatory blocks exist, keep one canonical copy and
     remove duplicates.

Keep this command narrow: it only installs the canonical reminder block.
UltraBrain behavior remains defined in `SKILL.md`.

Execute only this flow for this invocation. Do not run other actions unless the
user explicitly asks.
