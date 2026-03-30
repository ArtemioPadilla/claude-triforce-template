---
description: Implement a feature from an approved spec using the full triforce workflow
---

Implement the feature: $ARGUMENTS

Use Forja (Dev agent) with the implement-feature skill. If a spec exists in docs/specs/, read it first. If no spec exists, check if we need one before proceeding.

Follow the subagent orchestration workflow if the implementation has multiple tasks:
1. Read the spec/plan
2. Dispatch fresh subagent per task
3. Two-stage review (spec compliance, then code quality)
4. Use git worktrees for isolation
