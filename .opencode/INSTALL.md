# Installing OpenCode Plugins

This repository contains plugins for [OpenCode.ai](https://opencode.ai) that proactively inject skill reminders into your AI's context.

> **🤖 AI AGENTS:** If you are reading this to perform an installation:
> 1.  **List available plugins** found in `.opencode/plugins/`.
> 2.  **Ask the user** which plugins they want to install (allow multiple selection).
> 3.  **Perform installation** for the selected plugins only.

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- This repository cloned locally (recommended location: `~/.config/opencode/shihyuho-skills`)

## Installation Steps

### 1. Clone the Repository

If you haven't already, clone this repository to a stable location:

```bash
git clone https://github.com/shihyuho/skills.git ~/.config/opencode/shihyuho-skills
```

### 2. Register Plugins

Link the plugins you want to use to your OpenCode configuration.

> **Example**: Installing `lessons-learned`

```bash
# Create plugins directory if it doesn't exist
mkdir -p ~/.config/opencode/plugins

# Link the plugin file
ln -sf ~/.config/opencode/shihyuho-skills/.opencode/plugins/lessons-learned.js ~/.config/opencode/plugins/lessons-learned.js
```

### 3. Restart OpenCode

Restart your OpenCode application. The installed plugins will automatically active in new sessions.

## Updating

Simply pull the latest changes:

```bash
cd ~/.config/opencode/shihyuho-skills
git pull
```

Since you used symlinks, OpenCode will pick up the updates automatically after a restart.
