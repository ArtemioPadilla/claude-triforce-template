---
name: review-findings
description: >
  Addresses and fixes findings from a QA code review. Reads the review report,
  fixes critical and warning issues, and prepares for re-verification.
context: fork
agent: forja-dev
---

Fix the findings from the QA review: $ARGUMENTS

If no specific review is mentioned, look for the most recent review in `docs/reviews/`.

Follow these steps:

**ACTIVATE:**
- State your identity, role, and that you're fixing QA findings
- Surface any concerns about the findings — complexity, risk, dependencies

**⏸️ PAUSE — Pre-Fix Checklist (READ-DO):**
1. Read the review report in `docs/reviews/`
2. Read your MEMORY.md for context on past fixes and patterns
3. Understand each finding's root cause BEFORE writing any fix
4. Plan the fix order: 🔴 Critical first, then 🟡 Warnings
5. Identify if any fixes could conflict with each other

**FIX:**
6. For each finding:
   a. Understand the root cause
   b. Implement the fix
   c. Add/update tests to prevent recurrence
   d. Document what changed and why
7. Scan for dead code after all fixes

**⏸️ PAUSE — Pre-Handoff Checklist (DO-CONFIRM):**
Run the Pre-Handoff Checklist from your system prompt AND verify these additional items:
- [ ] Every 🔴 Critical finding addressed
- [ ] Every 🟡 Warning finding addressed (or explicitly deferred with justification)
- [ ] No new issues introduced by the fixes
- [ ] Tests pass after all changes

**HANDOFF:**
8. Update CHANGELOG.md
9. Update TECH_DEBT.md if any debt was resolved
10. Update your MEMORY.md with patterns learned
11. Write a Fix Report for QA re-verification using the Fix Report template
