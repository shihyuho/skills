---
name: code-tour
description: Guide an engineer through a feature's implementation with diagrams, concrete execution scenarios, and source-linked reading stops.
license: MIT
disable-model-invocation: true
---

# code-tour

Turn a code-reading question into a guided route through the implementation. Help the reader locate the moving parts and predict what happens in a concrete scenario.

## Choose the route

Use the conversation's feature, symbol, entry point, or confusing behavior as the starting point. Infer the reader's familiarity and desired depth from context. If no target can be identified, ask for the feature or code location needed to begin.

For a broad request, choose one representative behavior, state its boundary, and complete that first tour. For a narrow question or follow-up, cover only the relationship needed to answer it. Continue the same route when the reader asks to go deeper.

Use the requested checkout or revision without switching branches. Explain in chat by default; save a document only when requested. Inspect code without modifying it. Running code is optional evidence gathering: use an isolated, side-effect-free check when useful, and keep existing execution permissions in force.

## Follow the implementation

1. Find the entry point and the code that actually interprets the starting symbol. Use available symbol/reference navigation, with text search as a fallback. Follow callers, registration, configuration, or dispatch when they determine which implementation runs.
2. Trace a concrete input through the deciding condition to the returned value, state change, or external effect. Expand across files only while a missing relationship affects the explanation.
3. Check behavior claims against their implementation. A declaration, annotation, class name, comment, or inheritance edge can suggest where to look; the consumer and its wiring establish the effect. For dependency behavior, inspect the applicable version's source or authoritative documentation.
4. Where loading, asynchronous work, or transactions affect the result, locate their boundaries and show which effects occur inside and outside them. Report unresolved configuration or unavailable code as an uncertainty at the affected step.

Keep source locations for the decisive relationships while exploring. Distinguish a trace inferred from source from an execution actually observed, and label invented inputs as illustrative.

## Build the tour

Start with what this path accomplishes and one concrete input → outcome. Then connect the explanation, useful diagrams, and a navigable reading route. Adapt the order to the reader's question rather than narrating the order of tool calls.

Choose diagrams by what they clarify:

| Missing relationship | Useful view | Include |
| --- | --- | --- |
| Which types collaborate, implement a contract, or consume a marker | Class diagram | Relevant types, responsibilities, and verified realization/dependency relationships. |
| Who acts when, where a decision changes the path, or when data/effects appear | Sequence diagram | One concrete scenario, actual participants, calls, deciding conditions, and resulting effects. |
| Both structure and execution are needed | Complementary views | Shared names and an explicit connection between a runtime participant and its type. |
| A local expression or small distinction already answers the question | Prose, a snippet, or a small table | The deciding code and its consequence. |

Use Mermaid when the host supports it, or readable text when it does not. Honor a requested diagram type while explaining any important behavior it cannot establish. Keep actual identifiers recognizable; use aliases only to clarify roles. Every edge must represent a verified relationship, and sequence branches must match the source conditions. Summarize irrelevant internals and identify consequential omissions instead of drawing the whole repository.

Place explanations of conditions, data changes, and effects next to the corresponding diagram or step. Link nearby claims to precise source locations using the host's navigable file links or revision-pinned repository links. A directory listing or a link to a declaration alone does not explain where behavior is decided.

Give the reader an ordered route back into the code: for each useful stop, provide the source location and what to inspect there. Organize stops around questions such as where this begins, why this implementation is selected, and where the result changes. If saving a tour, record the repository and inspected revision, noting relevant working-tree differences. Use revision-pinned repository links or paths relative to the saved document so the route survives outside the current workspace.

Before finishing, check that the tour identifies the entry point, links the decisive relationships to source, and derives the illustrated result from those steps—or names the missing evidence. When a contrast helps, show the smallest changed input or condition and its different outcome. Invite deeper exploration only where it would resolve a remaining question; a quiz or approval between stops is optional, not part of the default tour.
