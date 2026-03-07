#!/usr/bin/env python3
"""Tests for tools/session-tracker.py.

Tests follow TDD Red-Green-Refactor with Arrange-Act-Assert pattern.
Covers: _count_findings(), _compute_handoffs(), _estimate_cost(),
_build_report(), and CLI commands.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Dict, List
from unittest.mock import patch

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

session_tracker = importlib.import_module("session-tracker")


# ---------------------------------------------------------------------------
# _count_findings tests
# ---------------------------------------------------------------------------


class TestCountFindings:
    """Tests for _count_findings() -- finding attribution per agent."""

    def test_attributes_security_review_to_centinela(self, tmp_path: Path) -> None:
        """GIVEN a review file named 'security-audit-trail.md' with findings
        WHEN _count_findings is called
        THEN findings are attributed to centinela-qa."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "security-audit-2026-03-01.md").write_text(
            "## Findings\n**[C-1]** Critical issue\n**[W-1]** Warning\n"
        )

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts["centinela-qa"] == 2
        assert counts["forja-dev"] == 0
        assert counts["prometeo-pm"] == 0

    def test_attributes_code_health_to_centinela(self, tmp_path: Path) -> None:
        """GIVEN a code-health review with findings
        WHEN _count_findings is called
        THEN findings are attributed to centinela-qa."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "code-health-2026-03-05.md").write_text(
            "**[W-1]** Warning one\n**[S-1]** Suggestion\n"
        )

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts["centinela-qa"] == 2

    def test_attributes_release_check_to_centinela(self, tmp_path: Path) -> None:
        """GIVEN a release-check review with findings
        WHEN _count_findings is called
        THEN findings are attributed to centinela-qa."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "release-check-0.5.0-2026-03-06.md").write_text(
            "**[C-1]** Criterion fail\n"
        )

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts["centinela-qa"] == 1

    def test_attributes_business_review_to_prometeo(self, tmp_path: Path) -> None:
        """GIVEN a business-review file with findings
        WHEN _count_findings is called
        THEN findings are attributed to prometeo-pm."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "business-review-auth-2026-03-01.md").write_text(
            "**[W-1]** Business concern\n**[W-2]** Scope issue\n"
        )

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts["prometeo-pm"] == 2
        assert counts["centinela-qa"] == 0

    def test_attributes_generic_review_to_forja(self, tmp_path: Path) -> None:
        """GIVEN a review file with a generic name (not security/code-health/release/business)
        WHEN _count_findings is called
        THEN findings are attributed to forja-dev."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "user-auth-review.md").write_text(
            "**[W-1]** Implementation issue\n"
        )

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts["forja-dev"] == 1

    def test_skips_readme(self, tmp_path: Path) -> None:
        """GIVEN a README.md in the reviews directory
        WHEN _count_findings is called
        THEN it is skipped."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "README.md").write_text("**[C-1]** Fake finding\n")

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts["centinela-qa"] == 0
        assert counts["forja-dev"] == 0
        assert counts["prometeo-pm"] == 0

    def test_empty_review_directory(self, tmp_path: Path) -> None:
        """GIVEN an empty reviews directory
        WHEN _count_findings is called
        THEN all counts are zero."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts == {"prometeo-pm": 0, "forja-dev": 0, "centinela-qa": 0}

    def test_nonexistent_review_directory(self, tmp_path: Path) -> None:
        """GIVEN a review directory that does not exist
        WHEN _count_findings is called
        THEN all counts are zero."""
        # Arrange
        review_dir = tmp_path / "nonexistent"

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts == {"prometeo-pm": 0, "forja-dev": 0, "centinela-qa": 0}

    def test_deduplicates_finding_ids(self, tmp_path: Path) -> None:
        """GIVEN a review file where the same finding ID appears multiple times
        WHEN _count_findings is called
        THEN each unique finding is counted only once."""
        # Arrange
        review_dir = tmp_path / "reviews"
        review_dir.mkdir()
        (review_dir / "code-health-2026-03-05.md").write_text(
            "**[W-1]** First mention\n"
            "Later reference to **[W-1]** again\n"
            "**[W-2]** Different finding\n"
        )

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", review_dir):
            counts = session_tracker._count_findings()

        # Assert
        assert counts["centinela-qa"] == 2


# ---------------------------------------------------------------------------
# _compute_handoffs tests
# ---------------------------------------------------------------------------


class TestComputeHandoffs:
    """Tests for _compute_handoffs() -- counting agent transitions."""

    def test_counts_agent_transitions(self) -> None:
        """GIVEN phases with agent changes
        WHEN _compute_handoffs is called
        THEN it counts the transitions."""
        # Arrange
        runs = [{
            "phases": [
                {"agent": "prometeo-pm"},
                {"agent": "forja-dev"},
                {"agent": "centinela-qa"},
            ],
        }]

        # Act
        result = session_tracker._compute_handoffs(runs)

        # Assert
        assert result == 2

    def test_no_transitions_same_agent(self) -> None:
        """GIVEN phases with the same agent throughout
        WHEN _compute_handoffs is called
        THEN handoffs is zero."""
        # Arrange
        runs = [{
            "phases": [
                {"agent": "forja-dev"},
                {"agent": "forja-dev"},
                {"agent": "forja-dev"},
            ],
        }]

        # Act
        result = session_tracker._compute_handoffs(runs)

        # Assert
        assert result == 0

    def test_empty_runs(self) -> None:
        """GIVEN no workflow runs
        WHEN _compute_handoffs is called
        THEN handoffs is zero."""
        # Act
        result = session_tracker._compute_handoffs([])

        # Assert
        assert result == 0

    def test_single_phase_no_handoff(self) -> None:
        """GIVEN a run with only one phase
        WHEN _compute_handoffs is called
        THEN handoffs is zero."""
        # Arrange
        runs = [{"phases": [{"agent": "prometeo-pm"}]}]

        # Act
        result = session_tracker._compute_handoffs(runs)

        # Assert
        assert result == 0

    def test_multiple_runs(self) -> None:
        """GIVEN multiple workflow runs each with transitions
        WHEN _compute_handoffs is called
        THEN it sums handoffs across all runs."""
        # Arrange
        runs = [
            {"phases": [{"agent": "prometeo-pm"}, {"agent": "forja-dev"}]},
            {"phases": [{"agent": "forja-dev"}, {"agent": "centinela-qa"}]},
        ]

        # Act
        result = session_tracker._compute_handoffs(runs)

        # Assert
        assert result == 2


# ---------------------------------------------------------------------------
# _estimate_cost tests
# ---------------------------------------------------------------------------


class TestEstimateCost:
    """Tests for _estimate_cost() -- cost calculation from tokens and pricing."""

    def test_basic_cost_calculation(self) -> None:
        """GIVEN known token counts, model mapping, and pricing
        WHEN _estimate_cost is called
        THEN it returns the correct cost."""
        # Arrange
        agent_tokens = {"forja-dev": 1_000_000}
        agent_models = {"forja-dev": "sonnet"}
        pricing = {"sonnet": {"input": 3.00, "output": 15.00}}

        # Act
        cost = session_tracker._estimate_cost(agent_tokens, agent_models, pricing)

        # Assert
        # 600K input tokens * $3/1M = $1.80
        # 400K output tokens * $15/1M = $6.00
        # Total = $7.80
        assert abs(cost - 7.80) < 0.01

    def test_zero_tokens_zero_cost(self) -> None:
        """GIVEN zero tokens
        WHEN _estimate_cost is called
        THEN cost is zero."""
        # Arrange
        agent_tokens = {"forja-dev": 0}
        agent_models = {"forja-dev": "sonnet"}
        pricing = {"sonnet": {"input": 3.00, "output": 15.00}}

        # Act
        cost = session_tracker._estimate_cost(agent_tokens, agent_models, pricing)

        # Assert
        assert cost == 0.0

    def test_multiple_agents(self) -> None:
        """GIVEN multiple agents with different models
        WHEN _estimate_cost is called
        THEN costs are summed across agents."""
        # Arrange
        agent_tokens = {
            "prometeo-pm": 100_000,
            "forja-dev": 100_000,
        }
        agent_models = {
            "prometeo-pm": "haiku",
            "forja-dev": "opus",
        }
        pricing = {
            "haiku": {"input": 0.25, "output": 1.25},
            "opus": {"input": 15.00, "output": 75.00},
        }

        # Act
        cost = session_tracker._estimate_cost(agent_tokens, agent_models, pricing)

        # Assert
        # haiku: 60K * 0.25/1M + 40K * 1.25/1M = 0.015 + 0.050 = 0.065
        # opus:  60K * 15/1M + 40K * 75/1M = 0.900 + 3.000 = 3.900
        # Total = 3.965
        assert abs(cost - 3.965) < 0.01

    def test_unknown_agent_defaults_to_sonnet(self) -> None:
        """GIVEN an agent not in the model mapping
        WHEN _estimate_cost is called
        THEN it defaults to sonnet pricing."""
        # Arrange
        agent_tokens = {"unknown-agent": 1_000_000}
        agent_models = {}
        pricing = {"sonnet": {"input": 3.00, "output": 15.00}}

        # Act
        cost = session_tracker._estimate_cost(agent_tokens, agent_models, pricing)

        # Assert
        assert abs(cost - 7.80) < 0.01


# ---------------------------------------------------------------------------
# _build_report tests
# ---------------------------------------------------------------------------


class TestBuildReport:
    """Tests for _build_report() -- report generation from workflow state."""

    def test_report_with_no_state(self) -> None:
        """GIVEN no workflow state (None)
        WHEN _build_report is called
        THEN it returns a report with zero values."""
        # Act
        with patch.object(session_tracker, "REVIEW_DIR", Path("/nonexistent")):
            report = session_tracker._build_report(None)

        # Assert
        assert report.total_estimated_cost == "$0.00"
        assert report.workflow_phases == 0
        assert report.handoffs_completed == 0

    def test_report_with_current_run(self) -> None:
        """GIVEN a workflow state with a current run and phases
        WHEN _build_report is called
        THEN phase counts and tokens are calculated."""
        # Arrange
        state = {
            "currentRun": {
                "phases": [
                    {"agent": "prometeo-pm", "phase": "SIGN_IN"},
                    {"agent": "forja-dev", "phase": "IN_PROGRESS"},
                ],
            },
            "history": [],
        }

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", Path("/nonexistent")):
            report = session_tracker._build_report(state)

        # Assert
        assert report.workflow_phases == 2
        assert report.handoffs_completed == 1
        assert report.agents["prometeo-pm"].estimated_tokens > 0
        assert report.agents["forja-dev"].estimated_tokens > 0

    def test_report_aggregates_history(self) -> None:
        """GIVEN a workflow state with history runs
        WHEN _build_report is called
        THEN phases from all runs are counted."""
        # Arrange
        state = {
            "currentRun": None,
            "history": [
                {
                    "phases": [
                        {"agent": "prometeo-pm", "phase": "SIGN_IN"},
                    ],
                },
                {
                    "phases": [
                        {"agent": "forja-dev", "phase": "IN_PROGRESS"},
                        {"agent": "centinela-qa", "phase": "TIME_OUT"},
                    ],
                },
            ],
        }

        # Act
        with patch.object(session_tracker, "REVIEW_DIR", Path("/nonexistent")):
            report = session_tracker._build_report(state)

        # Assert
        assert report.workflow_phases == 3


# ---------------------------------------------------------------------------
# _report_to_dict tests
# ---------------------------------------------------------------------------


class TestReportToDict:
    """Tests for _report_to_dict() -- serialization."""

    def test_serializes_all_fields(self) -> None:
        """GIVEN a SessionReport with populated fields
        WHEN _report_to_dict is called
        THEN all fields appear in the output dict."""
        # Arrange
        report = session_tracker.SessionReport(
            session_id="test-123",
            date="2026-03-07T00:00:00+00:00",
            total_estimated_cost="$1.50",
            workflow_phases=3,
            handoffs_completed=2,
        )
        report.agents["forja-dev"] = session_tracker.AgentMetrics(
            estimated_tokens=5000,
            time_ms=10000,
            checklists_run=2,
            findings_logged=1,
        )

        # Act
        result = session_tracker._report_to_dict(report)

        # Assert
        assert result["sessionId"] == "test-123"
        assert result["totalEstimatedCost"] == "$1.50"
        assert result["workflowPhases"] == 3
        assert result["handoffsCompleted"] == 2
        assert result["agents"]["forja-dev"]["estimatedTokens"] == 5000
        assert result["agents"]["forja-dev"]["checklistsRun"] == 2


# ---------------------------------------------------------------------------
# CLI command tests
# ---------------------------------------------------------------------------


class TestCLICommands:
    """Tests for CLI command functions."""

    def test_cmd_report_returns_zero(self) -> None:
        """GIVEN no workflow state file
        WHEN cmd_report is called
        THEN it returns 0."""
        # Act
        with patch.object(session_tracker, "WORKFLOW_STATE_FILE", Path("/nonexistent")):
            with patch.object(session_tracker, "REVIEW_DIR", Path("/nonexistent")):
                with patch.object(session_tracker, "ROUTING_CONFIG_FILE", Path("/nonexistent")):
                    result = session_tracker.cmd_report(pretty=False)

        # Assert
        assert result == 0

    def test_cmd_summary_returns_zero(self) -> None:
        """GIVEN no workflow state file
        WHEN cmd_summary is called
        THEN it returns 0."""
        # Act
        with patch.object(session_tracker, "WORKFLOW_STATE_FILE", Path("/nonexistent")):
            with patch.object(session_tracker, "REVIEW_DIR", Path("/nonexistent")):
                with patch.object(session_tracker, "ROUTING_CONFIG_FILE", Path("/nonexistent")):
                    result = session_tracker.cmd_summary()

        # Assert
        assert result == 0

    def test_cmd_export_creates_file(self, tmp_path: Path) -> None:
        """GIVEN a valid analytics directory
        WHEN cmd_export is called
        THEN it creates a session JSON file."""
        # Arrange
        analytics_dir = tmp_path / "analytics"

        # Act
        with patch.object(session_tracker, "WORKFLOW_STATE_FILE", Path("/nonexistent")):
            with patch.object(session_tracker, "REVIEW_DIR", Path("/nonexistent")):
                with patch.object(session_tracker, "ROUTING_CONFIG_FILE", Path("/nonexistent")):
                    with patch.object(session_tracker, "ANALYTICS_DIR", analytics_dir):
                        result = session_tracker.cmd_export()

        # Assert
        assert result == 0
        assert analytics_dir.exists()
        files = list(analytics_dir.glob("session-*.json"))
        assert len(files) == 1
        data = json.loads(files[0].read_text())
        assert "sessionId" in data


# ---------------------------------------------------------------------------
# Pricing loader tests
# ---------------------------------------------------------------------------


class TestLoadPricing:
    """Tests for _load_pricing() and _load_agent_models()."""

    def test_returns_defaults_when_no_config(self) -> None:
        """GIVEN no .agent-routing.json
        WHEN _load_pricing is called
        THEN it returns DEFAULT_PRICING."""
        # Act
        with patch.object(session_tracker, "ROUTING_CONFIG_FILE", Path("/nonexistent")):
            pricing = session_tracker._load_pricing()

        # Assert
        assert pricing == session_tracker.DEFAULT_PRICING

    def test_returns_defaults_when_invalid_json(self, tmp_path: Path) -> None:
        """GIVEN an invalid .agent-routing.json
        WHEN _load_pricing is called
        THEN it returns DEFAULT_PRICING."""
        # Arrange
        config_file = tmp_path / ".agent-routing.json"
        config_file.write_text("not valid json")

        # Act
        with patch.object(session_tracker, "ROUTING_CONFIG_FILE", config_file):
            pricing = session_tracker._load_pricing()

        # Assert
        assert pricing == session_tracker.DEFAULT_PRICING

    def test_loads_custom_pricing(self, tmp_path: Path) -> None:
        """GIVEN a valid .agent-routing.json with pricing
        WHEN _load_pricing is called
        THEN it returns the custom pricing."""
        # Arrange
        config_file = tmp_path / ".agent-routing.json"
        custom_pricing = {"custom-model": {"input": 1.00, "output": 5.00}}
        config_file.write_text(json.dumps({"pricing": custom_pricing}))

        # Act
        with patch.object(session_tracker, "ROUTING_CONFIG_FILE", config_file):
            pricing = session_tracker._load_pricing()

        # Assert
        assert pricing == custom_pricing

    def test_load_agent_models_defaults(self) -> None:
        """GIVEN no config file
        WHEN _load_agent_models is called
        THEN it returns DEFAULT_AGENT_MODELS."""
        # Act
        with patch.object(session_tracker, "ROUTING_CONFIG_FILE", Path("/nonexistent")):
            models = session_tracker._load_agent_models()

        # Assert
        assert models == session_tracker.DEFAULT_AGENT_MODELS

    def test_load_agent_models_from_config(self, tmp_path: Path) -> None:
        """GIVEN a config with routes
        WHEN _load_agent_models is called
        THEN it merges with defaults."""
        # Arrange
        config_file = tmp_path / ".agent-routing.json"
        config_file.write_text(json.dumps({
            "routes": {
                "forja-dev": {"model": "opus"},
            },
        }))

        # Act
        with patch.object(session_tracker, "ROUTING_CONFIG_FILE", config_file):
            models = session_tracker._load_agent_models()

        # Assert
        assert models["forja-dev"] == "opus"
        assert models["prometeo-pm"] == "sonnet"
