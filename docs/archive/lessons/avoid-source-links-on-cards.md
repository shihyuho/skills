---
id: avoid-source-links-on-cards
date: 2026-03-13
scope: project
tags: [metadata, maintenance, links, cards, maps, churn]
source: retrospective
confidence: 0.3
related: []
---

# Avoid keeping source links on every card

## Context
A task was completed where source links were maintained on every card to track origins.

## Mistake
Keeping source links on every card created maintenance overhead — when underlying maps or sources changed, all affected cards needed updates, causing significant churn.

## Lesson
- Do not automatically add persistent source links to every card
- Only add source links when they provide clear long-term value without maintenance cost
- Prefer ephemeral references or on-demand lookup over persistent links that require updates

## When to Apply
- When designing card metadata schemas
- When considering adding tracking links to any reusable content
- When source data is subject to frequent changes or migrations