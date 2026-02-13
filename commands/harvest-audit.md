---
description: "Audit second-brain quality, traceability, and anti-recursion safety."
---

Audit current second-brain outputs under `docs/notes` and report findings:

1. Traceability checks:
   - formal notes include `source_files` and `source_date`
2. Quality checks:
   - detect notes likely containing large verbatim source-of-truth blocks
   - detect unresolved markers (`unresolved_source_ref`)
3. Safety checks:
   - confirm no recursion pattern (notes summarizing `docs/notes` itself)
   - confirm source input remains `task_plan.md`, `findings.md`, `progress.md`

Return a brief pass/fail summary with concrete file paths for each issue.
