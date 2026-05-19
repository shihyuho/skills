# Kickoff

The handoff from plan review to coding. When you have reviewed a SPEC or PLAN and tell Claude to **start work**, the skill re-reads the approved document from disk, then implements it.

While it builds, it keeps a running implementation-notes file beside the spec — Markdown or HTML, your call at kickoff — recording only where the build diverges from or interprets the spec:

- **Design decisions** — choices made where the spec was ambiguous or silent
- **Deviations** — intentional departures from the spec, and why
- **Tradeoffs** — alternatives considered, and why the chosen one won
- **Open questions** — anything for you to confirm or revise

So you, the plan's author, see what changed without reading the whole diff. The file is maintained silently — open it whenever you want.

## Installation

```bash
npx skills add shihyuho/skills --skill kickoff -g
```
