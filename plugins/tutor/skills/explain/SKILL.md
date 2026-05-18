---
name: explain
description: Explain a concept, passage, or piece of code top-down — the whole picture first, then drill into the parts the learner picks. Use when the user invokes `/tutor:explain` or asks to understand something top-down or big-picture-first; for a sustained multi-session course use the `course` skill instead.
license: MIT
---

# Explain

Explain whatever the user points at — a topic, a passage, a piece of code — using top-down learning.

Run it interactively, not as one dump:

1. Open with the whole picture — what the subject is, what it is for, why it matters — then map out the handful of parts it breaks into.
2. Ask which part to open. The learner's pick drives the depth; explain that part the same way, and recurse as far as they pull.

If the subject is in the codebase, explain it from the real code instead of from memory.
