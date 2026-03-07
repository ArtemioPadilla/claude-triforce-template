#!/usr/bin/env python3
"""Tests for tools/workflow-tracker.py.

Tests follow TDD Red-Green-Refactor with Arrange-Act-Assert pattern.
Covers: start, phase, checklist, blocker, complete, status, history
subcommands and serialization round-trips.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Dict
from unittest.mock import patch

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

workflow_tracker = importlib.import_module("workflow-tracker")


# ---------------------------------------------------------------------------
# Serialization round-trip tests
# ---------------------------------------------------------------------------


class TestSerialization:
    """Tests for state <-> dict conversion."""

    def test_empty_state_round_trip(self) -> None:
        """GIVEN an empty WorkflowState
        WHEN converted to dict and back
        THEN the state is preserved."""
        # Arrange
        state = workflow_tracker.WorkflowState()

        # Act
        as_dict = workflow_tracker._state_to_dict(state)
        restored = workflow_tracker._dict_to_state(as_dict)

        # Assert
        assert restored.version == state.version
        assert restored.currentRun is None
        assert restored.history == []

    def test_full_state_round_trip(self) -> None:
        """GIVEN a WorkflowState with a run, phases, and checklists
        WHEN converted to dict and back
        THEN all data is preserved."""
        # Arrange
        item = workflow_tracker.ChecklistItem(text="Check identity", passed=True)
        checklist = workflow_tracker.Checklist(name="SIGN IN", items=[item])
        phase = workflow_tracker.Phase(
            agent="forja-dev",
            phase="SIGN_IN",
            startedAt="2026-03-07T00:00:00+00:00",
            completedAt="2026-03-07T00:01:00+00:00",
            checklists=[checklist],
        )
        run = workflow_tracker.WorkflowRun(
            id="run-123",
            feature="test-feature",
            startedAt="2026-03-07T00:00:00+00:00",
            phases=[phase],
            currentAgent="forja-dev",
            currentPhase="SIGN_IN",
            blockers=["Missing API key"],
        )
        state = workflow_tracker.WorkflowState(currentRun=run)

        # Act
        as_dict = workflow_tracker._state_to_dict(state)
        restored = workflow_tracker._dict_to_state(as_dict)

        # Assert
        assert restored.currentRun is not None
        assert restored.currentRun.id == "run-123"
        assert restored.currentRun.feature == "test-feature"
        assert len(restored.currentRun.phases) == 1
        assert restored.currentRun.phases[0].agent == "forja-dev"
        assert len(restored.currentRun.phases[0].checklists) == 1
        assert restored.currentRun.phases[0].checklists[0].name == "SIGN IN"
        assert restored.currentRun.phases[0].checklists[0].items[0].passed is True
        assert restored.currentRun.blockers == ["Missing API key"]

    def test_history_round_trip(self) -> None:
        """GIVEN a state with completed runs in history
        WHEN round-tripped through serialization
        THEN history is preserved."""
        # Arrange
        run = workflow_tracker.WorkflowRun(
            id="run-old",
            feature="old-feature",
            startedAt="2026-01-01T00:00:00+00:00",
            completedAt="2026-01-01T01:00:00+00:00",
        )
        state = workflow_tracker.WorkflowState(history=[run])

        # Act
        as_dict = workflow_tracker._state_to_dict(state)
        restored = workflow_tracker._dict_to_state(as_dict)

        # Assert
        assert len(restored.history) == 1
        assert restored.history[0].id == "run-old"
        assert restored.history[0].completedAt == "2026-01-01T01:00:00+00:00"


# ---------------------------------------------------------------------------
# File I/O tests
# ---------------------------------------------------------------------------


class TestFileIO:
    """Tests for _read_state() and _write_state()."""

    def test_read_returns_fresh_state_when_missing(self, tmp_path: Path) -> None:
        """GIVEN no state file on disk
        WHEN _read_state is called
        THEN it returns a fresh WorkflowState."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"

        # Act
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            state = workflow_tracker._read_state()

        # Assert
        assert state.currentRun is None
        assert state.history == []

    def test_write_then_read_preserves_state(self, tmp_path: Path) -> None:
        """GIVEN a WorkflowState written to disk
        WHEN _read_state is called
        THEN the same state is restored."""
        # Arrange
        state_file = tmp_path / "docs" / "workflow-state.json"
        run = workflow_tracker.WorkflowRun(
            id="run-test",
            feature="test",
            startedAt="2026-03-07T00:00:00+00:00",
        )
        state = workflow_tracker.WorkflowState(currentRun=run)

        # Act
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker._write_state(state)
            restored = workflow_tracker._read_state()

        # Assert
        assert restored.currentRun is not None
        assert restored.currentRun.id == "run-test"

    def test_read_handles_corrupt_json(self, tmp_path: Path) -> None:
        """GIVEN a corrupt state file on disk
        WHEN _read_state is called
        THEN it returns a fresh WorkflowState."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        state_file.write_text("not json {{{")

        # Act
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            state = workflow_tracker._read_state()

        # Assert
        assert state.currentRun is None


# ---------------------------------------------------------------------------
# cmd_start tests
# ---------------------------------------------------------------------------


class TestCmdStart:
    """Tests for cmd_start() -- starting a new workflow run."""

    def test_starts_new_run(self, tmp_path: Path) -> None:
        """GIVEN no active run
        WHEN cmd_start is called
        THEN it creates a new run and returns 0."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"

        # Act
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            result = workflow_tracker.cmd_start("my-feature")

        # Assert
        assert result == 0
        state = json.loads(state_file.read_text())
        assert state["currentRun"]["feature"] == "my-feature"

    def test_fails_when_run_already_active(self, tmp_path: Path) -> None:
        """GIVEN an active run exists
        WHEN cmd_start is called
        THEN it returns 1 (error)."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("first-feature")

            # Act
            result = workflow_tracker.cmd_start("second-feature")

        # Assert
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_phase tests
# ---------------------------------------------------------------------------


class TestCmdPhase:
    """Tests for cmd_phase() -- updating workflow phase."""

    def test_adds_phase_to_current_run(self, tmp_path: Path) -> None:
        """GIVEN an active run
        WHEN cmd_phase is called with valid agent and phase
        THEN it adds the phase and returns 0."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test-feature")

            # Act
            result = workflow_tracker.cmd_phase("prometeo-pm", "SIGN_IN")

        # Assert
        assert result == 0
        state = json.loads(state_file.read_text())
        assert len(state["currentRun"]["phases"]) == 1
        assert state["currentRun"]["phases"][0]["agent"] == "prometeo-pm"
        assert state["currentRun"]["phases"][0]["phase"] == "SIGN_IN"

    def test_closes_previous_phase_on_transition(self, tmp_path: Path) -> None:
        """GIVEN an active phase
        WHEN cmd_phase is called again
        THEN the previous phase gets a completedAt timestamp."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test-feature")
            workflow_tracker.cmd_phase("prometeo-pm", "SIGN_IN")

            # Act
            workflow_tracker.cmd_phase("forja-dev", "IN_PROGRESS")

        # Assert
        state = json.loads(state_file.read_text())
        assert state["currentRun"]["phases"][0]["completedAt"] is not None
        assert state["currentRun"]["phases"][1]["completedAt"] is None

    def test_fails_without_active_run(self, tmp_path: Path) -> None:
        """GIVEN no active run
        WHEN cmd_phase is called
        THEN it returns 1."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"

        # Act
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            result = workflow_tracker.cmd_phase("forja-dev", "SIGN_IN")

        # Assert
        assert result == 1

    def test_rejects_invalid_agent(self, tmp_path: Path) -> None:
        """GIVEN an active run
        WHEN cmd_phase is called with an invalid agent name
        THEN it returns 1."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")

            # Act
            result = workflow_tracker.cmd_phase("invalid-agent", "SIGN_IN")

        # Assert
        assert result == 1

    def test_rejects_invalid_phase(self, tmp_path: Path) -> None:
        """GIVEN an active run
        WHEN cmd_phase is called with an invalid phase name
        THEN it returns 1."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")

            # Act
            result = workflow_tracker.cmd_phase("forja-dev", "INVALID_PHASE")

        # Assert
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_checklist tests
# ---------------------------------------------------------------------------


class TestCmdChecklist:
    """Tests for cmd_checklist() -- recording checklist results."""

    def test_registers_checklist(self, tmp_path: Path) -> None:
        """GIVEN an active phase
        WHEN cmd_checklist is called with a name
        THEN the checklist is registered on the phase."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")
            workflow_tracker.cmd_phase("forja-dev", "SIGN_IN")

            # Act
            result = workflow_tracker.cmd_checklist("SIGN IN", None, None)

        # Assert
        assert result == 0
        state = json.loads(state_file.read_text())
        checklists = state["currentRun"]["phases"][0]["checklists"]
        assert len(checklists) == 1
        assert checklists[0]["name"] == "SIGN IN"

    def test_records_passed_item(self, tmp_path: Path) -> None:
        """GIVEN an active phase
        WHEN cmd_checklist is called with an item marked as passed
        THEN the item is recorded with passed=True."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")
            workflow_tracker.cmd_phase("forja-dev", "TIME_OUT")

            # Act
            result = workflow_tracker.cmd_checklist("Implementation Complete", "Tests passing", True)

        # Assert
        assert result == 0
        state = json.loads(state_file.read_text())
        items = state["currentRun"]["phases"][0]["checklists"][0]["items"]
        assert len(items) == 1
        assert items[0]["text"] == "Tests passing"
        assert items[0]["passed"] is True

    def test_records_failed_item(self, tmp_path: Path) -> None:
        """GIVEN an active phase
        WHEN cmd_checklist is called with an item marked as failed
        THEN the item is recorded with passed=False."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")
            workflow_tracker.cmd_phase("centinela-qa", "TIME_OUT")

            # Act
            result = workflow_tracker.cmd_checklist("Security Verification", "No hardcoded secrets", False)

        # Assert
        assert result == 0
        state = json.loads(state_file.read_text())
        items = state["currentRun"]["phases"][0]["checklists"][0]["items"]
        assert items[0]["passed"] is False

    def test_fails_without_active_phase(self, tmp_path: Path) -> None:
        """GIVEN an active run but no phase
        WHEN cmd_checklist is called
        THEN it returns 1."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")

            # Act
            result = workflow_tracker.cmd_checklist("Test", None, None)

        # Assert
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_blocker tests
# ---------------------------------------------------------------------------


class TestCmdBlocker:
    """Tests for cmd_blocker_add() and cmd_blocker_resolve()."""

    def test_adds_blocker(self, tmp_path: Path) -> None:
        """GIVEN an active run
        WHEN cmd_blocker_add is called
        THEN the blocker is added."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")

            # Act
            result = workflow_tracker.cmd_blocker_add("Missing API key")

        # Assert
        assert result == 0
        state = json.loads(state_file.read_text())
        assert "Missing API key" in state["currentRun"]["blockers"]

    def test_resolves_blocker(self, tmp_path: Path) -> None:
        """GIVEN an active run with a blocker
        WHEN cmd_blocker_resolve is called with the correct index
        THEN the blocker is removed."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")
            workflow_tracker.cmd_blocker_add("Blocker A")
            workflow_tracker.cmd_blocker_add("Blocker B")

            # Act
            result = workflow_tracker.cmd_blocker_resolve(0)

        # Assert
        assert result == 0
        state = json.loads(state_file.read_text())
        assert len(state["currentRun"]["blockers"]) == 1
        assert state["currentRun"]["blockers"][0] == "Blocker B"

    def test_resolve_invalid_index(self, tmp_path: Path) -> None:
        """GIVEN an active run with one blocker
        WHEN cmd_blocker_resolve is called with an out-of-range index
        THEN it returns 1."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")
            workflow_tracker.cmd_blocker_add("Blocker")

            # Act
            result = workflow_tracker.cmd_blocker_resolve(5)

        # Assert
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_complete tests
# ---------------------------------------------------------------------------


class TestCmdComplete:
    """Tests for cmd_complete() -- completing a workflow run."""

    def test_completes_run_and_moves_to_history(self, tmp_path: Path) -> None:
        """GIVEN an active run with phases
        WHEN cmd_complete is called
        THEN the run is moved to history and currentRun is None."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test-feature")
            workflow_tracker.cmd_phase("forja-dev", "SIGN_IN")

            # Act
            result = workflow_tracker.cmd_complete()

        # Assert
        assert result == 0
        state = json.loads(state_file.read_text())
        assert state["currentRun"] is None
        assert len(state["history"]) == 1
        assert state["history"][0]["feature"] == "test-feature"
        assert state["history"][0]["completedAt"] is not None

    def test_closes_last_open_phase(self, tmp_path: Path) -> None:
        """GIVEN an active run with an open phase
        WHEN cmd_complete is called
        THEN the last phase gets a completedAt."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")
            workflow_tracker.cmd_phase("forja-dev", "IN_PROGRESS")

            # Act
            workflow_tracker.cmd_complete()

        # Assert
        state = json.loads(state_file.read_text())
        assert state["history"][0]["phases"][0]["completedAt"] is not None

    def test_fails_without_active_run(self, tmp_path: Path) -> None:
        """GIVEN no active run
        WHEN cmd_complete is called
        THEN it returns 1."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"

        # Act
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            result = workflow_tracker.cmd_complete()

        # Assert
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_status and cmd_history tests
# ---------------------------------------------------------------------------


class TestCmdStatusAndHistory:
    """Tests for cmd_status() and cmd_history()."""

    def test_status_with_no_runs(self, tmp_path: Path) -> None:
        """GIVEN no workflow state
        WHEN cmd_status is called
        THEN it returns 0."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"

        # Act
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            result = workflow_tracker.cmd_status()

        # Assert
        assert result == 0

    def test_status_with_active_run(self, tmp_path: Path) -> None:
        """GIVEN an active run
        WHEN cmd_status is called
        THEN it returns 0."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("test")
            workflow_tracker.cmd_phase("forja-dev", "SIGN_IN")

            # Act
            result = workflow_tracker.cmd_status()

        # Assert
        assert result == 0

    def test_history_with_no_runs(self, tmp_path: Path) -> None:
        """GIVEN no completed runs
        WHEN cmd_history is called
        THEN it returns 0."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"

        # Act
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            result = workflow_tracker.cmd_history()

        # Assert
        assert result == 0

    def test_history_with_completed_runs(self, tmp_path: Path) -> None:
        """GIVEN completed workflow runs
        WHEN cmd_history is called
        THEN it returns 0."""
        # Arrange
        state_file = tmp_path / "workflow-state.json"
        with patch.object(workflow_tracker, "STATE_FILE", state_file):
            workflow_tracker.cmd_start("feature-a")
            workflow_tracker.cmd_complete()

            # Act
            result = workflow_tracker.cmd_history()

        # Assert
        assert result == 0
