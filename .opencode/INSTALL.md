# Harvest OpenCode Plugin Install Guide

> AI AGENTS:
> - Execute commands exactly as written.
> - Use absolute paths after setting `REPO_DIR`.
> - Run every verification command and stop on failure.

Plugin file:

- `.opencode/plugins/harvest.js`

Plugin name:

- `harvest`

## 0) Set Source Path

```bash
REPO_DIR="$(pwd)"
test -f "${REPO_DIR}/.opencode/plugins/harvest.js" && echo "OK plugin source"
```

## 1) Install OpenCode Plugin

### 1.1 Register plugin named `harvest`

```bash
mkdir -p ~/.config/opencode/plugins
rm -f ~/.config/opencode/plugins/harvest.js
ln -s "${REPO_DIR}/.opencode/plugins/harvest.js" ~/.config/opencode/plugins/harvest.js
```

### 1.2 Verify registration

```bash
ls -l ~/.config/opencode/plugins/harvest.js
```

### 1.3 Restart OpenCode

Restart OpenCode so the plugin is loaded at startup.

## 2) Runtime Verification

Edit any SOT file (`task_plan.md`, `findings.md`, `progress.md`) and verify:

```bash
test ! -d .harvest/auto-capture && echo "OK: no runtime state dir"
```

Expected behavior:

- SOT edit schedules capture
- Session idle triggers convergence capture
- Duplicate capture is prevented by fingerprint and cooldown
- No `.harvest/auto-capture/*` runtime dedupe files are created

## 3) Rollback

```bash
rm -f ~/.config/opencode/plugins/harvest.js
```
