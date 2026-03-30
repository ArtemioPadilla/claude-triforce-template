# Installing Agent Triforce in Codex

## Quick Install

```bash
cd ~/.codex
git clone https://github.com/ArtemioPadilla/claude-triforce-template.git agent-triforce
```

Then symlink skills into your Codex skills directory:

```bash
mkdir -p ~/.agents/skills
ln -sf ~/.codex/agent-triforce/.claude/skills/* ~/.agents/skills/
```

## Verify Installation

Start a new Codex session and ask:

> "What agents are available?"

You should see references to Prometeo (PM), Forja (Dev), and Centinela (QA).

## Updating

```bash
cd ~/.codex/agent-triforce && git pull
```
