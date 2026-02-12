# README Integration Template

## Purpose

Add a section to your project's README that tells users they can use an AI agent to perform the installation automatically.

## Core Elements

1. **Signal that AI can help** - Let users know this is "agent-friendly"
2. **Provide the URL** - Direct link to the raw install guide
3. **Simple instruction** - What to tell the AI

## Examples

### Minimal

```markdown
## Installation

> 🤖 Ask your AI agent: "Fetch and follow instructions from [URL]"
```

### With Context

```markdown
## Installation

You can install manually (see below) or ask an AI agent to do it for you:

> **AI-Assisted Setup**: Tell your AI agent to fetch and follow:
> `https://raw.githubusercontent.com/user/repo/main/INSTALL.md`
```

### Prominent (for AI-first tools)

```markdown
## Installation

> 🤖 **AI Agent Friendly**
>
> This project is designed for AI-assisted setup. Ask your AI:
> ```
> Fetch and follow instructions from:
> https://raw.githubusercontent.com/user/repo/main/INSTALL.md
> ```

<details>
<summary>Manual Installation</summary>

[Manual steps here...]

</details>
```

## URL Format

```
https://raw.githubusercontent.com/[USER]/[REPO]/[BRANCH]/[PATH]
```

- `[USER]` - GitHub username or org
- `[REPO]` - Repository name
- `[BRANCH]` - Usually `main` or `master`
- `[PATH]` - Path to install guide (e.g., `INSTALL.md`, `docs/setup.md`)
