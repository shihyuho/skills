# README Integration Template

## Purpose

Add a section to your project's README that tells users they can use an AI agent to perform the installation automatically.

## Core Elements

1. **Signal that AI can help** - Let users know this is "agent-friendly"
2. **Provide the URL** - Direct link to the install guide source
3. **Safe execution model** - Fetch, review, and explicit approval before execution

## Examples

### Minimal

```markdown
## Installation

> 🤖 Ask your AI agent: "Fetch [URL], review and summarize steps, then ask for my approval before execution."
```

### With Context

```markdown
## Installation

You can install manually (see below) or ask an AI agent to do it for you:

> **AI-Assisted Setup**: Tell your AI agent to fetch and review:
> `https://raw.githubusercontent.com/user/repo/main/INSTALL.md`
>
> Required flow: fetch -> review and validate -> explicit approval before execution.
```

### Prominent (for AI-first tools)

```markdown
## Installation

> 🤖 **AI Agent Friendly**
>
> This project is designed for AI-assisted setup. Ask your AI to use this workflow:
> ```
> 1) Fetch instructions from:
> https://raw.githubusercontent.com/user/repo/main/INSTALL.md
> 2) Review and summarize risks/changes
> 3) Ask for explicit approval before executing commands
> ```

> Agents must not execute remote content without human approval.

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

## Safety Requirement

- Include wording that agents **must not execute** remote instructions directly.
- Include wording that agents must stop for explicit approval before command execution.
