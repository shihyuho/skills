# tradeoffs evaluation cases

These cases define behavioral checks; their presence is not an executed benchmark.

Run each case in a fresh disposable workspace. Give the evaluated agent the prompt and staged input files; keep expected outputs and grader notes out of its context. For case 2, copy `files/validation-contract.md` to the workspace root. For case 3, copy `files/decisions/` to the workspace's `decisions/` directory and compare both original files byte-for-byte after the run. For case 4, copy `files/event-handler/` to the workspace's `event-handler/` directory. Keep the repository fixtures unchanged.

Compare the recommendation, supporting evidence, tool actions, and final filesystem state with `expected_output`. Grade the evidence and reasoning, not a particular research tool, workflow, or number of sources.

For case 5, provide access to external primary sources. Grader references: [JEP 444](https://openjdk.org/jeps/444) and the [JDK 21 virtual-thread guide](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html) describe pinning while blocking inside `synchronized`; the [JDK 24 migration guide](https://docs.oracle.com/en/java/javase/24/migrate/significant-changes-jdk-24.html) identifies JEP 491 as the change that removes it. These are reference options, not a required reading list. Record source URLs and access failures; if applicable primary evidence cannot be reached, mark external verification unverified and assess how the response handles that uncertainty.

For an Astra comparison, use the same cases, tools, approvals, and fresh workspace state for medium and high, recording the actual model, host version, effort, and skill commit. Keep old-skill and candidate runs separate; report unrun cases explicitly.
