"""
Test Coverage and Quality Skill.

Code coverage analysis, quality gates, and reporting.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class TestCoverageQualitySkill(Skill):
    """
    Test coverage and quality analysis.

    Features:
    - Coverage thresholds
    - Coverage reporting
    - Quality gates
    - Unused code detection
    - Complexity analysis
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Test Coverage and Quality",
        slug="test-coverage-quality",
        category=SkillCategory.TESTING_QUALITY,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["testing", "coverage", "quality", "istanbul", "codecov"],
        estimated_time_minutes=30,
        description="Code coverage analysis and quality gates",
    )

    dependencies: list = [
        Dependency(name="istanbul", version="^0.4.5", package_manager="npm", reason="Coverage library"),
        Dependency(name="codecov", version="^3.8.3", package_manager="npm", reason="Coverage reporting"),
        Dependency(name="pytest-cov", version="^4.1.0", package_manager="pip", reason="Coverage for pytest"),
        Dependency(name="coverage", version="^7.4.0", package_manager="pip", reason="Coverage library (Python)"),
    ]

    best_practices: list = [
        BestPractice(title="Meaningful Coverage", description="Focus on critical paths", code_reference="80% coverage on business logic", benefit="Quality over quantity"),
        BestPractice(title="Coverage Gates", description="Block PRs below threshold", code_reference="coverage: 80%", benefit="Maintain coverage standards"),
        BestPractice(title="Diff Coverage", description="Check coverage on changed lines", code_reference="codecov --fail-on-change", benefit="Prevent regressions"),
        BestPractice(title="Exclude Appropriately", description="Skip generated code, types", code_reference="exclude: ['**/*.d.ts']", benefit="Accurate coverage metrics"),
    ]

    usage_examples: list = [
        UsageExample(
            title="Jest Coverage Config",
            description="Coverage configuration for Node.js",
            code=r'''// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html', 'json-summary'],

  coverageThreshold: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },

  collectCoverageFrom: [
    'src/**/*.{ts,tsx,js,jsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
    '!src/**/index.ts',
    '!src/types/**',
    '!src/**/*.test.{ts,tsx}',
  ],

  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/tests/',
    '/dist/',
    'coverage',
    '\\\\.d\\.ts$',
  ],
};
''',
        ),
        UsageExample(
            title="Pytest Coverage Config",
            description="Coverage configuration for Python",
            code=r'''# pyproject.toml
[tool.coverage.run]
source = ["myapp"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/migrations/*",
    "*/tests/*",
    "*/conftest.py",
    "*/__main__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]

[tool.pytest.ini_options]
addopts = "--cov=myapp --cov-report=term-missing --cov-report=html --cov-report=xml --cov-fail-under=80"
''',
        ),
        UsageExample(
            title="GitHub Actions Coverage",
            description="CI coverage reporting",
            code=r'''name: Tests with Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests with coverage
        run: npm test -- --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          fail_ci_if_error: false
          verbose: true

      - name: Check coverage threshold
        run: |
          coverage=$(node -e "console.log(require('./coverage/coverage-summary.json').total.lines.pct)")
          if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "Coverage $coverage% is below 80% threshold"
            exit 1
          fi
          echo "Coverage: $coverage%"
''',
        ),
        UsageExample(
            title="Coverage Report HTML",
            description="Example coverage report structure",
            code=r'''<!-- coverage/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Coverage Report</title>
</head>
<body>
    <h1>Code Coverage Report</h1>

    <table>
        <thead>
            <tr>
                <th>File</th>
                <th>Statements</th>
                <th>Branches</th>
                <th>Functions</th>
                <th>Lines</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>src/utils/auth.ts</td>
                <td>95%</td>
                <td>88%</td>
                <td>100%</td>
                <td>95%</td>
            </tr>
            <tr>
                <td>src/services/payment.ts</td>
                <td>87%</td>
                <td>72%</td>
                <td>90%</td>
                <td>88%</td>
            </tr>
        </tbody>
    </table>

    <div class="summary">
        <p>Overall Coverage: 89%</p>
        <p>Lines: 1234/1387</p>
    </div>
</body>
</html>
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(title="100% Coverage Goal", description="Chasing perfect coverage", solution="Focus on critical business logic", impact="Wasted effort on trivial code"),
        AntiPattern(title="Coverage Without Assertions", description="Running tests without verifying", solution="Ensure tests have meaningful assertions", impact="False confidence"),
        AntiPattern(title="Ignoring Branch Coverage", description="Only tracking line coverage", solution="Require branch coverage >= 70%", impact="Missing untested paths"),
        AntiPattern(title="No Coverage Diff Checks", description="Allowing coverage to decrease", solution="Fail CI on coverage decrease", impact="Gradual quality degradation"),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "jest.config.js": self.usage_examples[0].code,
                "pyproject.toml": self.usage_examples[1].code,
                ".github/workflows/coverage.yml": self.usage_examples[2].code,
            },
            "metadata": {"threshold": options.get("threshold", 80)},
        }
