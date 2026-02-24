# Agent Triforce — Feature Roadmap
**Status**: Draft
**Version**: 0.1.0
**Date**: 2026-02-23
**Owner**: Prometeo (PM)
**Next Review**: 2026-03-23

---

## Overview

This roadmap defines 20 features for Agent Triforce across four prioritized phases. Features are sequenced by the intersection of strategic impact and delivery effort. Phase 1 (P0) contains the highest-leverage differentiators. Phase 4 (P3) contains high-complexity features that depend on earlier phases or require significant infrastructure.

The core product thesis: Agent Triforce is the only Claude Code multi-agent system built on a validated human-safety checklist methodology (Gawande + Boeing). Every feature on this roadmap either strengthens that core differentiator or removes friction that prevents the methodology from reaching its audience.

**Guiding constraint**: Features that are "differentiator" classification take precedence over "table stakes" at equal RICE scores, because they deepen the competitive moat that table-stakes features cannot build.

---

## Phase Overview Table

| ID | Feature | Phase | Complexity | Classification | Status |
|----|---------|-------|------------|----------------|--------|
| F01 | Agent Team Orchestration Mode | P0 | Medium | Differentiator | Implemented |
| F02 | Automated Handoff Protocol with Structured Artifacts | P0 | Medium | Differentiator | Implemented |
| F03 | Interactive Setup Wizard (`/setup` Enhancement) | P0 | Medium | Table Stakes | Implemented |
| F04 | LSP Integration for Real-Time Code Intelligence | P1 | Low | Table Stakes | Implemented |
| F05 | Security Scanner Hook (Pre-Commit) | P1 | Low | Table Stakes | Implemented |
| F06 | Static Analysis MCP Integration | P1 | Low | Differentiator | Implemented |
| F07 | Workflow Visualization and Progress Tracking | P1 | Medium | Differentiator | Implemented |
| F08 | Automated Test Generation Skill (`/generate-tests`) | P1 | Low-Medium | Table Stakes | Implemented |
| F09 | Smart Agent Routing (Model Selection) | P1 | Low-Medium | Table Stakes | Implemented |
| F10 | Plan Approval Gates Between Agents | P2 | Medium | Differentiator | Implemented |
| F11 | Release Readiness Report Generator | P2 | Low-Medium | Differentiator | Implemented |
| F12 | GitHub Actions / CI-CD Integration | P2 | Low-Medium | Table Stakes | Implemented |
| F13 | Linear / Jira / GitHub Issues MCP Integration | P2 | Low | Table Stakes | Implemented |
| F14 | Cross-Agent Persistent Memory with Conflict Detection | P2 | Medium | Differentiator | Implemented |
| F15 | Checklist Evolution System | P2 | Medium-High | Differentiator | Implemented |
| F16 | Live Dashboard with Session Analytics | P3 | Medium-High | Differentiator | Implemented |
| F17 | Spec-to-Implementation Traceability Matrix | P3 | Medium-High | Differentiator | Implemented |
| F18 | Context-Efficient Agent Spawning | P3 | Medium | Differentiator | Implemented |
| F19 | Non-Normal Procedure Training Mode (`/simulate-failure`) | P3 | Medium | Differentiator | Implemented |
| F20 | Codebase Knowledge Index | P3 | High | Differentiator | Implemented |

---

## Phase 1 — P0: Highest Impact (Foundation)

**Theme**: Make the Agent Triforce methodology fully operational as a native Claude Code experience. These features close the gap between the methodology as documented and the methodology as actually executed by agents.

**Success Metrics for Phase 1**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Median time to first successful PM-to-Dev handoff | < 5 minutes | Measured in user onboarding tests |
| Onboarding completion rate (wizard to first spec) | > 70% of new installs | GitHub clone traffic vs first spec created |
| Handoff artifact correctness (no missing required fields) | 100% | Automated validation on artifact generation |
| GitHub stars after Phase 1 launch | 100 | GitHub repo star count |

---

### F01 — Agent Team Orchestration Mode

**ID**: F01
**Status**: Planned
**Priority**: P0-Critical
**Complexity**: Medium
**Classification**: Differentiator

#### Description

Run Prometeo, Forja, and Centinela as a coordinated agent team using Claude Code's Agent Teams feature. Prometeo acts as team lead with the ability to delegate tasks to Forja and Centinela as teammates. Includes shared task lists and inter-agent messaging channels so agents can operate in parallel rather than purely sequential handoffs.

#### Problem Statement

Today, all three agents run sequentially via manual user invocation. Prometeo writes a spec, the user manually invokes Forja, Forja implements, the user manually invokes Centinela. True parallel orchestration allows Prometeo to define specs for feature B while Centinela reviews Forja's implementation of feature A. This is the workflow velocity unlock that distinguishes Agent Triforce from a collection of independent agent prompts.

No other plugin combines the Gawande/Boeing checklist methodology with native Claude Code agent team orchestration. This is the highest-leverage architectural investment on the roadmap.

#### User Stories

As a developer using Agent Triforce on a multi-feature sprint, I want the agents to coordinate work in parallel, so that I am not the manual bottleneck passing context between agents.

As an engineering team lead, I want Prometeo to act as the team lead that coordinates Forja and Centinela automatically, so that the PM/Dev/QA discipline is enforced without requiring me to manage each handoff step.

#### Acceptance Criteria

GIVEN a developer runs `/feature-spec [name]` to initiate a workflow,
WHEN the Agent Teams configuration is active,
THEN Prometeo spawns as team lead, delegates implementation to Forja, and notifies Centinela for review — without requiring additional manual invocations between phases.

GIVEN Forja is implementing feature A,
WHEN Prometeo has a new spec ready for feature B,
THEN Prometeo can begin spec work on feature B in a parallel task without waiting for Forja to complete feature A.

GIVEN Centinela issues a blocking finding during review,
WHEN the finding is communicated via inter-agent messaging,
THEN Forja receives the structured finding artifact directly and can begin remediation without user relay.

GIVEN the Agent Teams feature is not available in the user's Claude Code environment,
WHEN the user invokes a skill,
THEN the system gracefully falls back to sequential single-agent mode with no error and a single informational message explaining that parallel orchestration is unavailable.

#### Business Rules

- Prometeo is always the team lead; Forja and Centinela are teammates. This hierarchy is not configurable without an explicit ADR.
- Inter-agent messages must include the 4-field communication structure from CLAUDE.md: what was done, what to watch for, what's needed next, open questions.
- Checklist pause points (SIGN IN / TIME OUT / SIGN OUT) remain mandatory for each agent even in team mode. Parallelism does not bypass checklists.
- Fallback to sequential mode must be automatic and transparent. The user should not need to configure which mode to use.

#### Dependencies

- None (foundational feature)

---

### F02 — Automated Handoff Protocol with Structured Artifacts

**ID**: F02
**Status**: Planned
**Priority**: P0-Critical
**Complexity**: Medium
**Classification**: Differentiator

#### Description

Claude Code hooks auto-generate structured handoff documents (JSON and/or markdown) when one agent completes a phase. The artifact contains the four required fields from the CLAUDE.md Communication Schedule: "what was done," "what to watch for," "what's needed next," "open questions." This artifact is piped directly into the receiving agent's spawn prompt, eliminating context loss at handoff boundaries.

#### Problem Statement

The Communication Schedule in CLAUDE.md defines 6 handoff paths with specific fields, but relies entirely on human orchestration to move context between agents. In practice, handoff quality degrades when users are in a hurry or skip steps. The methodology's reliability depends on the consistency of handoffs — structured artifacts with automated generation make the methodology robust regardless of user discipline.

Structured handoffs with checklist verification at every boundary are the core of what makes this system different from a collection of prompts.

#### User Stories

As Forja completing an implementation, I want to auto-generate a structured handoff artifact for Centinela, so that I do not lose context about what I built, what I am unsure about, and what Centinela needs to specifically verify.

As Centinela receiving a handoff from Forja, I want the context about what was implemented and known risk areas to be in my spawn prompt automatically, so that I can begin the security and quality review with full situational awareness.

#### Acceptance Criteria

GIVEN Forja has completed implementation and is running its SIGN OUT checklist,
WHEN the `PostToolUse` hook triggers on SIGN OUT completion,
THEN a handoff artifact file is generated at `docs/handoffs/{feature-name}-forja-to-centinela-{timestamp}.md` containing all four required fields with no empty sections.

GIVEN a handoff artifact exists for a feature,
WHEN Centinela is invoked for that feature,
THEN the artifact content is automatically prepended to Centinela's spawn prompt so no manual copy-paste is required.

GIVEN a handoff artifact is generated,
WHEN any of the four required fields (what was done, what to watch for, what's needed next, open questions) is empty or missing,
THEN the hook blocks the handoff and prompts the sending agent to complete the artifact before proceeding.

GIVEN the handoff artifact directory does not exist,
WHEN the first artifact is generated,
THEN the directory is created automatically and a `.gitignore` entry is suggested (artifacts are ephemeral, not permanent project artifacts unless the team opts in).

#### Business Rules

- Handoff artifacts are ephemeral by default. Teams can opt into persisting them by removing the `.gitignore` entry.
- All six Communication Schedule paths from CLAUDE.md must have corresponding hook configurations: Prometeo-to-Forja, Forja-to-Prometeo (ambiguity), Forja-to-Centinela, Centinela-to-Forja, Centinela-to-Prometeo, Any-to-User.
- The JSON format is for machine processing (F01 Agent Teams integration). The markdown format is for human readability. Both are generated simultaneously.
- An agent cannot proceed to its next phase without a validated handoff artifact from the prior phase. "Validated" means all four fields are non-empty and the receiving agent ID matches the intended next agent.

#### Dependencies

- F01 (Agent Team Orchestration Mode) — the JSON artifact format must be compatible with F01's inter-agent messaging schema.

---

### F03 — Interactive Setup Wizard (`/setup` Enhancement)

**ID**: F03
**Status**: Planned
**Priority**: P0-Critical
**Complexity**: Medium
**Classification**: Table Stakes

#### Description

Transform the current minimal `/setup` command into a multi-step interactive wizard. The wizard detects the project's tech stack, suggests appropriate agent configurations, initializes the `docs/` directory structure, creates a starter CLAUDE.md with project-specific content, and optionally connects MCP servers (SonarQube, Linear, GitHub). Goal: a developer should go from zero to first spec in under 5 minutes.

#### Problem Statement

Onboarding failure is the primary adoption killer for any developer tool. The current setup is minimal: install the plugin and start. For a system as structured as Agent Triforce, this creates a gap between installation and productive use that most developers will not bridge without guidance. Competitors with simpler tooling win on first-use experience even when Agent Triforce's methodology is stronger.

#### User Stories

As a developer installing Agent Triforce for the first time, I want a guided setup that configures the system for my specific tech stack, so that I can start using agents within 5 minutes without reading documentation.

As an engineering team lead introducing Agent Triforce to a team, I want to be able to run setup interactively and have the system generate a sensible default CLAUDE.md for our project, so that the team has a consistent starting configuration without manual customization.

#### Acceptance Criteria

GIVEN a developer runs `/setup` in a project directory,
WHEN the wizard starts,
THEN it detects the tech stack by scanning for `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, or equivalent manifest files, and presents a confirmation of detected stack before proceeding.

GIVEN the wizard has detected or the user has confirmed the tech stack,
WHEN the wizard completes all steps,
THEN the following artifacts exist: `docs/` directory structure (specs, reviews, adr subdirectories), a project-specific CLAUDE.md that references the detected stack, and all three agent `.claude/agents/*.md` files with the tech stack preferences section populated.

GIVEN the wizard reaches the optional MCP server connection step,
WHEN the user declines MCP configuration,
THEN the wizard completes successfully and adds a `## MCP Configuration (Not Set Up)` section to CLAUDE.md with instructions for later setup. Nothing is blocked by declining MCP.

GIVEN a project has already been set up (CLAUDE.md and docs/ exist),
WHEN a developer runs `/setup`,
THEN the wizard detects existing configuration, prompts for confirmation before overwriting, and offers a "reconfigure only" mode that updates tech stack preferences without overwriting existing specs or memory files.

#### Business Rules

- The wizard must complete in under 5 minutes for a standard web project. If any step cannot complete automatically, it must provide a default and continue rather than blocking.
- Tech stack detection is best-effort. The wizard always shows the detected result and asks for confirmation before applying it.
- No credentials, API keys, or secrets are collected by the wizard. MCP server connections use only OAuth or token configurations that the user provides.
- The wizard must work offline (no network calls required for the base setup). MCP configuration is the only step that requires network access.

#### Dependencies

- None (can be developed independently, but F06 MCP integration and F13 issue tracker integration define what MCP options are offered in the wizard)

---

## Phase 2 — P1: High Impact, Low-Medium Effort

**Theme**: Strengthen the intelligence and automation of the agents with real diagnostic data, security guardrails, and cost efficiency. These features address the most common developer complaints about AI coding tools (cost, heuristic analysis, missing test generation) while adding differentiating capabilities.

**Success Metrics for Phase 1 Completion / Phase 2 Entry**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Security issues caught pre-commit vs post-commit | > 80% caught pre-commit | Security Scanner Hook hit rate |
| Agent cost reduction for code-health runs | 30% token reduction | Haiku vs Sonnet token usage comparison |
| Developer satisfaction with Centinela review quality | > 4/5 in user feedback | GitHub Discussions survey |
| GitHub stars | 300 | GitHub repo star count |

---

### F04 — LSP Integration for Real-Time Code Intelligence

**ID**: F04
**Status**: Planned
**Priority**: P1-High
**Complexity**: Low
**Classification**: Table Stakes

#### Description

Add `.lsp.json` configuration to the project so that agents — particularly Forja during implementation and Centinela during review — receive actual type errors, lint warnings, and language diagnostics rather than relying on heuristic analysis of code structure. The LSP connection surfaces real compiler and type-checker output into the agent's context.

#### Problem Statement

Currently, agents analyze code by reading files and applying heuristics. Forja misses type errors that a type checker would catch immediately. Centinela flags potential issues that the LSP already knows are valid code. Real diagnostic data would make both agents more accurate and reduce false positives in reviews, building developer trust in the system.

#### User Stories

As Forja implementing a TypeScript feature, I want to see actual TypeScript compiler errors in my context rather than inferring type issues from reading the code, so that I fix real errors rather than hypothetical ones.

As Centinela reviewing code, I want to know which code has active lint warnings from the project's configured linter, so that my review findings are anchored in real diagnostic data rather than heuristic analysis.

#### Acceptance Criteria

GIVEN a project with a TypeScript or Python codebase and an LSP server configured,
WHEN Forja edits a file that introduces a type error,
THEN Forja's context includes the LSP diagnostic message (error code, location, description) before the TIME OUT checklist runs.

GIVEN `.lsp.json` exists in the project root,
WHEN Centinela runs a code review,
THEN Centinela's context includes the current list of active LSP warnings and errors for the files in scope before the review begins.

GIVEN a project has no LSP configuration,
WHEN an agent runs,
THEN the agent proceeds normally with a single informational note that LSP diagnostics are unavailable, and no error is raised.

#### Business Rules

- LSP configuration is per-project (`.lsp.json` in project root). It is not a global plugin setting.
- Supported LSP servers in v1: `typescript-language-server`, `pylsp`, `rust-analyzer`. Additional servers are documented as community-contributed configurations.
- LSP diagnostics are injected into agent context as a structured block, not inline with code — they do not replace code reading, they supplement it.

#### Dependencies

- None

---

### F05 — Security Scanner Hook (Pre-Commit)

**ID**: F05
**Status**: Planned
**Priority**: P1-High
**Complexity**: Low
**Classification**: Table Stakes

#### Description

A `PreToolUse` hook scans every file write and edit operation for hardcoded secrets, SQL injection patterns, XSS vectors, and unsafe `eval` usage. If a pattern is detected, the hook blocks the operation and provides an explanation of the detected risk with a suggested remediation. Findings are logged to Centinela's audit trail for inclusion in the next security review.

#### Problem Statement

Security issues are currently caught only during periodic Centinela audits, which run after code has already been written and potentially committed. Pre-commit detection closes the gap between introduction and detection, reducing the cost of remediation and preventing secrets from entering version control. The Security Guidance plugin on the Claude Code marketplace has 25,500+ installs — this is a proven category with demonstrated demand.

#### User Stories

As Forja writing code, I want hardcoded secrets and injection vulnerabilities to be flagged at the moment of file write rather than during a later audit, so that I fix issues before they enter the codebase.

As a developer using Agent Triforce, I want the system to prevent secrets from being committed, so that I do not accidentally expose API keys or credentials even when working quickly.

#### Acceptance Criteria

GIVEN Forja writes a file containing a string matching a known secret pattern (e.g., `sk-`, `AKIA`, `ghp_`, hardcoded password assignments),
WHEN the `PreToolUse` hook fires on the file write,
THEN the write is blocked, a description of the detected pattern is returned to the agent, and the finding is appended to `docs/reviews/security-audit-trail.md`.

GIVEN Forja writes SQL code containing string concatenation in a query context,
WHEN the `PreToolUse` hook fires,
THEN the hook flags the pattern as a potential SQL injection risk and blocks the write, with a note explaining parameterized query alternatives.

GIVEN a file write contains no security-sensitive patterns,
WHEN the `PreToolUse` hook fires,
THEN the hook completes in under 100ms and does not block the operation.

GIVEN the security scanner flags a false positive on a test fixture file,
WHEN the developer adds the file path to `.agentignore`,
THEN subsequent writes to that file are not scanned by the security hook.

#### Business Rules

- The scanner must not have false positive rates above 5% on standard application code. Patterns must be validated against common codebases before release.
- Secret detection patterns are maintained in a versioned configuration file (`src/security/patterns.json`) so they can be updated without changing agent code.
- The audit trail file (`docs/reviews/security-audit-trail.md`) is append-only. Entries are never deleted, only acknowledged.
- `.agentignore` allows developers to exclude test fixtures, mock data files, and generated files from scanning. It follows `.gitignore` syntax.

#### Dependencies

- None (can be delivered independently)

---

### F06 — Static Analysis MCP Integration

**ID**: F06
**Status**: Planned
**Priority**: P1-High
**Complexity**: Low
**Classification**: Differentiator

#### Description

MCP server configuration files that connect Centinela to SonarQube, CodeScene, or similar static analysis tools. The MCP server pulls real code quality metrics, tech debt hotspots, complexity scores, and security vulnerability data into Centinela's review process. Centinela's findings are anchored in quantitative data rather than heuristic pattern matching.

#### Problem Statement

Centinela's current code reviews are qualitative — pattern-based observations without quantitative grounding. "This function is complex" is less actionable than "cyclomatic complexity 24, SonarQube Critical vulnerability in line 87." Static analysis tools already generate this data; Agent Triforce needs a bridge to consume it. When combined with the checklist methodology, evidence-based reviews become the differentiator versus competitors who also have review agents but no data pipeline.

#### User Stories

As Centinela performing a code review, I want SonarQube vulnerability data and complexity metrics available in my context, so that my findings are specific, quantified, and prioritized by severity rather than based on code reading alone.

As a developer receiving a Centinela review, I want to know the actual complexity score and open SonarQube issues for each finding, so that I can prioritize fixes by evidence rather than reviewer judgment.

#### Acceptance Criteria

GIVEN a project has a SonarQube instance configured in `.mcp.json`,
WHEN Centinela begins a `/security-audit` or `/code-health` workflow,
THEN Centinela's context includes: open vulnerabilities by severity, code duplication percentage, cyclomatic complexity for the top 10 most complex functions, and tech debt estimate in hours.

GIVEN the MCP server connection is unavailable,
WHEN Centinela runs,
THEN the agent proceeds with heuristic review and includes a note in the findings that static analysis data was unavailable, with no blocking error.

GIVEN SonarQube returns a Critical or Blocker severity vulnerability,
WHEN Centinela incorporates this into the review,
THEN the finding is elevated to the top of the findings list in the review document regardless of the overall review order.

#### Business Rules

- Supported integrations in v1: SonarQube (self-hosted and SonarCloud), CodeScene. Integration with additional tools is documented for community contribution.
- MCP configuration is per-project. No global configuration that applies to all projects.
- SonarQube credentials are never stored in any Agent Triforce configuration file. They are environment variables only.
- The MCP connection is read-only. Agent Triforce never writes to SonarQube.

#### Dependencies

- F03 (Interactive Setup Wizard) — MCP server configuration is offered as a step in the setup wizard.

---

### F07 — Workflow Visualization and Progress Tracking

**ID**: F07
**Status**: Planned
**Priority**: P1-High
**Complexity**: Medium
**Classification**: Differentiator

#### Description

A dashboard (terminal output or markdown-rendered file) that shows the current workflow stage, which pause point the system is at (SIGN IN / TIME OUT / SIGN OUT), which checklists have passed or failed, which agent is active, and what is blocking progress. The methodology becomes visible and auditable rather than implicit.

#### Problem Statement

The WHO Surgical Safety Checklist's documented success relies in part on visibility — the checklist is read aloud, everyone in the room confirms, everyone can see what was checked and what was not. In Agent Triforce's current state, the methodology is invisible: agents run their checklists internally and the user has no view into what was verified, skipped, or blocked. A visible workflow state makes the discipline tangible, buildable, and debuggable. It is also the strongest demonstration tool for the "methodology-first" positioning strategy.

#### User Stories

As a developer running a PM-to-Dev-to-QA workflow, I want to see which phase the system is currently in and which checklists have passed, so that I know the current state without reading agent logs.

As an engineering team lead evaluating Agent Triforce, I want to see a visual representation of the checklist methodology in action, so that I can demonstrate the discipline of the system to my team and stakeholders.

#### Acceptance Criteria

GIVEN a workflow is in progress,
WHEN the developer runs `/status`,
THEN a rendered view is displayed showing: current active agent, current phase (SIGN IN / in-progress / TIME OUT / SIGN OUT), checklist items completed vs pending for the current phase, and the most recent handoff artifact summary.

GIVEN a checklist item fails (a required field is empty, an assumption is undocumented),
WHEN the TIME OUT pause point is reached,
THEN the dashboard shows the specific failing item highlighted, and the workflow is blocked until the item is resolved.

GIVEN a complete workflow run (PM spec to Dev implementation to QA review) completes,
WHEN the developer views the workflow history,
THEN a summary shows all three agents' checklist pass/fail records, timestamps for each phase transition, and a list of all open questions that were logged during the run.

#### Business Rules

- The dashboard must be renderable in a standard terminal (ANSI color codes acceptable, no external GUI dependencies required).
- Checklist state is persisted to `docs/workflow-state.json` so it survives session interruptions. A workflow can be resumed.
- The `/status` command is non-destructive — it only reads state, never modifies it.

#### Dependencies

- F02 (Automated Handoff Protocol) — workflow state is updated from handoff artifacts.

---

### F08 — Automated Test Generation Skill (`/generate-tests`)

**ID**: F08
**Status**: Planned
**Priority**: P1-High
**Complexity**: Low-Medium
**Classification**: Table Stakes

#### Description

A new skill `/generate-tests [module-or-function]` that analyzes a module or function and generates test cases following FIRST principles (Fast, Isolated, Repeatable, Self-validating, Timely) and the Arrange-Act-Assert pattern. The skill integrates with Forja's TDD workflow: generated tests can be run immediately as the "Red" phase of Red-Green-Refactor.

#### Problem Statement

81% of development teams report using AI assistance in testing, yet no dedicated test generation skill exists in Agent Triforce. Forja generates tests during implementation but without a dedicated skill, the quality and coverage are inconsistent. A dedicated skill with explicit FIRST principles and AAA structure elevates test generation from "code that runs" to "tests that prove behavior."

#### User Stories

As Forja implementing a feature in TDD mode, I want to generate failing tests for a function before implementing it, so that I can start the Red phase of Red-Green-Refactor immediately without writing boilerplate.

As a developer who has existing code without tests, I want to run `/generate-tests` on a module and receive a complete test file following project conventions, so that I can add test coverage to legacy code efficiently.

#### Acceptance Criteria

GIVEN a developer runs `/generate-tests src/auth/token.py`,
WHEN the skill analyzes the file,
THEN a test file is generated at `tests/auth/test_token.py` containing: at minimum one test per public function, one happy-path test and one edge-case test per function, all tests following Arrange-Act-Assert structure, all tests passing FIRST principles (no network calls, no file system dependencies in unit tests unless explicitly testing I/O).

GIVEN a function has complex business logic with multiple branches,
WHEN `/generate-tests` is run for that function,
THEN tests are generated for each identified branch, and a comment in the test file lists any branches that could not be automatically inferred and require manual test authoring.

GIVEN the project uses pytest (Python) or Vitest (TypeScript),
WHEN tests are generated,
THEN the generated tests use the framework idioms (pytest fixtures, `describe`/`it` blocks) and can be executed by running the standard test command without modification.

#### Business Rules

- Generated tests are a starting point, not production-ready coverage. The skill adds a comment header noting that generated tests require human review before merge.
- The skill does not generate tests for private functions (prefixed with `_` in Python, not exported in TypeScript). Behavior is configurable.
- Test generation must not produce tests with hardcoded expected values from implementation code — tests must be based on spec or docstring, not on reading the implementation output.

#### Dependencies

- None (independent skill)

---

### F09 — Smart Agent Routing (Model Selection)

**ID**: F09
**Status**: Planned
**Priority**: P1-High
**Complexity**: Low-Medium
**Classification**: Table Stakes

#### Description

Configuration that assigns different Claude models to different agents and task types. Haiku for code-health scans, Sonnet for standard implementation, Opus for complex architecture decisions and multi-phase features. Includes cost estimate preview before running a workflow, so developers can make informed choices about model selection per run.

#### Problem Statement

Cost is the number-one complaint from Claude Code power users. All agents currently use the same model (the user's default), which is wasteful for routine tasks. A code-health scan that could run on Haiku is running on Opus. This represents a 15-20x cost premium for work that does not require frontier-model reasoning. Smart routing makes Agent Triforce cost-efficient for daily use.

#### User Stories

As a developer running daily code-health checks, I want them to automatically use a cost-efficient model, so that I am not spending frontier-model tokens on routine linting and dead code analysis.

As a developer starting a complex multi-phase feature, I want the PM and QA agents to use a high-capability model, so that specs are thorough and security reviews are comprehensive even at higher token cost.

As a developer, before running a workflow, I want to see a cost estimate, so that I can decide whether to proceed with the current model configuration or adjust it.

#### Acceptance Criteria

GIVEN an agent routing configuration exists (`.agent-routing.json`),
WHEN `/code-health` is invoked,
THEN Centinela uses the model configured for `code-health` tasks (default: Haiku) rather than the global default model.

GIVEN a developer runs a multi-phase Tier L feature workflow,
WHEN the workflow starts,
THEN a cost estimate is displayed (e.g., "Estimated: $0.08-$0.15 based on Haiku for code-health, Sonnet for implementation") before any agent is invoked, and the user confirms before proceeding.

GIVEN a developer overrides the model for a single run with `--model opus`,
WHEN the workflow executes,
THEN that specific run uses Opus regardless of the routing configuration, and the actual token usage is logged after completion.

#### Business Rules

- Model routing is defined in `.agent-routing.json` at the project root. Default configuration is provided by the setup wizard (F03).
- The cost estimate is an estimate only. Actual token usage varies. The estimate uses average token counts from benchmark runs, not real-time prediction.
- If the configured model for a task is not available in the user's Claude plan, the system falls back to the user's plan's most capable available model and notifies the user.

#### Dependencies

- F03 (Interactive Setup Wizard) — routing configuration is offered during setup.

---

## Phase 3 — P2: Medium Priority

**Theme**: Deepen the integration of Agent Triforce with the broader development ecosystem (CI/CD, issue trackers, static analysis) and close gaps in the system's ability to enforce its own discipline (approval gates, release readiness, memory consistency).

**Success Metrics for Phase 2 Completion / Phase 3 Entry**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Security issues caught pre-commit (F05) | > 80% catch rate | Security hook hit rate vs post-commit findings |
| GitHub Actions integration adoption | 20% of installs use CI template | GitHub Actions template usage tracking |
| Memory conflict detection accuracy | < 5% false positives | Manual audit of conflict detections vs actual conflicts |
| GitHub stars | 750 | GitHub repo star count |

---

### F10 — Plan Approval Gates Between Agents

**ID**: F10
**Status**: Planned
**Priority**: P2-Medium
**Complexity**: Medium
**Classification**: Differentiator

#### Description

Formal approval gates between Prometeo and Forja, and between Forja and Centinela. Before Forja begins coding, Prometeo reviews and approves the implementation plan. Before Centinela signs off on a release, a structured quality gate checklist must pass. Gates use Claude Code hooks to enforce the workflow. No agent can advance to the next phase without documented gate passage.

#### Problem Statement

Currently there is no formal barrier between spec approval and implementation start. Forja can begin implementation before Prometeo has reviewed whether the approach aligns with the spec. This is the software equivalent of a surgeon skipping the SIGN IN checklist because they are confident in the procedure. The gate is most valuable when experienced practitioners skip it — which they will, under pressure.

#### User Stories

As Prometeo, I want to review Forja's implementation plan before coding begins, so that I can catch architectural misalignments with the spec before they are baked into code.

As an engineering team lead, I want documented evidence that approval gates were passed for each feature, so that I have an audit trail of when specs were approved and by whom.

#### Acceptance Criteria

GIVEN Forja has written an implementation plan for a feature,
WHEN Forja reaches the SIGN OUT checkpoint before coding,
THEN a gate document is generated at `docs/gates/{feature-name}-plan-gate.md` and Prometeo's approval is required (either automated via criteria check or manual confirmation) before Forja proceeds to implementation.

GIVEN Centinela has completed a review and all blocker findings are resolved,
WHEN Centinela's SIGN OUT runs,
THEN a gate document is generated at `docs/gates/{feature-name}-release-gate.md` summarizing passing criteria and the go/no-go decision.

GIVEN a required gate approval has not been completed,
WHEN an agent attempts to advance to the next phase,
THEN the hook blocks the advancement and returns the gate document path with outstanding items listed.

#### Business Rules

- Gate documents are permanent artifacts (not `.gitignore`d). They are the audit trail.
- In an automated pipeline (F01 Agent Teams), gates can be auto-approved if all criteria are met and the user has enabled auto-approve mode. Auto-approve mode is disabled by default.
- A gate can be force-overridden by the developer with an explicit `--override-gate` flag and a required reason string. The override is logged in the gate document.

#### Dependencies

- F02 (Automated Handoff Protocol) — gate documents extend the handoff artifact format.
- F07 (Workflow Visualization) — gates are displayed in the workflow dashboard.

---

### F11 — Release Readiness Report Generator

**ID**: F11
**Status**: Planned
**Priority**: P2-Medium
**Complexity**: Low-Medium
**Classification**: Differentiator

#### Description

Enhance `/release-check` to produce a comprehensive structured release readiness report. The report covers: test coverage percentage, security audit status, open tech debt items, CHANGELOG completeness, dependency freshness (outdated packages), and open issues. Outputs a go/no-go recommendation with a confidence score and specific blockers listed.

#### Problem Statement

The current `/release-check` skill is basic — it runs a checklist but produces a qualitative report. Engineering teams and engineering managers need an actionable, structured release gate document with specific pass/fail criteria, not a qualitative summary. A checklist-verified release gate is a direct product expression of the core methodology and a selling point for enterprise adoption.

#### User Stories

As a developer preparing a release, I want a structured report showing exactly which criteria pass and which fail before I tag a release, so that I do not ship with known blockers.

As an engineering manager, I want a documented go/no-go report with a confidence score for each release, so that I have a paper trail for release decisions and can improve the process over time.

#### Acceptance Criteria

GIVEN a developer runs `/release-check`,
WHEN the report generates,
THEN it includes: test coverage percentage (pass if > 80%), security scanner status (pass if no Critical/High open findings), CHANGELOG entry for the current version (pass if entry exists), dependency freshness (pass if no Critical CVEs in dependencies), open tech debt severity (pass if no P0/P1 items in TECH_DEBT.md).

GIVEN all criteria pass,
WHEN the report generates,
THEN the report includes a GO recommendation with confidence score (0-100, based on margin above thresholds) and the report is saved to `docs/reviews/release-check-{version}-{date}.md`.

GIVEN one or more criteria fail,
WHEN the report generates,
THEN the report includes a NO-GO recommendation, lists each failing criterion with specific remediation steps, and does not block the developer from releasing (it is advisory, not enforcement, unless gate F10 is active).

#### Business Rules

- The confidence score is calculated as: average of (actual value / threshold value) for all passing criteria, capped at 100. A criterion at 2x its threshold does not contribute more than 100%.
- The report is always saved, regardless of go/no-go result. Reports are append-only — new reports create new files, they do not overwrite previous reports.
- Threshold values are configurable in `.release-config.json`. The defaults from the spec are the recommended starting points.

#### Dependencies

- F05 (Security Scanner Hook) — security scanner status is pulled from the audit trail.
- F10 (Plan Approval Gates) — if gates are active, gate status is included in the report.

---

### F12 — GitHub Actions / CI-CD Integration

**ID**: F12
**Status**: Planned
**Priority**: P2-Medium
**Complexity**: Low-Medium
**Classification**: Table Stakes

#### Description

GitHub Actions workflow templates that run Agent Triforce agents in CI pipelines. Includes: Centinela running automated PR security review on every pull request, `/security-audit` on push to main, `/release-check` before deploy. Templates are provided in `docs/ci-templates/` and can be copied into `.github/workflows/`.

#### Problem Statement

Agents currently run only locally. There is no CI/CD integration, which means security audits and release checks can be skipped when developers are under deadline pressure. Moving Centinela into CI makes the quality gate non-optional for teams using GitHub Actions. Enterprise adoption requires CI integration — it is a table stakes requirement for teams with compliance obligations.

#### User Stories

As an engineering team lead, I want Centinela to automatically review every pull request for security issues and code quality, so that quality gates are enforced by CI rather than requiring manual invocation.

As a developer with a CI pipeline, I want the release check to run automatically before deployment, so that a deploy with a failing security audit is blocked at the pipeline level.

#### Acceptance Criteria

GIVEN a project has the Centinela PR review workflow template installed,
WHEN a pull request is opened or updated,
THEN a GitHub Actions workflow runs Centinela on the changed files and posts the findings as a PR comment within 5 minutes.

GIVEN the Centinela review finds a Critical or High severity security issue,
WHEN the PR review workflow completes,
THEN the GitHub Actions check fails (non-zero exit code), blocking merge until the finding is resolved or explicitly acknowledged by an authorized reviewer.

GIVEN a project has the release check workflow template installed,
WHEN a release tag is pushed,
THEN the `/release-check` workflow runs and its go/no-go result is attached to the release as a workflow summary.

#### Business Rules

- Workflow templates are provided as-is and require manual installation by the developer. They are not auto-installed.
- The CI workflow runs Centinela with a reduced context window (`--mode ci`) that skips non-essential checklist items to reduce token cost in CI.
- CI runs must complete within 5 minutes for PR review and 10 minutes for release check. If these limits are exceeded, the workflow times out with a warning (not a failure).

#### Dependencies

- F05 (Security Scanner Hook) — security patterns used in CI are the same as the pre-commit hook patterns.
- F09 (Smart Agent Routing) — CI runs default to Haiku to control costs.

---

### F13 — Linear / Jira / GitHub Issues MCP Integration

**ID**: F13
**Status**: Planned
**Priority**: P2-Medium
**Complexity**: Low
**Classification**: Table Stakes

#### Description

MCP server configuration files connecting agents to popular issue trackers. Prometeo pulls ticket details into spec creation. Forja updates ticket status during implementation. Centinela links review findings to open issues. Supports Linear, Jira, and GitHub Issues via MCP server configurations.

#### Problem Statement

Agent Triforce currently operates without awareness of the project management context. Prometeo writes specs without knowing which issues are blocking or what the sprint priority is. Forja implements without updating ticket status. Centinela files findings into review documents but not into the team's issue tracker where they will be actioned. The disconnect reduces adoption in team environments where issue trackers are the source of truth.

#### User Stories

As Prometeo writing a feature spec, I want to pull the relevant Linear ticket description and acceptance criteria into the spec automatically, so that the spec reflects the stakeholder-defined requirements without manual copy-paste.

As Forja implementing a feature, I want to update the Linear/Jira ticket status to "In Progress" and "Done" as I work, so that the team's project board reflects actual implementation status without manual updates.

#### Acceptance Criteria

GIVEN a Linear MCP server is configured and a ticket ID is provided to `/feature-spec`,
WHEN Prometeo begins spec creation,
THEN the ticket's title, description, and labels are pulled from Linear and pre-populated into the spec template before the PM agent begins work.

GIVEN Forja completes implementation and runs SIGN OUT,
WHEN the GitHub Issues MCP is configured,
THEN the associated issue is updated with a comment linking to the implementation commit and the status is moved to the configured "done" state.

GIVEN Centinela finds a High or Critical issue during review,
WHEN the issue tracker MCP is configured,
THEN Centinela creates a new issue in the tracker with the finding title, description, severity, and a link to the review document.

GIVEN no issue tracker MCP is configured,
WHEN any agent runs,
THEN agents proceed normally with no error. Issue tracker integration is fully optional.

#### Business Rules

- Each issue tracker is configured independently. Linear, Jira, and GitHub Issues can be configured simultaneously.
- The MCP integration is read-write for status updates and issue creation, but read-only for ticket content (agents do not modify original ticket descriptions).
- Issue creation from Centinela findings is opt-in per run. The default is to not auto-create issues to avoid flooding the tracker with duplicate findings.

#### Dependencies

- F03 (Interactive Setup Wizard) — issue tracker MCP configuration is offered during setup.

---

### F14 — Cross-Agent Persistent Memory with Conflict Detection

**ID**: F14
**Status**: Planned
**Priority**: P2-Medium
**Complexity**: Medium
**Classification**: Differentiator

#### Description

Structured memory entries (timestamped, categorized, source-referenced) with cross-agent memory synchronization. A conflict detection mechanism identifies when agents hold contradictory observations: Prometeo categorizing a feature as "simple" while Centinela has flagged the same component as "high risk." Conflicts surface in the next workflow run for explicit resolution.

#### Problem Statement

Each agent maintains its own `MEMORY.md` file with no awareness of what other agents have recorded. This creates the possibility of misaligned assumptions that persist across sessions. A PM who believes a module is stable may spec features that Centinela knows are fragile from prior review. No other multi-agent plugin has cross-agent memory awareness. Memory conflicts are the source of "everyone thought someone else was handling it" failures — a classic ineptitude failure that Gawande's checklist research directly addresses.

#### User Stories

As Prometeo writing a spec for a module that Centinela has previously flagged as fragile, I want to see the conflict between my "new feature" plan and Centinela's "high risk" assessment before I finalize the spec, so that I can either address the risk or make an explicit decision to proceed with awareness of it.

As a developer, I want a single view of what all three agents know about a component, so that I can see whether their assessments are aligned or whether there are unresolved disagreements.

#### Acceptance Criteria

GIVEN Prometeo records "auth module: stable, no known issues" in its MEMORY.md,
WHEN Centinela has a conflicting entry "auth module: critical vulnerability found 2026-02-15, pending fix",
THEN the next time any agent references the auth module, the conflict is surfaced in the agent's context as a flagged item requiring resolution before proceeding.

GIVEN a conflict between agent memory entries is detected,
WHEN the conflict is surfaced,
THEN it includes: agent A's entry (with timestamp and source), agent B's conflicting entry (with timestamp and source), and three resolution options: accept A, accept B, or mark as "under investigation" with a note.

GIVEN a developer resolves a conflict by accepting one entry,
WHEN the resolution is saved,
THEN the losing entry is archived (not deleted) in a `memory-archive/` directory with a note referencing the resolution decision.

#### Business Rules

- Conflict detection runs automatically at the start of every agent SIGN IN. It is not a separate command.
- A conflict exists when two agents reference the same entity (module, feature, component) with incompatible assessments (e.g., "stable" vs "high risk," "complete" vs "in progress").
- Entity matching uses keyword matching against a configurable entity glossary, not semantic embedding. The v1 implementation is intentionally simple to avoid over-engineering.
- Unresolved conflicts do not block workflow execution. They are surfaced as warnings, not errors, in v1.

#### Dependencies

- F07 (Workflow Visualization) — conflicts are visible in the workflow dashboard.

---

### F15 — Checklist Evolution System

**ID**: F15
**Status**: Planned
**Priority**: P2-Medium
**Complexity**: Medium-High
**Classification**: Differentiator

#### Description

A mechanism to track checklist effectiveness over time. Records when checklist items catch real issues and when issues slip through without being caught by a checklist. Generates a "checklist health report" analyzing which items are catching issues (high value), which are consistently passing without finding anything (potentially unnecessary or too broad), and which issues recur without a corresponding checklist item (coverage gaps). Produces suggestions for checklist evolution.

#### Problem Statement

CLAUDE.md states explicitly: "Checklists evolve based on actual failures and lessons learned. Update them when they catch something new or miss something important." However, there is no mechanism to actually track this. Boorman's principle — that checklists must be "field-tested and updated" — is written in the system prompt but has no implementation. A checklist system that cannot evolve will accumulate dead items and miss new failure modes. This is the deepest expression of the core methodology on the entire roadmap.

#### User Stories

As a developer using Agent Triforce for 3 months, I want a report showing which checklist items have caught real issues versus which have never triggered, so that I can remove stale items and add items for failure modes I have actually experienced.

As the Agent Triforce maintainer, I want aggregated (anonymized) data on which checklist items are most commonly catching issues across users, so that I can improve the default checklists based on real field data.

#### Acceptance Criteria

GIVEN a checklist item catches a real issue during a workflow run (i.e., an agent reports the item triggered a correction),
WHEN the workflow completes,
THEN the event is logged to `docs/checklist-health/events.jsonl` with: checklist name, item index, description, workflow run ID, timestamp, and whether the finding was confirmed as a real issue.

GIVEN at least 10 workflow runs have been recorded,
WHEN a developer runs `/checklist-health`,
THEN a report is generated showing: hit rate per checklist item (issues caught / opportunities to catch), false positive rate, items with 0 hits in the last 20 runs (candidates for removal or rewording), and issue types that appeared in workflow runs but have no corresponding checklist item.

GIVEN the checklist health report identifies a high-frequency uncovered issue type,
WHEN the report is reviewed,
THEN a suggested new checklist item is generated with wording following Boorman's principles (simple, verifiable, under 10 words), ready for human review and inclusion.

#### Business Rules

- Checklist health data is local by default. Users can opt into anonymized aggregate contribution.
- No checklist item is automatically added or removed. All suggestions require human review and explicit acceptance.
- The system tracks checklist items by ID (each item has a stable ID), not by text. Rewording an item preserves its history; adding a new item starts a fresh history.
- Checklist health events are appended to `docs/checklist-health/events.jsonl`. This file is never modified after write — only appended to.

#### Dependencies

- F07 (Workflow Visualization) — checklist state tracking (which items ran, which triggered findings) feeds into the evolution system.

---

## Phase 4 — P3: Future

**Theme**: High-complexity capabilities that make Agent Triforce a compliance-grade, cost-optimized, and training-ready system for enterprise and regulated-industry use cases.

**Success Metrics for Phase 3 Completion / Phase 4 Entry**

| Metric | Target | Measurement |
|--------|--------|-------------|
| CI-CD integration adoption | 30% of installs | GitHub Actions template usage |
| Release check go/no-go accuracy | > 90% (no GO-recommended releases fail) | Post-release incident tracking |
| Issue tracker integration adoption | 25% of team installs | MCP config presence in forks |
| GitHub stars | 1,500 | GitHub repo star count |

---

### F16 — Live Dashboard with Session Analytics

**ID**: F16
**Status**: Planned
**Priority**: P3-Low
**Complexity**: Medium-High
**Classification**: Differentiator

#### Description

A real-time session analytics dashboard displaying: tokens consumed per agent, handoff count for the current session, checklist pass/fail rates, time-to-completion per phase, and estimated cost for the session. Available as both a terminal output and an exportable JSON report for integration with team cost-tracking tools.

#### Problem Statement

There is no visibility into agent performance, resource consumption, or cost across workflow runs. Developers and team leads cannot answer "how much does running a full PM-Dev-QA cycle cost?" or "which agent consumes the most tokens?" without manual tracking. For enterprise adoption, cost accountability and performance tracking are non-negotiable.

#### User Stories

As a developer running multiple features per day, I want to see the total token cost and time spent for each workflow session, so that I can understand and optimize my AI development costs.

As an engineering manager, I want monthly session analytics showing which types of workflows (full PM-Dev-QA vs code-health vs security audit) consume the most resources, so that I can make informed decisions about when to use each workflow type.

#### Acceptance Criteria

GIVEN a workflow run completes,
WHEN the developer views the session report,
THEN the report includes: tokens per agent (prompt + completion), estimated cost in USD (at published API rates), total time from first SIGN IN to final SIGN OUT, number of checklists run, and number of findings logged.

GIVEN a workflow is in progress,
WHEN the developer runs `/status`,
THEN the dashboard shows the running totals for tokens and estimated cost for the current session alongside workflow state (F07).

GIVEN a developer exports session analytics,
WHEN the export runs,
THEN a `docs/analytics/session-{date}.json` file is generated in a documented schema that can be imported into cost-tracking tools.

#### Business Rules

- Cost estimates use current published API pricing from Anthropic. A `pricing.json` configuration file allows users to update prices without upgrading the plugin.
- Token counts are approximate for sessions where the exact prompt is not recoverable. Approximation methodology is documented and consistent.
- Session data is local only. No telemetry is sent externally.

#### Dependencies

- F07 (Workflow Visualization) — the dashboard extends F07's status display with analytics data.
- F09 (Smart Agent Routing) — cost estimates are per-model and require routing configuration.

---

### F17 — Spec-to-Implementation Traceability Matrix

**ID**: F17
**Status**: Planned
**Priority**: P3-Low
**Complexity**: Medium-High
**Classification**: Differentiator

#### Description

Auto-generate a traceability matrix linking every acceptance criterion in a Prometeo spec to the implementation files in Forja, the test cases that verify each criterion, and the Centinela review findings relevant to each criterion. The matrix updates automatically each workflow cycle. Regulated industries (healthcare, fintech, defense) require this for compliance audits.

#### Problem Statement

CLAUDE.md references IEEE 830 traceability as a software engineering principle, but there is no automation for it. Traceability is currently manual: a developer looking at a Centinela finding must manually trace it back to the spec criterion it violates. For regulated industries, this manual tracing is both error-prone and inadequate for audit. The traceability matrix turns Agent Triforce into a compliance tool — a significantly higher-value category than a developer productivity tool.

#### User Stories

As a developer with a compliance audit, I want a traceability matrix showing which test covers which acceptance criterion from the spec, so that I can demonstrate complete requirements coverage without manually cross-referencing documents.

As Centinela finding a security vulnerability, I want to link my finding to the specific acceptance criterion it violates, so that the developer knows exactly which spec requirement needs to be revisited.

#### Acceptance Criteria

GIVEN a feature has a spec with numbered acceptance criteria and Forja has implemented it,
WHEN the traceability matrix is generated,
THEN a document exists at `docs/traceability/{feature-name}-matrix.md` with columns: Criterion ID, Criterion Text (from spec), Implementation File(s), Test Case(s), Review Finding(s), Status (covered/partial/missing).

GIVEN Centinela logs a finding during review,
WHEN the finding references a spec criterion,
THEN the traceability matrix is updated to reflect the finding in the Review Finding column for that criterion.

GIVEN an acceptance criterion has no corresponding test case,
WHEN the traceability matrix generates,
THEN the criterion row is flagged with Status: "missing" and a note that `/generate-tests` (F08) can be run to address the gap.

#### Business Rules

- Criterion IDs are assigned by Prometeo at spec creation time and are stable across the feature's lifecycle. They are in the format `{feature-id}-AC-{NNN}`.
- The traceability matrix is a derived document — it is generated from spec, implementation, tests, and review artifacts. It is never edited manually.
- If no spec exists for an implementation (code without a spec), the traceability matrix generates with a warning row noting the missing spec.

#### Dependencies

- F02 (Automated Handoff Protocol) — handoff artifacts include criterion-level references.
- F08 (Automated Test Generation) — test cases need stable IDs for the matrix.
- F10 (Plan Approval Gates) — gate documents reference criterion IDs.

---

### F18 — Context-Efficient Agent Spawning

**ID**: F18
**Status**: Planned
**Priority**: P3-Low
**Complexity**: Medium
**Classification**: Differentiator

#### Description

Progressive context loading for agent spawn prompts. Instead of loading the full system prompt, CLAUDE.md, and all MEMORY.md content on every agent invocation, the spawning mechanism loads a minimal base prompt and then selectively loads only the sections of memory, specs, and docs relevant to the specific task. Estimated 30-50% token reduction for routine tasks (code-health, small bug fixes).

#### Problem Statement

Every agent invocation currently loads the full agent system prompt (which is large), the full CLAUDE.md, and the full MEMORY.md. For a routine code-health scan, 90% of this context is irrelevant. This represents a significant and avoidable token cost that accumulates across daily use. It also means larger projects with extensive MEMORY.md and spec history pay an increasing context tax on every invocation, regardless of task scope.

#### User Stories

As a developer running daily code-health scans, I want the scan to load only the context relevant to code health, so that I am not paying for the full PM and feature spec context on every scan.

As a developer on a large project with extensive agent memory, I want context loading to scale gracefully as the project grows, so that the token cost of routine tasks does not grow proportionally with the project's history.

#### Acceptance Criteria

GIVEN a developer runs `/code-health`,
WHEN the agent spawns,
THEN only the Centinela code-health relevant sections are loaded (code review checklist, relevant patterns, tech stack) rather than the full CLAUDE.md and all spec history. Token usage for `/code-health` is reduced by at least 30% versus the baseline (full context load).

GIVEN a developer runs a full Tier L feature spec workflow,
WHEN the workflow spans multiple agents,
THEN each agent loads the specific context relevant to its phase (Prometeo loads existing specs for the feature area; Forja loads the spec and relevant implementation files; Centinela loads the spec, implementation files, and review checklists).

GIVEN context-efficient spawning is active,
WHEN a developer needs to override it and load full context (for debugging or complex cross-cutting concerns),
THEN running the command with `--full-context` loads everything as before, with no behavior change.

#### Business Rules

- Context efficiency must not compromise correctness. If a selective load causes an agent to miss relevant context and produce an incorrect output, that is a bug, not acceptable behavior.
- The baseline for "30% token reduction" is the v1.0 full-context load, measured on a reference project with a defined size (50 files, 3 completed feature specs, 1 month of memory).
- Context selection rules are versioned and tested against known workflows to prevent regressions.

#### Dependencies

- F01 (Agent Team Orchestration Mode) — team mode requires shared context scope, which must be compatible with progressive loading.
- F14 (Cross-Agent Persistent Memory) — the structured memory format (F14) enables selective memory loading for F18.

---

### F19 — Non-Normal Procedure Training Mode (`/simulate-failure`)

**ID**: F19
**Status**: Planned
**Priority**: P3-Low
**Complexity**: Medium
**Classification**: Differentiator

#### Description

A `/simulate-failure` skill that intentionally introduces failure scenarios into a controlled workflow run: an ambiguous spec (to trigger Prometeo's NON-NORMAL: Requirement Ambiguity checklist), a test failure (to trigger Forja's NON-NORMAL recovery), a simulated security vulnerability (to trigger Centinela's NON-NORMAL: Security Finding checklist). Functions as a fire drill for the agent system — verifying that Non-Normal procedures activate correctly and that the methodology is robust under pressure.

#### Problem Statement

CLAUDE.md defines Non-Normal READ-DO checklists for all three agents, but these checklists have never been formally tested. In aviation safety, non-normal procedure proficiency requires regular practice — Boeing's research shows that pilots who practice emergency procedures perform them correctly under stress; those who only read them do not. Agent Triforce's Non-Normal checklists are written but never exercised. The training mode is the only concept on this roadmap derived directly from aviation emergency procedure methodology — no competitor has anything comparable.

#### User Stories

As a developer wanting to verify that Agent Triforce handles ambiguous requirements correctly, I want to run a controlled simulation of a requirement ambiguity scenario, so that I can confirm the agents invoke the Non-Normal Requirement Ambiguity checklist rather than guessing.

As a team lead introducing Agent Triforce to a new team, I want to run a training simulation that exercises all three Non-Normal procedures, so that the team understands what correct non-normal behavior looks like before they encounter a real failure.

#### Acceptance Criteria

GIVEN a developer runs `/simulate-failure --scenario ambiguous-spec`,
WHEN the simulation runs,
THEN Prometeo receives a deliberately ambiguous spec and the system verifies that Prometeo invokes the NON-NORMAL: Requirement Ambiguity checklist (STOP — list ambiguities, document interpretations, assess impact, escalate or document assumption), rather than proceeding with a guess.

GIVEN a developer runs `/simulate-failure --scenario security-finding`,
WHEN the simulation runs,
THEN Centinela encounters a simulated vulnerability and the system verifies that Centinela invokes the NON-NORMAL procedure (document vulnerability before attempting fix), produces the correct severity classification, and escalates with the correct communication path.

GIVEN a simulation run completes,
WHEN the results are displayed,
THEN each Non-Normal procedure that was invoked is scored as PASS (correct invocation) or FAIL (skipped or incorrect), with a summary report saved to `docs/training/simulation-{date}.md`.

GIVEN a Non-Normal procedure FAILS in simulation,
WHEN the failure is reported,
THEN the report identifies exactly which checklist item was missed and provides the item text so the developer can understand the gap.

#### Business Rules

- Simulation scenarios never modify production files, specs, or reviews. All simulation artifacts are written to a `docs/training/` directory.
- Simulation mode is clearly labeled in all outputs with "SIMULATION MODE" to prevent confusion with real workflow outputs.
- Available scenarios in v1: `ambiguous-spec`, `failing-tests`, `security-finding`. Additional scenarios are documented as community-contributed.

#### Dependencies

- F02 (Automated Handoff Protocol) — simulations generate handoff artifacts in the same format as real workflows to verify compatibility.
- F07 (Workflow Visualization) — simulation results are displayed in the workflow dashboard.

---

### F20 — Codebase Knowledge Index

**ID**: F20
**Status**: Planned
**Priority**: P3-Low
**Complexity**: High
**Classification**: Differentiator

#### Description

A lightweight, persistent codebase map that is a shared artifact across all three agents. Contains: module structure, key public functions with signatures and docstrings, inter-module dependency graph, architecture patterns (identified from directory structure and naming conventions), and known hotspots (files flagged by Centinela or marked in TECH_DEBT.md). Similar in concept to Aider's Repository Map, but shared across all three agents and integrated with the Agent Triforce memory system.

#### Problem Statement

Each agent independently rediscovers the codebase on every invocation by reading files. Forja re-analyzes the module structure before every implementation. Centinela re-maps the dependency graph before every review. Prometeo writes specs without a precise map of what already exists. This is not only a token cost problem — it is a consistency problem. Three independent codedbase analyses will diverge. The Codebase Knowledge Index is the single source of truth that all agents share, eliminating the biggest efficiency gap in multi-agent systems (independently identified as the top complaint about AI coding tools).

#### User Stories

As Forja implementing a feature in a large codebase, I want a pre-built map of the module structure and key function signatures available in my context, so that I can navigate the codebase without spending tokens re-reading files I have already analyzed.

As Centinela performing a security review, I want a dependency graph of the module under review already computed, so that I can identify which components are affected by a vulnerability without manually tracing imports.

#### Acceptance Criteria

GIVEN a developer runs `/setup` or `/reindex` on a project,
WHEN the index build completes,
THEN a `docs/codebase-index.json` file exists containing: all modules with their file paths, exported functions/classes with signatures, inter-module dependency edges, and files flagged in TECH_DEBT.md.

GIVEN the codebase index exists,
WHEN any agent spawns,
THEN the index summary (module list and high-level structure, not full signatures) is included in the agent's context by default. Full signature detail is loaded only for the modules relevant to the current task.

GIVEN a file is edited by Forja,
WHEN the edit completes,
THEN the codebase index entry for that file is updated automatically (incremental update, not full rebuild).

GIVEN the codebase index is stale (last updated > 24 hours ago or > 50 file changes since last update),
WHEN an agent spawns,
THEN the agent receives a warning that the index may be stale and is offered the option to run `/reindex` before proceeding.

#### Business Rules

- Index build time must not exceed 60 seconds for codebases up to 500 files. Above 500 files, an incremental build mode is used.
- The index is stored in `docs/codebase-index.json`. It is committed to version control by default (so team members share the index), but can be gitignored.
- The index does not store file contents — only structure, signatures, and metadata. It is safe to commit.
- Index format is versioned. A version mismatch between the index and the current Agent Triforce version triggers a rebuild prompt.

#### Dependencies

- F18 (Context-Efficient Agent Spawning) — the index is the primary mechanism for selective context loading in F18.
- F14 (Cross-Agent Persistent Memory) — the index complements agent memory; memory holds decisions and observations, the index holds structural facts.

---

## Dependency Graph

The following table shows which features are prerequisites for other features. A feature should not be scheduled until all its dependencies are complete.

```
F01 (Agent Team Orchestration)
  └── F18 (Context-Efficient Spawning) [must be compatible]

F02 (Automated Handoff Protocol)
  ├── F07 (Workflow Visualization) [consumes handoff artifacts]
  ├── F10 (Plan Approval Gates) [extends handoff format]
  ├── F17 (Traceability Matrix) [references handoff artifact fields]
  └── F19 (Simulation Mode) [generates handoff artifacts to verify compatibility]

F03 (Setup Wizard)
  ├── F06 (Static Analysis MCP) [offered during setup]
  ├── F09 (Smart Agent Routing) [routing config created during setup]
  └── F13 (Issue Tracker MCP) [offered during setup]

F05 (Security Scanner Hook)
  ├── F11 (Release Readiness Report) [pulls from security audit trail]
  └── F12 (GitHub Actions CI) [same pattern library used in CI]

F07 (Workflow Visualization)
  ├── F10 (Plan Approval Gates) [gates displayed in dashboard]
  ├── F14 (Cross-Agent Memory) [conflicts displayed in dashboard]
  ├── F15 (Checklist Evolution) [checklist state feeds evolution tracking]
  ├── F16 (Live Dashboard Analytics) [extends F07 display]
  └── F19 (Simulation Mode) [simulation results displayed in dashboard]

F08 (Automated Test Generation)
  └── F17 (Traceability Matrix) [test IDs needed for matrix]

F09 (Smart Agent Routing)
  ├── F12 (GitHub Actions CI) [CI defaults to Haiku via routing]
  └── F16 (Live Dashboard Analytics) [cost estimates per model]

F10 (Plan Approval Gates)
  └── F11 (Release Readiness Report) [gate status included in report]
  └── F17 (Traceability Matrix) [gates reference criterion IDs]

F14 (Cross-Agent Memory)
  └── F18 (Context-Efficient Spawning) [structured memory enables selective loading]

F18 (Context-Efficient Spawning)
  └── F20 (Codebase Knowledge Index) [index is the primary selective context mechanism]
```

**Critical path for Phase 1**: F03 → F01 → F02 (setup enables orchestration; orchestration enables automated handoffs).

**Critical path for Phase 2**: F05 → F12 (security scanner patterns are reused in CI); F09 → F16 (routing config enables cost analytics).

**Critical path for Phase 3-4**: F07 → F15 → F16 (workflow visibility enables evolution tracking enables analytics).

---

## Competitive Landscape

### Current State (2026-02-23)

| Feature Category | wshobson/agents (73 plugins) | michael-harris (126 agents) | Agent Triforce |
|-----------------|-------------------------------|------------------------------|----------------|
| PM / Dev / QA role separation | Partial (some role-specialized agents) | Partial (role agents exist) | Full (Prometeo/Forja/Centinela) |
| Checklist methodology | None | None | WHO Surgical Safety model (24 checklists, 117 items) |
| Cross-session agent memory | None documented | None documented | MEMORY.md per agent |
| Handoff protocol | Manual | Manual | Defined (6 paths), manual execution |
| Security pre-commit scanning | Not built-in | Not built-in | Planned (F05) |
| Agent team orchestration | Not documented | Not documented | Planned (F01) |
| Workflow visualization | None | None | Planned (F07) |
| Static analysis integration | Not documented | Not documented | Planned (F06) |
| CI/CD integration | Not documented | Not documented | Planned (F12) |
| Traceability matrix | None | None | Planned (F17) |
| Non-normal training mode | None | None | Planned (F19) |
| Checklist evolution tracking | None | None | Planned (F15) |

### What Competitors Do Better (Honest Assessment)

| Category | Competitor Advantage | Agent Triforce Response |
|----------|---------------------|------------------------|
| Breadth of specialized agents | wshobson: 73 specialized agents; michael-harris: 126 | Depth over breadth is a deliberate design choice. 3 disciplined agents > 73 undisciplined ones. |
| Onboarding simplicity | Competitors are simpler to start using | F03 (Setup Wizard) closes this gap in Phase 1. |
| Individual specialized tasks | Single-purpose agents for niche tasks (Stripe setup, etc.) | Out of scope. Agent Triforce is a workflow discipline framework, not a task library. |

### What No Competitor Has (Agent Triforce's Moat)

1. **WHO Surgical Safety Checklist methodology**: The SIGN IN / TIME OUT / SIGN OUT pause point structure, borrowed from a system with documented lives-saved outcomes. The intellectual depth creates a moat competitors cannot credibly claim after Agent Triforce owns the positioning.

2. **Non-Normal procedure system (F19)**: Emergency READ-DO checklists for all three agents, with a training mode to verify they activate correctly. This is a direct application of Boeing/FAA emergency procedure methodology. No competitor has this concept.

3. **Checklist evolution system (F15)**: Tracking checklist effectiveness and generating improvement suggestions from real failure data. Directly implements Boorman's "field-tested and updated" principle. No competitor has checklist effectiveness tracking.

4. **Cross-agent memory with conflict detection (F14)**: Multi-agent memory with automatic conflict surfacing. No other plugin has multi-agent memory awareness.

5. **Spec-to-implementation traceability (F17)**: IEEE 830 traceability with automation. Positions Agent Triforce as a compliance tool, not just a developer productivity tool.

---

## Open Questions

1. **Agent Teams API availability**: F01 depends on Claude Code's Agent Teams feature. Is this feature available in the current Claude Code release, or is this on Anthropic's roadmap? Timeline unknown — this could block the P0 critical path.

2. **Hook API completeness**: F02, F05, F10 all depend on `PreToolUse` and `PostToolUse` hooks. Are there documented rate limits or capability gaps in the Claude Code hooks API that would affect these features?

3. **LSP integration security**: F04 requires the LSP server to have file system access. Are there security implications for connecting an LSP server in the Claude Code environment that Forja needs to design around?

4. **Cost estimate accuracy for F09**: Token-based cost estimates for model routing require knowing approximate prompt sizes for each workflow type. What is the acceptable margin of error for cost estimates before they lose usefulness? Proposed: +/- 30%.

5. **Traceability matrix format (F17)**: Should the matrix use the Prometeo-assigned criterion IDs (`{feature-id}-AC-NNN`) or should it interoperate with external issue tracker IDs from F13? This is a schema decision that affects multiple downstream features.

6. **Codebase index language support (F20)**: Which languages should the v1 index support? Proposed scope: Python, TypeScript, JavaScript. Rust and Go as community-contributed parsers. Decision needed before F20 spec is finalized.

7. **Checklist health data ownership (F15)**: Should aggregate (anonymized) checklist health data be opt-in for contribution to a central repository to improve default checklists across all users? Privacy and consent implications need to be addressed.

---

*Roadmap authored by Prometeo (PM) — 2026-02-23*
*Next review: 2026-03-23*
*Related spec: `docs/specs/plugin-promotion-plan.md`*
