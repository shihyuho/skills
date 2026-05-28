---
name: explain
description: Explain a topic, a passage, or a piece of code top-down — open with the whole picture, then drill into the parts the learner picks. Use when the user wants a single subject explained big-picture-first, asks for a top-down explanation, or wants to explore the subject and drill in on demand instead of one exhaustive dump.
license: MIT
---

# Explain

Explain whatever the user points at — a topic, a passage, a piece of code — top-down: open with the whole picture (what the subject is, what it's for, why it matters), then map its handful of parts.

Then judge whether to gate. Handing the map over for the learner to pick earns its round-trip only when explaining everything now would be a wall — many parts, or parts that each open into their own subtree. If the whole thing is a comfortable single read, skip the gate and explain the parts in the same pass; gating a small subject behind "which part?" is pure friction. Either way, honor an explicit signal ("all of it" / "one at a time").

When you drill down, ask which part to open, explain it the same way, and recurse as deep as the learner pulls. Start each level with a breadcrumb (e.g. `Indexes › B-tree`) so the learner sees where they are.

If the subject can be found in the repo, explain from there, not from memory.
