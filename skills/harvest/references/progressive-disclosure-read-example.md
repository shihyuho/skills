# Progressive Disclosure Read Examples

## Decision lookup
- intent: find prior decision on rollout strategy
- read order: `docs/notes/index.md` -> `docs/notes/decisions.md` -> target decision note
- stop condition: stop once the decision note is read, or after two reads with no new leads

## Timeline investigation
- intent: trace project timeline for the cache rollout
- read order: `docs/notes/index.md` -> `docs/notes/projects.md` -> relevant project timeline file(s)
- stop condition: stop once the timeline file is read, or after two reads with no new leads

## Knowledge pattern retrieval
- intent: retrieve reusable pattern for throttling API calls
- read order: `docs/notes/index.md` -> `docs/notes/knowledge.md` -> matching knowledge note
- stop condition: stop once the knowledge note is read, or after two reads with no new leads
