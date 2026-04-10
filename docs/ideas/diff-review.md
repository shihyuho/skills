# grill-diff: Fast Mode Enhancement

## Problem Statement

How might we make grill-diff faster and more practical for daily use — supporting both self-review and PR review — while keeping its depth when needed, and adding spec/plan cross-referencing to catch implementation drift?

## Recommended Direction

Add a **fast mode** to the existing `grill-diff` skill. Fast mode spawns multiple Strategy personas that internally grill each file. If all personas pass, the file is auto-advanced silently. If any persona finds an issue, the agent enters the existing grill-diff interactive mode to interrogate the user.

No separate skill. No Aspect toolbox. The Strategy personas ARE the review — each one naturally covers the dimensions it cares about. `attacker` looks at security, `newcomer` looks at readability, `senior` looks at architecture. No need to tell them what to look at.

The key insight: fast mode isn't "less thorough." It's multiple versions of the griller grilling the code internally first, before deciding whether to grill you.

## Key Assumptions to Validate

- [ ] LLM applying 3+ different Strategy personas on the same file actually catches more issues than a single careful pass — test with real diffs of varying complexity
- [ ] Agent can reliably self-select appropriate strategies from the toolbox without human guidance — risk of always picking the same 3
- [ ] Structured summary at the end provides enough signal for the user to decide which files need deeper review

## Design Decisions

### Mode Selection

- If the user's prompt clearly indicates a mode (e.g., "快速掃一下" vs "仔細烤"), use that mode
- If ambiguous, ask the user before starting
- Two modes: `fast` (agent grills itself with multiple personas) and `deep` (current grill-diff behavior)
- `review-diff` is the default for this skill; users who want interactive deep-dive should use `grill-diff` instead

### Diff Scope (priority cascade)

| Priority | Source | Trigger |
|----------|--------|---------|
| 1 | User-specified files | User explicitly lists file paths |
| 2 | Staged changes | `git diff --cached` when staged changes exist |
| 3 | Unstaged changes | `git diff` when no staged changes |
| 4 | Branch vs branch | User specifies e.g., `against develop` |
| 5 | PR URL | `https://github.com/org/repo/pull/123` |
| 6 | Branch diff | Current branch vs default branch (fallback) |

### Strategy Toolbox (Mindset / Persona)

Agent selects **at least 3** Strategy personas per file. Each persona conducts a full review from its own mindset — no formal Aspect framework needed, each persona naturally covers the dimensions it cares about:

| ID | Strategy | Mindset | Core Question | Best For |
|----|----------|---------|---------------|----------|
| `verify` | 正向驗證 | Developer | 「這段 code 說要做 X，它真的做到了嗎？」 | Logic errors, spec misalignment, missing edge cases |
| `nitpick` | 挑毛病 | Skeptic | 「這裡一定有 bug，在哪？」 | Race conditions, off-by-one, implicit assumptions |
| `newcomer` | 新人視角 | Junior engineer | 「我第一次看這段，我看得懂嗎？」 | Readability, unclear naming, missing context |
| `attacker` | 攻擊者 | Red team | 「我要怎麼讓這段 code 壞掉？」 | Security holes, malicious input, resource exhaustion |
| `revert` | 刪除挑戰 | Minimalist | 「把這個改動 revert 掉，什麼會壞？」 | Scope creep, unnecessary modifications, over-engineering |
| `maintainer` | 維護者未來視角 | You in 6 months | 「半年後改這段的人會罵什麼？」 | Tech debt, hidden coupling, missing tests |
| `senior` | Review 老手 | Senior reviewer | 「PR review 我會問什麼？」 | Architecture decisions, performance concerns, pattern consistency |

### Flow Per File (Fast Mode)

1. Agent picks 3+ strategies appropriate for this file
2. Runs each strategy as a complete review pass
3. All passes clean → auto-advance to next file (silent)
4. Any pass finds an issue → **enter grill mode**: stop and interrogate the user one question at a time, probing every aspect of the finding until shared understanding is reached, then continue to next file

### Spec/Plan Cross-Reference

- Gather spec/plan files upfront (existing grill-diff step 2)
- Pragmatic approach: only flag **obvious** deviations
  - Changes that contradict spec requirements
  - Large modifications not covered by any spec item
  - Small related refactoring (renaming, formatting) is acceptable
- Include spec alignment status in the summary report

### Summary Report

After reviewing all files, produce a structured summary:

```
## Review Summary

**Mode:** fast | **Files reviewed:** 12 | **Issues found:** 3
**Spec:** task_plan.md

### Files

| File | Status | Findings |
|------|--------|----------|
| src/auth.ts | Issue | Potential null dereference on line 42 |
| src/api.ts | Clean | — |
| src/config.ts | Drift | Change not covered by spec |
| ... | ... | ... |

### Spec Alignment
- [ ] Requirement A: Implemented in src/auth.ts, src/api.ts
- [x] Requirement B: No corresponding changes found
- [ ] Requirement C: Implemented in src/handler.ts

### Overall Verdict
3 files need attention. Want to deep-dive into any of them?
```

## MVP Scope

Modify `grill-diff` SKILL.md to add:
1. Mode selection logic (fast/deep, ask if ambiguous)
2. Strategy toolbox definition
3. Fast mode workflow (multi-persona self-grill → auto-advance or enter grill mode)
4. Summary report template
5. Updated diff scope cascade (add user-specified files)

## Not Doing (and Why)

- **New skill** — without Aspect toolbox, fast mode is just grill-diff with internal personas first; same identity, same fire
- **Aspect toolbox** — Strategy personas naturally cover the dimensions they care about; a formal Aspect framework would be telling them what they already know
- **Parallel agent architecture** (like code-review.md reference) — overkill for interactive review, adds complexity without proportional value
- **Strict spec enforcement** — pragmatic approach catches real drift without false positives on reasonable refactoring
- **Confidence scoring / filtering** (like code-review.md reference) — adds a layer of abstraction between the agent and the user; direct communication is better

## Open Questions

- Should the summary report format be customizable, or is one format enough?
- How to handle very large diffs (50+ files) in fast mode — batch by directory? prioritize by risk?
- Should deep mode also get the Strategy toolbox, or keep its current "ask about everything" behavior?
