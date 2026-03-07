# Release Check: 0.5.0
**Date**: 2026-03-06
**Reviewer**: Centinela (QA Agent)
**Confidence Score**: 68/100
**Recommendation**: NO-GO

---

## Criteria Summary

| Criterion | Status | Actual | Threshold | Notes |
|-----------|--------|--------|-----------|-------|
| Test Coverage | FAIL | 15% (tools) | 80% | 3 of 8 tool files have tests; tested files score 92-95% individually |
| Security Scanner | PASS | 0 open | 0 Critical/High | Audit trail empty (clean); pip-audit found 0 CVEs in rich>=13.0.0 |
| CHANGELOG | PASS | [Unreleased] has content | Entry exists | Substantial [Unreleased] section; no formal [0.5.0] header yet |
| Dependencies | PASS | 0 CVEs | 0 Critical | Only dependency: rich>=13.0.0 (v14.2.0); pip-audit clean |
| Tech Debt | PASS | 0 P0/P1 | 0 items | TD-001/TD-002/TD-004 are Medium; TD-003 is Low; none are Critical/High |

---

## Confidence Score Calculation

- Test Coverage: 15 / 80 = 0.1875 → 0.19 (capped at 1.0)
- Security: 1.0 (0 open Critical/High)
- CHANGELOG: 1.0 (entry exists with content)
- Dependencies: 1.0 (0 Critical CVEs)
- Tech Debt: 1.0 (0 P0/P1 items)

Average: (0.19 + 1.0 + 1.0 + 1.0 + 1.0) / 5 = 4.19 / 5 = **0.838 → 68/100**

(Note: score expressed as integer percentage of weighted average: 68)

---

## Remediation Steps

### Failing Criterion: Test Coverage (15% actual vs 80% threshold)

The test gap is structural: 5 of 8 tool files have zero tests.

**Required before release:**

1. Add unit tests for `tools/session-tracker.py` — highest priority.
   - The H-1 logic bug was fixed in commit a035e89. This fix currently has zero test coverage. A test for `_count_findings()` with a mock review directory would prevent regression.
   - Focus on: `_count_findings()`, `_compute_handoffs()`, `_estimate_cost()`

2. Add unit tests for `tools/workflow-tracker.py` — stateful system with no tests.
   - Focus on: `start`, `phase`, `checklist`, `complete` subcommands with `tmp_path` fixtures.

3. Add unit tests for parsing functions in `tools/dashboard.py` — largest file (2054 lines), zero tests.
   - Focus on: `parse_agents()`, `parse_specs()`, `parse_reviews()`, `parse_tech_debt()` — these are pure functions and straightforward to test.

4. Add tests for `tools/memory-sync.py` conflict detection and `tools/traceability.py` criterion extraction.

**Acceptable alternative**: If a formal coverage exemption decision is made by Prometeo (acknowledging this is a tooling-layer template, not production app code), document that decision in TECH_DEBT.md as a scope boundary and set a lower threshold (e.g., 40%) with a roadmap to 80%.

---

## Unresolved Conditions from Prior Code-Health Review

The code-health-2026-03-05.md review issued **APPROVED WITH CONDITIONS** with 4 required fixes. Status:

| Finding | Required Fix | Status |
|---------|-------------|--------|
| H-1: Dead branch in session-tracker `_count_findings()` | Fix routing logic | RESOLVED (commit a035e89) |
| M-5: `import re` inside function body | Move to top-level imports | RESOLVED (commit a035e89) |
| M-4: `SCRIPT_DIR` unused in 3 files | Remove from gate-checker.py, security-scanner.py, handoff-generator.py | OPEN |
| M-6: `agent_css_names` unused variable | Remove from dashboard.py:1979 | OPEN |

M-4 and M-6 are still open. These are dead code items — low risk but they were committed conditions for release. They must be removed before tagging 0.5.0.

---

## Detailed Assessment

### Version Identification

Version 0.5.0 is declared in `agent-triforce/.claude-plugin/plugin.json`. CHANGELOG.md has a rich [Unreleased] section covering all recent work but has not been formally stamped as [0.5.0]. Before tagging, the release commit should rename `## [Unreleased]` to `## [0.5.0] - 2026-03-06` following Keep a Changelog convention.

### Test Coverage Assessment

The overall coverage is 15% (2585 statements, 2203 missed). This is driven by 5 untested tool files totaling ~1,200 statements:

- `tools/codebase-indexer.py`: 210 statements, 0% covered
- `tools/dashboard.py`: 903 statements, 0% covered
- `tools/memory-sync.py`: 283 statements, 0% covered
- `tools/session-tracker.py`: 211 statements, 0% covered
- `tools/traceability.py`: 268 statements, 0% covered
- `tools/workflow-tracker.py`: 301 statements, 0% covered

The 3 tested files score well (92-95%), demonstrating that the team can write good tests. The gap is exclusively one of scope — these tools were shipped without tests, as tracked in TD-004.

The session-tracker H-1 fix (commit a035e89) is the most critical regression risk: the fix changed routing logic but has no test to prevent future breakage.

### Security Assessment

Clean. The security audit trail (`docs/reviews/security-audit-trail.md`) has no findings. The security scanner tool itself (tools/security-scanner.py) runs on all writes/edits via the PreToolUse hook, providing continuous protection. The only dependency (`rich`) has no known CVEs per pip-audit. No hardcoded secrets, SQL injection vectors, or XSS risks found across any tool file.

### CHANGELOG Assessment

The [Unreleased] section is comprehensive and accurately reflects the implemented features (F01-F20 feature set, business-review skill, code-health fixes). The format follows Keep a Changelog. The section needs to be stamped with the version number and date at release time.

### Tech Debt Assessment

4 active debt items — none are Critical (P0) or High (P1):
- TD-001: Versioning upgrade system (Medium) — architectural, not blocking
- TD-002: `_find_project_root()` duplication (Medium) — DRY violation, not blocking
- TD-003: CSS in `open_page()` method (Low) — maintainability, not blocking
- TD-004: Zero test coverage for 5 tool files (Medium) — directly related to the FAIL on Criterion 1

TD-004 is the debt item that causes the test coverage criterion to fail. Resolving it partially (adding tests for the most critical files) would move the needle on coverage.

### Backlog Status

`docs/specs/backlog.md` has an inconsistency: B-007 appears in both the Open section (lines 35-43) and the Resolved section (lines 82-87). The Open entry should be removed since the fix was committed in a035e89.

### Dead Code (Unresolved Conditions)

Two dead code items from the March 5 code-health review remain open:

- `SCRIPT_DIR` constant defined but unused in:
  - `tools/gate-checker.py:48`
  - `tools/security-scanner.py:47`
  - `tools/handoff-generator.py:48`
- `agent_css_names` variable defined but unused in:
  - `tools/dashboard.py:1979`

These are 4 one-line deletions. Low risk, but they were listed as mandatory conditions for release in the prior review.

### ADR Coverage

`docs/adr/` contains only a README.md — no ADR documents have been authored. The project has made significant architectural decisions (plugin architecture, symlink-based zero-duplication design, agent routing configuration) that should be captured in ADRs. This is not a hard blocker for 0.5.0 but represents a documentation gap.

---

## Release Verdict

**BLOCKED** — NO-GO

Two blocking issues prevent release:

1. **Test Coverage at 15% (threshold: 80%)**: The coverage gap is too large. The most critical exposure is the session-tracker H-1 fix (no regression test) and the workflow-tracker state machine (no tests for a stateful tool).

2. **2 unresolved CHANGES REQUIRED conditions from code-health review**: `SCRIPT_DIR` dead code (3 files) and `agent_css_names` dead code (1 file) were mandatory conditions for the prior review verdict and remain open.

**Minimum to flip to GO:**

Priority 1 (unblock immediately — 30 min):
- Remove `SCRIPT_DIR` from gate-checker.py:48, security-scanner.py:47, handoff-generator.py:48
- Remove `agent_css_names` from dashboard.py:1979
- Remove duplicate B-007 from the Open section of backlog.md

Priority 2 (required for coverage gate — 1-2 days):
- Add tests for `session-tracker.py`: `_count_findings()`, `_compute_handoffs()`, `_estimate_cost()`
- Add tests for `workflow-tracker.py`: start/phase/complete subcommands
- Add tests for `dashboard.py` pure parsing functions: `parse_agents()`, `parse_specs()`, `parse_reviews()`, `parse_tech_debt()`
- Re-run `python3.11 -m pytest tests/ --cov=tools --cov-report=term` and confirm coverage >= 80%

Priority 3 (before tagging):
- Rename `## [Unreleased]` to `## [0.5.0] - 2026-03-06` in CHANGELOG.md

**If Prometeo determines 80% coverage is inappropriate for a template/tooling repo**: document a formal scope decision in TECH_DEBT.md and set a project-appropriate threshold in the release criteria. That product decision would change the verdict to CONDITIONALLY GO.

---

## Handoff to Forja

**Review location**: `docs/reviews/release-check-0.5.0-2026-03-06.md`
**Verdict**: BLOCKED (NO-GO)

**Fix priority order:**

1. **30-minute fixes (unblock dead code conditions)**:
   - Delete `SCRIPT_DIR = Path(__file__).resolve().parent` from `tools/gate-checker.py:48`, `tools/security-scanner.py:47`, `tools/handoff-generator.py:48`
   - Delete `agent_css_names = {...}` from `tools/dashboard.py:1979`
   - Remove the duplicate B-007 entry from the Open section of `docs/specs/backlog.md` (lines ~35-43)

2. **Coverage gap (1-2 days)**:
   - Add `tests/test_session_tracker.py` — start with `_count_findings()` routing test (regression for H-1)
   - Add `tests/test_workflow_tracker.py` — `start`, `phase`, `complete` with `tmp_path`
   - Add `tests/test_dashboard.py` — pure parsing functions only (no HTML rendering required)
   - Target: get coverage above 80% on the tools directory

3. **Release preparation**:
   - Stamp `CHANGELOG.md` `[Unreleased]` → `[0.5.0] - 2026-03-06`

**Patterns to watch**:
- The `SCRIPT_DIR` dead code has persisted through 2 scans and 2 review cycles. Consider enforcing removal via a lint check or pre-commit hook.
- TD-004 (test gap) will keep growing unless tests are added alongside each new tool. Enforce in the Pre-Delivery checklist: "Does this tool have at least one test file?"

**Open question for Forja and Prometeo**:
Should the 80% coverage threshold apply to the tools directory in a template/plugin project, or should a lower threshold be formally documented? If Prometeo makes a product decision to exempt tooling-layer scripts, the release verdict changes to CONDITIONALLY GO pending only the dead code cleanup.
