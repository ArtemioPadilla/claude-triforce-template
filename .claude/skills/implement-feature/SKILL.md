---
name: implement-feature
description: >
  Implements a feature from its specification. Reads the spec, designs architecture,
  writes code, tests, and documentation. Use after a feature spec has been approved.
context: fork
agent: forja-dev
---

Implement the feature: $ARGUMENTS

Follow these steps:

**ACTIVATE:**
- State your identity, role, and what you're about to build
- Surface any initial technical concerns or unknowns

**⏸️ PAUSE — Run Pre-Implementation Checklist (READ-DO):**
1. Read your MEMORY.md to recall past architectural decisions
2. Find and read the spec in `docs/specs/` for this feature
3. Identify interfaces/contracts to define first
4. Check existing codebase patterns this feature should follow
5. If significant architecture decisions are needed, create an ADR in `docs/adr/`
6. Confirm you understand ALL acceptance criteria

**BUILD:**
7. Implement the feature in `src/` following project conventions
8. Write tests in `tests/` (unit + integration for critical paths)
9. Scan for and remove any dead code you introduced or found

**⏸️ PAUSE — Run Pre-Handoff Checklist (DO-CONFIRM):**
10. Run through every item in the Pre-Handoff Checklist from your system prompt
11. Fix any failures BEFORE proceeding to handoff

**HANDOFF:**
12. Update CHANGELOG.md under `## [Unreleased]` → `### Added/Changed/Fixed`
13. Update TECH_DEBT.md if any debt was added or resolved
14. Update your MEMORY.md with architectural decisions made
15. Write the Dev → QA Handoff using the communication template
