# tldr: Honor explicit scan-time signals

## Problem Statement
How might we make the `tldr` skill respect user-specified scan times
(`in 10 mins`, `quick`) without inflating SKILL.md or replacing the
2-min default?

## Recommended Direction
Add **one line** of runtime rule to `skills/tldr/SKILL.md`, immediately
after the existing baseline scan-target line. Do not modify the baseline
framing — the 2-min default is working as intended; the gap is only the
missing override rule.

The added rule (candidate α):

```
If the user gives an explicit scan time (e.g. `in 10 mins`, `quick`),
honor it over the 2-min default.
```

Density signals (`詳細一點`, `深一點`, `完整版`) are a different signal
class and are **not** covered by this rule. They are deferred until
observed in a real session.

`README.md` is not touched — it is already silent on time budget, and
SKILL.md is sufficient as the runtime surface.

## Key Assumptions to Validate
- [ ] Users express scan-time preferences with explicit time words
      (`in X mins`, `quick`, `5 分鐘版`) rather than density phrases.
      **Validate:** watch the next 2–3 real `/tldr` sessions and log the
      prompt shapes that miss the rule.
- [ ] One added line is enough; the model will not still cite "2-minute
      budget" as an internal constraint when a user-specified time is
      present. **Validate:** run a follow-up `in X mins` session and
      inspect the model's reasoning for self-reprimand phrasing.

## MVP Scope

**In:**
- Single added line in `skills/tldr/SKILL.md` after the baseline
  scan-target line.
- Example list in the rule: `in 10 mins`, `quick`.

**Out (deferred):**
- Density signals (`詳細一點`, `深一點`, `完整版`).
- Output destination default (feedback 1.3).
- Link discipline (feedback 1.2).
- Description widening (feedback 2.1).
- Condense-in-hand vs research-then-condense split (feedback 2.2).
- Negative rule "don't self-reprimand" (Variation D).
- Rewriting the baseline `two minutes` framing.

## Not Doing (and Why)
- **Don't touch baseline framing** — user's explicit judgment: 2 min
  is fine; only the override rule is missing.
- **Don't cover density signals this pass** — different signal class,
  no direct observation in the source incident.
- **Don't bundle 1.2 / 1.3 / P2 / P3** — N=2 observation base (one
  session, two invocations) is too thin to justify 9 simultaneous
  edits. Wait for stronger evidence.
- **Don't create planning-with-files artifacts** — this scope (one-line
  patch + one-pager) does not warrant task_plan / findings / progress.

## Open Questions
- After the fix lands, does the model still internally cite "2-min
  budget" when the user asks for 10 min? If yes, the next iteration
  escalates to Variation D (explicit negative rule).
- Should this rule eventually move into a shared meta-rule for skills
  with numeric defaults (applies to any skill where user signals can
  override a default)? Decision: premature — revisit after a second
  skill exhibits the same symptom.
