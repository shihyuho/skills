---
description: "Capture current work into second-brain timeline immediately."
---

Invoke the `harvest:harvest` skill and follow it exactly as presented.

Force a key-update snapshot for current work now using the same contract as any other trigger entrypoint:

- append a timeline event with `when`, `change`, `why`, `source_ref`
- use same-day append behavior when timeline file already exists
- compute `sot_fingerprint` from `task_plan.md`, `findings.md`, `progress.md`
- no-op if the same `sot_fingerprint` already exists in timeline metadata
- include `sot_fingerprint` in the new snapshot metadata
- avoid formal decision/knowledge publication unless milestone conditions are met
