"""
CI/CD Pipeline Skill.

GitHub Actions workflows for automated testing, building, and deployment.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill,
    SkillMetadata,
    SkillCategory,
    SkillDifficulty,
    Dependency,
    BestPractice,
    UsageExample,
    AntiPattern,
)


class CICDPipelineSkill(Skill):
    """
    CI/CD pipeline patterns with GitHub Actions.

    Features:
    - Automated testing on PR
    - Build and push Docker images
    - Deploy to staging/production
    - Environment-based workflows
    - Caching for faster builds
    - Security scanning
    """

    metadata: SkillMetadata = SkillMetadata(
        name="CI/CD Pipeline",
        slug="cicd-pipeline",
        category=SkillCategory.DEVOPS_CI_CD,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["cicd", "github-actions", "deployment", "automation", "testing"],
        estimated_time_minutes=60,
        description="Complete CI/CD pipeline with GitHub Actions",
    )

    dependencies: list = [
        Dependency(
            name="actions/checkout",
            version="v4",
            package_manager="github-actions",
            reason="Checkout repository",
        ),
        Dependency(
            name="actions/setup-node",
            version="v4",
            package_manager="github-actions",
            reason="Setup Node.js environment",
        ),
        Dependency(
            name="docker/build-push-action",
            version="v5",
            package_manager="github-actions",
            reason="Build and push Docker images",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Reusable Workflows",
            description="Extract common logic to reusable workflows",
            code_reference=".github/workflows/reusable-test.yml",
            benefit="DRY, maintainability, consistency",
        ),
        BestPractice(
            title="Cache Dependencies",
            description="Cache node_modules, pip packages",
            code_reference="uses: actions/cache@v4",
            benefit="Faster builds, reduced costs",
        ),
        BestPractice(
            title="Use Environments",
            description="Define staging, production environments",
            code_reference="environment: production",
            benefit="Environment-specific secrets, protection rules",
        ),
        BestPractice(
            title="Require PR Reviews",
            description="Branch protection rules for main",
            code_reference="required_reviews: 1",
            benefit="Code quality, knowledge sharing",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Node.js CI Pipeline",
            description="Test, build, and lint on every PR",
            code=r"""name: Node.js CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Test
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: false

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            myapp:latest
            myapp:${{ github.sha }}
          cache-from: type=registry,ref=myapp:buildcache
          cache-to: type=registry,ref=myapp:buildcache,mode=max
""",
        ),
        UsageExample(
            name="Python CI Pipeline",
            description="Test, lint, and build Python app",
            code=r"""name: Python CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint
        run: |
          ruff check .
          black --check .

      - name: Type check
        run: mypy .

      - name: Test
        run: pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install safety
        run: pip install safety

      - name: Check dependencies
        run: safety check -r requirements.txt
""",
        ),
        UsageExample(
            name="Deploy to Production",
            description="Production deployment with approval",
            code=r"""name: Deploy to Production

on:
  workflow_run:
    workflows: ["Node.js CI"]
    types:
      - completed
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    environment:
      name: production
      url: https://myapp.com

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        run: |
          # Deploy script
          echo "Deploying to production..."

      - name: Health check
        run: |
          curl -f https://myapp.com/health || exit 1

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Production deployment successful! ${{ github.sha }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
""",
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Hardcoded Secrets in workflow files",
            why="Security vulnerability - secrets exposed in code",
            good="Use GitHub Secrets (${{ secrets.SECRET_NAME }})",
        ),
        AntiPattern(
            bad="No Concurrency Control - Multiple workflows running simultaneously",
            why="Wasted resources, race conditions, conflicting deployments",
            good="Use concurrency group to cancel redundant runs",
        ),
        AntiPattern(
            bad="Skipping Tests on Main - Direct push without tests",
            why="Broken main branch, undetected bugs in production",
            good="Require CI passing for merge via branch protection",
        ),
        AntiPattern(
            bad="No Caching - Installing dependencies from scratch every time",
            why="Slow builds, higher costs, wasted compute resources",
            good="Cache node_modules, pip packages, Docker layers",
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate CI/CD pipeline files."""
        options = options or {}

        language = options.get("language", "node")
        include_deploy = options.get("include_deploy", True)
        include_security = options.get("include_security", True)

        result = {
            "files": {},
            "metadata": {
                "language": language,
                "includes_deploy": include_deploy,
                "includes_security": include_security,
            },
        }

        if language == "node":
            result["files"][".github/workflows/ci.yml"] = self.usage_examples[0].code
        else:
            result["files"][".github/workflows/ci.yml"] = self.usage_examples[1].code

        if include_deploy:
            result["files"][".github/workflows/deploy.yml"] = self.usage_examples[2].code

        if include_security:
            result["files"][".github/workflows/security.yml"] = r"""name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
"""

        return result
