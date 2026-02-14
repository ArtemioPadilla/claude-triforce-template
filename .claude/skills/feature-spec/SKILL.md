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
1. Read existing specs in `docs/specs/` to understand current patterns and avoid conflicts
2. Read your MEMORY.md to recall past product decisions
3. Create a comprehensive spec at `docs/specs/{feature-name}.md` using the template from your system prompt
4. Ensure all acceptance criteria are testable and unambiguous
5. List all dependencies, risks, and open questions
6. Update your MEMORY.md with the key decisions made
7. Add an entry to CHANGELOG.md under `## [Unreleased]` → `### Planned`
