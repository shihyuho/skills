---
name: grill-diff
description: Review git changed files using deep interactive grilling or fast specialist-filtered review. Deep mode discusses every finding with the user. Fast mode consults internal specialists first, only bringing high-value findings to the user.
---

## Mode

If the user clearly indicates fast (e.g. "快速掃", "fast"), use fast mode. If clearly deep (e.g. "仔細烤", "grill", "deep"), use deep mode. If ambiguous (including bare `/grill-diff`), ask.

## Diff Scope

File scope and diff baseline are independent and combine freely (e.g. "fast against develop src/auth.ts").

- **Files:** user-specified if listed, otherwise all changed files.
- **Baseline:** staged > unstaged > user-specified branch > PR URL > current branch vs default branch.

## Review

Ask if there is a related spec or plan file. Read all changed files to build the full picture, then go through files one at a time. Interrogate every aspect of each change.

If a question can be answered by exploring the codebase, specs, or tests, explore yourself instead of asking.

**When you spot a finding:**

- **Deep mode:** discuss with the user, one question at a time, until shared understanding.
- **Fast mode:** pick 3+ specialists relevant to the finding. Consult sequentially — each sees earlier opinions, then gives opinion + confidence (high / medium / low). Classify:
  - Any specialist rated **high** → present to user
  - Highest is **medium**, or specialists disagree → present to user as "uncertain"
  - All rated **low** → drop silently

  After all findings in a file are classified, merge duplicates and link related ones. Present surviving findings one at a time — same grill-mode as deep. Files with no surviving findings advance silently.

## Specialists

| ID | Expertise | Core Question |
|----|-----------|---------------|
| verify | Correctness | "This code claims to do X — does it actually?" |
| nitpick | Edge cases | "There's definitely a bug here — where is it?" |
| newcomer | Readability | "First time seeing this — do I understand it?" |
| attacker | Security | "How do I break this?" |
| revert | Necessity | "If we revert this change, what breaks?" |
| maintainer | Maintainability | "What will someone curse about this in 6 months?" |
| senior | Architecture | "What would I flag in a PR review?" |
