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
1. Read your MEMORY.md to recall past architectural decisions
2. Find and read the spec in `docs/specs/` for this feature
3. If the feature requires significant architecture decisions, create an ADR in `docs/adr/`
4. Implement the feature in `src/` following project conventions
5. Write tests in `tests/` (unit + integration for critical paths)
6. Run self-review against quality gates in your system prompt
7. Scan for and remove any dead code you introduced or found
8. Update CHANGELOG.md under `## [Unreleased]` → `### Added/Changed/Fixed`
9. Update TECH_DEBT.md if any debt was added or resolved
10. Update your MEMORY.md with architectural decisions made
11. Prepare a clear handoff summary for QA review
