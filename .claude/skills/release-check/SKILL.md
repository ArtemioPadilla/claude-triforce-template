---
name: release-check
description: >
  Pre-release verification checklist. Validates that all features are complete,
  tests pass, docs are updated, no critical issues remain, and the release is safe.
context: fork
agent: centinela-qa
---

Run a pre-release verification for: $ARGUMENTS

Follow these steps:
1. Read CHANGELOG.md — is it up to date with all changes?
2. Read TECH_DEBT.md — are there any critical items blocking release?
3. Run all tests and verify they pass
4. Run `/code-health` scan (check for dead code, unused deps)
5. Run `/security-audit` on changed files
6. Verify all specs in `docs/specs/` with status "In Development" have acceptance criteria met
7. Check that all review findings with "CHANGES REQUIRED" have been resolved
8. Verify documentation is current (README, API docs, ADRs)
9. Write release assessment to `docs/reviews/release-check-{version}.md`
10. Provide final verdict: READY FOR RELEASE | BLOCKED (with reasons)
