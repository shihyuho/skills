# grill-diff

Review git changes file by file, interrogating every aspect of each diff until reaching shared understanding.

## How It Works

1. **Determine diff scope** — staged changes > unstaged changes > branch diff against default branch. User can override (e.g. a PR URL).
2. **Gather context** — asks if there is a related spec or plan file to understand the goal.
3. **Read all changed files** — builds the full picture before starting.
4. **Grill file by file** — asks one question at a time, exploring the codebase to answer its own questions when possible.
5. **Flag unnecessary changes** — challenges any change not required by the stated goal. Probe: "What breaks if we revert this?"

## Usage

```
/grill-diff
```

Against a specific target:

```
/grill-diff against develop
/grill-diff https://github.com/org/repo/pull/123
```

## Installation

```bash
npx skills add shihyuho/skills --skill=grill-diff
```
