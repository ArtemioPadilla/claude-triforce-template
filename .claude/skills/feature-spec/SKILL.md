---
name: feature-spec
description: >
  Creates a complete product feature specification. Use when defining new features,
  writing user stories, or planning product work. Generates structured specs in docs/specs/.
context: fork
agent: prometeo-pm
---

Create a feature specification for: $ARGUMENTS

Follow these steps:

**ACTIVATE:**
- State your identity, role, and what you're about to do
- Surface any initial concerns about this feature request

**RESEARCH (READ-DO):**
1. Read existing specs in `docs/specs/` to understand current patterns and avoid conflicts
2. Read your MEMORY.md to recall past product decisions
3. Identify dependencies on existing features or systems

**BUILD:**
4. Create a comprehensive spec at `docs/specs/{feature-name}.md` using the template from your system prompt
5. Ensure all acceptance criteria are testable and unambiguous
6. List all dependencies, risks, and open questions

**⏸️ PAUSE — Run Spec Readiness Checklist (DO-CONFIRM):**
7. Run through every item in the Spec Readiness Checklist from your system prompt
8. Fix any gaps BEFORE proceeding to handoff

**HANDOFF:**
9. Write the PM → Dev Handoff using the communication template
10. Update your MEMORY.md with the key decisions made
11. Add an entry to CHANGELOG.md under `## [Unreleased]` → `### Planned`
