#!/usr/bin/env python3
"""Tests for tools/security-scanner.py.

Tests follow TDD Red-Green-Refactor: each test was written before the
implementation it verifies. All tests use Arrange-Act-Assert pattern.
"""
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import importlib
security_scanner = importlib.import_module("security-scanner")


# ---------------------------------------------------------------------------
# Pattern loading tests
# ---------------------------------------------------------------------------

class TestLoadPatterns:
    """Tests for load_patterns()."""

    def test_loads_default_patterns_file(self, tmp_path: Path) -> None:
        """GIVEN a valid patterns JSON file
        WHEN load_patterns is called
        THEN it returns compiled pattern dicts with regex objects."""
        # Arrange
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text(json.dumps({
            "version": "1.0.0",
            "patterns": [{
                "id": "TEST_PATTERN",
                "regex": "secret_value",
                "severity": "critical",
                "message": "Test secret found",
                "category": "test",
            }],
        }))

        # Act
        result = security_scanner.load_patterns(patterns_file)

        # Assert
        assert len(result) == 1
        assert result[0]["id"] == "TEST_PATTERN"
        assert result[0]["severity"] == "critical"
        assert result[0]["regex"].pattern == "secret_value"

    def test_exits_on_missing_file(self, tmp_path: Path) -> None:
        """GIVEN a nonexistent patterns file path
        WHEN load_patterns is called
        THEN it exits with code 2."""
        # Arrange
        missing = tmp_path / "nonexistent.json"

        # Act & Assert
        try:
            security_scanner.load_patterns(missing)
            assert False, "Should have raised SystemExit"
        except SystemExit as exc:
            assert exc.code == 2

    def test_exits_on_invalid_json(self, tmp_path: Path) -> None:
        """GIVEN a file with invalid JSON
        WHEN load_patterns is called
        THEN it exits with code 2."""
        # Arrange
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not json {{{")

        # Act & Assert
        try:
            security_scanner.load_patterns(bad_file)
            assert False, "Should have raised SystemExit"
        except SystemExit as exc:
            assert exc.code == 2

    def test_exits_on_invalid_regex(self, tmp_path: Path) -> None:
        """GIVEN a patterns file with an invalid regex
        WHEN load_patterns is called
        THEN it exits with code 2."""
        # Arrange
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text(json.dumps({
            "version": "1.0.0",
            "patterns": [{
                "id": "BAD_REGEX",
                "regex": "[invalid(",
                "severity": "high",
                "message": "Bad pattern",
            }],
        }))

        # Act & Assert
        try:
            security_scanner.load_patterns(patterns_file)
            assert False, "Should have raised SystemExit"
        except SystemExit as exc:
            assert exc.code == 2


# ---------------------------------------------------------------------------
# Agentignore tests
# ---------------------------------------------------------------------------

class TestAgentignore:
    """Tests for load_agentignore() and is_ignored()."""

    def test_loads_patterns_from_agentignore(self, tmp_path: Path) -> None:
        """GIVEN an .agentignore file with patterns
        WHEN load_agentignore is called
        THEN it returns non-empty, non-comment lines."""
        # Arrange
        ignore_file = tmp_path / ".agentignore"
        ignore_file.write_text("# Comment\ntests/fixtures/*\n\n*.min.js\n")

        # Act
        result = security_scanner.load_agentignore(tmp_path)

        # Assert
        assert result == ["tests/fixtures/*", "*.min.js"]

    def test_returns_empty_when_no_file(self, tmp_path: Path) -> None:
        """GIVEN no .agentignore file
        WHEN load_agentignore is called
        THEN it returns an empty list."""
        # Act
        result = security_scanner.load_agentignore(tmp_path)

        # Assert
        assert result == []

    def test_is_ignored_matches_glob(self) -> None:
        """GIVEN a path matching an ignore pattern
        WHEN is_ignored is called
        THEN it returns True."""
        # Arrange
        patterns = ["tests/fixtures/*"]

        # Act & Assert
        assert security_scanner.is_ignored("tests/fixtures/secret.txt", patterns)

    def test_is_ignored_matches_basename(self) -> None:
        """GIVEN a file whose basename matches an ignore pattern
        WHEN is_ignored is called
        THEN it returns True."""
        # Arrange
        patterns = ["*.min.js"]

        # Act & Assert
        assert security_scanner.is_ignored("dist/bundle.min.js", patterns)

    def test_is_ignored_no_match(self) -> None:
        """GIVEN a path not matching any ignore pattern
        WHEN is_ignored is called
        THEN it returns False."""
        # Arrange
        patterns = ["tests/fixtures/*"]

        # Act & Assert
        assert not security_scanner.is_ignored("src/app.py", patterns)


# ---------------------------------------------------------------------------
# Scanning tests
# ---------------------------------------------------------------------------

class TestScanContent:
    """Tests for scan_content()."""

    def _make_patterns(self, pattern_defs: list) -> list:
        """Helper to create compiled pattern objects."""
        import re
        return [{
            "id": p["id"],
            "regex": re.compile(p["regex"]),
            "severity": p["severity"],
            "message": p["message"],
            "category": p.get("category", "test"),
        } for p in pattern_defs]

    def test_detects_aws_key(self) -> None:
        """GIVEN content containing an AWS access key
        WHEN scan_content is called
        THEN it returns a finding with SECRET_AWS_KEY."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "SECRET_AWS_KEY",
            "regex": "AKIA[0-9A-Z]{16}",
            "severity": "critical",
            "message": "AWS key",
        }])
        content = 'aws_key = "AKIAIOSFODNN7EXAMPLE"'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert len(findings) == 1
        assert findings[0]["pattern"] == "SECRET_AWS_KEY"
        assert findings[0]["line"] == 1
        assert findings[0]["severity"] == "critical"

    def test_detects_openai_key(self) -> None:
        """GIVEN content containing an OpenAI key
        WHEN scan_content is called
        THEN it returns a finding."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "SECRET_OPENAI_KEY",
            "regex": "sk-[a-zA-Z0-9]{20,}",
            "severity": "critical",
            "message": "OpenAI key",
        }])
        content = 'api_key = "sk-abcdefghij1234567890extra"'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert len(findings) == 1
        assert findings[0]["pattern"] == "SECRET_OPENAI_KEY"

    def test_detects_github_token(self) -> None:
        """GIVEN content containing a GitHub personal access token
        WHEN scan_content is called
        THEN it returns a finding."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "SECRET_GITHUB_TOKEN",
            "regex": "ghp_[a-zA-Z0-9]{36}",
            "severity": "critical",
            "message": "GitHub token",
        }])
        content = 'token = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij"'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert len(findings) == 1
        assert findings[0]["pattern"] == "SECRET_GITHUB_TOKEN"

    def test_detects_hardcoded_password(self) -> None:
        """GIVEN content with a hardcoded password
        WHEN scan_content is called
        THEN it returns a finding."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "SECRET_GENERIC_PASSWORD",
            "regex": "(?i)(?:password|passwd|pwd)\\s*=\\s*[\"'][^\"']{4,}[\"']",
            "severity": "high",
            "message": "Hardcoded password",
        }])
        content = 'password = "hunter2secret"'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert len(findings) == 1
        assert findings[0]["pattern"] == "SECRET_GENERIC_PASSWORD"

    def test_detects_sql_injection_fstring(self) -> None:
        """GIVEN content with SQL f-string interpolation
        WHEN scan_content is called
        THEN it returns a finding."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "SQL_INJECTION_FSTRING",
            "regex": "f[\"']\\s*(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE)\\b",
            "severity": "high",
            "message": "SQL injection risk",
        }])
        content = 'query = f"SELECT * FROM users WHERE id = {user_id}"'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert len(findings) == 1
        assert findings[0]["pattern"] == "SQL_INJECTION_FSTRING"

    def test_detects_xss_innerhtml(self) -> None:
        """GIVEN content with innerHTML assignment
        WHEN scan_content is called
        THEN it returns a finding."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "XSS_INNERHTML",
            "regex": "\\.innerHTML\\s*=",
            "severity": "high",
            "message": "XSS risk",
        }])
        content = 'element.innerHTML = userInput;'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert len(findings) == 1
        assert findings[0]["pattern"] == "XSS_INNERHTML"

    def test_detects_eval(self) -> None:
        """GIVEN content with eval() usage
        WHEN scan_content is called
        THEN it returns a finding."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "UNSAFE_EVAL",
            "regex": "(?<!\\w)eval\\s*\\(",
            "severity": "high",
            "message": "Unsafe eval",
        }])
        content = 'result = eval(user_input)'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert len(findings) == 1
        assert findings[0]["pattern"] == "UNSAFE_EVAL"

    def test_clean_content_returns_empty(self) -> None:
        """GIVEN content with no security issues
        WHEN scan_content is called
        THEN it returns an empty findings list."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "SECRET_AWS_KEY",
            "regex": "AKIA[0-9A-Z]{16}",
            "severity": "critical",
            "message": "AWS key",
        }])
        content = 'greeting = "Hello, World!"'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert findings == []

    def test_multiple_findings_on_different_lines(self) -> None:
        """GIVEN content with issues on multiple lines
        WHEN scan_content is called
        THEN it returns findings with correct line numbers."""
        # Arrange
        patterns = self._make_patterns([
            {"id": "P1", "regex": "secret_a", "severity": "high", "message": "A"},
            {"id": "P2", "regex": "secret_b", "severity": "critical", "message": "B"},
        ])
        content = "line1\nsecret_a here\nline3\nsecret_b here"

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert len(findings) == 2
        assert findings[0]["line"] == 2
        assert findings[1]["line"] == 4

    def test_reports_correct_line_for_multiline(self) -> None:
        """GIVEN content with a finding on line 5
        WHEN scan_content is called
        THEN the finding reports line 5."""
        # Arrange
        patterns = self._make_patterns([{
            "id": "TEST", "regex": "MARKER", "severity": "medium", "message": "Found",
        }])
        content = "a\nb\nc\nd\nMARKER here"

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        assert findings[0]["line"] == 5


# ---------------------------------------------------------------------------
# Blocking determination tests
# ---------------------------------------------------------------------------

class TestDetermineBlocked:
    """Tests for determine_blocked()."""

    def test_critical_severity_blocks(self) -> None:
        """GIVEN findings with critical severity
        WHEN determine_blocked is called
        THEN it returns True."""
        # Arrange
        findings = [{"severity": "critical"}]

        # Act & Assert
        assert security_scanner.determine_blocked(findings) is True

    def test_high_severity_blocks(self) -> None:
        """GIVEN findings with high severity
        WHEN determine_blocked is called
        THEN it returns True."""
        # Arrange
        findings = [{"severity": "high"}]

        # Act & Assert
        assert security_scanner.determine_blocked(findings) is True

    def test_medium_severity_does_not_block(self) -> None:
        """GIVEN findings with only medium severity
        WHEN determine_blocked is called
        THEN it returns False."""
        # Arrange
        findings = [{"severity": "medium"}]

        # Act & Assert
        assert security_scanner.determine_blocked(findings) is False

    def test_empty_findings_does_not_block(self) -> None:
        """GIVEN no findings
        WHEN determine_blocked is called
        THEN it returns False."""
        # Act & Assert
        assert security_scanner.determine_blocked([]) is False


# ---------------------------------------------------------------------------
# Audit trail tests
# ---------------------------------------------------------------------------

class TestAuditTrail:
    """Tests for append_audit_trail()."""

    def test_creates_audit_file_if_missing(self, tmp_path: Path) -> None:
        """GIVEN no existing audit trail file
        WHEN append_audit_trail is called with findings
        THEN it creates the file with header and entries."""
        # Arrange
        audit_path = tmp_path / "audit.md"
        findings = [{
            "pattern": "TEST_PAT",
            "line": 10,
            "severity": "high",
            "message": "Test finding",
            "category": "test",
            "matched_line": "secret = 'x'",
        }]

        # Act
        security_scanner.append_audit_trail(audit_path, "test.py", findings)

        # Assert
        content = audit_path.read_text()
        assert "# Security Audit Trail" in content
        assert "TEST_PAT" in content
        assert "test.py" in content

    def test_appends_to_existing_file(self, tmp_path: Path) -> None:
        """GIVEN an existing audit trail file
        WHEN append_audit_trail is called
        THEN it appends without overwriting."""
        # Arrange
        audit_path = tmp_path / "audit.md"
        audit_path.write_text("# Existing content\n")
        findings = [{
            "pattern": "P1",
            "line": 1,
            "severity": "critical",
            "message": "Found",
            "category": "test",
            "matched_line": "x",
        }]

        # Act
        security_scanner.append_audit_trail(audit_path, "f.py", findings)

        # Assert
        content = audit_path.read_text()
        assert "# Existing content" in content
        assert "P1" in content

    def test_skips_when_no_findings(self, tmp_path: Path) -> None:
        """GIVEN no findings
        WHEN append_audit_trail is called
        THEN it does not create or modify any file."""
        # Arrange
        audit_path = tmp_path / "audit.md"

        # Act
        security_scanner.append_audit_trail(audit_path, "f.py", [])

        # Assert
        assert not audit_path.exists()


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

class TestMainCLI:
    """Integration tests for the main() entry point."""

    def test_scan_file_clean(self, tmp_path: Path) -> None:
        """GIVEN a clean file
        WHEN main is called with --file
        THEN exit code is 0 and output shows no findings."""
        # Arrange
        clean_file = tmp_path / "clean.py"
        clean_file.write_text('greeting = "Hello"\n')
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text(json.dumps({
            "version": "1.0.0",
            "patterns": [{
                "id": "TEST", "regex": "NEVER_MATCH_THIS",
                "severity": "critical", "message": "Should not match",
            }],
        }))

        # Act
        exit_code = security_scanner.main([
            "--file", str(clean_file),
            "--patterns", str(patterns_file),
        ])

        # Assert
        assert exit_code == 0

    def test_scan_file_blocked(self, tmp_path: Path) -> None:
        """GIVEN a file with a secret
        WHEN main is called with --file
        THEN exit code is 1."""
        # Arrange
        bad_file = tmp_path / "bad.py"
        bad_file.write_text('key = "AKIAIOSFODNN7EXAMPLE1"\n')
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text(json.dumps({
            "version": "1.0.0",
            "patterns": [{
                "id": "SECRET_AWS_KEY",
                "regex": "AKIA[0-9A-Z]{16}",
                "severity": "critical",
                "message": "AWS key",
            }],
        }))

        # Act
        exit_code = security_scanner.main([
            "--file", str(bad_file),
            "--patterns", str(patterns_file),
        ])

        # Assert
        assert exit_code == 1

    def test_scan_ignored_file(self, tmp_path: Path) -> None:
        """GIVEN a file matching .agentignore
        WHEN main is called
        THEN exit code is 0 (ignored)."""
        # Arrange
        ignored_file = tmp_path / "test.min.js"
        ignored_file.write_text('var key = "AKIAIOSFODNN7EXAMPLE1";\n')
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text(json.dumps({
            "version": "1.0.0",
            "patterns": [{
                "id": "SECRET_AWS_KEY",
                "regex": "AKIA[0-9A-Z]{16}",
                "severity": "critical",
                "message": "AWS key",
            }],
        }))
        ignore_file = tmp_path / ".agentignore"
        ignore_file.write_text("*.min.js\n")

        # Act
        exit_code = security_scanner.main([
            "--file", str(ignored_file),
            "--patterns", str(patterns_file),
            "--project-root", str(tmp_path),
        ])

        # Assert
        assert exit_code == 0

    def test_audit_trail_written_on_findings(self, tmp_path: Path) -> None:
        """GIVEN a file with findings and --audit-trail specified
        WHEN main is called
        THEN the audit trail file is created with entries."""
        # Arrange
        bad_file = tmp_path / "bad.py"
        bad_file.write_text('password = "supersecret"\n')
        patterns_file = tmp_path / "patterns.json"
        patterns_file.write_text(json.dumps({
            "version": "1.0.0",
            "patterns": [{
                "id": "SECRET_GENERIC_PASSWORD",
                "regex": "(?i)password\\s*=\\s*[\"'][^\"']{4,}[\"']",
                "severity": "high",
                "message": "Hardcoded password",
            }],
        }))
        audit_path = tmp_path / "audit.md"

        # Act
        security_scanner.main([
            "--file", str(bad_file),
            "--patterns", str(patterns_file),
            "--audit-trail", str(audit_path),
        ])

        # Assert
        assert audit_path.exists()
        content = audit_path.read_text()
        assert "SECRET_GENERIC_PASSWORD" in content


# ---------------------------------------------------------------------------
# Edge case tests
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge cases and regression tests."""

    def test_truncate_long_line(self) -> None:
        """GIVEN a line longer than 120 chars
        WHEN _truncate is called
        THEN it truncates with ellipsis."""
        # Arrange
        long_line = "x" * 200

        # Act
        result = security_scanner._truncate(long_line, 120)

        # Assert
        assert len(result) == 120
        assert result.endswith("...")

    def test_truncate_short_line(self) -> None:
        """GIVEN a line shorter than max_len
        WHEN _truncate is called
        THEN it returns the line unchanged."""
        # Arrange & Act
        result = security_scanner._truncate("short", 120)

        # Assert
        assert result == "short"

    def test_scan_with_real_patterns_file(self) -> None:
        """GIVEN the real patterns.json file
        WHEN loaded and used to scan a known bad string
        THEN it detects the issue."""
        # Arrange
        patterns = security_scanner.load_patterns(
            PROJECT_ROOT / "src" / "security" / "patterns.json"
        )
        content = 'AWS_KEY = "AKIAIOSFODNN7EXAMPLE1"'

        # Act
        findings = security_scanner.scan_content(content, patterns)

        # Assert
        aws_findings = [f for f in findings if f["pattern"] == "SECRET_AWS_KEY"]
        assert len(aws_findings) == 1
