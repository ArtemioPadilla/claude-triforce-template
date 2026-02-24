#!/usr/bin/env python3
"""Tests for tools/gate-checker.py.

Tests follow TDD Red-Green-Refactor with Arrange-Act-Assert pattern.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

gate_checker = importlib.import_module("gate-checker")


# ---------------------------------------------------------------------------
# Gate document parsing tests
# ---------------------------------------------------------------------------

class TestParseGateDocument:
    """Tests for parse_gate_document()."""

    def test_parses_pending_document(self) -> None:
        """GIVEN a gate document with PENDING status
        WHEN parse_gate_document is called
        THEN status is PENDING."""
        # Arrange
        content = (
            "# Gate: user-auth -- Plan Approval Gate\n"
            "**Date**: 2026-02-24\n"
            "**Status**: PENDING\n"
            "\n"
            "## Criteria\n"
            "- [ ] Spec coverage verified\n"
            "- [ ] Architecture reviewed\n"
            "\n"
            "## Approval\n"
            "**Approved by**: {agent or user}\n"
            "**Override reason** (if applicable): {reason}\n"
        )

        # Act
        result = gate_checker.parse_gate_document(content)

        # Assert
        assert result["status"] == "PENDING"
        assert len(result["criteria"]) == 2
        assert result["criteria"][0]["text"] == "Spec coverage verified"
        assert result["criteria"][0]["checked"] is False
        assert result["approved_by"] == ""

    def test_parses_approved_document(self) -> None:
        """GIVEN a gate document with APPROVED status
        WHEN parse_gate_document is called
        THEN status is APPROVED and approved_by is set."""
        # Arrange
        content = (
            "**Status**: APPROVED\n"
            "\n"
            "## Criteria\n"
            "- [x] Spec coverage verified\n"
            "- [x] Architecture reviewed\n"
            "\n"
            "## Approval\n"
            "**Approved by**: Prometeo (PM)\n"
        )

        # Act
        result = gate_checker.parse_gate_document(content)

        # Assert
        assert result["status"] == "APPROVED"
        assert result["criteria"][0]["checked"] is True
        assert result["criteria"][1]["checked"] is True
        assert result["approved_by"] == "Prometeo (PM)"

    def test_parses_overridden_document(self) -> None:
        """GIVEN a gate document with OVERRIDDEN status
        WHEN parse_gate_document is called
        THEN status is OVERRIDDEN and override_reason is set."""
        # Arrange
        content = (
            "**Status**: OVERRIDDEN\n"
            "\n"
            "## Criteria\n"
            "- [ ] Spec coverage verified\n"
            "\n"
            "## Approval\n"
            "**Approved by**: {agent or user}\n"
            "**Override reason** (if applicable): Critical hotfix needed\n"
        )

        # Act
        result = gate_checker.parse_gate_document(content)

        # Assert
        assert result["status"] == "OVERRIDDEN"
        assert result["override_reason"] == "Critical hotfix needed"

    def test_parses_mixed_criteria(self) -> None:
        """GIVEN a gate document with mixed checked/unchecked criteria
        WHEN parse_gate_document is called
        THEN criteria reflect the correct checked state."""
        # Arrange
        content = (
            "**Status**: PENDING\n"
            "\n"
            "## Criteria\n"
            "- [x] First item done\n"
            "- [ ] Second item pending\n"
            "- [X] Third item done (uppercase X)\n"
        )

        # Act
        result = gate_checker.parse_gate_document(content)

        # Assert
        assert len(result["criteria"]) == 3
        assert result["criteria"][0]["checked"] is True
        assert result["criteria"][1]["checked"] is False
        assert result["criteria"][2]["checked"] is True


# ---------------------------------------------------------------------------
# Criteria checking tests
# ---------------------------------------------------------------------------

class TestAllCriteriaMet:
    """Tests for all_criteria_met()."""

    def test_all_checked(self) -> None:
        """GIVEN all criteria are checked
        WHEN all_criteria_met is called
        THEN it returns True."""
        # Arrange
        criteria = [
            {"text": "A", "checked": True},
            {"text": "B", "checked": True},
        ]

        # Act & Assert
        assert gate_checker.all_criteria_met(criteria) is True

    def test_some_unchecked(self) -> None:
        """GIVEN some criteria are unchecked
        WHEN all_criteria_met is called
        THEN it returns False."""
        # Arrange
        criteria = [
            {"text": "A", "checked": True},
            {"text": "B", "checked": False},
        ]

        # Act & Assert
        assert gate_checker.all_criteria_met(criteria) is False

    def test_empty_criteria(self) -> None:
        """GIVEN no criteria
        WHEN all_criteria_met is called
        THEN it returns False."""
        # Act & Assert
        assert gate_checker.all_criteria_met([]) is False


# ---------------------------------------------------------------------------
# Gate document generation tests
# ---------------------------------------------------------------------------

class TestGenerateGateDocument:
    """Tests for generate_gate_document()."""

    def test_generates_pending_document(self) -> None:
        """GIVEN feature name, gate type, and criteria
        WHEN generate_gate_document is called
        THEN it returns a markdown document with PENDING status."""
        # Act
        result = gate_checker.generate_gate_document(
            "user-auth", "plan-gate",
            ["Spec coverage verified", "Architecture reviewed"],
        )

        # Assert
        assert "# Gate: user-auth -- Plan Approval Gate" in result
        assert "**Status**: PENDING" in result
        assert "- [ ] Spec coverage verified" in result
        assert "- [ ] Architecture reviewed" in result

    def test_generates_with_empty_criteria(self) -> None:
        """GIVEN no criteria
        WHEN generate_gate_document is called
        THEN it includes a placeholder criterion."""
        # Act
        result = gate_checker.generate_gate_document(
            "feature-x", "release-gate", [],
        )

        # Assert
        assert "No criteria specified" in result


# ---------------------------------------------------------------------------
# Status update tests
# ---------------------------------------------------------------------------

class TestUpdateGateStatus:
    """Tests for update_gate_status()."""

    def test_updates_status(self) -> None:
        """GIVEN a document with PENDING status
        WHEN update_gate_status is called with APPROVED
        THEN the status field changes to APPROVED."""
        # Arrange
        content = "**Status**: PENDING\n"

        # Act
        result = gate_checker.update_gate_status(content, "APPROVED")

        # Assert
        assert "**Status**: APPROVED" in result
        assert "PENDING" not in result

    def test_updates_approved_by(self) -> None:
        """GIVEN a document with placeholder approved_by
        WHEN update_gate_status is called with approved_by
        THEN the approved_by field is updated."""
        # Arrange
        content = "**Approved by**: {agent or user}\n"

        # Act
        result = gate_checker.update_gate_status(
            content, "APPROVED", approved_by="Prometeo (PM)",
        )

        # Assert
        assert "**Approved by**: Prometeo (PM)" in result

    def test_updates_override_reason(self) -> None:
        """GIVEN a document with placeholder override reason
        WHEN update_gate_status is called with override_reason
        THEN the override reason is updated."""
        # Arrange
        content = "**Override reason** (if applicable): {reason}\n"

        # Act
        result = gate_checker.update_gate_status(
            content, "OVERRIDDEN", override_reason="Critical hotfix",
        )

        # Assert
        assert "**Override reason** (if applicable): Critical hotfix" in result


# ---------------------------------------------------------------------------
# Check criteria in content tests
# ---------------------------------------------------------------------------

class TestCheckCriteriaInContent:
    """Tests for check_criteria_in_content()."""

    def test_checks_all_criteria(self) -> None:
        """GIVEN unchecked criteria
        WHEN check_criteria_in_content is called with checked=True
        THEN all criteria become checked."""
        # Arrange
        content = "- [ ] First\n- [ ] Second\n"

        # Act
        result = gate_checker.check_criteria_in_content(content, checked=True)

        # Assert
        assert "- [x] First" in result
        assert "- [x] Second" in result

    def test_unchecks_all_criteria(self) -> None:
        """GIVEN checked criteria
        WHEN check_criteria_in_content is called with checked=False
        THEN all criteria become unchecked."""
        # Arrange
        content = "- [x] First\n- [X] Second\n"

        # Act
        result = gate_checker.check_criteria_in_content(content, checked=False)

        # Assert
        assert "- [ ] First" in result
        assert "- [ ] Second" in result


# ---------------------------------------------------------------------------
# File operations tests
# ---------------------------------------------------------------------------

class TestFileOperations:
    """Tests for gate file I/O operations."""

    def test_gate_file_path(self) -> None:
        """GIVEN feature and gate type
        WHEN gate_file_path is called
        THEN it returns the correct path."""
        # Act
        result = gate_checker.gate_file_path(
            Path("/tmp/gates"), "user-auth", "plan-gate",
        )

        # Assert
        assert result == Path("/tmp/gates/user-auth-plan-gate.md")

    def test_read_gate_returns_none_when_missing(self, tmp_path: Path) -> None:
        """GIVEN no gate file exists
        WHEN read_gate is called
        THEN it returns None."""
        # Act
        result = gate_checker.read_gate(tmp_path, "missing", "plan-gate")

        # Assert
        assert result is None

    def test_write_and_read_gate(self, tmp_path: Path) -> None:
        """GIVEN a gate document
        WHEN write_gate and read_gate are called
        THEN content is preserved."""
        # Arrange
        content = "# Test gate\n**Status**: PENDING\n"

        # Act
        gate_checker.write_gate(tmp_path, "test-feat", "plan-gate", content)
        result = gate_checker.read_gate(tmp_path, "test-feat", "plan-gate")

        # Assert
        assert result == content

    def test_write_creates_directory(self, tmp_path: Path) -> None:
        """GIVEN a nonexistent directory
        WHEN write_gate is called
        THEN it creates the directory."""
        # Arrange
        nested = tmp_path / "sub" / "gates"

        # Act
        gate_checker.write_gate(nested, "feat", "plan-gate", "content")

        # Assert
        assert nested.exists()


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

class TestMainCLI:
    """Integration tests for the main() entry point."""

    def test_create_gate(self, tmp_path: Path) -> None:
        """GIVEN valid create arguments
        WHEN main is called with create
        THEN exit code is 0 and gate file is created."""
        # Act
        exit_code = gate_checker.main([
            "create",
            "--feature", "user-auth",
            "--gate-type", "plan-gate",
            "--criteria", "Spec reviewed",
            "--criteria", "Architecture approved",
            "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 0
        gate_file = tmp_path / "user-auth-plan-gate.md"
        assert gate_file.exists()
        content = gate_file.read_text()
        assert "PENDING" in content
        assert "Spec reviewed" in content

    def test_check_pending_gate(self, tmp_path: Path) -> None:
        """GIVEN a pending gate
        WHEN main is called with check
        THEN exit code is 1 (not passed)."""
        # Arrange
        gate_checker.main([
            "create", "--feature", "feat", "--gate-type", "plan-gate",
            "--criteria", "Item", "--gates-dir", str(tmp_path),
        ])

        # Act
        exit_code = gate_checker.main([
            "check", "--feature", "feat", "--gate-type", "plan-gate",
            "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 1

    def test_check_approved_gate(self, tmp_path: Path) -> None:
        """GIVEN an approved gate
        WHEN main is called with check
        THEN exit code is 0 (passed)."""
        # Arrange
        gate_checker.main([
            "create", "--feature", "feat", "--gate-type", "plan-gate",
            "--criteria", "Item", "--gates-dir", str(tmp_path),
        ])
        gate_checker.main([
            "approve", "--feature", "feat", "--gate-type", "plan-gate",
            "--approved-by", "Prometeo", "--gates-dir", str(tmp_path),
        ])

        # Act
        exit_code = gate_checker.main([
            "check", "--feature", "feat", "--gate-type", "plan-gate",
            "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 0

    def test_check_missing_gate(self, tmp_path: Path) -> None:
        """GIVEN no gate file
        WHEN main is called with check
        THEN exit code is 1 (not found)."""
        # Act
        exit_code = gate_checker.main([
            "check", "--feature", "missing", "--gate-type", "plan-gate",
            "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 1

    def test_approve_gate(self, tmp_path: Path) -> None:
        """GIVEN a pending gate
        WHEN main is called with approve
        THEN exit code is 0 and gate status is APPROVED."""
        # Arrange
        gate_checker.main([
            "create", "--feature", "feat", "--gate-type", "release-gate",
            "--criteria", "Tests pass", "--gates-dir", str(tmp_path),
        ])

        # Act
        exit_code = gate_checker.main([
            "approve", "--feature", "feat", "--gate-type", "release-gate",
            "--approved-by", "Centinela (QA)", "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 0
        content = (tmp_path / "feat-release-gate.md").read_text()
        assert "APPROVED" in content
        assert "Centinela (QA)" in content

    def test_override_gate(self, tmp_path: Path) -> None:
        """GIVEN a pending gate
        WHEN main is called with override and a reason
        THEN exit code is 0 and gate status is OVERRIDDEN."""
        # Arrange
        gate_checker.main([
            "create", "--feature", "feat", "--gate-type", "plan-gate",
            "--criteria", "Criterion", "--gates-dir", str(tmp_path),
        ])

        # Act
        exit_code = gate_checker.main([
            "override", "--feature", "feat", "--gate-type", "plan-gate",
            "--override-reason", "Critical hotfix",
            "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 0
        content = (tmp_path / "feat-plan-gate.md").read_text()
        assert "OVERRIDDEN" in content
        assert "Critical hotfix" in content

    def test_create_duplicate_fails(self, tmp_path: Path) -> None:
        """GIVEN an existing gate
        WHEN main is called with create again
        THEN exit code is 2 (error)."""
        # Arrange
        gate_checker.main([
            "create", "--feature", "feat", "--gate-type", "plan-gate",
            "--gates-dir", str(tmp_path),
        ])

        # Act
        exit_code = gate_checker.main([
            "create", "--feature", "feat", "--gate-type", "plan-gate",
            "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 2

    def test_approve_missing_gate_fails(self, tmp_path: Path) -> None:
        """GIVEN no gate file
        WHEN main is called with approve
        THEN exit code is 2 (error)."""
        # Act
        exit_code = gate_checker.main([
            "approve", "--feature", "missing", "--gate-type", "plan-gate",
            "--approved-by", "X", "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 2

    def test_override_missing_gate_fails(self, tmp_path: Path) -> None:
        """GIVEN no gate file
        WHEN main is called with override
        THEN exit code is 2 (error)."""
        # Act
        exit_code = gate_checker.main([
            "override", "--feature", "missing", "--gate-type", "plan-gate",
            "--override-reason", "Reason", "--gates-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 2
