---
name: grill-diff
description: Review git changed files using deep interactive grilling or fast multi-strategy self-review. Deep mode interrogates every aspect of each change one question at a time. Fast mode applies multiple reviewer personas internally, only stopping for interaction when issues are found.
---

## Mode Selection

Determine the review mode from the user's prompt:
- Clearly fast (e.g. "快速掃", "fast") → fast mode.
- Clearly deep (e.g. "仔細烤", "grill", "deep") → deep mode.
- Ambiguous (including bare `/grill-diff` with no modifier) → ask the user which mode they want.

## Diff Scope

Two independent dimensions that combine freely (e.g. "fast against develop src/auth.ts" reviews only `src/auth.ts` diffed against develop).

**File scope** — which files to review:
- User-specified files if explicitly listed, otherwise all changed files.

**Diff baseline** — what to compare against (priority cascade):
1. Staged changes (`git diff --cached`) when staged changes exist
2. Unstaged changes (`git diff`) when no staged changes
3. User-specified branch (e.g. "against develop")
4. PR URL
5. Current branch vs default branch (fallback)

## Strategy Toolbox

Seven reviewer personas. The value is not cognitive separation — it is forcing genuinely different questions about the same code. Each persona triggers a different reasoning path. When switching strategies, actually shift your line of questioning; do not go through the motions.

| ID | Name | Mindset | Core Question |
|----|------|---------|---------------|
| verify | Positive Validation | Developer | "This code claims to do X — does it actually?" |
| nitpick | Bug Hunter | Skeptic | "There's definitely a bug here — where is it?" |
| newcomer | Fresh Eyes | Junior engineer | "First time seeing this — do I understand it?" |
| attacker | Attacker | Red team | "How do I break this?" |
| revert | Revert Challenge | Minimalist | "If we revert this change, what breaks?" |
| maintainer | Future Maintainer | You in 6 months | "What will someone curse about this in 6 months?" |
| senior | Senior Reviewer | Senior reviewer | "What would I flag in a PR review?" |

**Selection guidance** (not hard rules):
- `verify`: relevant for almost every file.
- `nitpick`: especially for files with complex conditional logic or arithmetic.
- `attacker`: prioritize for files handling user input, auth, APIs.
- `newcomer`: prioritize for complex logic, new modules.
- `revert`: prioritize for files with many scattered changes.
- The rest: agent judgment.
- This list may evolve based on effectiveness.

## Fast Mode

0. Ask if there is a related spec or plan file. If provided, use as background knowledge for all strategies. Pragmatic spec comparison: only flag obvious contradictions or large unrelated modifications — small refactoring is acceptable.
1. Read all changed files first to build the full picture.
2. For each file, pick 3+ strategies with a short rationale. Output the selection, e.g.:
   `src/auth.ts → verify, attacker, revert (handles auth + scattered changes)`
3. Run each strategy as a complete review pass with genuine question switching.
4. Output results:
   - Clean files compressed to one line: `✓ src/api.ts — verify, attacker, newcomer: all clean`
   - Issues expanded with per-strategy results, e.g.:
     ```
     src/auth.ts → verify, attacker, revert (handles auth + scattered changes)
     verify: clean
     attacker: ⚠️ token validation can be bypassed with empty string
     revert: clean
     ```
5. All clean → auto-advance to next file.
6. Any issue → enter grill mode: interrogate the user one question at a time until shared understanding. Multiple findings addressed in natural order. Then next file.

If a question can be answered by exploring the codebase, specs, or tests, explore them yourself instead of asking.

## Deep Mode

Review changed files one by one. Interrogate every aspect of each change, one question at a time, until reaching shared understanding before moving to the next file.

0. Ask if there is a related spec or plan file to understand the goal of the changes.
1. Read all changed files first to build the full picture.
2. Go through files one at a time. Ask one question at a time.

If a question can be answered by exploring the codebase, specs, or tests, explore them yourself instead of asking.
