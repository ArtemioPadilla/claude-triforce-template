# Security Patterns

Versioned pattern definitions for the Agent Triforce security scanner.

## Files

- **patterns.json** -- Pattern definitions (regex, severity, message) used by `tools/security-scanner.py` to detect hardcoded secrets, SQL injection, XSS, and unsafe eval patterns.

## Updating Patterns

To add or modify patterns, edit `patterns.json` directly. Each pattern requires:

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (UPPER_SNAKE_CASE) |
| `regex` | Python-compatible regular expression |
| `severity` | `critical`, `high`, or `medium` |
| `message` | Human-readable explanation with remediation guidance |
| `category` | Pattern category: `hardcoded_secret`, `sql_injection`, `xss`, `unsafe_eval`, `hardcoded_url` |

Critical and high severity findings block file writes. Medium severity findings are logged but do not block.
