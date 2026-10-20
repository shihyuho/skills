# Writing a skill README

Every skill at `skills/<skill>/` carries a human-facing `README.md` beside its `SKILL.md`. Its reader is an engineer using AI coding agents, deciding whether this skill fits the task in front of them and how to start it; they know coding agents and know nothing of this skill's implementation.

The agent never fires a user-invoke skill on its own, so the engineer is the index that has to remember it exists and when to reach for it. That memory is cognitive load, and the README exists to carry it: one page that lets one reader hold one skill in their head, what it does, when to reach for it, and what a good run looks like. The page is not the skill and not a copy of `SKILL.md`: agent execution instructions stay in `SKILL.md` and its references, development history stays in issues and pull requests, and the page explains the why rather than the process, because a human choosing a tool does not need the runbook.

When the `explain` skill is available, it sets how each section is written; `AGENTS.md` sets the language; principles 6 and 9 in [skill-design.md](skill-design.md) (no tombstones, no consumer pointers) apply to the README as they apply to the skill.

## When to act

- A new skill ships with its README in the same change.
- A change that alters what the skill does, how it starts, or what it needs re-syncs the README in the same change. When it retires, renames or moves something readers relied on, `Common questions` answers where it went.
- An invocation change updates the how-it-starts sentence in `When to use`, alongside the root `README.md` grouping that `docs/invocation-classification.md` owns.

## The page

Fixed headings in the order below. A section with nothing to say is left out; the opening and `It's working if` are always present. The opening and `When to use` orient the reader; `It's working if` and `Common questions` are where the page stops summarising the skill and answers the reader's own situation, which is why the first is never left out and the second is never padded.

Each section in the template holds the instruction for writing it.

<page-template>

# <skill-name>

The text between the H1 and the first H2, with no heading of its own, and three things only. The first sentence is the job, what the skill does in one sentence; the root `README.md` lists the same sentence. The second is the defining constraint, the one fact that makes the skill behave differently from the obvious default, usually as "Unlike <default>, it …" so the default is named and the reader sees what the skill refuses to do. Then at most one diagram of what it does, with one legend line beneath it when its labels need naming. Neighbours, how it starts, mechanism and longer term definitions have sections of their own below.

## When to use

Three beats. The situations, as a list when there are several. How it starts, in one sentence: "This skill must be invoked explicitly." for a user-invoke skill; for a model-invoke one, the context the agent fires in, "The agent uses it on its own when <context>; you can also invoke it directly." The neighbour to use instead when this is not it, with a because-clause; an alternative for the reader, never a list of who loads this skill.

## Before you start

Only when the reader needs something in place, or needs to know where the skill will write: tools and access (a logged-in `gh`, write access to the branch), prior setup (a tracker configured, another plugin installed), or a workspace the skill keeps across runs (config or cache, see `docs/skill-user-data.md`), named so the reader knows where it lands. A stateless skill that runs anywhere has no prerequisites, so the section is left out.

## Getting started

The first invocation, copyable. Options worth knowing go under `### Options`, as a table when there are several; a prompt meant to run on a schedule gets its own H3.

## <free name>

The one mechanism worth explaining, in the skill's own vocabulary: the loop it runs, the artifact it produces, the fork it makes. A single H2, with H3 subsections when it has parts, and only what changes a decision the reader makes. The leading word lives here, or in the opening when the page has no free section, used as the skill uses it; it pays off twice, since the reader learns what the skill is and learns the word they will later think with to reach for it.

## It's working if

A few bullets naming what the reader sees when the skill is doing its job, each checkable without opening `SKILL.md`: a signal in their own work or in the trace in front of them. "The document gets shorter as it gets better" qualifies; "the output matches the template byte for byte" is a compliance check on the skill's internals wearing this section's name.

## Common questions

Questions someone asked, each in bold with the answer beneath it, no sub-headings. Hunt before writing: `gh issue list --repo shihyuho/skills --search "<skill> in:title" --state all`, the pull requests `git log -- skills/<skill>` leads to (with the earlier path added when the skill was renamed, since the history before the rename stays there), and the "where did it go" a retirement, rename or move produces. Size the section to what the hunt finds; an invented question teaches nothing. Order by how often each comes up, say the unflattering thing where it is true, and quote the question rather than the asker. Leave the section out when the hunt finds nothing.

## Limitations

What it does not do and where it stops.

</page-template>

## Conventions

- Branches go in a table or a list, never in a paragraph. Where the page presents a choice (two artifacts, four situations, five options), the reader is scanning for the one row that matches their situation.
- Keep the page low-load: it exists to carry the reader's cognitive load, so furniture (a spare heading, a restated link, a second diagram, a term defined twice) works against it; the legend line under the one diagram is part of the diagram, not furniture. The free section is where a page grows, so it stays one H2.
- Speak the skill's language: the leading words the `SKILL.md` uses, so page and skill share one vocabulary.

## Done when

- The README sits beside `SKILL.md`, under the headings above in that order, with no heading the skill has nothing to say under.
- The opening holds the job sentence, the defining constraint and at most one diagram with its legend, nothing else; the root `README.md` lists the same job sentence.
- `When to use` states how it starts, matching the skill's invocation marker, and, where a neighbour is confusable with it, names the alternative rather than the consumers.
- `Before you start` is present where tooling, setup or a persisted workspace exists, and absent where none does.
- The free section, when there is one, is one H2, and the leading word surfaces there or in the opening.
- Every `It's working if` bullet is checkable without opening `SKILL.md`.
- The hunt for questions ran, and `Common questions` is sized to what it found.
- The page is in English, and every in-page link still resolves after a heading change.
- No `SKILL.md` step is reproduced. Retired behavior is answered in `Common questions` with where it went, not denied in passing; a sentence that blocks a live default stays where it blocks it, as principle 6 in [skill-design.md](skill-design.md) draws the line.
