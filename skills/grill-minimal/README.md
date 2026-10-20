# grill-minimal

Grill a plan, decision, or idea toward the smallest complete solution: the simplest approach and narrowest scope that still meet its goals and constraints. Unlike plain grilling, which follows every question the plan raises, it first asks whether the scope behind each question is needed, puts what no goal needs up as a cut, and recommends the smallest answer that still meets every goal and constraint.

## When to use

- A plan has grown, and you suspect parts of it serve no goal.
- You're choosing between approaches and want the simplest one that still does the whole job.
- An idea is about to become work, and you want its smallest complete version settled first.

This skill must be invoked explicitly. To stress-test a plan without the pull toward less, use `grilling` directly, because grill-minimal will keep proposing cuts to a design you mean to keep broad.

## Before you start

The interview comes from [mattpocock/skills](https://github.com/mattpocock/skills), installed in the same agent:

- `grilling` is required; without it, grill-minimal reports it missing and stops.
- `domain-modeling` is optional; with it, settled terms land in the repository's `GLOSSARY.md` and hard-to-reverse decisions can become ADRs under `docs/adr/`.

## Getting started

```text
/grill-minimal <plan, decision, or idea>
```

In Codex, use `$grill-minimal <plan, decision, or idea>`. With no argument, it grills the plan the conversation is about. Stating the goals and constraints in the invocation saves the round that would otherwise ask for them.

## Smallest complete

The two words hold each other in check. _Smallest_: every piece of scope traces back to a goal or constraint you stated, and what traces to none comes back to you as a proposed cut. _Complete_: what a goal or constraint requires stays, even when it is the expensive part. Without goals there is nothing to measure smallest against, which is why vague goals get settled before anything else. The goals themselves stay yours; the cutting happens in how they are met.

## It's working if

- It asks what the plan must achieve and what it can't violate before anything that depends on them, unless you already said.
- Its recommendations include cuts, each traced to no goal or constraint needing that scope.
- What a stated constraint requires survives, even when you suggest dropping it to go faster.

## Limitations

- It trims the approach and scope, never the goals; a goal you'd be better off dropping stays until you drop it.
- It ends with settled decisions, not an implementation.
- Without `domain-modeling`, the settled terms and decisions stay in the conversation.
