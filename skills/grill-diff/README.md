# grill-diff

Review git changes using deep interactive grilling or fast multi-strategy self-review.

## Modes

- **Fast mode** — Agent applies multiple reviewer personas internally per file. Clean files are auto-advanced. Issues trigger interactive grilling.
- **Deep mode** — File-by-file interactive interrogation of every aspect (original grill-diff behavior).

## How It Works

1. **Select mode** — fast or deep. If not specified, you'll be asked.
2. **Determine diff scope** — staged changes > unstaged changes > specified branch > PR URL > default branch. Optionally specify files to narrow scope.
3. **Gather context** — asks if there is a related spec or plan file.
4. **Read all changed files** — builds the full picture before starting.
5. **Review file by file:**
   - **Fast:** Agent self-reviews with 3+ strategy personas, shows results. Clean → next. Issue → grill mode.
   - **Deep:** Asks one question at a time about every aspect of each change.
6. **Flag unnecessary changes** — challenges any change not required by the stated goal.

## Usage

```
/grill-diff
/grill-diff fast
/grill-diff deep
```

Against a specific target:

```
/grill-diff fast against develop
/grill-diff deep against develop
```

Narrow to specific files:

```
/grill-diff fast src/auth.ts src/api.ts
/grill-diff fast against develop src/auth.ts
```

Review a pull request:

```
/grill-diff fast https://github.com/org/repo/pull/123
```

## Installation

```bash
npx skills add shihyuho/skills --skill=grill-diff
```
