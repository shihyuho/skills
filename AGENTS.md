# AGENTS.md

## Global Constraints
- Validate changed skills with `npx --yes skills-ref validate <skill-dir>`; do not assume `package.json` provides task scripts.
- If you change `skills/fanfuaji/scripts/`, also run `python3 -m pytest skills/fanfuaji/scripts/test_fanfuaji_security.py -v`.
- Every published directory under `skills/` must include `SKILL.md`.
- If you add, remove, or rename anything under `skills/` or `commands/`, update the corresponding lists in `README.md` in the same change.
- Under `skills/`, avoid `_`-prefixed subdirectories; use `.`-prefixed names for hidden helpers.
- Treat checked-in workflows and tests as the source of truth for verification; do not treat local planning or workspace artifacts as canonical repo policy.
