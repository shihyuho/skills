# Skills Collection

Shihyu's curated collection of agent skills.

## Available Skills

- **[lessons-learned](skills/lessons-learned/)** - Stop your AI agent from making the same mistake twice.

## OpenCode Plugins

For [OpenCode](https://opencode.ai) users, this repository provides plugins that proactively inject skill reminders into the AI's context. This ensures the AI knows **when** to use a skill without you having to ask.

### Available Plugins

- **lessons-learned**: Automatically reminds the AI to suggest documenting lessons after errors, repeated retries, or complex tasks.

👉 **[Installation Guide](.opencode/INSTALL.md)**

> [!TIP]
> You can ask your AI to read the Installation Guide and perform the setup for you!
> ```
> Fetch and follow instructions from https://raw.githubusercontent.com/shihyuho/skills/refs/heads/main/.opencode/INSTALL.md
> ```

## Installation

```bash
npx skills add shihyuho/skills --skill='*'
```

or to install all of them globally:

```bash
npx skills add shihyuho/skills --skill='*' -g
```

Learn more about the CLI usage at [skills](https://github.com/vercel-labs/skills).

## Usage

Skills are automatically available once installed. AI will use them when relevant tasks are detected.

## License

MIT
