---
name: security-audit
description: >
  Deep security audit of code, dependencies, and infrastructure. Checks OWASP Top 10,
  authentication, authorization, data protection, and dependency vulnerabilities.
  Use before releases or after significant changes.
context: fork
agent: centinela-qa
---

Perform a security audit on: $ARGUMENTS

If no specific scope is provided, audit the entire `src/` directory.

Follow these steps:
1. Read your MEMORY.md for previously found vulnerabilities and patterns
2. **OWASP Top 10** systematic check:
   - A01: Broken Access Control — check auth/authz on all endpoints
   - A02: Cryptographic Failures — check encryption, key management, hashing
   - A03: Injection — SQL, NoSQL, OS command, LDAP injection vectors
   - A04: Insecure Design — business logic flaws, missing rate limits
   - A05: Security Misconfiguration — default configs, verbose errors, CORS
   - A06: Vulnerable Components — `npm audit` / `pip audit`
   - A07: Auth Failures — weak passwords, missing MFA, session management
   - A08: Data Integrity — deserialization, unsigned updates
   - A09: Logging Failures — sensitive data in logs, missing audit trail
   - A10: SSRF — server-side request forgery vectors
3. **Secrets scan**: grep for API keys, tokens, passwords, connection strings
4. **Dependency audit**: check all deps for known CVEs
5. **Smart contracts** (if Solidity): reentrancy, integer overflow, access control, front-running
6. Write report to `docs/reviews/security-audit-{date}.md`
7. Update MEMORY.md with vulnerabilities and patterns found
8. Update TECH_DEBT.md with security-related debt
