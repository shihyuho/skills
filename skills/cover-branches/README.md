# cover-branches

Find branch coverage gaps in changed code and write missing tests to fill them.

## How It Works

1. **Identify changes** — reads `git diff` to find changed source and test files.
2. **Analyze gaps** — launches parallel agents:
   - **Source ↔ Test**: checks every logic branch (conditionals, error handling, early returns, fallbacks) has a corresponding test.
   - **Spec ↔ Test** (optional): checks every requirement scenario in a user-provided spec file has a corresponding test.
3. **Fix gaps** — writes missing test cases, then runs tests to verify.

## Usage

```
/cover-branches
```

With a spec file for scenario coverage:

```
/cover-branches path/to/spec.md
```

## Installation

```bash
npx skills add shihyuho/skills --skill=cover-branches
```
