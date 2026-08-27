# scope-it-remake

A lightweight alternative to `scope-it`: discuss scope, tickets and delivery continuously, then publish the agreed Delivery Map after one exact-write approval.

Use compatible planning skills or completed artifacts. Source choices are shared across repositories; override them with `--scope-source <name>` or `--ticket-source <name>`. A missing or incompatible source prompts a choice instead of generating its content.

Scope and Map share one planning post. A single ticket is a separate comment on that home; multiple tickets are child items. The final Map contains delivery decisions and handoff links, not discussion progress. Approved planning files retain their Carry/Carrier and optional integration-lane safeguards.

## Installation

```bash
npx skills add shihyuho/skills --skill scope-it-remake -g
```
