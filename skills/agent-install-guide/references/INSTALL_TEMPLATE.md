# INSTALL_TEMPLATE.md

This is a **conceptual guide**, not a fill-in-the-blank template. Adapt the structure based on what the tool actually needs.

---

## Required Sections

### Meta-Instructions Block

Always include a block at the top telling the executing AI agent what to do:

```markdown
> **🤖 AI AGENTS:** [Brief instruction for the agent]
> 1. [First action - e.g., ask user preference, list options]
> 2. [Installation action]
> 3. [Verification action]
```

### Prerequisites (if any)

Only include if the tool has actual dependencies. Skip if none.

**Examples of what might go here:**
- Required runtimes (Node.js, Python, Go)
- Required tools (git, curl, make)
- OS requirements
- Account/API key requirements

### Installation

The core installation steps. Format varies widely:

| Type | Example |
|------|---------|
| Package manager | `npm install -g toolname` |
| Clone + build | `git clone ... && make install` |
| Download binary | `curl -L ... \| tar xz` |
| Symlink config | `ln -sf $(pwd)/config ~/.config/tool/` |

**Key principles:**
- Use idempotent commands (`mkdir -p`, `ln -sf`)
- Use absolute or conventional paths (`~/.config/`, `~/.local/bin/`)
- Avoid vague instructions ("put it somewhere safe")

### Verification

How to confirm installation succeeded. Always include this.

**Examples:**
- `which toolname` - binary in PATH
- `toolname --version` - correct version
- `ls ~/.config/tool/` - config exists
- `toolname health-check` - tool-specific validation

### Configuration (if needed)

Only if the tool requires post-install configuration. Skip if not needed.

### Troubleshooting (if helpful)

Common issues and fixes. Optional but recommended for complex installs.

---

## Optional Sections

Include only when relevant to the specific tool:

- **Shell Configuration** - Only if PATH modification needed
- **Uninstallation** - How to cleanly remove
- **Upgrade** - How to update to newer versions
- **Platform-specific notes** - macOS vs Linux differences

---

## Anti-patterns to Avoid

| ❌ Don't | ✅ Do |
|----------|-------|
| "Download to a safe location" | "Download to `~/.local/share/toolname`" |
| "Add to your PATH" | Provide the exact `export PATH=...` command |
| "Edit your config file" | Provide heredoc with full content |
| `mkdir config` | `mkdir -p ~/.config/toolname` |
| `ln -s ./file target` | `ln -sf $(pwd)/file target` |
