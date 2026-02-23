# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- **Plugin Promotion and Monetization Plan**: Comprehensive 4-phase promotion and monetization strategy for the Agent Triforce Claude Code plugin. Covers GitHub discovery infrastructure, content marketing (Show HN, Reddit, Twitter/X), community building (Product Hunt, Substack, YouTube), enterprise partnerships, GitHub Sponsors tiers, consulting offer ($1.5K–$20K), digital product packs, and enterprise licensing. See `docs/specs/plugin-promotion-plan.md`.

### Added
- **Plugin Marketplace**: Packaged Agent Triforce as an installable Claude Code plugin marketplace. Users can install with `/plugin marketplace add ArtemioPadilla/claude-triforce-template` then `/plugin install agent-triforce@agent-triforce`. Includes 3 agents, 6 skills (namespaced as `/agent-triforce:*`), and 2 new commands (`setup` for project scaffolding, `methodology` for checklist reference). Zero-duplication architecture using symlinks from plugin to canonical `.claude/` files. Includes `dashboard` command and SubagentStop hook that auto-regenerates the HTML dashboard after every agent session

### Changed
- **Prometeo spec templates**: Replaced single spec template with tiered system (S/M/L). Tier S has 5 sections for quick fixes, Tier M (default) has 14 sections with Glossary, Non-Functional Requirements, and Constraints & Assumptions, Tier L adds 5 more sections (Phased Delivery, API Contract, Migration, Testing Strategy, Story Map). All tiers include explicit `**Tier**` metadata field
- **Prometeo behavioral rules**: Added INVEST validation (Independent, Negotiable, Valuable, Estimable, Small, Testable) as a mandatory check for every user story
- **Prometeo Spec Completion checklist**: Updated to be tier-aware -- first item now verifies tier declaration and tier-required sections; success metrics scoped to M/L tiers; INVEST validation added to acceptance criteria check
- **feature-spec skill**: Added tier selection step (ask user or default to M), INVEST validation breakdown, and IEEE 830 quality attribute verification for M/L tiers
- **Agent files**: Embedded condensed `## Methodology` section into all 3 agent files (prometeo-pm, forja-dev, centinela-qa). Includes pause point definitions, communication paths, workflow diagrams, and FLY THE AIRPLANE principle. Fixes subagent context loss — agents now carry methodology when invoked via skills with `context: fork`
- **Centinela QA agent**: Added Review Dimensions (Code Quality, Architecture Compliance, Spec Compliance) after review template. Added Code Quality, Architecture Compliance, and Test Quality sections to review template. Enhanced Test Quality Assessment with FIRST principles, Arrange-Act-Assert pattern, and coverage-by-type. Upgraded Quality Verification checklist with Clean Code, architecture compliance, and spec traceability items
- **security-audit skill**: Added architecture review (dependency direction, layer separation) and test strategy review (security-critical path coverage) as steps 5-6
- **code-health skill**: Replaced code smells scan with Clean Code violations (30-line functions, 300-line files, 3-level nesting, DRY, primitive obsession, feature envy, god classes). Added architecture compliance step (dependency direction, layer leakage, Screaming Architecture)
- **release-check skill**: Added spec traceability verification and test quality verification (FIRST principles, Arrange-Act-Assert) as steps 8-9 in Testing & Quality Gate
- **Forja Dev agent**: Added Engineering Principles section (Clean Architecture, TDD, Clean Code, Refactoring, 12-Factor, GoF Design Patterns). Expanded Implementation Process to 7-step TDD cycle (design, red, green, refactor, coverage, document, handoff). Updated behavioral rules with TDD-first, Boy Scout Rule, YAGNI. Upgraded Implementation Complete checklist (TDD test-first, dependency direction, explicit error handling) and Pre-Delivery checklist (refactoring pass, Screaming Architecture)
- **implement-feature skill**: Added DESIGN phase (interfaces first, Clean Architecture layers), TDD Build cycle (Red/Green/Refactor with Arrange-Act-Assert), and explicit REFACTORING PASS before Pre-Delivery
- **review-findings skill**: Enhanced FIX section with Clean Code principles (Extract Method, Rename, Move, Replace Conditional with Polymorphism), Arrange-Act-Assert test updates, Boy Scout Rule scan, and "no new code smells" verification
- **CLAUDE.md**: Added Software Engineering Principles section (IEEE 830/INVEST specs, Clean Architecture, TDD/Clean Code, FIRST testing, Refactoring, 12-Factor/GoF). Updated Code Standards with function size limit (<30 lines) and error handling preference
- **Dashboard**: Added spec tier badge (S/M/L) to Feature Pipeline kanban cards in both HTML and terminal renderers

### Fixed
<!-- Dev adds fixes here -->

### Security
<!-- QA adds security fixes here -->

### Removed
<!-- Dev adds removed features here -->

## [0.1.0] - 2026-02-22

### Added
- **Multi-agent system**: 3 specialized agents (Prometeo PM, Forja Dev, Centinela QA) with dedicated configuration files, permission modes, and model assignments
- **6 skills**: `/feature-spec`, `/implement-feature`, `/review-findings`, `/security-audit`, `/code-health`, `/release-check` — each mapped to the appropriate agent
- **24 checklists** (117 items) using WHO Surgical Safety Checklist methodology: SIGN IN / TIME OUT / SIGN OUT pause points, DO-CONFIRM and READ-DO types, Boorman's 5-9 killer items rule
- **Communication Schedule**: 6 defined handoff paths between agents with structured handoff protocol (what was done, what to watch for, what's needed, open questions)
- **Error Recovery**: NON-NORMAL READ-DO checklists for each agent with FLY THE AIRPLANE step-1 reminders
- **tools/dashboard.py**: Comprehensive multi-agent system dashboard with two output modes: Rich terminal UI and self-contained dark-themed HTML. 10 sections: What's Next (state-based action suggestions), System Overview (agent cards), Feature Pipeline (Kanban board, always-visible columns), Quality Gate (review verdicts with unique finding counts), Tech Debt Register (age tracking), Workflow Status (visual flow diagrams with active stage highlighting), Communication Schedule (6 handoff paths from CLAUDE.md), Architecture Decisions (ADR tracking), Recent Activity (git log, changelog, agent memory), Checklist Inventory (summary + per-agent breakdown). Features: sticky nav bar, stats summary bar, Quick Actions command reference, responsive CSS (900px/600px breakpoints), rich empty states with guidance. Python 3.9+ compatible, zero-dependency HTML mode, defensive parsing for all data sources
- **docs/portability/**: Portability guide for porting the framework to downstream projects
- **Project conventions**: Conventional Commits, branch naming, file location standards, code quality rules, Keep a Changelog format, TECH_DEBT.md tracking
