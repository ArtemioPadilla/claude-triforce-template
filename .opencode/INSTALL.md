# Installing Agent Triforce in OpenCode

## Quick Install

```bash
cd ~/.opencode
git clone https://github.com/ArtemioPadilla/claude-triforce-template.git agent-triforce
```

## Configuration

Add to your OpenCode config:

```json
{
  "skills": {
    "agent-triforce": "~/.opencode/agent-triforce/.claude/skills"
  }
}
```

## Verify Installation

Start a new OpenCode session. The agent skills should be available automatically.

## Updating

```bash
cd ~/.opencode/agent-triforce && git pull
```
