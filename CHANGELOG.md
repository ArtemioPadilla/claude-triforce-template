# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
<!-- PM adds planned features here -->

### Added
- **tools/dashboard.py**: Comprehensive multi-agent system dashboard with two output modes: Rich terminal UI and self-contained dark-themed HTML. 10 sections: What's Next (state-based action suggestions), System Overview (agent cards), Feature Pipeline (Kanban board, always-visible columns), Quality Gate (review verdicts with unique finding counts), Tech Debt Register (age tracking), Workflow Status (visual flow diagrams with active stage highlighting), Communication Schedule (6 handoff paths from CLAUDE.md), Architecture Decisions (ADR tracking), Recent Activity (git log, changelog, agent memory), Checklist Inventory (summary + per-agent breakdown). Features: sticky nav bar, stats summary bar, Quick Actions command reference, responsive CSS (900px/600px breakpoints), rich empty states with guidance. Python 3.9+ compatible, zero-dependency HTML mode, defensive parsing for all data sources

### Changed
- **CLAUDE.md**: Replaced Activation Phenomenon with Three Pause Points framework (SIGN IN / TIME OUT / SIGN OUT — WHO surgical checklist naming). Added Communication Schedule table (6 handoff paths), Error Recovery section with per-agent FLY THE AIRPLANE. Updated Every Agent MUST to reference SIGN IN/SIGN OUT
- **prometeo-pm.md**: Restructured with dedicated `## Checklists` section. 6 checklists: SIGN IN, Spec Completion, NON-NORMAL: Requirement Ambiguity (new), Handoff-to-Forja, Handoff-to-Centinela (new), SIGN OUT (new). Removed inline activation protocol and communication section
- **forja-dev.md**: Restructured with dedicated `## Checklists` section. 9 checklists: SIGN IN, Implementation Complete (split from Pre-Handoff), Pre-Delivery (split from Pre-Handoff), NON-NORMAL: Build Failure Recovery (new), NON-NORMAL: Test Failure Recovery (new), Receiving-from-Prometeo (new), Handoff-to-Centinela, Fix Report, SIGN OUT (new)
- **centinela-qa.md**: Restructured with dedicated `## Checklists` section. 9 checklists: SIGN IN, Security Verification (split from Pre-Verdict), Quality Verification (split from Pre-Verdict), Release Readiness (new), NON-NORMAL: Critical Vulnerability Response, Findings Handoff-to-Forja, Findings Summary-to-Prometeo (new), Receiving-from-Forja (new), SIGN OUT (new)
- **All 6 skills**: Renamed ACTIVATE → SIGN IN, PAUSE → TIME OUT, HANDOFF → SIGN OUT. All checklist references now point to canonical names in agent files

### Fixed
- **tools/dashboard.py**: Removed unused `Tuple` import [W-1], refactored 299-line `render_terminal()` into 13 focused `_term_*` section functions matching the HTML renderer's pattern [W-4], fixed review finding counter to deduplicate IDs across sections, added "Approved With Conditions" to What's Next actions, fixed workflow active border-color override by inline styles
- **Repository hygiene**: Deleted stale `tools/__pycache__/` [W-2] and empty `firebase-debug.log` [W-3]
- **.gitignore**: Fixed agent memory pattern from `.claude/agent-memory/*/` to `.claude/agent-memory/` to correctly exclude all nested files [S-3]
- **requirements.txt**: Added optional dependency declaration for `rich>=13.0.0` (only needed for terminal mode) [S-1]

### Security
<!-- QA adds security fixes here -->

### Removed
<!-- Dev adds removed features here -->
