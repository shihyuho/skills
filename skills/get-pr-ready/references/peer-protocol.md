# Peer review protocol

Read this file when establishing or communicating with reviewer task B.

## Capability and identity handshake

B must be reachable through durable host task coordination, have access to the same project, use the same authenticated GitHub login as A, and be able to invoke the exact installed `engineering:pr-review` skill. A task created by this skill also requires a clean independent worktree. A user-supplied task may contain unrelated prior context or an existing workspace; use it exactly as supplied and make every request self-contained.

Do not infer task identity from a title. A host-specific stable task reference is required when B is supplied, and it must identify a task other than A; treat a self-reference as a non-retryable input error rather than deadlocking or reviewing inline. Confirm through host task metadata that the exact task can be addressed, then use the first complete review request below as the only content handshake; do not require a supplied task to be blank, dedicated, or on a particular worktree. A matching native review and validated result prove project access, GitHub identity, and skill execution. Failure to create, address, or send to B is a setup failure and is retried once; a returned review `error` follows the loop's separate review-error rule.

## Review request

Generate a unique `request_id` for every dispatch. Start or continue B with the following complete prompt, substituting only the bracketed values. Record the dispatched turn/run reference or delivery cursor when the host exposes one; never confuse an earlier terminal turn in a reused task with completion of this request.

```text
Review protocol: get-pr-ready/v1
Request ID: [request_id]
Pull request: [absolute PR URL]
Expected HEAD: [40-character head SHA]

Invoke the exact `engineering:pr-review` skill in specified-PR mode to perform and publish one fresh native GitHub review of this pull request at Expected HEAD. The user's get-pr-ready invocation explicitly authorizes a fresh review for this request even when this account already reviewed the same SHA; do not reuse or suppress a review because of deduplication. Follow that skill's complete static-review and head-pinning rules.

You are the reviewer only. Do not edit files, fix code, commit, push, merge, add or remove labels, or poll for later changes. Because the PR is self-authored under the same GitHub account, publish an ordinary native COMMENT review when GitHub will not accept APPROVE or REQUEST_CHANGES; express the quality result only in the return envelope below. Do not put the protocol version, Request ID, or envelope into the GitHub review body.

When the attempt ends, whether publication succeeds or fails, return only this YAML mapping to the requesting task, with all fields present and no surrounding prose:
request_id: [request_id]
requested_head: [expected SHA]
reviewed_head: [native review commit SHA]
conclusion: [must_fix|clean|low_confidence|error]
review_id: [native GitHub review ID or null]
review_url: [native GitHub review URL or null]
reviewer_login: [authenticated GitHub login or null]
error: [concise error or null]

Use must_fix when at least one verified finding must be resolved before the PR meets the engineering:pr-review quality bar. Use clean when there is no such finding. Use low_confidence when the review cannot make a defensible quality judgment despite completing available checks. Use error only when the review or native publication could not complete.
```

B must run a fresh review for every request, including repeated requests for the same SHA. The native GitHub review body stays idiomatic and contains no loop correlation markers.

## Waiting and retrieval

Wait on the B turn that received this request with bounded host waits, not a time deadline:

- `queued` or `running`: wait again.
- `completed`: read that turn's result and locate exactly one envelope with the current `request_id`.
- `failed`, or the dispatched turn `completed` without a matching envelope: treat as `error`.

Prior turns, messages, terminal states, and envelopes in a supplied task are context only. Never accept them for a new request or treat them as the dispatched turn's completion.

## Result verification

Before trusting a conclusion, retrieve the native review by `review_id` from the PR and verify all of the following:

- the envelope `request_id` equals the dispatched ID;
- `requested_head` equals the dispatched expected SHA;
- the native review exists on the requested PR and its URL and ID match the envelope;
- the native review was submitted and is not pending;
- the native review author's login equals both `reviewer_login` and A's authenticated login;
- the native review commit ID equals `reviewed_head` and the dispatched expected SHA;
- the PR's current head SHA still equals that SHA.

Null review identity on `must_fix`, `clean`, or `low_confidence` is invalid and becomes `error`. An `error` result may use null review fields. If the PR head moved, discard the result as stale and dispatch a new request for the current head; a stale result does not consume an error retry or fix round.
