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
1. Read your MEMORY.md for previously known issues
2. Scan for dead code:
   - Unused imports: `ruff check --select F401 src/` or `biome lint src/`
   - Unused variables/functions: grep for definitions not referenced elsewhere
   - Commented-out code blocks: search for patterns like `// `, `# `, `/* */` spanning 3+ lines
   - Unreachable code after return/throw/break/continue
   - Files not imported by any other file
3. Check for outdated dependencies:
   - `pip list --outdated` or `npm outdated`
   - Known vulnerabilities: `pip audit` or `npm audit`
4. Scan for code smells:
   - Functions longer than 50 lines
   - Files longer than 500 lines
   - Deeply nested code (>4 levels)
   - Duplicated logic blocks
5. Check TODO/FIXME comments — do they have issue references?
6. Write findings to `docs/reviews/code-health-{date}.md`
7. Update `TECH_DEBT.md` with new findings
8. Update your MEMORY.md with patterns discovered
