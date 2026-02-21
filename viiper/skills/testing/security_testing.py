"""
Security Testing Skill.

Security scanning, vulnerability detection, and penetration testing.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class SecurityTestingSkill(Skill):
    """
    Security testing and vulnerability scanning.

    Features:
    - Dependency scanning
    - SAST (Static Application Security Testing)
    - DAST (Dynamic Application Security Testing)
    - Secret detection
    - OWASP Top 10 testing
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Security Testing",
        slug="security-testing",
        category=SkillCategory.TESTING_SECURITY,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["testing", "security", "sast", "dast", "owasp", "vulnerability"],
        estimated_time_minutes=45,
        description="Security testing and vulnerability scanning",
    )

    dependencies: list = [
        Dependency(name="npm-audit", version="latest", package_manager="npm", reason="Dependency auditing"),
        Dependency(name="snyk", version="latest", package_manager="npm", reason="Security scanning"),
        Dependency(name="owasp-zap", version="latest", package_manager="system", reason="DAST scanning"),
        Dependency(name="bandit", version="latest", package_manager="pip", reason="Python security linter"),
        Dependency(name="safety", version="latest", package_manager="pip", reason="Python dependency scanning"),
    ]

    best_practices: list = [
        BestPractice(title="Scan Dependencies", description="Regular vulnerability scans", code_reference="npm audit, snyk test", benefit="Catch vulnerable packages"),
        BestPractice(title="SAST in CI", description="Static analysis for security", code_reference="Semgrep, CodeQL", benefit="Find security bugs early"),
        BestPractice(title="Secret Detection", description="Prevent leaked credentials", code_reference="git-secrets, detect-secrets", benefit="No credentials in code"),
        BestPractice(title="OWASP Testing", description="Test Top 10 vulnerabilities", code_reference="SQL injection, XSS, CSRF tests", benefit="Common attack prevention"),
    ]

    usage_examples: list = [
        UsageExample(
            title="Security CI Pipeline",
            description="Automated security scanning",
            code=r'''name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  dependency-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4

      - name: Install dependencies
        run: npm ci

      - name: Run npm audit
        run: npm audit --audit-level=moderate

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2

  secret-detection:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Detect secrets
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified

  python-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5

      - name: Install safety
        run: pip install safety bandit

      - name: Check dependencies
        run: safety check -r requirements.txt

      - name: Run bandit
        run: bandit -r myapp/ -ll
''',
        ),
        UsageExample(
            title="OWASP Test Cases",
            description="Security test scenarios",
            code=r'''import request from 'supertest';
import { describe, it, expect } from 'vitest';

describe('Security Tests', () => {
  describe('SQL Injection', () => {
    it('should reject SQL injection in query params', async () => {
      const injections = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "1; DELETE FROM users",
      ];

      for (const injection of injections) {
        const response = await request(app)
          .get(`/api/users?id=${encodeURIComponent(injection)}`);

        // Should not return all users or error with SQL details
        expect(response.status).not.toBe(200);
        expect(response.body).not.toMatch(/sql|syntax|query/i);
      }
    });
  });

  describe('XSS Prevention', () => {
    it('should escape HTML in user input', async () => {
      const xssPayloads = [
        '<script>alert("XSS")</script>',
        '<img src=x onerror=alert(1)>',
        'javascript:alert(1)',
      ];

      for (const payload of xssPayloads) {
        const response = await request(app)
          .post('/api/comments')
          .send({ content: payload });

        const saved = await db.comments.findOne({ where: { id: response.body.id } });
        expect(saved.content).not.toMatch(/<script>/i);
      }
    });
  });

  describe('Authentication Bypass', () => {
    it('should require auth for protected routes', async () => {
      const protectedRoutes = [
        '/api/users/me',
        '/api/orders',
        '/api/settings',
      ];

      for (const route of protectedRoutes) {
        const response = await request(app).get(route);
        expect(response.status).toBe(401);
      }
    });
  });

  describe('Rate Limiting', () => {
    it('should rate limit login attempts', async () => {
      for (let i = 0; i < 10; i++) {
        const response = await request(app)
          .post('/api/login')
          .send({ email: 'test@test.com', password: 'wrong' });

        if (i >= 5) {
          expect(response.status).toBe(429);
        }
      }
    });
  });
});
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(title="No Dependency Scanning", description="Using vulnerable packages", solution="npm audit, snyk in CI", impact="Known vulnerabilities in production"),
        AntiPattern(title="Hardcoded Secrets", description="API keys in code", solution="Use environment variables, secrets manager", impact="Credential leaks"),
        AntiPattern(title="No Input Validation", description="Trusting user input", solution="Validate and sanitize all inputs", impact="Injection attacks"),
        AntiPattern(title="Verbose Errors", description="Stack traces in production", solution="Generic error messages", impact="Information disclosure"),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                ".github/workflows/security.yml": self.usage_examples[0].code,
                "tests/security/owasp.test.ts": self.usage_examples[1].code,
            },
            "metadata": {},
        }
