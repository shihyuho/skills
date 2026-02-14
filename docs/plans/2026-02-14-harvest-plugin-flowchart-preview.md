# Harvest Plugin Flowchart Preview (Compact)

This version keeps only the most important decision points.

```mermaid
flowchart TD
  A[Manual run once] --> B[Initialize docs/notes]
  B --> C[SOT changed\ntask_plan/findings/progress]
  C --> D[Plugin auto trigger\ndebounce and idle]
  D --> E[Prompt: invoke harvest:harvest]
  E --> F[Skill executes capture]
  F --> G{docs/notes ready?}
  G -->|No| H[Bootstrap minimal notes]
  G -->|Yes| I[Check sot_fingerprint dedupe]
  H --> I
  I --> J{Already captured?}
  J -->|Yes| K[No-op]
  J -->|No| L[Append same-day snapshot]
  K --> M[Done]
  L --> M
```
