# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[lessons-learned](skills/lessons-learned/)** - Stop your AI agent from making the same mistake twice.
- **[time-to-skill](skills/time-to-skill/)** - Turn repetitive workflows into reusable skills automatically.
- **[agent-install-guide](skills/agent-install-guide/)** - Write installation guides that AI agents can reliably execute.
- **[fanfuaji](skills/fanfuaji/)** - Chinese terminology conversion (Traditional ↔ Simplified) using [zhconvert.org](https://zhconvert.org/) API.

## Installation

### 1. Install Skills (Required)

First, install the skills collection:

```bash
npx skills add shihyuho/skills --skill='*'
```

### 2. Install OpenCode Plugins (Optional)

For [OpenCode](https://opencode.ai) users, you can **optionally** install plugins to make these skills **proactive**. Instead of waiting for you to invoke a skill, the AI will intelligent suggest using it when relevant (e.g., after an error).

**Available Plugins:**
- **lessons-learned**: Automatically suggests documenting lessons after errors, repeated retries, or complex tasks.
- **time-to-skill**: Monitors repeated task patterns and suggests converting them into reusable skills.

👉 **[Plugin Installation Guide](.opencode/INSTALL.md)**

> [!TIP]
> You can ask your AI to read the Plugin Installation Guide and perform the setup for you!
> ```
> Fetch and follow instructions from https://raw.githubusercontent.com/shihyuho/skills/refs/heads/main/.opencode/INSTALL.md
> ```

## Usage

Skills are automatically available once installed. AI will use them when relevant tasks are detected. If you installed the OpenCode plugins, the AI will also proactively remind you to use them.

## License

MIT
