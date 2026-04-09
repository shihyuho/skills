---
name: grill-diff
description: Review git changed files using deep interactive grilling or fast specialist-filtered review. Deep mode discusses every finding with the user. Fast mode consults internal specialists first, only bringing high-value findings to the user.
---

## Mode Selection

Determine the review mode from the user's prompt:
- Clearly fast (e.g. "快速掃", "fast") → fast mode.
- Clearly deep (e.g. "仔細烤", "grill", "deep") → deep mode.
- Ambiguous (including bare `/grill-diff` with no modifier) → ask the user which mode they want.

## Diff Scope

Two independent dimensions that combine freely (e.g. "fast against develop src/auth.ts" reviews only `src/auth.ts` diffed against develop).

**File scope** — user-specified files if explicitly listed, otherwise all changed files.

**Diff baseline** — priority cascade:
1. Staged changes (`git diff --cached`) when staged changes exist
2. Unstaged changes (`git diff`) when no staged changes
3. User-specified branch (e.g. "against develop")
4. PR URL
5. Current branch vs default branch (fallback)

## Specialist Toolbox (fast mode reference)

Seven specialists consulted per-finding (not per-file). The value is forcing genuinely different questions about the same code — each specialist triggers a different reasoning path.

| ID | Specialist | Expertise | Core Question |
|----|-----------|-----------|---------------|
| verify | Positive Validation | Correctness | "This code claims to do X — does it actually?" |
| nitpick | Bug Hunter | Edge cases | "There's definitely a bug here — where is it?" |
| newcomer | Fresh Eyes | Readability | "First time seeing this — do I understand it?" |
| attacker | Attacker | Security | "How do I break this?" |
| revert | Revert Challenge | Necessity | "If we revert this change, what breaks?" |
| maintainer | Future Maintainer | Maintainability | "What will someone curse about this in 6 months?" |
| senior | Senior Reviewer | Architecture | "What would I flag in a PR review?" |

**Selection guidance** (per finding, not per file):
- `verify`: relevant for almost any finding.
- `nitpick`: findings involving conditional logic or arithmetic.
- `attacker`: findings involving auth, input validation, data exposure.
- `newcomer`: findings about complex or unclear code.
- `revert`: findings about changes that seem unnecessary or out of scope.
- The rest: agent judgment.

## Review Flow

Both modes share the same file-by-file review. The only difference is what happens when a finding is spotted.

### 0. Ask for spec/plan

Ask if there is a related spec or plan file. If provided, use as background knowledge throughout the review. Pragmatic spec comparison: only flag obvious contradictions or large unrelated modifications — small refactoring is acceptable.

### 1. Read all changed files

Read every changed file first to build the full picture before reviewing.

### 2. Go through files one at a time

Interrogate every aspect of each change. When you spot a finding:

**Deep mode** — discuss directly with the user, one question at a time, until reaching shared understanding before moving on.

**Fast mode** — consult specialists before involving the user:
1. Pick 3+ specialists relevant to this specific finding.
2. Consult sequentially — each specialist sees earlier opinions, then gives their own opinion + confidence (high / medium / low).
3. Classify the finding:
   - **needs change**: any specialist rated high confidence.
   - **uncertain**: highest rating is medium, or specialists disagree.
   - **no issue**: all rated low → drop silently.
4. After all findings in a file are classified, merge duplicates and link related findings.
5. Present surviving findings (needs change + uncertain) to the user one at a time — same grill-mode interrogation as deep mode.
6. Files with no surviving findings: advance silently with a one-line summary.

### 3. Self-explore when needed

In both modes, if a question can be answered by exploring the codebase, specs, or tests, explore them yourself instead of asking the user. "Fast" means minimizing user interruption, not skipping agent work.
