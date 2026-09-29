# Revisit response evals

Run each prompt with its fixture in an isolated context. The fixture supplies frozen tracker and investigation observations, so replay the discussion without contacting services, executing diagnostic tests, or changing a repository. Read the selected version of `revisit` and its available dependencies. Record user-visible progress messages and the final response separately.

Keep `expected_output` and `assertions` out of the executor's context. Grade the final response on its own wherever an assertion says "final"; a good explanation only in progress messages does not satisfy those assertions. For follow-ups, supply the prior conversation from the fixture.

Cases 1–4 use abridged evidence from the four user-supplied Fairybell chats reviewed on 2026-09-29. Cases 5–8 are synthetic transfer and continuity cases. These fixtures are response tests, not current repository verification. Examples that add concrete values beyond the evidence should be identifiable as illustrations.

Compare the changed skill with a snapshot of the previous version using the same prompt, fixture, model, and reasoning effort. Report actual execution coverage and inspect nondiscriminating assertions; a passing frozen replay does not establish that a reader will always understand on the first attempt.
