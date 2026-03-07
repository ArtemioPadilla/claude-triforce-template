# Technical Debt Register

Track all known technical debt. Updated by both Dev (Forja) and QA (Centinela) agents.

## Active Debt

<!-- Use this format for each debt item:

### [TD-{NNN}] {Short description}
- **Type**: Design | Code | Test | Infra | Security | Dependency
- **Severity**: Critical | High | Medium | Low
- **Found**: {YYYY-MM-DD}
- **Estimated effort**: {hours or T-shirt size}
- **Impact if not fixed**: {what happens}
- **Proposed fix**: {approach}

-->

### [TD-001] Versioning and upgrade system for the Agent Triforce framework
- **Type**: Design
- **Severity**: Medium
- **Found**: 2026-02-15
- **Estimated effort**: L (half day)
- **Impact if not fixed**: Users who create projects from this template cannot receive upstream improvements (new checklists, methodology refinements, new skills) without manually diffing and merging. Porting to downstream projects takes 2+ hours of manual merge work per upgrade.
- **Proposed fix**: Marker-based upgrade system. Wrap framework content in `<!-- triforce:begin SECTION_ID -->` / `<!-- triforce:end SECTION_ID -->` HTML comments. A bash script (`scripts/triforce-upgrade.sh`) replaces content between markers while preserving user customizations. Skills (100% framework) get replaced entirely. Full design in `.claude/plans/cuddly-scribbling-flute.md`. Key decisions:
  - 3 marked regions in CLAUDE.md (system-overview, methodology, workflow-rules)
  - 2 marked regions per agent file (core-responsibilities, checklists)
  - YAML frontmatter is user-owned (hooks, tools are project-specific)
  - `triforce.json` manifest tracks version and file strategies
  - Zero external dependencies — pure bash

### [TD-002] `_find_project_root()` duplicated verbatim across all 8 tool files
- **Type**: Code
- **Severity**: Medium
- **Found**: 2026-03-05
- **Estimated effort**: S (1-2 hours)
- **Impact if not fixed**: Any change to project root detection logic requires 8 file edits. High risk of version drift between tools over time.
- **Proposed fix**: Extract to `tools/_common.py` shared module (or `src/utils.py`) and import from there. All 8 tool files affected: dashboard.py, memory-sync.py, traceability.py, session-tracker.py, workflow-tracker.py, handoff-generator.py, gate-checker.py, security-scanner.py.

### [TD-003] `_HtmlBuilder.open_page()` embeds ~440-line CSS stylesheet inline
- **Type**: Code
- **Severity**: Low
- **Found**: 2026-03-05
- **Estimated effort**: S (30 minutes)
- **Impact if not fixed**: CSS is uneditable with syntax highlighting; the method is unmaintainable; future CSS changes risk introducing Python string escaping errors.
- **Proposed fix**: Extract CSS to a module-level constant `_HTML_CSS = """..."""` in dashboard.py and reference it from `open_page()`. Reduces the method from ~440 lines to ~10 lines.

### [TD-004] Test coverage gap for 3 of 8 tool files
- **Type**: Test
- **Severity**: Medium
- **Found**: 2026-03-05
- **Updated**: 2026-03-07
- **Estimated effort**: M (half day)
- **Impact if not fixed**: Regressions in memory-sync.py, traceability.py, and codebase-indexer.py go undetected.
- **Current state**: 5 of 8 tool files now have tests (session-tracker, workflow-tracker, dashboard parsing added 2026-03-07). The 5 tested files score 75-95% individually. Overall tools/ coverage is 43% due to 3 remaining untested files at 0% and dashboard rendering code (900+ lines of HTML/terminal output).
- **Proposed fix**: Add tests for memory-sync.py (conflict detection), traceability.py (criterion extraction), and codebase-indexer.py (module scanning). Dashboard rendering tests are lower priority (presentation layer).

## Resolved Debt

<!-- Move items here when fixed, add resolution date and how it was resolved -->

_No resolved debt yet._
