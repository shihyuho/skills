# skill-review evals

Each case in `evals.json` names a fixture that `fixtures.py` builds: a fresh repository, a host whose source skills return controlled findings, and stub commands that log every call. The fixtures are generated rather than stored as files so their `SKILL.md` targets are never discovered as real skills.

Build a workspace outside the checkout, or in an ignored `.*-workspace/` directory:

```bash
python3 skills/skill-review/evals/fixtures.py build <workspace> --runs 3 --configs with_skill old_skill
```

Run each case in a fresh context with the version of `skill-review` under test and a brief that says: read `host/HOST.md` first, since it replaces the Skill tool; treat `repo/` as the working directory; take `context.md`, when present, as the conversation so far; then answer the case's `prompt` as the user's message. Keep `expected_output` and `assertions` out of the executor's context. Save its final reply to `outputs/reply.md` and its tool calls to `outputs/transcript.md`.

`python3 skills/skill-review/evals/fixtures.py check <workspace>` then writes `state.<run>.json` beside each run directory, where an executor can't read it: the edits, staging, commits and stub calls that file-level assertions rest on. Grade the remaining assertions from the reply and the transcript.

Compare against a snapshot of the previous version with the same fixtures, model and reasoning effort, and carry the conclusions into the pull request.
