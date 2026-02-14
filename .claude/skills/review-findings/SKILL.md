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
1. Read the review report in `docs/reviews/`
2. Read your MEMORY.md for context on past fixes
3. Address findings in priority order: 🔴 Critical first, then 🟡 Warnings
4. For each finding:
   a. Understand the root cause
   b. Implement the fix
   c. Add/update tests to prevent recurrence
   d. Document what changed and why
5. Scan for dead code after all fixes
6. Update CHANGELOG.md
7. Update TECH_DEBT.md if any debt was resolved
8. Update your MEMORY.md with patterns learned
9. Prepare a fix report summarizing all changes for QA re-verification
