# Agent Install Guide

This skill helps AI agents write installation guides that other AI agents can reliably execute.

## The Problem

Human-written guides often contain ambiguity that humans can resolve but AI agents cannot:

| Human Guide Says | AI Agent Thinks |
|------------------|-----------------|
| "Clone this repo" | Where? Current directory? Home? |
| "Run the setup script" | Which file? `setup.sh`? `install.sh`? |
| "Add to your PATH" | Which shell? What command exactly? |

## The Solution

Agent-Ready guides are **deterministic**, **idempotent**, and **verifiable**:

- **Deterministic**: Every instruction has exactly one interpretation
- **Idempotent**: Commands are safe to run multiple times
- **Verifiable**: Each step has a way to confirm success

## Example Transformation

**Before** (vague):
```
1. Clone this repo
2. Run the setup script  
3. Add the binary to your PATH
```

**After** (agent-ready):
```
> 🤖 AI AGENTS: Follow steps below, verify in Section 3.

1. Clone: git clone https://github.com/user/repo.git ~/.local/share/mytool
2. Setup: ~/.local/share/mytool/scripts/setup.sh
3. PATH: echo 'export PATH="$HOME/.local/share/mytool/bin:$PATH"' >> ~/.zshrc
4. Verify: which mytool && mytool --version
```

## Core Principles

This skill teaches AI agents to internalize these concepts:

1. **No ambiguous paths** - Use `~/.config/`, `~/.local/`, `$(pwd)`, not "somewhere safe"
2. **Idempotent commands** - `mkdir -p`, `ln -sf`, `rm -f` instead of fragile alternatives
3. **Verification steps** - Every significant action should be confirmable
4. **Ask when choices exist** - Don't assume; prompt the user

## How It Works

1. AI is asked to create an install guide
2. AI loads this skill for principles
3. AI asks user for filename preference (default: `INSTALL.md`)
4. AI generates guide following Agent-Ready principles
5. AI optionally offers to add a reference to the project README

## Limitations

- **Unix-focused**: macOS/Linux patterns. Windows needs different handling.
- **CLI-only**: No GUI installation support.
- **User-space**: Designed for `~/` installations, not system-wide.

## Related Files

- [SKILL.md](./SKILL.md) - Instructions for AI agents
- [references/install-template.md](./references/install-template.md) - Structural concepts
- [references/readme-integration-template.md](./references/readme-integration-template.md) - Adding AI-friendly notices to README

## License

MIT
