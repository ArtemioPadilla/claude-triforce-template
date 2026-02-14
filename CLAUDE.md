# 🔱 Claude Triforce — Multi-Agent Development System

## System Overview

This project uses 3 specialized agents. Always use the appropriate agent for each task:

- **Prometeo (PM)**: Product strategy, feature specs, business logic, prioritization
- **Forja (Dev)**: Architecture, implementation, infrastructure, documentation
- **Centinela (QA)**: Security audit, code review, testing, compliance, dead code detection

## Agent Invocation

Use agents explicitly:
- "Use Prometeo to define the feature for [X]"
- "Use Forja to implement [X]"
- "Use Centinela to audit [X]"

Or use skills:
- `/feature-spec [description]` → Runs with Prometeo
- `/implement-feature [spec-name]` → Runs with Forja
- `/security-audit [scope]` → Runs with Centinela
- `/code-health` → Runs with Centinela
- `/release-check` → Runs with Centinela
- `/review-findings [review-file]` → Runs with Forja

## Workflow Rules

### Standard Feature Flow
```
PM (spec) → Dev (implement) → QA (audit) → Dev (fix findings) → QA (re-verify)
```

### Code Health Flow (run periodically)
```
QA (scan) → Dev (cleanup) → QA (verify)
```

### Every Agent MUST on Every Invocation:
1. Read their own MEMORY.md first to recall past context
2. Read relevant docs in `docs/` before starting work
3. Update their MEMORY.md with key decisions/findings before finishing
4. Update CHANGELOG.md if any code or spec changed
5. Update TECH_DEBT.md if tech debt was added, found, or resolved

## Project Conventions

### File Locations
- Feature specs: `docs/specs/{feature-name}.md`
- Architecture Decision Records: `docs/adr/ADR-{NNN}-{title}.md`
- QA reviews: `docs/reviews/{feature-name}-review.md`
- Source code: `src/`
- Tests: `tests/`

### Git Conventions
- Branches: `{type}/{ticket-short-description}` (feat/, fix/, refactor/, docs/, test/)
- Commits: Conventional Commits (feat:, fix:, docs:, refactor:, test:, chore:)

### Code Standards
- Python: type hints everywhere, docstrings on public functions, no bare except
- TypeScript: strict mode, no `any` without documented justification, JSDoc on exports
- No hardcoded secrets, URLs, or config values
- No commented-out code (it's in git history)
- No TODO/FIXME without a linked issue or ticket reference
- Structured logging (JSON format)
- All public APIs documented with OpenAPI/Swagger

### Documentation
- Every module has a README explaining purpose and usage
- Architecture changes require an ADR
- CHANGELOG.md follows Keep a Changelog format
- TECH_DEBT.md tracks all known technical debt

## Tech Stack Preferences
- **Python**: FastAPI, Pydantic, SQLAlchemy, pytest, ruff
- **TypeScript**: Next.js, React, Zod, Vitest, Biome
- **Blockchain/Web3**: Solidity, Hardhat, Ethers.js, Foundry
- **Infrastructure**: AWS CDK, Docker, GitHub Actions
- **Data**: PostgreSQL, Redis, DynamoDB
