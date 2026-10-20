---
name: grill-minimal
description: "Grill a plan, decision, or idea toward the smallest complete solution: the simplest approach and narrowest scope that still meet its goals and constraints."
license: MIT
disable-model-invocation: true
---

# grill-minimal

Grill a plan, decision, or idea toward the smallest complete solution: the simplest approach and narrowest scope that still meet its goals and constraints. Unlike plain grilling, which follows every question the plan raises, it first asks whether the scope behind each question is needed, and recommends the smallest complete answer; whatever a goal or constraint requires stays in, and so does what the kept scope needs to work.

Take the plan, decision, or idea, with any goals and constraints already stated, from `$ARGUMENTS` or the conversation. Load `grilling` and run it on that subject; it conducts the interview and decides when the session is done. When `grilling` can't be loaded, report it missing and stop. When `domain-modeling` is available, load it too, so the terms and decisions the session settles are written down as they land.

## Smallest complete

The goals and constraints are the yardstick every answer is measured against, so when they are unstated or vague, settle them before the questions that depend on them. They are the user's to set; the cutting happens in the approach and scope that serve them.

Smallest cuts capabilities. Before taking up a piece of scope, trace it to the goal or constraint that needs it. Scope that traces to none goes to the user as a cut, with the cut as your recommendation.

Complete keeps two things, even when they are the costly part: what a goal or constraint requires, and what makes the kept scope work, meaning its correct behavior, its edge cases, its security, its tests, and the quality bar the codebase already holds. The second half covers the quality of what stays, never a new capability.

Each recommended answer is the smallest complete one: the simplest approach that fully meets the goals and constraints and works.
