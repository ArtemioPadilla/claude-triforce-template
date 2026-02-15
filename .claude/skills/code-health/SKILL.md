---
name: code-health
description: >
  Scans the codebase for dead code, tech debt, outdated dependencies, and code quality
  issues. Use periodically or before releases to maintain code hygiene.
context: fork
agent: centinela-qa
---

Run a comprehensive code health scan on the codebase.

Follow these steps:

**ACTIVATE:**
- State your identity, role, and that you're running a code health scan
- Note any areas of concern based on past scans

**⏸️ PAUSE — Run Pre-Review Checklist (READ-DO):**
1. Read your MEMORY.md for previously known issues and patterns
2. Check recent CHANGELOG.md entries to understand what changed since last scan
3. Run existing tests to confirm baseline state

**SCAN:**
4. Scan for dead code:
   - Unused imports: `ruff check --select F401 src/` or `biome lint src/`
   - Unused variables/functions: grep for definitions not referenced elsewhere
   - Commented-out code blocks: search for patterns like `// `, `# `, `/* */` spanning 3+ lines
   - Unreachable code after return/throw/break/continue
   - Files not imported by any other file
5. Check for outdated dependencies:
   - `pip list --outdated` or `npm outdated`
   - Known vulnerabilities: `pip audit` or `npm audit`
6. Scan for code smells:
   - Functions longer than 50 lines
   - Files longer than 500 lines
   - Deeply nested code (>4 levels)
   - Duplicated logic blocks
7. Check TODO/FIXME comments — do they have issue references?

**⏸️ PAUSE — Scan Complete Checklist (DO-CONFIRM):**
- [ ] All source directories scanned (not just `src/` — also `tests/`, config files)
- [ ] Dead code findings verified (not false positives from dynamic imports or plugins)
- [ ] Dependency vulnerabilities checked with automated tools
- [ ] Findings prioritized: Critical > Warning > Suggestion
- [ ] Previous scan findings compared — are old issues resolved or recurring?

**HANDOFF:**
8. Write findings to `docs/reviews/code-health-{date}.md`
9. Write the QA → Dev Handoff using the communication template
10. Update `TECH_DEBT.md` with new findings
11. Update your MEMORY.md with patterns discovered
