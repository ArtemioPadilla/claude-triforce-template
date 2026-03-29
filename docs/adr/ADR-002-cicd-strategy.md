# ADR-002: CI/CD Strategy

**Date**: 2026-03-29
**Status**: Accepted
**Context**: Agent Triforce Pipeline Architecture

## Context

Agent Triforce has three CI workflow templates in `templates/ci/` (pr-review.yml, security-audit.yml, release-check.yml) but lacks a documented strategy explaining:
- Why these specific pipeline stages were chosen
- How quality gates map to the development workflow
- What branching model the project follows
- How the pipeline stages relate to each other

## Decision

### Branching Model: Git Flow-Lite

Formalize the branching convention already implicit in CLAUDE.md:

- **`main`**: Always releasable. Protected branch. Merges only via PR.
- **Feature branches**: `{type}/{ticket-short-description}` where type is one of: `feat/`, `fix/`, `refactor/`, `docs/`, `test/`, `chore/`
- **Release tags**: `v{major}.{minor}.{patch}` following Semantic Versioning
- **No develop branch**: `main` serves as both integration and release branch. Simplicity over ceremony.

### Pipeline Stages and Quality Gates

| Stage | Trigger | What Runs | Agent | Gate | Speed |
|-------|---------|-----------|-------|------|-------|
| **Commit** | Push to any branch | Lint, unit tests, `security-scanner.py` patterns | None (automated) | All checks pass | Fast (<2 min) |
| **PR Review** | PR opened/updated | Centinela code review | Centinela (Haiku) | No Critical/High findings | Medium (~5 min) |
| **Merge to main** | PR merged | Full security-audit + license compliance | Centinela (Haiku) | No Critical findings | Medium (~10 min) |
| **Release** | Tag `v*` pushed | release-check (all 8 criteria) | Centinela (Sonnet) | GO verdict, confidence >= 70 | Slow (~10 min) |

### Quality Gate Philosophy

- **CI gates are binary**: pass or fail. A PR with a Critical finding cannot merge. This aligns with the principle that fast feedback should be unambiguous.
- **Release decisions are nuanced**: The release-check produces a continuous confidence score (0-100) alongside the GO/NO-GO verdict. A score of 72 (GO) tells you more than a simple "pass."
- **Fail fast, verify thoroughly**: Commit-stage checks are cheap and fast (lint, unit tests). Each subsequent stage adds depth but also cost. This is a deliberate trade-off.

### Static Analysis Mapping

The project does not integrate SonarQube or similar server-based tools. Instead, Centinela's skills provide equivalent coverage:

| SonarQube Concept | Agent Triforce Equivalent | Skill |
|---|---|---|
| Code smells | Clean Code violations (>30 line functions, >3 nesting) | code-health |
| Bugs | Defect findings in code review | review-findings |
| Vulnerabilities | OWASP Top 10 scan | security-audit |
| Duplications | Dead code detection, DRY violations | code-health |
| Coverage | Test coverage threshold (80%) | release-check |
| License compliance | Dependency license scan | security-audit |

### Template Installation

The CI templates in `templates/ci/` are ready to use. To install:

1. Copy templates: `cp -r templates/ci/ .github/workflows/`
2. Set `ANTHROPIC_API_KEY` as a GitHub repository secret
3. (Optional) Adjust model and timeout settings in workflow files

See `agent-triforce/commands/ci-setup.md` for detailed instructions.

## Consequences

- All PRs go through Centinela review before merge
- Security audit runs on every merge to main, not just releases
- License compliance is checked at merge time (catches issues early)
- Release confidence score enables data-driven release decisions
- No additional infrastructure required -- GitHub Actions + Anthropic API only

## References

- Rossel, S. (2017). *Continuous Integration, Delivery, and Deployment*. Packt Publishing. Ch. 1 (CI/CD foundations, quality gates), Ch. 3 (branching models, tagging).
- Humble, J. & Farley, D. (2010). *Continuous Delivery*. Addison-Wesley. (Pipeline stage design principles)
