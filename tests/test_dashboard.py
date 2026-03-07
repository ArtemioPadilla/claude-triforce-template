#!/usr/bin/env python3
"""Tests for tools/dashboard.py -- pure parsing functions.

Tests follow TDD Red-Green-Refactor with Arrange-Act-Assert pattern.
Covers: _parse_frontmatter(), _parse_checklists(), parse_specs(),
parse_reviews(), parse_tech_debt(), parse_changelog(), parse_adrs().
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Dict, List
from unittest.mock import patch

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

dashboard = importlib.import_module("dashboard")


# ---------------------------------------------------------------------------
# _parse_frontmatter tests
# ---------------------------------------------------------------------------


class TestParseFrontmatter:
    """Tests for _parse_frontmatter() -- YAML-like frontmatter parsing."""

    def test_parses_simple_key_value(self) -> None:
        """GIVEN frontmatter with key-value pairs
        WHEN _parse_frontmatter is called
        THEN it returns a dict with correct values."""
        # Arrange
        text = "---\nname: Test Agent\nmodel: opus\n---\n# Body"

        # Act
        result = dashboard._parse_frontmatter(text)

        # Assert
        assert result["name"] == "Test Agent"
        assert result["model"] == "opus"

    def test_parses_list_items(self) -> None:
        """GIVEN frontmatter with a list under a key
        WHEN _parse_frontmatter is called
        THEN list items are joined with commas."""
        # Arrange
        text = "---\ntools:\n  - Read\n  - Write\n  - Bash\n---\n"

        # Act
        result = dashboard._parse_frontmatter(text)

        # Assert
        assert result["tools"] == "Read,Write,Bash"

    def test_returns_empty_dict_when_no_frontmatter(self) -> None:
        """GIVEN text without --- markers
        WHEN _parse_frontmatter is called
        THEN it returns an empty dict."""
        # Arrange
        text = "# Just a heading\nSome content."

        # Act
        result = dashboard._parse_frontmatter(text)

        # Assert
        assert result == {}

    def test_handles_empty_text(self) -> None:
        """GIVEN an empty string
        WHEN _parse_frontmatter is called
        THEN it returns an empty dict."""
        # Act
        result = dashboard._parse_frontmatter("")

        # Assert
        assert result == {}

    def test_handles_multiline_description(self) -> None:
        """GIVEN frontmatter with a multiline > description
        WHEN _parse_frontmatter is called
        THEN continuation lines are joined."""
        # Arrange
        text = "---\ndescription: >\n  This is a long\n  description text\nmodel: sonnet\n---\n"

        # Act
        result = dashboard._parse_frontmatter(text)

        # Assert
        assert "This is a long" in result["description"]
        assert "description text" in result["description"]
        assert result["model"] == "sonnet"

    def test_handles_dashes_in_key_names(self) -> None:
        """GIVEN frontmatter with hyphenated keys
        WHEN _parse_frontmatter is called
        THEN keys are preserved as-is."""
        # Arrange
        text = "---\npermissionMode: bypassPermissions\n---\n"

        # Act
        result = dashboard._parse_frontmatter(text)

        # Assert
        assert result["permissionMode"] == "bypassPermissions"


# ---------------------------------------------------------------------------
# _parse_checklists tests
# ---------------------------------------------------------------------------


class TestParseChecklists:
    """Tests for _parse_checklists() -- checklist heading extraction."""

    def test_parses_do_confirm_checklist(self) -> None:
        """GIVEN text with a DO-CONFIRM checklist heading
        WHEN _parse_checklists is called
        THEN it extracts name, type, and item count."""
        # Arrange
        text = "## Checklists\n### SIGN IN (DO-CONFIRM) --- 5 items\n- [ ] Item 1\n"

        # Act
        result = dashboard._parse_checklists(text)

        # Assert
        assert len(result) == 1
        assert result[0].name == "SIGN IN"
        assert result[0].checklist_type == "DO-CONFIRM"
        assert result[0].item_count == 5

    def test_parses_read_do_checklist(self) -> None:
        """GIVEN text with a READ-DO checklist heading
        WHEN _parse_checklists is called
        THEN it extracts the correct type."""
        # Arrange
        text = "### Build Failure Recovery (READ-DO) --- 5 items\n"

        # Act
        result = dashboard._parse_checklists(text)

        # Assert
        assert len(result) == 1
        assert result[0].checklist_type == "READ-DO"

    def test_parses_multiple_checklists(self) -> None:
        """GIVEN text with multiple checklist headings
        WHEN _parse_checklists is called
        THEN all are extracted."""
        # Arrange
        text = (
            "### SIGN IN (DO-CONFIRM) --- 5 items\n"
            "### Implementation Complete (DO-CONFIRM) --- 6 items\n"
            "### Handoff-to-Centinela (READ-DO) --- 5 items\n"
        )

        # Act
        result = dashboard._parse_checklists(text)

        # Assert
        assert len(result) == 3

    def test_handles_em_dash(self) -> None:
        """GIVEN text with em-dash (unicode) separator
        WHEN _parse_checklists is called
        THEN it still parses correctly."""
        # Arrange
        text = "### SIGN IN (DO-CONFIRM) \u2014 5 items\n"

        # Act
        result = dashboard._parse_checklists(text)

        # Assert
        assert len(result) == 1
        assert result[0].item_count == 5

    def test_returns_empty_for_no_checklists(self) -> None:
        """GIVEN text without checklist headings
        WHEN _parse_checklists is called
        THEN it returns an empty list."""
        # Arrange
        text = "# Agent File\nJust regular content."

        # Act
        result = dashboard._parse_checklists(text)

        # Assert
        assert result == []


# ---------------------------------------------------------------------------
# parse_specs tests
# ---------------------------------------------------------------------------


class TestParseSpecs:
    """Tests for parse_specs() -- feature spec parsing."""

    def test_parses_spec_with_all_fields(self, tmp_path: Path) -> None:
        """GIVEN a spec file with title, status, priority, date, tier, and ACs
        WHEN parse_specs is called
        THEN all fields are extracted."""
        # Arrange
        spec_dir = tmp_path / "specs"
        spec_dir.mkdir()
        (spec_dir / "user-auth.md").write_text(
            "# Feature: User Authentication\n"
            "**Status**: Approved\n"
            "**Priority**: P0\n"
            "**Date**: 2026-03-01\n"
            "**Tier**: M\n"
            "\n"
            "## Acceptance Criteria\n"
            "**GIVEN** a user with valid credentials\n"
            "**GIVEN** a user with invalid credentials\n"
        )

        # Act
        with patch.object(dashboard, "SPEC_DIR", spec_dir):
            specs = dashboard.parse_specs()

        # Assert
        assert len(specs) == 1
        assert specs[0].title == "User Authentication"
        assert specs[0].status == "Approved"
        assert specs[0].priority == "P0"
        assert specs[0].tier == "M"
        assert specs[0].ac_count == 2

    def test_skips_readme(self, tmp_path: Path) -> None:
        """GIVEN a README.md in the specs directory
        WHEN parse_specs is called
        THEN it is skipped."""
        # Arrange
        spec_dir = tmp_path / "specs"
        spec_dir.mkdir()
        (spec_dir / "README.md").write_text("# Specs README\n")

        # Act
        with patch.object(dashboard, "SPEC_DIR", spec_dir):
            specs = dashboard.parse_specs()

        # Assert
        assert specs == []

    def test_handles_missing_fields(self, tmp_path: Path) -> None:
        """GIVEN a spec file with minimal content
        WHEN parse_specs is called
        THEN defaults are used for missing fields."""
        # Arrange
        spec_dir = tmp_path / "specs"
        spec_dir.mkdir()
        (spec_dir / "minimal.md").write_text("# Some heading\nSome content.\n")

        # Act
        with patch.object(dashboard, "SPEC_DIR", spec_dir):
            specs = dashboard.parse_specs()

        # Assert
        assert len(specs) == 1
        assert specs[0].title == "minimal"
        assert specs[0].status == "Unknown"

    def test_empty_directory(self, tmp_path: Path) -> None:
        """GIVEN an empty specs directory
        WHEN parse_specs is called
        THEN it returns an empty list."""
        # Arrange
        spec_dir = tmp_path / "specs"
        spec_dir.mkdir()

        # Act
        with patch.object(dashboard, "SPEC_DIR", spec_dir):
            specs = dashboard.parse_specs()

        # Assert
        assert specs == []

    def test_nonexistent_directory(self, tmp_path: Path) -> None:
        """GIVEN a nonexistent specs directory
        WHEN parse_specs is called
        THEN it returns an empty list."""
        # Act
        with patch.object(dashboard, "SPEC_DIR", tmp_path / "nonexistent"):
            specs = dashboard.parse_specs()

        # Assert
        assert specs == []


# ---------------------------------------------------------------------------
# parse_reviews tests
# ---------------------------------------------------------------------------


class TestParseReviews:
    """Tests for parse_reviews() -- review file parsing."""

    def test_parses_code_health_review(self, tmp_path: Path) -> None:
        """GIVEN a code-health review with unique findings
        WHEN parse_reviews is called
        THEN finding counts and verdict are correct."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "code-health-2026-03-05.md").write_text(
            "# Code Health Scan\n"
            "## Verdict\n**APPROVED WITH CONDITIONS**\n"
            "## Findings\n"
            "**[C-1]** Critical issue\n"
            "**[W-1]** Warning one\n"
            "**[W-2]** Warning two\n"
            "**[S-1]** Suggestion\n"
        )

        # Act
        with patch.object(dashboard, "REVIEW_DIR", review_dir):
            reviews = dashboard.parse_reviews()

        # Assert
        assert len(reviews) == 1
        assert reviews[0].review_type == "code-health"
        assert reviews[0].critical_count == 1
        assert reviews[0].warning_count == 2
        assert reviews[0].suggestion_count == 1
        assert reviews[0].verdict == "Approved With Conditions"

    def test_detects_security_audit_type(self, tmp_path: Path) -> None:
        """GIVEN a security-audit review file
        WHEN parse_reviews is called
        THEN review_type is 'security-audit'."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "security-audit-trail.md").write_text(
            "# Security Audit\n**APPROVED**\n"
        )

        # Act
        with patch.object(dashboard, "REVIEW_DIR", review_dir):
            reviews = dashboard.parse_reviews()

        # Assert
        assert reviews[0].review_type == "security-audit"

    def test_detects_release_check_type(self, tmp_path: Path) -> None:
        """GIVEN a release-check review file
        WHEN parse_reviews is called
        THEN review_type is 'release-check'."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "release-check-0.5.0.md").write_text(
            "# Release Check\n**CHANGES REQUIRED**\n"
        )

        # Act
        with patch.object(dashboard, "REVIEW_DIR", review_dir):
            reviews = dashboard.parse_reviews()

        # Assert
        assert reviews[0].review_type == "release-check"
        assert reviews[0].verdict == "Changes Required"

    def test_deduplicates_finding_ids(self, tmp_path: Path) -> None:
        """GIVEN a review where the same finding ID appears multiple times
        WHEN parse_reviews is called
        THEN each unique finding is counted only once."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "code-health-2026-01-01.md").write_text(
            "## High\n**[W-1]** First mention\n"
            "## Handoff\n**[W-1]** Same finding referenced again\n"
            "**[W-2]** Different finding\n"
        )

        # Act
        with patch.object(dashboard, "REVIEW_DIR", review_dir):
            reviews = dashboard.parse_reviews()

        # Assert
        assert reviews[0].warning_count == 2

    def test_skips_readme(self, tmp_path: Path) -> None:
        """GIVEN a README.md in reviews directory
        WHEN parse_reviews is called
        THEN it is skipped."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "README.md").write_text("# Reviews README\n**[C-1]** Fake\n")

        # Act
        with patch.object(dashboard, "REVIEW_DIR", review_dir):
            reviews = dashboard.parse_reviews()

        # Assert
        assert reviews == []


# ---------------------------------------------------------------------------
# parse_tech_debt tests
# ---------------------------------------------------------------------------


class TestParseTechDebt:
    """Tests for parse_tech_debt() -- TECH_DEBT.md parsing."""

    def test_parses_active_debt_items(self, tmp_path: Path) -> None:
        """GIVEN a TECH_DEBT.md with active items
        WHEN parse_tech_debt is called
        THEN items are extracted with correct fields."""
        # Arrange
        debt_file = tmp_path / "TECH_DEBT.md"
        debt_file.write_text(
            "# Technical Debt Register\n\n"
            "## Active Debt\n\n"
            "### [TD-001] Missing test coverage\n"
            "- **Type**: Test\n"
            "- **Severity**: Medium\n"
            "- **Found**: 2026-03-05\n"
            "- **Estimated effort**: L (1-2 days)\n"
            "- **Impact if not fixed**: Regressions\n"
            "\n"
            "## Resolved Debt\n\n"
            "_No resolved debt yet._\n"
        )

        # Act
        with patch.object(dashboard, "TECH_DEBT_FILE", debt_file):
            items = dashboard.parse_tech_debt()

        # Assert
        assert len(items) == 1
        assert items[0].item_id == "TD-001"
        assert items[0].title == "Missing test coverage"
        assert items[0].debt_type == "Test"
        assert items[0].severity == "Medium"
        assert items[0].is_resolved is False

    def test_parses_resolved_items(self, tmp_path: Path) -> None:
        """GIVEN a TECH_DEBT.md with only resolved items
        WHEN parse_tech_debt is called
        THEN resolved items have is_resolved=True."""
        # Arrange
        debt_file = tmp_path / "TECH_DEBT.md"
        debt_file.write_text(
            "## Active Debt\n"
            "_No active debt._\n"
            "\n"
            "## Resolved Debt\n\n"
            "### [TD-099] Fixed issue\n"
            "- **Type**: Code\n"
            "- **Severity**: Low\n"
            "- **Found**: 2026-01-01\n"
            "- **Estimated effort**: S\n"
        )

        # Act
        with patch.object(dashboard, "TECH_DEBT_FILE", debt_file):
            items = dashboard.parse_tech_debt()

        # Assert
        assert len(items) == 1
        assert items[0].is_resolved is True

    def test_handles_multiple_items(self, tmp_path: Path) -> None:
        """GIVEN a TECH_DEBT.md with multiple active items
        WHEN parse_tech_debt is called
        THEN all items are extracted."""
        # Arrange
        debt_file = tmp_path / "TECH_DEBT.md"
        debt_file.write_text(
            "## Active Debt\n\n"
            "### [TD-001] First item\n"
            "- **Type**: Code\n"
            "- **Severity**: High\n"
            "- **Found**: 2026-01-01\n"
            "- **Estimated effort**: M\n"
            "\n"
            "### [TD-002] Second item\n"
            "- **Type**: Design\n"
            "- **Severity**: Medium\n"
            "- **Found**: 2026-02-01\n"
            "- **Estimated effort**: L\n"
            "\n"
            "## Resolved Debt\n"
        )

        # Act
        with patch.object(dashboard, "TECH_DEBT_FILE", debt_file):
            items = dashboard.parse_tech_debt()

        # Assert
        assert len(items) == 2
        assert items[0].item_id == "TD-001"
        assert items[1].item_id == "TD-002"

    def test_handles_missing_file(self, tmp_path: Path) -> None:
        """GIVEN no TECH_DEBT.md file
        WHEN parse_tech_debt is called
        THEN it returns an empty list."""
        # Act
        with patch.object(dashboard, "TECH_DEBT_FILE", tmp_path / "nonexistent.md"):
            items = dashboard.parse_tech_debt()

        # Assert
        assert items == []


# ---------------------------------------------------------------------------
# parse_changelog tests
# ---------------------------------------------------------------------------


class TestParseChangelog:
    """Tests for parse_changelog() -- CHANGELOG.md Unreleased section parsing."""

    def test_counts_items_per_category(self, tmp_path: Path) -> None:
        """GIVEN a CHANGELOG.md with categorized items under Unreleased
        WHEN parse_changelog is called
        THEN category counts are correct."""
        # Arrange
        changelog_file = tmp_path / "CHANGELOG.md"
        changelog_file.write_text(
            "# Changelog\n\n"
            "## [Unreleased]\n\n"
            "### Added\n"
            "- Feature A\n"
            "- Feature B\n"
            "\n"
            "### Fixed\n"
            "- Bug fix X\n"
            "\n"
            "## [0.1.0] - 2026-01-01\n"
        )

        # Act
        with patch.object(dashboard, "CHANGELOG_FILE", changelog_file):
            summary = dashboard.parse_changelog()

        # Assert
        assert summary.categories["Added"] == 2
        assert summary.categories["Fixed"] == 1

    def test_handles_no_unreleased_section(self, tmp_path: Path) -> None:
        """GIVEN a CHANGELOG.md without an Unreleased section
        WHEN parse_changelog is called
        THEN it returns an empty summary."""
        # Arrange
        changelog_file = tmp_path / "CHANGELOG.md"
        changelog_file.write_text("# Changelog\n\n## [1.0.0]\n\n### Added\n- Stuff\n")

        # Act
        with patch.object(dashboard, "CHANGELOG_FILE", changelog_file):
            summary = dashboard.parse_changelog()

        # Assert
        assert summary.categories == {}

    def test_handles_missing_file(self, tmp_path: Path) -> None:
        """GIVEN no CHANGELOG.md file
        WHEN parse_changelog is called
        THEN it returns an empty summary."""
        # Act
        with patch.object(dashboard, "CHANGELOG_FILE", tmp_path / "nonexistent.md"):
            summary = dashboard.parse_changelog()

        # Assert
        assert summary.categories == {}


# ---------------------------------------------------------------------------
# parse_adrs tests
# ---------------------------------------------------------------------------


class TestParseAdrs:
    """Tests for parse_adrs() -- Architecture Decision Record parsing."""

    def test_parses_adr_file(self, tmp_path: Path) -> None:
        """GIVEN an ADR file with standard fields
        WHEN parse_adrs is called
        THEN it extracts number, title, status, and date."""
        # Arrange
        adr_dir = tmp_path / "adr"
        adr_dir.mkdir()
        (adr_dir / "ADR-001-use-python.md").write_text(
            "# ADR-001: Use Python for tooling\n"
            "**Date**: 2026-03-01\n"
            "**Status**: Accepted\n"
            "\n"
            "## Context\nWe need a scripting language.\n"
        )

        # Act
        with patch.object(dashboard, "ADR_DIR", adr_dir):
            adrs = dashboard.parse_adrs()

        # Assert
        assert len(adrs) == 1
        assert adrs[0].number == "001"
        assert adrs[0].title == "Use Python for tooling"
        assert adrs[0].status == "Accepted"
        assert adrs[0].adr_date == "2026-03-01"

    def test_handles_empty_adr_directory(self, tmp_path: Path) -> None:
        """GIVEN an ADR directory with no ADR-*.md files
        WHEN parse_adrs is called
        THEN it returns an empty list."""
        # Arrange
        adr_dir = tmp_path / "adr"
        adr_dir.mkdir()
        (adr_dir / "README.md").write_text("# ADRs\n")

        # Act
        with patch.object(dashboard, "ADR_DIR", adr_dir):
            adrs = dashboard.parse_adrs()

        # Assert
        assert adrs == []

    def test_handles_nonexistent_directory(self, tmp_path: Path) -> None:
        """GIVEN no ADR directory
        WHEN parse_adrs is called
        THEN it returns an empty list."""
        # Act
        with patch.object(dashboard, "ADR_DIR", tmp_path / "nonexistent"):
            adrs = dashboard.parse_adrs()

        # Assert
        assert adrs == []

    def test_handles_multiple_adr_statuses(self, tmp_path: Path) -> None:
        """GIVEN ADR files with different statuses
        WHEN parse_adrs is called
        THEN each status is correctly parsed."""
        # Arrange
        adr_dir = tmp_path / "adr"
        adr_dir.mkdir()
        (adr_dir / "ADR-001-first.md").write_text(
            "# ADR-001: First Decision\n**Status**: Proposed\n"
        )
        (adr_dir / "ADR-002-second.md").write_text(
            "# ADR-002: Second Decision\n**Status**: Deprecated\n"
        )

        # Act
        with patch.object(dashboard, "ADR_DIR", adr_dir):
            adrs = dashboard.parse_adrs()

        # Assert
        assert len(adrs) == 2
        assert adrs[0].status == "Proposed"
        assert adrs[1].status == "Deprecated"


# ---------------------------------------------------------------------------
# _read_file_safe tests
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# compute_health tests
# ---------------------------------------------------------------------------


class TestComputeHealth:
    """Tests for compute_health() -- system health status determination."""

    def test_healthy_when_no_issues(self) -> None:
        """GIVEN no critical/high debt and no concerning reviews
        WHEN compute_health is called
        THEN it returns HEALTHY."""
        # Arrange
        debt = [dashboard.TechDebtItem(
            item_id="TD-001", title="Minor issue", debt_type="Code",
            severity="Medium", found_date="2026-01-01", effort="S",
            is_resolved=False,
        )]
        reviews: list = []
        specs: list = []

        # Act
        result = dashboard.compute_health(debt, reviews, specs)

        # Assert
        assert result == dashboard.HealthStatus.HEALTHY

    def test_critical_on_critical_debt(self) -> None:
        """GIVEN critical tech debt
        WHEN compute_health is called
        THEN it returns CRITICAL."""
        # Arrange
        debt = [dashboard.TechDebtItem(
            item_id="TD-001", title="Security hole", debt_type="Security",
            severity="Critical", found_date="2026-01-01", effort="S",
            is_resolved=False,
        )]

        # Act
        result = dashboard.compute_health(debt, [], [])

        # Assert
        assert result == dashboard.HealthStatus.CRITICAL

    def test_critical_on_changes_required_with_critical_findings(self) -> None:
        """GIVEN a review with CHANGES REQUIRED and critical findings
        WHEN compute_health is called
        THEN it returns CRITICAL."""
        # Arrange
        reviews = [dashboard.ReviewInfo(
            filename="test-review.md", review_type="feature",
            verdict="Changes Required", critical_count=1,
            warning_count=0, suggestion_count=0,
        )]

        # Act
        result = dashboard.compute_health([], reviews, [])

        # Assert
        assert result == dashboard.HealthStatus.CRITICAL

    def test_warning_on_high_debt(self) -> None:
        """GIVEN high severity tech debt
        WHEN compute_health is called
        THEN it returns WARNING."""
        # Arrange
        debt = [dashboard.TechDebtItem(
            item_id="TD-001", title="Performance issue", debt_type="Code",
            severity="High", found_date="2026-01-01", effort="M",
            is_resolved=False,
        )]

        # Act
        result = dashboard.compute_health(debt, [], [])

        # Assert
        assert result == dashboard.HealthStatus.WARNING

    def test_warning_on_approved_with_conditions(self) -> None:
        """GIVEN a review with APPROVED WITH CONDITIONS
        WHEN compute_health is called
        THEN it returns WARNING."""
        # Arrange
        reviews = [dashboard.ReviewInfo(
            filename="test-review.md", review_type="code-health",
            verdict="Approved With Conditions", critical_count=0,
            warning_count=2, suggestion_count=0,
        )]

        # Act
        result = dashboard.compute_health([], reviews, [])

        # Assert
        assert result == dashboard.HealthStatus.WARNING

    def test_ignores_resolved_debt(self) -> None:
        """GIVEN only resolved critical debt
        WHEN compute_health is called
        THEN it returns HEALTHY."""
        # Arrange
        debt = [dashboard.TechDebtItem(
            item_id="TD-001", title="Resolved issue", debt_type="Code",
            severity="Critical", found_date="2026-01-01", effort="S",
            is_resolved=True,
        )]

        # Act
        result = dashboard.compute_health(debt, [], [])

        # Assert
        assert result == dashboard.HealthStatus.HEALTHY


# ---------------------------------------------------------------------------
# _read_file_safe tests
# ---------------------------------------------------------------------------


class TestReadFileSafe:
    """Tests for _read_file_safe() -- safe file reading."""

    def test_reads_existing_file(self, tmp_path: Path) -> None:
        """GIVEN an existing file
        WHEN _read_file_safe is called
        THEN it returns the contents."""
        # Arrange
        f = tmp_path / "test.txt"
        f.write_text("hello")

        # Act
        result = dashboard._read_file_safe(f)

        # Assert
        assert result == "hello"

    def test_returns_empty_for_missing_file(self, tmp_path: Path) -> None:
        """GIVEN a nonexistent file
        WHEN _read_file_safe is called
        THEN it returns an empty string."""
        # Act
        result = dashboard._read_file_safe(tmp_path / "missing.txt")

        # Assert
        assert result == ""
