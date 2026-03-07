"""Tests for tools/growth-tracker.py -- growth tracking and pre-launch gate verification.

Tests follow FIRST principles and Arrange-Act-Assert pattern.
Covers: GrowthPhase determination, LaunchGate checking, metrics parsing,
weekly log recording, and CLI subcommands.
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import module under test (follows established project pattern)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = PROJECT_ROOT / "tools"
SCRIPT = str(TOOLS_DIR / "growth-tracker.py")

sys.path.insert(0, str(TOOLS_DIR))
gt = importlib.import_module("growth-tracker")


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Run growth-tracker.py as subprocess and return result."""
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )


# ---------------------------------------------------------------------------
# GrowthPhase tests
# ---------------------------------------------------------------------------
class TestGrowthPhase:
    """Test growth phase determination from metrics."""

    def test_phase_0_when_stars_below_10(self):
        # Arrange
        metrics = gt.GrowthMetrics(stars=5, forks=0, repo_age_days=15)

        # Act
        phase = gt.determine_phase(metrics)

        # Assert
        assert phase == gt.GrowthPhase.PRE_LAUNCH

    def test_phase_1_when_stars_between_10_and_50(self):
        # Arrange
        metrics = gt.GrowthMetrics(stars=25, forks=3, repo_age_days=35)

        # Act
        phase = gt.determine_phase(metrics)

        # Assert
        assert phase == gt.GrowthPhase.SOFT_LAUNCH

    def test_phase_2_when_stars_between_50_and_200(self):
        # Arrange
        metrics = gt.GrowthMetrics(stars=120, forks=15, repo_age_days=60)

        # Act
        phase = gt.determine_phase(metrics)

        # Assert
        assert phase == gt.GrowthPhase.CONTENT_MOMENTUM

    def test_phase_3_when_stars_above_200(self):
        # Arrange
        metrics = gt.GrowthMetrics(stars=350, forks=40, repo_age_days=120)

        # Act
        phase = gt.determine_phase(metrics)

        # Assert
        assert phase == gt.GrowthPhase.COMMUNITY

    def test_phase_0_when_repo_too_young_despite_stars(self):
        # Arrange -- even with 15 stars, repo age < 30 days stays in pre-launch
        metrics = gt.GrowthMetrics(stars=15, forks=2, repo_age_days=20)

        # Act
        phase = gt.determine_phase(metrics)

        # Assert
        assert phase == gt.GrowthPhase.PRE_LAUNCH


# ---------------------------------------------------------------------------
# LaunchGate tests
# ---------------------------------------------------------------------------
class TestLaunchGates:
    """Test pre-launch readiness gate checking."""

    def test_all_gates_pass_returns_all_passed(self):
        # Arrange
        gates = [
            gt.LaunchGate(name="Install verified", passed=True, detail="OK"),
            gt.LaunchGate(name="README above fold", passed=True, detail="OK"),
        ]

        # Act
        result = gt.evaluate_gates(gates)

        # Assert
        assert result["passed"] is True
        assert result["total"] == 2
        assert result["passing"] == 2

    def test_failing_gate_returns_not_passed(self):
        # Arrange
        gates = [
            gt.LaunchGate(name="Install verified", passed=True, detail="OK"),
            gt.LaunchGate(
                name="README above fold",
                passed=False,
                detail="Methodology not in first 200 words",
            ),
        ]

        # Act
        result = gt.evaluate_gates(gates)

        # Assert
        assert result["passed"] is False
        assert result["total"] == 2
        assert result["passing"] == 1
        assert result["failing"][0]["name"] == "README above fold"

    def test_empty_gates_returns_not_passed(self):
        # Act
        result = gt.evaluate_gates([])

        # Assert
        assert result["passed"] is False
        assert result["total"] == 0


# ---------------------------------------------------------------------------
# Metrics parsing tests
# ---------------------------------------------------------------------------
class TestMetricsParsing:
    """Test parsing of growth-log.md table format."""

    def test_parse_growth_log_single_entry(self):
        # Arrange
        content = textwrap.dedent("""\
            # Growth Log

            | Date | Stars | Forks | Visitors | Clones | Top Referrers | Content Published | Curated List Updates | Notes |
            |------|-------|-------|----------|--------|---------------|-------------------|---------------------|-------|
            | 2026-03-04 | 1 | 0 | \u2014 | \u2014 | \u2014 | \u2014 | ccplugins PR #46 open | Baseline entry. |
        """)

        # Act
        entries = gt.parse_growth_log(content)

        # Assert
        assert len(entries) == 1
        assert entries[0]["date"] == "2026-03-04"
        assert entries[0]["stars"] == 1
        assert entries[0]["forks"] == 0

    def test_parse_growth_log_multiple_entries(self):
        # Arrange
        content = textwrap.dedent("""\
            # Growth Log

            | Date | Stars | Forks | Visitors | Clones | Top Referrers | Content Published | Curated List Updates | Notes |
            |------|-------|-------|----------|--------|---------------|-------------------|---------------------|-------|
            | 2026-03-04 | 1 | 0 | \u2014 | \u2014 | \u2014 | \u2014 | Baseline | First entry |
            | 2026-03-11 | 5 | 1 | 20 | 8 | github.com | \u2014 | \u2014 | Growing |
        """)

        # Act
        entries = gt.parse_growth_log(content)

        # Assert
        assert len(entries) == 2
        assert entries[1]["stars"] == 5
        assert entries[1]["forks"] == 1

    def test_parse_growth_log_handles_dash_as_zero(self):
        # Arrange
        content = textwrap.dedent("""\
            # Growth Log

            | Date | Stars | Forks | Visitors | Clones | Top Referrers | Content Published | Curated List Updates | Notes |
            |------|-------|-------|----------|--------|---------------|-------------------|---------------------|-------|
            | 2026-03-04 | 1 | \u2014 | \u2014 | \u2014 | \u2014 | \u2014 | \u2014 | \u2014 |
        """)

        # Act
        entries = gt.parse_growth_log(content)

        # Assert
        assert entries[0]["forks"] == 0
        assert entries[0]["visitors"] == 0
        assert entries[0]["clones"] == 0

    def test_parse_empty_content_returns_empty_list(self):
        # Act
        entries = gt.parse_growth_log("")

        # Assert
        assert entries == []


# ---------------------------------------------------------------------------
# Format log entry tests
# ---------------------------------------------------------------------------
class TestFormatLogEntry:
    """Test formatting a metrics entry as a growth-log table row."""

    def test_format_entry_as_table_row(self):
        # Arrange
        entry = {
            "date": "2026-03-11",
            "stars": 5,
            "forks": 1,
            "visitors": 20,
            "clones": 8,
            "top_referrers": "github.com",
            "content_published": "Show HN",
            "curated_list_updates": "ccplugins accepted",
            "notes": "Good week",
        }

        # Act
        row = gt.format_log_entry(entry)

        # Assert
        assert "2026-03-11" in row
        assert "5" in row
        assert "Show HN" in row

    def test_format_entry_with_zero_values_uses_dash(self):
        # Arrange
        entry = {
            "date": "2026-03-11",
            "stars": 0,
            "forks": 0,
            "visitors": 0,
            "clones": 0,
            "top_referrers": "",
            "content_published": "",
            "curated_list_updates": "",
            "notes": "",
        }

        # Act
        row = gt.format_log_entry(entry)

        # Assert
        # Zero numeric values and empty strings render as em-dash placeholders
        assert "\u2014" in row


# ---------------------------------------------------------------------------
# README gate checks
# ---------------------------------------------------------------------------
class TestReadmeGateChecks:
    """Test README content verification for pre-launch gates."""

    def test_check_methodology_above_fold_passes(self):
        # Arrange
        readme_content = textwrap.dedent("""\
            # Agent Triforce

            A system that applies checklist methodology from The Checklist Manifesto
            by Atul Gawande and Boeing's checklist engineering to AI agents.

            ## Install
            Some install instructions here.
        """)

        # Act
        gate = gt.check_readme_methodology(readme_content)

        # Assert
        assert gate.passed is True

    def test_check_methodology_below_fold_fails(self):
        # Arrange -- methodology mentioned after 200+ words of other content
        filler = " ".join(["word"] * 250)
        readme_content = (
            f"# Agent Triforce\n\n{filler}\n\n"
            "## Methodology\nChecklist methodology here."
        )

        # Act
        gate = gt.check_readme_methodology(readme_content)

        # Assert
        assert gate.passed is False

    def test_check_github_topics_all_present(self):
        # Arrange
        topics = [
            "claude-code", "multi-agent", "developer-tools",
            "prompt-engineering", "checklist", "claude-code-plugin",
            "code-review", "security-audit",
        ]

        # Act
        gate = gt.check_github_topics(topics)

        # Assert
        assert gate.passed is True

    def test_check_github_topics_missing_some(self):
        # Arrange
        topics = ["claude-code", "multi-agent"]

        # Act
        gate = gt.check_github_topics(topics)

        # Assert
        assert gate.passed is False
        assert "missing" in gate.detail.lower()


# ---------------------------------------------------------------------------
# Milestone gate tests
# ---------------------------------------------------------------------------
class TestMilestoneGates:
    """Test milestone-based action unlocking from growth-plan Appendix E."""

    def test_unlocked_actions_for_pre_launch(self):
        # Arrange
        metrics = gt.GrowthMetrics(stars=1, forks=0, repo_age_days=12)

        # Act
        actions = gt.get_unlocked_actions(metrics)

        # Assert
        assert any(
            "pre-launch" in a.lower() or "readiness" in a.lower()
            for a in actions
        )

    def test_unlocked_actions_for_30_days_10_stars(self):
        # Arrange
        metrics = gt.GrowthMetrics(stars=12, forks=2, repo_age_days=32)

        # Act
        actions = gt.get_unlocked_actions(metrics)

        # Assert
        assert any("hesreallyhim" in a.lower() for a in actions)

    def test_unlocked_actions_for_300_stars(self):
        # Arrange
        metrics = gt.GrowthMetrics(stars=350, forks=30, repo_age_days=120)

        # Act
        actions = gt.get_unlocked_actions(metrics)

        # Assert
        assert any("product hunt" in a.lower() for a in actions)

    def test_locked_milestones_shows_blockers(self):
        # Arrange
        metrics = gt.GrowthMetrics(stars=5, forks=0, repo_age_days=20)

        # Act
        locked = gt.get_locked_milestones(metrics)

        # Assert
        assert len(locked) > 0
        assert all("blockers" in m for m in locked)
        assert all(len(m["blockers"]) > 0 for m in locked)


# ---------------------------------------------------------------------------
# _parse_numeric tests
# ---------------------------------------------------------------------------
class TestParseNumeric:
    """Test numeric parsing edge cases."""

    def test_parse_integer(self):
        assert gt._parse_numeric("42") == 42

    def test_parse_with_commas(self):
        assert gt._parse_numeric("1,234") == 1234

    def test_parse_dash(self):
        assert gt._parse_numeric("\u2014") == 0

    def test_parse_hyphen(self):
        assert gt._parse_numeric("-") == 0

    def test_parse_na(self):
        assert gt._parse_numeric("N/A") == 0

    def test_parse_empty(self):
        assert gt._parse_numeric("") == 0

    def test_parse_whitespace(self):
        assert gt._parse_numeric("  ") == 0

    def test_parse_non_numeric(self):
        assert gt._parse_numeric("abc") == 0


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------
class TestCLI:
    """Test CLI subcommands."""

    def test_status_subcommand_outputs_json(self):
        # Act
        result = run_cli("status")

        # Assert
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "phase" in data
        assert "metrics" in data

    def test_check_subcommand_outputs_json(self):
        # Act
        result = run_cli("check")

        # Assert
        assert result.returncode in (0, 1)  # 0 = all pass, 1 = some fail
        data = json.loads(result.stdout)
        assert "passed" in data
        assert "gates" in data

    def test_milestones_subcommand_outputs_json(self):
        # Act
        result = run_cli("milestones")

        # Assert
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "unlocked" in data
        assert "locked" in data

    def test_invalid_subcommand_exits_with_error(self):
        # Act
        result = run_cli("nonexistent")

        # Assert
        assert result.returncode != 0

    def test_no_subcommand_exits_with_help(self):
        # Act
        result = run_cli()

        # Assert
        assert result.returncode == 2
