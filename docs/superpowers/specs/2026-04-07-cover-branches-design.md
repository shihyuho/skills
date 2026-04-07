# cover-branches — Design Spec

## Objective

A skill that finds branch coverage gaps in changed code and fixes them. Two layers of gap analysis:

1. **Src ↔ Test** — Analyze logic branches in source code (conditional branches, error handling, early returns, default/fallback values) and verify each branch has a corresponding test.
2. **Spec ↔ Test** — (When user provides a spec file) Extract all requirement scenarios from the spec and verify each scenario has a corresponding test.

## Workflow

Modeled after the built-in `simplify` skill pattern: find issues, fix issues.

### Phase 1: Identify Changes

- Run `git diff` (or `git diff HEAD` if there are staged changes) to identify changed src and test files.
- If no git changes, fall back to files the user mentioned or edited earlier in the conversation.

### Phase 2: Launch Gap Analysis Agents in Parallel

Use the Agent tool to launch agents concurrently. Pass each agent the full diff for complete context.

#### Agent 1: Src ↔ Test Branch Coverage (always launched)

For each changed source file:

1. Read the source file and identify all logic branches — conditional branches, error handling, early returns, default/fallback values, and any other branching constructs relevant to the file's language.
2. Find the corresponding test file(s). Infer the mapping from project conventions (naming, directory structure, imports).
3. For each branch, determine if a test exercises that path.
4. Report gaps in natural language: which branches lack test coverage and what test scenarios are missing.
5. If no corresponding test file exists, report that as a gap — Phase 3 will create one following existing project conventions.

#### Agent 2: Spec ↔ Test Scenario Coverage (launched only when user provides a spec file)

1. Read the spec file.
2. Extract all testable scenarios: functional requirements, boundary conditions, error handling, edge cases, acceptance criteria, user stories.
3. Find the corresponding test file(s).
4. For each scenario, determine coverage status: **covered** or **gap**.
5. Report gaps in natural language: which scenarios lack test coverage and what is missing.

### Phase 3: Fix Gaps

- Wait for all agents to complete.
- Merge findings from both agents, avoiding obviously redundant test cases.
- Directly write missing test cases to fill the gaps.
- When a spec contains contradictions, or when the correct test behavior cannot be inferred from the source code, ask the user before writing the test.
- After writing all test cases, run the tests to verify they pass. Infer the test command from project configuration (`package.json`, `Makefile`, `pom.xml`, etc.); if unable to infer, ask the user.
- When done, briefly summarize what was added (or confirm coverage is already complete).
- If no spec file was provided, remind the user they can re-run with a spec file path for scenario coverage analysis.

## Input

- The user may provide a path to a spec file in the conversation. When provided, Agent 2 is launched in addition to Agent 1.

## Trigger Conditions

- After implementing a feature or fixing a bug, to verify test completeness.
- When the user wants to audit whether tests match the spec.
- When reviewing code and suspecting untested branches.

## Non-Goals

- Does not run coverage tools (istanbul, c8, etc.). Analysis is purely semantic.
- Does not generate specs. If no spec exists, only Src ↔ Test analysis runs.
- Does not refactor existing tests. Only adds missing test cases.

## Success Criteria

- Every logic branch in changed source files has a corresponding test scenario.
- When a spec is provided, every spec scenario has at least one corresponding test.
- No false-positive gaps reported (ambiguous cases are escalated to the user).
- New test cases follow existing test file conventions (framework, naming, structure).
