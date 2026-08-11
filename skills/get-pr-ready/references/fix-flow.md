# Fix flow

Read this file only after accepting a fresh `must_fix` review.

## Freeze the workset

The workset is exactly the accepted native review identified by `review_id`: its review body plus inline comments belonging to that review. Do not absorb other reviews, issue comments, later human feedback, or this skill's own replies into the round.

Split compound feedback into independently decidable findings. For every finding, pin the relevant source and repository guidance at the reviewed SHA and classify it as:

- `fix`: the claim is supported and requires a code, test, or documentation change;
- `reject`: evidence shows the claim is incorrect or the proposed change would violate the intended behavior;
- `non-actionable`: no concrete change is requested or available evidence cannot identify a safe scoped change.

Do not equate reviewer wording with authority. Record enough evidence to explain every classification.

## Apply and verify fixes

Before each edit, commit, push, reply, or resolution checkpoint, re-read PR state and head. Merged maps to `done` and closed-unmerged to `cancelled`; do not start another mutation after either transition. Before editing, also require the reviewed head. If it moved, abandon this workset and request a fresh review.

For each `fix`, make the smallest complete change in the verified PR-head worktree while preserving unrelated and untracked work. Run all repository-mandated validation plus at least one focused check that directly exercises each fix. If any required validation fails, do not commit or push; preserve the worktree and finish as `blocked` with the failing evidence.

If there are no file changes after classification, do not create an empty commit. Reply with the evidence for each rejected or non-actionable finding, resolve only conclusively handled inline threads when GitHub permits it, and return to the fresh-review step on the same head.

## Commit and publish

When files changed:

1. Reconfirm the PR is open at the reviewed head, the current branch and intended diff, the verified head remote/ref, and the absence of unrelated staged paths.
2. Create cohesive commits containing only this round's fixes. Include these trailers on every fix commit:

   ```text
   Loop-Review: <review-id>
   Loop-Request: <request-id>
   ```

3. Push normally and fast-forward only to the verified PR head remote/ref. Never force-push.
4. Retrieve the PR again and require its head SHA to equal the pushed commit before claiming or replying that a fix is present.

If the head changes unexpectedly after editing begins, preserve the local fix but do not commit, push, reply, or resolve from this stale workset. Return to a fresh review of the current PR head. Revalidate and reapply only changes supported by a later accepted review; never reset, force-push, or silently carry a stale fix onto the new head.

## Close the accepted review

After every claimed fix exists on the current PR head:

- reply to each fixed inline finding with the change, focused verification, and commit SHA, then resolve its thread;
- reply to rejected or non-actionable findings with concise evidence and resolve the thread only when the disposition is conclusive and resolution is available;
- answer an actionable review-body finding in the narrowest appropriate GitHub location;
- do not add a redundant PR summary comment when the individual replies already close the workset.

The round is complete only when every finding from the accepted review has a posted disposition or an appropriate thread resolution, and every claimed fix is present on current PR HEAD. Then return to the fresh-review step.
