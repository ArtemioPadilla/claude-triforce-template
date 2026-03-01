# Test Strategy: {Project/Release Name}

**Date**: {YYYY-MM-DD}
**Owner**: Prometeo (planning) + Centinela (verification)
**Status**: Draft | Active | Archived

## 1. Objectives
{What does testing aim to achieve? What confidence level before release?}

## 2. Scope
- **In scope**: {features, modules, integrations to test}
- **Out of scope**: {what we will NOT test, with rationale}

## 3. Test Levels

| Level | What | Tools | Owner | Coverage Target |
|-------|------|-------|-------|-----------------|
| Unit | Business logic, pure functions | pytest / Vitest | Forja | >80% |
| Integration | API contracts, DB interactions, service boundaries | pytest / Vitest | Forja | Critical paths |
| E2E | User-facing flows | Playwright / Cypress | Forja | Happy paths + top 3 risk scenarios |
| Security | OWASP Top 10, dependency audit | Centinela + tools | Centinela | All endpoints |

## 4. Risk-Based Priority

| Area | Risk Level | Reason | Test Priority |
|------|-----------|--------|---------------|
| {area} | {Critical/High/Medium/Low} | {why} | {test first/second/last} |

## 5. Test Data
- **Builders/Factories**: {approach — factories, fixtures, seed scripts}
- **Sensitive data**: {PII handling — anonymization, synthetic data}
- **External services**: {stub/mock strategy for third-party APIs}

## 6. Test Environment
- **Local**: {how to run tests locally}
- **CI**: {pipeline config, parallelization}
- **Staging**: {pre-production validation if applicable}

## 7. Entry/Exit Criteria
- **Entry**: code compiles, unit tests pass, code review complete
- **Exit**: all Critical/High defects fixed, >80% coverage, no open security findings

## 8. Defect Management
- Critical/High: block release, fix immediately
- Medium: fix before next release
- Low: backlog

## 9. Reporting
- Test results in QA reviews (`docs/reviews/`)
- Coverage tracked via `/agent-triforce:release-check`
- Traceability via `/agent-triforce:traceability`
