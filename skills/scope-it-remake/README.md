# scope-it-remake

Coordinate interchangeable scope and ticket workflows, then connect their published outputs in one Delivery Map.

The selected skills own their content, reviews and publication. Scope is confirmed and published first, then passed to the ticket skill; the coordinator finally confirms and publishes the Map with any needed handoff links. These are separate approvals, so Scope and tickets are visible before the Map.

Publication keeps the agreed placement: an existing issue hosts Scope without replacing the report, one ticket follows Scope on that same issue, and multiple tickets become children. These preferences are passed to the selected skills while retaining their full content and checks.

The Map is an index, not a progress tracker; every ticket links the information another agent needs without this skill or the planning conversation.

Choose scope and ticket skills independently, by name or with `--scope-skill <skill>` / `--ticket-skill <skill>`. Confirmed defaults can be remembered across repositories; older saved choices need consent before becoming reusable planning delegations. Publication and planning-file writes remain subject to the current approval.

## Planning skill examples

| Collection | Scope | Planning / ticket content |
| --- | --- | --- |
| Matt Pocock | `to-spec` | `to-tickets` |
| [Superpowers 6.2.0](https://github.com/obra/superpowers/tree/v6.2.0/skills) | `brainstorming` | `writing-plans` |
| [Addy Osmani](https://github.com/addyosmani/agent-skills/tree/7cb7a20bb38b199728d456999c725a0488490ab6/skills) | `spec-driven-development` | `planning-and-task-breakdown` |

These are examples, not required installations. An implementation plan still needs a compatible skill to shape delivery tickets. Each phase's writes require current approval; the coordinator publishes the Map through repository tools without requiring a Git helper skill.

Planning files such as ADRs or `CONTEXT.md` changes need a retrievable version, destination and responsible ticket. Shared handoff information appears once in the Map and is linked from affected tickets; repository and executor workflows own the Git, CI and implementation procedures. Shared integration delivery is optional.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it-remake -g
```
