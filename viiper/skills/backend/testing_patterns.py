"""Premium Testing Patterns Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class TestingPatternsSkill(Skill):
    """Robust testing patterns for unit, integration, and E2E validation."""

    metadata: SkillMetadata = SkillMetadata(
        name="Testing Patterns Library",
        slug="testing-patterns",
        category=SkillCategory.TESTING_UNIT,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["testing", "pytest", "jest", "vitest", "mocks", "fixtures"],
        estimated_time_minutes=35,
        description="Core testing patterns including mock injections, database fixtures, and API test suites.",
    )

    dependencies: list = [
        Dependency(name="pytest", version="^7.4.0", package_manager="pip", reason="Python testing framework"),
        Dependency(name="pytest-asyncio", version="^0.23.0", package_manager="pip", reason="Async support for pytest"),
        Dependency(name="jest", version="^29.7.0", package_manager="npm", reason="Node.js testing framework"),
        Dependency(name="supertest", version="^6.3.3", package_manager="npm", reason="API testing library for Node.js"),
    ]

    best_practices: list = [
        BestPractice(
            title="Isolated Database for Tests",
            description="Use a separate test database or transactions that rollback after each test to ensure isolation.",
            code_reference="@pytest.fixture(autouse=True) async def db_rollback(session): ...",
            benefit="Tests don't pollute each other's data, ensuring reproducibility.",
        ),
        BestPractice(
            title="Consistent Mocking",
            description="Mock external services (APIs, Email) at the boundary to avoid slow and brittle tests.",
            code_reference="jest.spyOn(emailService, 'send').mockResolvedValue(true);",
            benefit="Fast feedback loops and resilience to external outages.",
        ),
        BestPractice(
            title="Arrange-Act-Assert (AAA)",
            description="Structure test cases consistently into setup, execution, and verification phases.",
            code_reference="const user = await createTestUser(); // Arrange\nconst res = await api.get('/me'); // Act\nexpect(res.status).toBe(200); // Assert",
            benefit="Readable tests that are easy to debug and maintain.",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Pytest Async Mock",
            description="Mocking an async service in Python.",
            code='''@pytest.mark.asyncio
async def test_user_login(mocker):
    mocker.patch("auth_service.verify_token", return_value={"id": 1})
    # rest of test...''',
        ),
        UsageExample(
            name="Jest Supertest API",
            description="Testing an Express endpoint.",
            code='''const request = require('supertest');
test('GET /ping', async () => {
    const res = await request(app).get('/ping');
    expect(res.body.status).toBe('ok');
});''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Relying on specific data order",
            why="Database results without explicit ORDER BY can change, causing flaky tests.",
            good="Always specify order or verify existence rather than position.",
        ),
        AntiPattern(
            bad="Global shared state in tests",
            why="Leads to race conditions and ordering dependencies.",
            good="Use fresh fixtures for every test case.",
        ),
    ]

    file_structure: dict = {
        "tests/conftest.py": "Global pytest configuration",
        "tests/integration/test_api.py": "Integration tests example",
        "tests/jest.setup.js": "Jest configuration",
    }

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "tests/conftest.py": "# Pytest fixtures...\n",
            "tests/jest.setup.js": "// Jest setup...\n",
        }
