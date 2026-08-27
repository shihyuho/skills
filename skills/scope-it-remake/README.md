# scope-it-remake

Experiment with a Wayfinder-inspired Delivery Map that advances one planning frontier at a time and accepts interchangeable scope and ticket sources.

This user-invoked prototype lives beside `scope-it`; it does not replace or migrate the existing workflow. `to-spec`, `to-tickets`, other compatible skills, and completed artifacts can supply planning content through capability-based contracts. It remembers approved source choices as a reusable global default with sparse repository overrides, asks when no compatible producer can be resolved, accepts `--scope-source` or `--ticket-source` to replace stored choices explicitly, keeps one top-level Delivery Map home, and keeps execution plans separate from tracker tickets.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it-remake -g
```
