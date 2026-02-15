---
name: release-check
description: >
  Pre-release verification checklist. Validates that all features are complete,
  tests pass, docs are updated, no critical issues remain, and the release is safe.
context: fork
agent: centinela-qa
---

Run a pre-release verification for: $ARGUMENTS

This is the highest-stakes checklist in the system. Like a pilot's pre-flight check, every item matters.

Follow these steps:

**ACTIVATE:**
- State your identity, role, and that you're running a pre-release check
- Note any known risks or concerns about this release

**⏸️ PAUSE 1 — Documentation & Debt Check (READ-DO):**
1. Read CHANGELOG.md — is it up to date with all changes?
2. Read TECH_DEBT.md — are there any critical items blocking release?
3. Verify all specs in `docs/specs/` with status "In Development" have acceptance criteria met
4. Verify documentation is current (README, API docs, ADRs)

**⏸️ PAUSE 2 — Testing & Quality Gate (DO-CONFIRM):**
5. Run all tests and verify they pass
6. Run `/code-health` scan (check for dead code, unused deps)
7. Check that all review findings with "CHANGES REQUIRED" have been resolved
- [ ] All tests passing
- [ ] No critical dead code or dependency vulnerabilities
- [ ] All CHANGES REQUIRED findings resolved
- [ ] CHANGELOG complete and accurate

**⏸️ PAUSE 3 — Security Gate (DO-CONFIRM):**
8. Run `/security-audit` on changed files
- [ ] No critical security findings
- [ ] No hardcoded secrets or credentials
- [ ] Dependencies free of known critical CVEs
- [ ] Auth/authz enforced on all protected endpoints

**VERDICT:**
9. Write release assessment to `docs/reviews/release-check-{version}.md`
10. Provide final verdict: **READY FOR RELEASE** | **BLOCKED** (with specific reasons and what must be fixed)

A release blocked here prevents issues reaching users. This is the last line of defense.
