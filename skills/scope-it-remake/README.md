# scope-it-remake

Coordinate interchangeable scope and ticket workflows into one Delivery Map with its own continuation protocol.

The selected skills own their content, reviews and publication. Scope is confirmed and published first, then passed to the ticket skill; the coordinator finally confirms and publishes the Map with any needed handoff links. These are separate approvals, so Scope and tickets are visible before the Map.

Publication keeps the agreed placement: an existing parent hosts Scope without replacing the report, one Ticket uses that parent as its identity, and multiple Tickets become children. The Map is one canonical parent comment; Ticket artifacts neither copy nor link back to it.

The Map is a low-resolution delivery index, not a Scope or progress tracker. It embeds the compact selection protocol, so a later session needs only the parent—not this skill or the planning chat—to choose one live Ticket before loading its details. The executor owns claim and implementation.

Choose scope and ticket skills independently, by name or with `--scope-skill <skill>` / `--ticket-skill <skill>`. Confirmed defaults can be remembered across repositories; older saved choices need consent before becoming reusable planning delegations. Publication and planning-file writes remain subject to the current approval.

## Planning skill examples

| Collection | Scope | Planning / ticket content |
| --- | --- | --- |
| Matt Pocock | `to-spec` | `to-tickets` |
| [Superpowers 6.2.0](https://github.com/obra/superpowers/tree/v6.2.0/skills) | `brainstorming` | `writing-plans` |
| [Addy Osmani](https://github.com/addyosmani/agent-skills/tree/7cb7a20bb38b199728d456999c725a0488490ab6/skills) | `spec-driven-development` | `planning-and-task-breakdown` |

These are examples, not required installations. An implementation plan still needs a compatible skill to shape delivery tickets. Each phase's writes require current approval; the coordinator publishes the Map through repository tools without requiring a Git helper skill.

Planning files such as ADRs or `CONTEXT.md` changes need a retrievable version, destination and responsible Ticket. Shared delivery information appears once in the Map; repository and executor workflows own claim, Git, CI and implementation. Shared integration delivery is optional.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it-remake -g
```
