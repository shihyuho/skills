# scope-it-remake

A delivery-map coordinator: discuss scope, tickets and delivery with interchangeable planning skills, approve the whole package, then publish and verify it.

The Map is an index of agreed deliverables, not a progress tracker. Scope and Map share one planning post; one ticket is a separate comment on that home, while multiple tickets are child items. Existing complete artifacts can satisfy the planning work without rerunning their producer.

Choose the skills for scope and tickets independently, by name or with `--scope-source <name>` / `--ticket-source <name>`. Confirmed defaults are remembered across repositories; v3 preferences record consent to future planning delegation, while older preferences require a one-time migration confirmation. Publication and Git writes still require the final package approval.

## Planning skill examples

| Collection | Scope | Planning / ticket content |
| --- | --- | --- |
| Matt Pocock | `to-spec` | `to-tickets` |
| [Superpowers 6.2.0](https://github.com/obra/superpowers/tree/v6.2.0/skills) | `brainstorming` | `writing-plans` |
| [Addy Osmani](https://github.com/addyosmani/agent-skills/tree/7cb7a20bb38b199728d456999c725a0488490ab6/skills) | `spec-driven-development` | `planning-and-task-breakdown` |

These are concrete examples, not defaults or required installations. Their normal workflows can include file writes, commits or further skills; the planning delegation stops at content and required checks. Superpowers produces an implementation plan, whose coding steps are not automatically delivery tickets. Addy's planning skill can supply vertical slices with acceptance criteria and dependencies. Use the actual output's role, and avoid repeating work already supplied by an upstream skill.

Approved ADRs, `CONTEXT.md` changes and similar planning files are saved on the actual delivery path, with a verified version another agent can retrieve. This is part of publishing a complete plan, not starting implementation, and needs no particular Git helper skill. Shared integration delivery remains optional.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it-remake -g
```
