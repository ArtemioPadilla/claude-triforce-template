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

## Checklist Methodology

This system applies principles from *The Checklist Manifesto* (Atul Gawande) and Boeing's checklist engineering (Daniel Boorman). Checklists are not training wheels — they are cognitive safety nets that catch the flaws of memory, attention, and thoroughness inherent in all of us.

### Core Philosophy
- **Ineptitude, not ignorance**: Failures come from not applying what we already know, not from lack of knowledge
- **Checklists supplement expertise**: They are reminders of the most critical steps — not comprehensive how-to guides. They do not replace skill; they enhance it
- **"FLY THE AIRPLANE"**: Step 1 of any emergency checklist is to remember your primary mission. Never get so lost in process that you forget the goal
- **Discipline is professionalism**: The discipline to consult a checklist, no matter how experienced you are, is what separates reliable systems from fragile ones
- **Systems over components**: Individually excellent agents aren't enough — they must mesh together through structured coordination

### Checklist Design Rules (Boorman's Principles)
Every checklist in this system MUST follow these rules:
1. **Clear pause point**: A specific moment where you STOP and consult the checklist
2. **5-9 killer items only**: Focused on the steps most dangerous to skip and most commonly overlooked. Not everything — just the critical few
3. **Under 60 seconds**: If it takes longer, it will be skipped or shortcut
4. **Simple, exact wording**: No vague language. Each item is a concrete, verifiable action
5. **DO-CONFIRM or READ-DO**: Every checklist declares its type (see below)
6. **Field-tested and updated**: Checklists evolve based on actual failures and lessons learned. Update them when they catch something new or miss something important

### Two Types of Checklists
- **DO-CONFIRM**: You do your work from memory and experience, then PAUSE and run the checklist to confirm nothing was missed. Used when the team has expertise and the work is familiar.
- **READ-DO**: You read each item and do it as you go, step by step. Used for unfamiliar procedures, complex sequences, or when precision matters more than speed.

### Activation Phenomenon (Team Briefing Protocol)
Before any agent begins work, they MUST:
1. **State their identity and role**: "I am [Agent Name], [role description]"
2. **State what they're about to do**: The task, scope, and approach
3. **Surface concerns**: Any risks, unknowns, or blockers they see upfront

This is not ceremony — research shows that introducing roles and stating the plan activates participation, responsibility, and situational awareness. Teams that brief perform dramatically better than those that skip it.

### Workflow Pause Points
Every workflow has defined pause points where checklists are mandatory:

```
Standard Feature Flow:
PM (spec) → ⏸️ SPEC READY → Dev (implement) → ⏸️ PRE-HANDOFF → QA (audit) → ⏸️ VERDICT → Dev (fix) → ⏸️ FIX COMPLETE → QA (re-verify)
```

```
Code Health Flow:
QA (scan) → ⏸️ SCAN COMPLETE → Dev (cleanup) → ⏸️ CLEANUP DONE → QA (verify)
```

At each ⏸️ pause point, the active agent MUST run their designated checklist before proceeding to the next phase.

### Cross-Agent Communication Checklists
At every handoff between agents, the sending agent must provide:
1. **What was done**: Summary of work completed
2. **What to watch for**: Known risks, edge cases, concerns
3. **What's needed next**: Explicit expectations for the receiving agent
4. **Open questions**: Anything unresolved that needs the next agent's input

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
1. **Activate** — State identity, task, and concerns (Activation Phenomenon)
2. Read their own MEMORY.md first to recall past context
3. Read relevant docs in `docs/` before starting work
4. Run the appropriate checklist at each pause point in their workflow
5. Update their MEMORY.md with key decisions/findings before finishing
6. Update CHANGELOG.md if any code or spec changed
7. Update TECH_DEBT.md if tech debt was added, found, or resolved

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
