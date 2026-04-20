# grill-me-quick

Grill the user's plan or design, but auto-decide on confident calls — ask only when uncertain or high-risk. Uses Chain-of-Verification (CoVe) to validate factual claims via independent subagents when confidence is borderline.

## How It Works

1. **Walk the design tree** — one decision at a time, provide a recommended answer.
2. **Tag claims as `load-bearing` or `peripheral`** — the tag IS the identification of a claim; untagged sentences are not claims.
3. **Self-score two axes** — `fact` (claims true?) and `reason` (argument sound?).
4. **Escalate to CoVe verification** only when confidence is borderline (5–7) or blast radius is high.
5. **Subagents verify independently** — structured input pack, adversarial brief, strict output schema. The verifier never sees the draft.
6. **Gate** — lock in, ask the user, or escalate.

## Design Basis

Built on [Chain-of-Verification (Dhuliawala et al., 2023)](https://arxiv.org/abs/2309.11495) — specifically the *factored* and *factor+revise* variants where verification questions are answered without the verifier seeing the draft. This avoids the confirmation bias inherent in self-scoring.

The paper's key finding: independent verification raises long-form factual accuracy by ~28% over a model that scores its own work. Subagents are the natural implementation of that independence.

## Usage

```
/grill-me-quick <target>
```

Examples:

```
/grill-me-quick this migration plan
/grill-me-quick the auth refactor in src/auth/
```

If invoked without a target, the skill asks what to grill.

## Installation

```bash
npx skills add shihyuho/skills --skill grill-me-quick -g
```
