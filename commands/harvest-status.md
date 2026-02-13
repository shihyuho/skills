---
description: "Show current harvest status for source-of-truth and second-brain structure."
---

Show a compact status report for:

1. Source-of-truth files in project root:
   - `task_plan.md`
   - `findings.md`
   - `progress.md`
2. Required second-brain files:
   - `docs/notes/index.md`
   - `docs/notes/projects.md`
   - `docs/notes/decisions.md`
   - `docs/notes/knowledge.md`
3. Optional content counts:
   - timeline notes under `docs/notes/projects/*/timeline/*.md`
   - decision notes under `docs/notes/decisions/*.md` (excluding template)
   - knowledge notes under `docs/notes/knowledge/*.md` (excluding template)
4. Number of `unresolved_source_ref` occurrences under `docs/notes`.

If required second-brain files are missing, recommend running `/harvest-start`.
