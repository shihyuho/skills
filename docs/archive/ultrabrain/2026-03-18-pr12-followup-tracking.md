# PR #12 Follow-up: Tracking Issue for Inconsistencies and Fix Order

## Summary

PR #12 introduced several improvements to the `ultrabrain` skill, including staged recall, an updated map taxonomy, and stronger thin-card rewrite rules. This tracking issue captures findings from post-PR review indicating that some downstream artifacts (`commands/`, skill-local evals, and validation scripts) have not yet fully caught up to the updated canonical behavior. The goal is to align on the canonical contract, prioritize findings, and agree on a fix order before implementing changes.

## Findings

### High priority

**Finding 1: Eval 4 validates a deprecated taxonomy concept**

- **Issue**: Eval 4 in `skills/ultrabrain/evals/ultrabrain-evals.json` (line 44) expects a "troubleshooting lens" as the first recall action. This concept existed before PR #12 but was removed from the canonical taxonomy. The expectation persists in the eval file but no longer reflects current behavior.
- **Type**: Confirmed inconsistency — the eval explicitly references a concept that was removed from `skills/ultrabrain/SKILL.md`.
- **Evidence**:
  - `skills/ultrabrain/evals/ultrabrain-evals.json` lines 43–44: expects "Starts with a troubleshooting lens or domain debugging path"
  - `skills/ultrabrain/SKILL.md`: current taxonomy centers on `home`, `domain maps`, `lessons-moc`, `general-moc`, and `review lenses`; no "troubleshooting lens" appears

**Finding 2: Recall command does not fully reflect the staged recall workflow**

- **Issue**: `commands/ultrabrain-recall.md` frames recall as a single "Map recall" action executed once before planning. The canonical skill describes a staged recall workflow with seed recall, gap-driven loops, and targeted high-value recall before execution. The command file's wording does not capture this multi-stage nature.
- **Type**: Validation gap — the command guidance is incomplete but does not contradict the skill directly.
- **Evidence**:
  - `commands/ultrabrain-recall.md` line 5: "starting with the **Map recall** portion"
  - `skills/ultrabrain/SKILL.md` section "Recall Workflow" (lines 167–245): describes seed recall → gap-driven recall → targeted recall, not a single recall pass

**Finding 3: Eval 8 assumes decision=skip but skill does not formally define it**

- **Issue**: Eval 8 expects the model to consider `decision=skip` as a valid capture outcome when a lesson is too generic or already covered. However, `skills/ultrabrain/SKILL.md` only defines `decision=rewrite-first`, `decision=create`, and `decision=update`. The `decision=skip` behavior is implied in the eval but not explicitly documented as part of the canonical contract.
- **Type**: Open decision — the eval introduces an expectation that the skill does not formally codify. Whether `decision=skip` should be added to the contract is undecided.
- **Evidence**:
  - `skills/ultrabrain/evals/ultrabrain-evals.json` lines 87–88: expects "Considers `decision=skip` as a valid outcome"
  - `skills/ultrabrain/SKILL.md` lines 294–337: only defines `decision=rewrite-first`, `decision=create`, and `decision=update`

### Medium priority

**Finding 4: Thin-card validation script does not catch all spec violations**

- **Issue**: The validation script `skills/ultrabrain/evals/check_ultrabrain_thin_card.py` checks for thin-card detection and rewrite-first signals, but it does not catch cases where the response jumps to a final decision (like `decision=create`) without first signaling rewrite. The script does have a check for this (lines 53–58), but it does not validate that all required rewrite signals are present before any final decision appears.
- **Type**: Validation gap — the script exists but may miss subtle violations where rewrite-first is not explicitly stated but should have been.
- **Evidence**:
  - `skills/ultrabrain/evals/check_ultrabrain_thin_card.py` lines 27–30: checks for `decision=create` or `decision=update`
  - `skills/ultrabrain/SKILL.md` lines 303–305: requires returning `decision=rewrite-first` before any create/update decision for thin cards

**Finding 5: Groom command delegates detailed guidance to references/map-grooming.md**

- **Issue**: `commands/ultrabrain-groom.md` provides minimal invocation guidance and refers users to `skills/ultrabrain/references/map-grooming.md` for detailed grooming rules. Whether this two-step lookup (command → reference) is sufficient for command users who need quick, actionable guidance is an open question.
- **Type**: Open question — the command functions as designed, but its adequacy for the intended user flow is not validated.
- **Evidence**:
  - `commands/ultrabrain-groom.md` lines 5–6: "follow the **MOC Grooming** section in `SKILL.md`"
  - The command does not explicitly mention the detailed rules in `references/map-grooming.md`

## Proposed Discussion Questions

1. Is `skills/ultrabrain/SKILL.md` the canonical source of truth for post-PR #12 behavior when `commands/` or `evals/` disagree?

2. Should `decision=skip` be added to the canonical capture contract, or should eval 8 be narrowed to the existing decision set?

3. Should fixes land in one follow-up PR or as a small ordered sequence of PRs?

## Recommended Fix Order

1. Clarify the canonical contract where it is still ambiguous.
2. Update `skills/ultrabrain/evals/ultrabrain-evals.json` to match that contract.
3. Update `commands/` files so invocation guidance matches the skill.
4. Tighten machine checks such as `skills/ultrabrain/evals/check_ultrabrain_thin_card.py`.
