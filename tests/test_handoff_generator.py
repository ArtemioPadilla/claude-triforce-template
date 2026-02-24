#!/usr/bin/env python3
"""Tests for tools/handoff-generator.py.

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

handoff_generator = importlib.import_module("handoff-generator")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _valid_fields() -> Dict[str, str]:
    """Return a complete set of valid handoff fields."""
    return {
        "what_done": "Implemented feature X with tests",
        "what_watch": "Edge case on concurrent access",
        "what_next": "Review security of token handling",
        "open_questions": "Should tokens expire after 24h or 48h?",
    }


# ---------------------------------------------------------------------------
# Agent validation tests
# ---------------------------------------------------------------------------

class TestValidateAgents:
    """Tests for validate_agents()."""

    def test_valid_agents(self) -> None:
        """GIVEN valid from and to agents
        WHEN validate_agents is called
        THEN it returns no errors."""
        # Act
        errors = handoff_generator.validate_agents("forja", "centinela")

        # Assert
        assert errors == []

    def test_invalid_from_agent(self) -> None:
        """GIVEN an invalid from agent
        WHEN validate_agents is called
        THEN it returns an error."""
        # Act
        errors = handoff_generator.validate_agents("invalid", "centinela")

        # Assert
        assert len(errors) == 1
        assert "invalid" in errors[0].lower() or "Invalid" in errors[0]

    def test_invalid_to_agent(self) -> None:
        """GIVEN an invalid to agent
        WHEN validate_agents is called
        THEN it returns an error."""
        # Act
        errors = handoff_generator.validate_agents("forja", "unknown")

        # Assert
        assert len(errors) == 1

    def test_same_agent(self) -> None:
        """GIVEN same from and to agent
        WHEN validate_agents is called
        THEN it returns an error."""
        # Act
        errors = handoff_generator.validate_agents("forja", "forja")

        # Assert
        assert len(errors) == 1
        assert "same" in errors[0].lower()

    def test_all_valid_agent_names(self) -> None:
        """GIVEN each valid agent name
        WHEN used as from agent
        THEN validation passes."""
        for agent in ("prometeo", "forja", "centinela"):
            others = {"prometeo", "forja", "centinela"} - {agent}
            errors = handoff_generator.validate_agents(agent, others.pop())
            assert errors == [], f"Failed for agent: {agent}"


# ---------------------------------------------------------------------------
# Field validation tests
# ---------------------------------------------------------------------------

class TestValidateFields:
    """Tests for validate_fields()."""

    def test_all_fields_present(self) -> None:
        """GIVEN all required fields are non-empty
        WHEN validate_fields is called
        THEN it returns no errors."""
        # Arrange
        fields = _valid_fields()

        # Act
        errors = handoff_generator.validate_fields(fields)

        # Assert
        assert errors == []

    def test_empty_what_done(self) -> None:
        """GIVEN what_done is empty
        WHEN validate_fields is called
        THEN it returns one error."""
        # Arrange
        fields = _valid_fields()
        fields["what_done"] = ""

        # Act
        errors = handoff_generator.validate_fields(fields)

        # Assert
        assert len(errors) == 1
        assert "What Was Done" in errors[0]

    def test_whitespace_only_field(self) -> None:
        """GIVEN a field with only whitespace
        WHEN validate_fields is called
        THEN it is treated as empty."""
        # Arrange
        fields = _valid_fields()
        fields["what_watch"] = "   \n  "

        # Act
        errors = handoff_generator.validate_fields(fields)

        # Assert
        assert len(errors) == 1

    def test_missing_field(self) -> None:
        """GIVEN a missing field key
        WHEN validate_fields is called
        THEN it returns an error."""
        # Arrange
        fields = _valid_fields()
        del fields["open_questions"]

        # Act
        errors = handoff_generator.validate_fields(fields)

        # Assert
        assert len(errors) == 1
        assert "Open Questions" in errors[0]

    def test_multiple_empty_fields(self) -> None:
        """GIVEN multiple empty fields
        WHEN validate_fields is called
        THEN it returns one error per empty field."""
        # Arrange
        fields = {"what_done": "", "what_watch": "", "what_next": "", "open_questions": ""}

        # Act
        errors = handoff_generator.validate_fields(fields)

        # Assert
        assert len(errors) == 4


# ---------------------------------------------------------------------------
# Artifact building tests
# ---------------------------------------------------------------------------

class TestBuildArtifactData:
    """Tests for build_artifact_data()."""

    def test_builds_correct_structure(self) -> None:
        """GIVEN valid inputs
        WHEN build_artifact_data is called
        THEN it returns a dict with handoff and content sections."""
        # Arrange
        fields = _valid_fields()

        # Act
        result = handoff_generator.build_artifact_data(
            "forja", "centinela", "user-auth", fields, "20260224T120000Z",
        )

        # Assert
        assert "handoff" in result
        assert "content" in result
        assert result["handoff"]["from_agent"] == "forja"
        assert result["handoff"]["to_agent"] == "centinela"
        assert result["handoff"]["feature"] == "user-auth"
        assert result["content"]["what_done"] == fields["what_done"]

    def test_display_names_populated(self) -> None:
        """GIVEN valid agent names
        WHEN build_artifact_data is called
        THEN display names are populated."""
        # Act
        result = handoff_generator.build_artifact_data(
            "prometeo", "forja", "feature-x", _valid_fields(), "20260224T000000Z",
        )

        # Assert
        assert result["handoff"]["from_display"] == "Prometeo (PM)"
        assert result["handoff"]["to_display"] == "Forja (Dev)"


# ---------------------------------------------------------------------------
# Markdown rendering tests
# ---------------------------------------------------------------------------

class TestRenderMarkdown:
    """Tests for render_markdown()."""

    def test_contains_all_sections(self) -> None:
        """GIVEN valid artifact data
        WHEN render_markdown is called
        THEN output contains all 4 required sections."""
        # Arrange
        data = handoff_generator.build_artifact_data(
            "forja", "centinela", "user-auth", _valid_fields(), "20260224T120000Z",
        )

        # Act
        md = handoff_generator.render_markdown(data)

        # Assert
        assert "## What Was Done" in md
        assert "## What to Watch For" in md
        assert "## What's Needed Next" in md
        assert "## Open Questions" in md

    def test_contains_header_info(self) -> None:
        """GIVEN valid artifact data
        WHEN render_markdown is called
        THEN output contains feature name and agent info."""
        # Arrange
        data = handoff_generator.build_artifact_data(
            "forja", "centinela", "user-auth", _valid_fields(), "20260224T120000Z",
        )

        # Act
        md = handoff_generator.render_markdown(data)

        # Assert
        assert "user-auth" in md
        assert "Forja (Dev)" in md
        assert "Centinela (QA)" in md


# ---------------------------------------------------------------------------
# File output tests
# ---------------------------------------------------------------------------

class TestWriteArtifacts:
    """Tests for write_artifacts()."""

    def test_creates_both_files(self, tmp_path: Path) -> None:
        """GIVEN valid artifact data
        WHEN write_artifacts is called
        THEN both .md and .json files are created."""
        # Arrange
        data = handoff_generator.build_artifact_data(
            "forja", "centinela", "user-auth", _valid_fields(), "20260224T120000Z",
        )

        # Act
        md_path, json_path = handoff_generator.write_artifacts(
            tmp_path, "user-auth", "forja", "centinela", "20260224T120000Z", data,
        )

        # Assert
        assert md_path.exists()
        assert json_path.exists()
        assert md_path.suffix == ".md"
        assert json_path.suffix == ".json"

    def test_creates_directory_if_missing(self, tmp_path: Path) -> None:
        """GIVEN a nonexistent output directory
        WHEN write_artifacts is called
        THEN it creates the directory."""
        # Arrange
        output_dir = tmp_path / "subdir" / "handoffs"
        data = handoff_generator.build_artifact_data(
            "prometeo", "forja", "feature-x", _valid_fields(), "20260224T000000Z",
        )

        # Act
        handoff_generator.write_artifacts(
            output_dir, "feature-x", "prometeo", "forja", "20260224T000000Z", data,
        )

        # Assert
        assert output_dir.exists()

    def test_json_is_valid(self, tmp_path: Path) -> None:
        """GIVEN valid artifact data
        WHEN write_artifacts creates the JSON file
        THEN the JSON is parseable and matches the data."""
        # Arrange
        data = handoff_generator.build_artifact_data(
            "forja", "centinela", "user-auth", _valid_fields(), "20260224T120000Z",
        )

        # Act
        _, json_path = handoff_generator.write_artifacts(
            tmp_path, "user-auth", "forja", "centinela", "20260224T120000Z", data,
        )

        # Assert
        loaded = json.loads(json_path.read_text())
        assert loaded["handoff"]["from_agent"] == "forja"
        assert loaded["content"]["what_done"] == _valid_fields()["what_done"]


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

class TestMainCLI:
    """Integration tests for the main() entry point."""

    def test_successful_generation(self, tmp_path: Path) -> None:
        """GIVEN valid CLI arguments
        WHEN main is called
        THEN exit code is 0 and files are created."""
        # Arrange
        fields = _valid_fields()

        # Act
        exit_code = handoff_generator.main([
            "--from", "forja",
            "--to", "centinela",
            "--feature", "user-auth",
            "--what-done", fields["what_done"],
            "--what-watch", fields["what_watch"],
            "--what-next", fields["what_next"],
            "--open-questions", fields["open_questions"],
            "--output-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 0
        md_files = list(tmp_path.glob("*.md"))
        json_files = list(tmp_path.glob("*.json"))
        assert len(md_files) == 1
        assert len(json_files) == 1

    def test_blocks_on_empty_field(self, tmp_path: Path) -> None:
        """GIVEN an empty required field
        WHEN main is called
        THEN exit code is 1 (blocked)."""
        # Act
        exit_code = handoff_generator.main([
            "--from", "forja",
            "--to", "centinela",
            "--feature", "user-auth",
            "--what-done", "Did stuff",
            "--what-watch", "",
            "--what-next", "Review it",
            "--open-questions", "None",
            "--output-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 1

    def test_invalid_agent_returns_error(self, tmp_path: Path) -> None:
        """GIVEN an invalid agent name
        WHEN main is called
        THEN exit code is 2."""
        # Act
        exit_code = handoff_generator.main([
            "--from", "badagent",
            "--to", "centinela",
            "--feature", "x",
            "--what-done", "x",
            "--what-watch", "x",
            "--what-next", "x",
            "--open-questions", "x",
            "--output-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 2

    def test_dry_run(self, tmp_path: Path) -> None:
        """GIVEN --dry-run flag
        WHEN main is called with valid args
        THEN exit code is 0 and no files are created."""
        # Arrange
        fields = _valid_fields()

        # Act
        exit_code = handoff_generator.main([
            "--from", "forja",
            "--to", "centinela",
            "--feature", "user-auth",
            "--what-done", fields["what_done"],
            "--what-watch", fields["what_watch"],
            "--what-next", fields["what_next"],
            "--open-questions", fields["open_questions"],
            "--output-dir", str(tmp_path),
            "--dry-run",
        ])

        # Assert
        assert exit_code == 0
        assert list(tmp_path.glob("*")) == []

    def test_from_json_file(self, tmp_path: Path) -> None:
        """GIVEN a JSON file with handoff fields
        WHEN main is called with --from-json
        THEN fields are read from the JSON file."""
        # Arrange
        fields = _valid_fields()
        json_file = tmp_path / "fields.json"
        json_file.write_text(json.dumps(fields))

        # Act
        exit_code = handoff_generator.main([
            "--from", "prometeo",
            "--to", "forja",
            "--feature", "feature-x",
            "--from-json", str(json_file),
            "--output-dir", str(tmp_path),
        ])

        # Assert
        assert exit_code == 0
