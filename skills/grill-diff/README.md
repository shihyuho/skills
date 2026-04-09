# grill-diff

Review git changes using deep interactive grilling or fast specialist-filtered review.

## Modes

- **Deep mode** — File-by-file interactive interrogation of every aspect. Every finding is discussed with the user.
- **Fast mode** — Same review, but findings are filtered through internal specialists first. Only high-value findings reach the user.

## How It Works

1. **Select mode** — fast or deep. If not specified, you'll be asked.
2. **Determine diff scope** — file scope and diff baseline are independent and combine freely.
3. **Gather context** — asks if there is a related spec or plan file.
4. **Read all changed files** — builds the full picture before starting.
5. **Review file by file** — interrogate every aspect of each change. When a finding is spotted:
   - **Deep:** discuss with the user, one question at a time.
   - **Fast:** consult 3+ specialists, classify by confidence, only present confirmed/uncertain findings.

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
