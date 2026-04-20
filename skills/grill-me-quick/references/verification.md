# Reference: Subagent Verification & Aggregation

Loaded when `grill-me-quick` escalates a decision to Chain-of-Verification (CoVe).

## Why subagents, not a second self-prompt

The agent that drafted the answer cannot reliably verify it — seeing the draft biases the verifier toward rationalizing. Independence is the point. Subagents have their own context, so they cannot peek.

## Subagent input pack

Dispatch **one subagent per claim, in parallel**. Each receives a structured input pack — nothing else from the draft or surrounding conversation:

```
CLAIM:           <the single claim being verified, one sentence>
LOAD_BEARING:    yes | no
PROJECT:         <name · primary language · framework + version>
RELATED_PATHS:   <file paths the subagent may Read, if any>
DOMAIN_QUIRKS:   <up to 2 bullets, each ≤ 1 line; project-specific deviations
                  from standard behavior — e.g. "authenticate() is patched to
                  bypass MFA for service accounts">

# Deliberately NOT passed (independence is load-bearing):
# - The draft answer or any reasoning from it
# - The decision's alternatives or trade-off analysis
# - Other claims or their verification results
# - Main agent's self-score
```

## Subagent brief

- **Adversarial reviewer.** Its job is to find problems, not to agree.
- **Tool access:** WebSearch / Grep / Read / Bash — prefer real evidence over model memory.
- If the pack feels insufficient to judge, return `uncertain`. Do not guess.

## Required output (strict)

```
claim:      <what is being verified>
verdict:    confirmed | refuted | uncertain
evidence:   <source / file:line / command output>
confidence: H | M | L
```

## Aggregation

Evaluated in order; first matching rule wins.

0. Subagent output violates the schema (missing or invalid fields):
   - **Load-bearing** → ask the user about that claim directly.
   - **Peripheral** → treat as `uncertain` + L for rule 4.
   - Do not retry. Do not attempt best-effort parse.
1. Any `refuted` on a **load-bearing** claim → `fact` ≤ 3, stop and ask user.
2. Any `uncertain` on a **load-bearing** claim → ask user about that claim. Do not compute `fact` from the remaining subagents alone. Verification failure on a decision's keystone claim is the user's call, not the aggregator's.
3. `refuted` on **peripheral** claim(s) → −1 from `fact` per peripheral refutation, floor at 4.
4. `uncertain` on **peripheral** claim(s) → treat as L confidence for rule 5.
5. Otherwise → `fact` = lowest confidence across all claims (H=9, M=6, L=3 as rough mapping).

If a subagent's evidence suggests a `peripheral`-tagged claim is actually load-bearing (decision collapses without it), re-tag before aggregating.
