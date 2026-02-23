# 🔱 agent-triforce-template

A template repository that sets up a 3-agent development system for production-grade software development. Powered by [Claude Code](https://code.claude.com) as the runtime engine.

## Agents

| Agent | Name | Role | Model | Mode |
|-------|------|------|-------|------|
| 🎯 PM | **Prometeo** | Product specs, business logic, prioritization | Sonnet | Plan (read-only) |
| ⚡ Dev | **Forja** | Architecture, implementation, testing, docs | Inherit | Accept Edits |
| 🛡️ QA | **Centinela** | Security, code review, compliance, dead code | Sonnet | Default |

## Quick Start

```bash
# 1. Use this template to create your new project
gh repo create my-project --template your-username/agent-triforce-template

# 2. Clone and enter
cd my-project

# 3. Start Claude Code — agents load automatically
claude
```

## Usage

### Direct Agent Invocation
```
> Use Prometeo to define the feature for user authentication
> Use Forja to implement the auth feature
> Use Centinela to audit the auth implementation
```

### Via Skills (Slash Commands)
```
> /feature-spec User authentication with OAuth2
> /implement-feature auth-oauth2
> /security-audit auth-oauth2
> /code-health
> /release-check v1.0.0
> /review-findings auth-oauth2-review
```

### Standard Workflow
```
/feature-spec → /implement-feature → /security-audit → /review-findings → repeat
```

## Project Structure

```
.
├── CLAUDE.md                          # Orchestrator (agent rules & conventions)
├── CHANGELOG.md                       # Keep a Changelog format
├── TECH_DEBT.md                       # Technical debt register
├── .claude/
│   ├── agents/
│   │   ├── prometeo-pm.md             # PM agent definition
│   │   ├── forja-dev.md               # Dev agent definition
│   │   └── centinela-qa.md            # QA agent definition
│   ├── skills/
│   │   ├── feature-spec/SKILL.md      # → PM agent
│   │   ├── implement-feature/SKILL.md # → Dev agent
│   │   ├── code-health/SKILL.md       # → QA agent
│   │   ├── security-audit/SKILL.md    # → QA agent
│   │   ├── release-check/SKILL.md     # → QA agent
│   │   └── review-findings/SKILL.md   # → Dev agent
│   └── agent-memory/                  # Auto-generated persistent memory
│       ├── prometeo-pm/MEMORY.md
│       ├── forja-dev/MEMORY.md
│       └── centinela-qa/MEMORY.md
├── docs/
│   ├── specs/                         # Feature specifications (PM writes)
│   ├── adr/                           # Architecture Decision Records (Dev writes)
│   └── reviews/                       # Code reviews & audit reports (QA writes)
├── src/                               # Source code (Dev writes)
└── tests/                             # Tests (Dev writes, QA verifies)
```

## Key Features

- **Persistent Memory**: Each agent remembers decisions across sessions via `memory: project`
- **Auto-formatting**: Dev agent auto-runs linters after every file edit via hooks
- **Permission Enforcement**: PM can't edit code (plan mode), QA is read-only by default
- **Dead Code Detection**: QA scans for dead code on every review and via `/code-health`
- **Continuous Documentation**: Every agent flow generates documentation as a side effect
- **Skill-based Workflows**: `/feature-spec`, `/implement-feature`, `/security-audit` etc.

## Customization

### Changing Tech Stack
Edit `CLAUDE.md` → "Tech Stack Preferences" section.

### Adding New Skills
Create a new directory in `.claude/skills/{skill-name}/SKILL.md`.

### Modifying Agent Behavior
Edit the corresponding file in `.claude/agents/`.

### Project-Specific Rules
Add to `CLAUDE.md` or create `.claude/rules/` files.

## Requirements

### Runtime
- [Claude Code](https://code.claude.com) v2.1.32+ (the AI coding agent that powers agent orchestration)
- Claude Max or Pro subscription (or API key)

> **Note**: Agent Triforce is a provider-agnostic methodology. The `.claude/` directory contains the Claude Code runtime configuration (agents, skills, hooks, memory). The checklist framework, agent roles, and workflows are portable to other AI coding tools as they mature to support multi-agent orchestration.
