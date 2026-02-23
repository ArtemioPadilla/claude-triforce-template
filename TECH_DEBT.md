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
- **Impact if not fixed**: Users who create projects from this template cannot receive upstream improvements (new checklists, methodology refinements, new skills) without manually diffing and merging. Porting to downstream projects (like downstream-project) takes 2+ hours of manual merge work per upgrade.
- **Proposed fix**: Marker-based upgrade system. Wrap framework content in `<!-- triforce:begin SECTION_ID -->` / `<!-- triforce:end SECTION_ID -->` HTML comments. A bash script (`scripts/triforce-upgrade.sh`) replaces content between markers while preserving user customizations. Skills (100% framework) get replaced entirely. Full design in `.claude/plans/cuddly-scribbling-flute.md`. Key decisions:
  - 3 marked regions in CLAUDE.md (system-overview, methodology, workflow-rules)
  - 2 marked regions per agent file (core-responsibilities, checklists)
  - YAML frontmatter is user-owned (hooks, tools are project-specific)
  - `triforce.json` manifest tracks version and file strategies
  - Zero external dependencies — pure bash
- **See also**: `docs/portability/downstream-project.md` (portability guide for downstream repos)

## Resolved Debt

<!-- Move items here when fixed, add resolution date and how it was resolved -->

_No resolved debt yet._
