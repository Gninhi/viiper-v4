"""
Integration Testing Skill.

Testing component interactions and API endpoints.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class IntegrationTestingSkill(Skill):
    """
    Integration testing patterns.

    Features:
    - API endpoint testing
    - Database integration tests
    - Service layer testing
    - Test containers
    - Transaction rollback
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Integration Testing",
        slug="integration-testing",
        category=SkillCategory.TESTING_INTEGRATION,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["testing", "integration", "api-testing", "supertest", "http-test"],
        estimated_time_minutes=50,
        description="Integration testing for APIs and services",
    )

    dependencies: list = [
        Dependency(name="supertest", version="^6.3.3", package_manager="npm", reason="HTTP assertion (Node.js)"),
        Dependency(name="pytest-asyncio", version="^0.23.0", package_manager="pip", reason="Async test support"),
        Dependency(name="httpx", version="^0.26.0", package_manager="pip", reason="HTTP client (Python)"),
        Dependency(name="testcontainers", version="^3.7.0", package_manager="pip", reason="Docker for tests"),
    ]

    best_practices: list = [
        BestPractice(title="Test Real Dependencies", description="Use real database, cache in tests", code_reference="Testcontainers for PostgreSQL", benefit="Catch integration issues early"),
        BestPractice(title="Transaction Rollback", description="Rollback after each test", code_reference="BEGIN; test; ROLLBACK;", benefit="Test isolation, clean state"),
        BestPractice(title="Factory Pattern", description="Test data factories", code_reference="UserFactory.create()", benefit="DRY, maintainable test data"),
        BestPractice(title="API Contract Testing", description="Verify request/response schemas", code_reference="expect(response.body).toMatchSchema()", benefit="Catch breaking changes"),
    ]

    usage_examples: list = [
        UsageExample(
            title="API Integration Tests (Node.js)",
            description="Testing Express endpoints",
            code=r'''import request from 'supertest';
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { app } from '../src/app';
import { db } from '../src/db';

describe('Users API', () => {
  beforeAll(async () => {
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear();
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject({
        id: expect.any(String),
        email: userData.email,
        name: userData.name,
      });
    });

    it('should return 400 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'invalid', password: 'pass123', name: 'Test' })
        .expect(400);

      expect(response.body.errors).toContainEqual(
        expect.objectContaining({ field: 'email' })
      );
    });

    it('should return 409 for duplicate email', async () => {
      await request(app).post('/api/users').send({
        email: 'existing@example.com',
        password: 'password123',
        name: 'Existing',
      });

      await request(app)
        .post('/api/users')
        .send({
          email: 'existing@example.com',
          password: 'password123',
          name: 'Duplicate',
        })
        .expect(409);
    });
  });

  describe('GET /api/users/:id', () => {
    it('should return user by id', async () => {
      const { body: created } = await request(app)
        .post('/api/users')
        .send({ email: 'get@example.com', password: 'pass', name: 'Get' });

      const response = await request(app)
        .get(`/api/users/${created.id}`)
        .expect(200);

      expect(response.body.id).toBe(created.id);
    });

    it('should return 404 for non-existent user', async () => {
      await request(app).get('/api/users/nonexistent').expect(404);
    });
  });
});
''',
        ),
        UsageExample(
            title="API Integration Tests (Python)",
            description="Testing FastAPI endpoints",
            code=r'''import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from myapp.main import app
from myapp.db import database, engine, Base

@pytest.fixture
async def client():
    """Test client with test database"""
    Base.metadata.create_all(bind=engine)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Should create a new user"""
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User",
    }

    response = await client.post("/api/users", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    """Should get user by ID"""
    # Create user first
    create_response = await client.post("/api/users", json={
        "email": "get@example.com",
        "password": "pass",
        "name": "Get User",
    })
    user_id = create_response.json()["id"]

    # Get user
    response = await client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id

@pytest.mark.asyncio
async def test_user_not_found(client: AsyncClient):
    """Should return 404 for non-existent user"""
    response = await client.get("/api/users/nonexistent")
    assert response.status_code == 404

@pytest.mark.parametrize("email,expected_status", [
    ("invalid", 400),
    ("missing@domain", 400),
    ("valid@email.com", 201),
])
async def test_user_validation(client: AsyncClient, email, expected_status):
    """Test email validation"""
    response = await client.post("/api/users", json={
        "email": email,
        "password": "pass123",
        "name": "Test",
    })
    assert response.status_code == expected_status
''',
        ),
        UsageExample(
            title="Test Fixtures Factory",
            description="Reusable test data factories",
            code=r'''// test/factories.ts

class UserFactory {
  static create(overrides = {}) {
    return {
      id: crypto.randomUUID(),
      email: `user${Date.now()}@test.com`,
      password: 'hashed_password',
      name: 'Test User',
      role: 'user',
      createdAt: new Date(),
      ...overrides,
    };
  }

  static async createInDb(overrides = {}) {
    const user = this.create(overrides);
    await db.users.insert(user);
    return user;
  }
}

class ProductFactory {
  static create(overrides = {}) {
    return {
      id: crypto.randomUUID(),
      name: 'Test Product',
      price: 99.99,
      stock: 100,
      ...overrides,
    };
  }
}

class OrderFactory {
  static create(overrides = {}) {
    return {
      id: crypto.randomUUID(),
      userId: crypto.randomUUID(),
      items: [],
      total: 0,
      status: 'pending',
      ...overrides,
    };
  }
}

export { UserFactory, ProductFactory, OrderFactory };
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(title="Testing Through UI", description="E2E tests for everything", solution="Test at appropriate level", impact="Slow, flaky tests"),
        AntiPattern(title="Shared Test State", description="Tests affecting each other", solution="Isolate test data", impact="Flaky tests, order dependency"),
        AntiPattern(title="No Cleanup", description="Test data accumulates", solution="Cleanup after each test", impact="Slow tests, database bloat"),
        AntiPattern(title="Real External Services", description="Calling real payment APIs", solution="Mock external services", impact="Slow, costly, flaky tests"),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "tests/integration/api.test.ts": self.usage_examples[0].code,
                "tests/integration/test_api.py": self.usage_examples[1].code,
                "tests/factories.ts": self.usage_examples[2].code,
            },
            "metadata": {"framework": options.get("framework", "express")},
        }
