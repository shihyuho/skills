---
name: tradeoffs
description: "Decide which discussed option is most worth choosing by comparing incremental value with added cost, risk, and complexity. Use when the user faces a real choice between alternatives and wants a recommendation or explicit trade-off analysis before deciding."
license: MIT
---

# tradeoffs

## Invocation input

`$ARGUMENTS` below means the arguments supplied when the skill is invoked explicitly; model invocation usually leaves it empty. In inherited `Context` blocks, run each `!` command to collect the named value; those expressions are not expanded automatically in a skill.

Turn the options in **this conversation** into a recommendation about which is most worth choosing.

`$ARGUMENTS`: an optional focus hint (`focus on caching`) or save path. Empty, including model invocation, means the whole discussion and printing to chat.

## Decision method

1. State the goal, success boundary, and baseline. The baseline is usually the simplest viable option or not making the proposed change.
2. Compare every option against that same baseline:
   - **Incremental value** — what outcome it improves or harm it prevents; consider severity, exposure conditions, blast radius, and recoverability.
   - **Incremental burden** — implementation and long-term cognitive, testing, operational, and migration costs, plus new failure modes the option creates.
   - **Sufficiency and reversibility** — whether a cheaper option already meets the success boundary and how difficult the choice is to revise.
   - **Best fit** — when several options are viable, identify what distinguishes them and show what each optimizes, sacrifices, and assumes relative to the user's priorities.
3. Mark decision-relevant claims as **known**, **inferred**, or **unknown**. Keep only unknowns that could change the recommendation, frame each as a precise question, and use qualitative comparisons unless the available evidence grounds numeric probabilities, costs, or scores.
4. Pass each decisive unknown through a **research gate**:
   - **Local verification** — resolve facts in the supplied artifacts or current working directory with a small, safe, read-only check.
   - **External research** — when the answer depends on outside knowledge, investigate high-trust primary sources such as official documentation, specifications, source code, or first-party APIs.
   - **Explicit assumption** — when resolution needs new authority, writes, material scope expansion, or disproportionate effort, state the assumption instead of blocking the recommendation.
   Complete the gate when every decisive unknown is either resolved with evidence or carried into the recommendation as an explicit assumption.
5. Recompare the options after the research gate, then choose the option whose incremental value best justifies its incremental burden. Make a recommendation under imperfect evidence; when uncertainty dominates, prefer the simplest sufficient, reversible choice or the smallest validation step that preserves optionality.
6. State the evidence or threshold that would reverse the recommendation.

## Rules

- Ground options and evidence in the conversation and supplied artifacts. A clearly missed lower-cost option may be added, labelled **(new, not previously discussed)**.
- Treat the existence of a bug, race, risk, or safeguard as evidence to weigh; justify action through the actual value and burden.
- Prefer the simplest option when it is sufficient, and choose broader coverage only when its additional value earns the burden.
- When alternatives are implicit, compare the proposed change with the baseline. When no real choice exists, ask for the decision question.
- Include only implementation detail and tradeoffs that distinguish the decision.

## Output

Keep code, paths, and `file:line` verbatim. Cite every externally researched decision-relevant claim next to the source that supports it.

- Lead with the recommended option and the decisive reason.
- Show the smallest useful comparison of incremental value versus incremental burden; use a table only when it improves the decision.
- Identify the assumptions and weak evidence on which the recommendation depends.
- End with the flip conditions and the next action, if one is needed.
- Use only the headings the decision needs.

## Save

Default: print to chat, then ask whether to save. Default path `docs/decisions/<slug>.md` in the **current project** repo (kebab-case slug, `mkdir -p` first). If `$ARGUMENTS` gives a path, save there. Never overwrite — suffix `-2`, `-3`, …

ARGUMENTS: $ARGUMENTS
