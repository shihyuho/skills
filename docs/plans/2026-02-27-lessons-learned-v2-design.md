# Lessons-Learned v2 Design

## Context

Optimize `skills/lessons-learned/` using `skill-design` + `skill-creator` principles to strengthen a self-improvement loop:

- Capture reusable lessons after work
- Recall relevant lessons before work
- Use Zettelkasten-style atomic cards
- Keep `workflow-orchestration` unchanged in this iteration

## Scope and Non-Goals

### In Scope

- Refactor `skills/lessons-learned/SKILL.md` trigger contract and workflow clarity
- Improve `references/card-template.md`
- Add linking heuristics guidance for high-value cards
- Define measurable quality benchmarks (trigger, recall, capture, linking)

### Out of Scope

- Modifying `skills/workflow-orchestration/SKILL.md`
- Introducing heavy infrastructure (database/event sourcing)
- Mandatory deep graph traversal on every recall

## Chosen Approach

Selected architecture: **contract-first modular refinement**.

Why:

- Keeps current markdown-native model and low operational cost
- Improves determinism and discoverability for agent triggering
- Adds selective wikilinks for higher-value knowledge graph effects
- Enables quality evaluation without overengineering

## Architecture

### Storage Model

```
docs/lessons/
├── _index.md
└── <lesson-id>.md
```

Cards remain atomic and tag-searchable, with lightweight relationship links.

### Card Metadata (frontmatter)

- `id`: semantic kebab-case ID
- `date`: ISO date
- `tags`: 3-6 lowercase tags
- `source`: `user-correction` / `bug-fix` / `retrospective`
- `related`: 0-3 wikilinks to related lesson cards (`[[card-id]]`)

## Workflow Design

### 1) Recall (before work)

1. Read `docs/lessons/_index.md`.
2. Extract task keywords.
3. Match tags and load 1-3 primary cards.
4. Expand by `related` links up to +2 cards (max total 5).
5. Convert loaded lessons into execution constraints.

### 2) Capture (after work)

1. Evaluate reusability and prevention value.
2. If criteria match, auto-capture card.
3. Generate `related` suggestions via linking heuristics.
4. Append/update `_index.md`.
5. Report captured lesson IDs to user.

### 3) Index Recovery Rule

- If `_index.md` missing and no lesson cards exist: treat as first run, skip recall.
- If `_index.md` missing but cards exist: regenerate `_index.md`, continue recall, and report recovery.

## High-Value Wikilink Rule

Create `related` links when a lesson meets **at least 2** of:

1. Cross-task reusable
2. High-cost mistake (multiple attempts or significant time loss)
3. Critical parameter/config/decision dependency
4. Naturally connects to >= 2 existing lesson cards

## Error Handling and Guardrails

- Missing `related` targets: ignore safely + warn, do not block task
- Enforce tag count (3-6)
- Deduplicate by semantic similarity (prefer update over duplicate card)
- Recall token guard: hard cap at 5 total cards

## Quality Evaluation Plan (skill-creator aligned)

### Structural Validation

- `npx --yes skills-ref validate ./skills/lessons-learned` passes

### Behavioral Benchmarks

- Trigger precision >= 0.85 on 12 scenario prompts
- Recall usefulness >= 8/10 sampled prompts (human-rated)
- Capture format compliance >= 9/10 sampled captures
- Related-link creation rate >= 0.8 when high-value rule is met
- Broken related-link rate = 0

## Planned File Changes

- `skills/lessons-learned/SKILL.md`
- `skills/lessons-learned/references/card-template.md`
- `skills/lessons-learned/references/linking-heuristics.md` (new)
- `skills/lessons-learned/README.md` (if absent, add human-facing adoption guide)

## Risks and Mitigations

- Risk: link noise from over-linking
  - Mitigation: 2-of-4 high-value gate + max 3 related links
- Risk: drift between index and cards
  - Mitigation: index recovery rule + validation checklist
- Risk: trigger ambiguity
  - Mitigation: explicit trigger phrases and negative trigger examples

## Acceptance Criteria

- Design constraints above are reflected in updated skill docs
- Validation and benchmark checklist is executable and documented
- Recall/capture/linking behavior is deterministic and bounded
