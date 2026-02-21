"""
Test Fixtures and Mocking Skill.

Test data management, mocking strategies, and test utilities.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class TestFixturesMockingSkill(Skill):
    """
    Test fixtures and mocking patterns.

    Features:
    - Test data factories
    - Database seeding
    - API mocking
    - Service mocking
    - Clock mocking
    - File system mocking
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Test Fixtures and Mocking",
        slug="test-fixtures-mocking",
        category=SkillCategory.TESTING_UNIT,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["testing", "mocking", "fixtures", "test-data", "factories"],
        estimated_time_minutes=35,
        description="Test data factories and mocking strategies",
    )

    dependencies: list = [
        Dependency(name="jest", version="^29.7.0", package_manager="npm", reason="Testing framework with mocking"),
        Dependency(name="faker", version="^2.0.0", package_manager="npm", reason="Fake data generation"),
        Dependency(name="pytest-factoryboy", version="^2.6.0", package_manager="pip", reason="Factory Boy for pytest"),
        Dependency(name="responses", version="^0.24.0", package_manager="pip", reason="HTTP mocking (Python)"),
    ]

    best_practices: list = [
        BestPractice(title="Factory Pattern", description="Reusable test data builders", code_reference="UserFactory.create({ role: 'admin' })", benefit="DRY, flexible test data"),
        BestPractice(title="Mock External Services", description="Never call real APIs in tests", code_reference="jest.mock('./api')", benefit="Fast, reliable tests"),
        BestPractice(title="Seed Test Data", description="Consistent data for integration tests", code_reference="await db.seed('users', 'products')", benefit="Predictable test scenarios"),
        BestPractice(title="Mock Time", description="Control time in tests", code_reference="jest.useFakeTimers()", benefit="Test time-dependent logic"),
    ]

    usage_examples: list = [
        UsageExample(
            title="Test Factories (Node.js)",
            description="Reusable test data factories with Faker",
            code=r'''import { faker } from '@faker-js/faker';

class UserFactory {
  static create(overrides = {}) {
    return {
      id: faker.string.uuid(),
      email: faker.internet.email(),
      password: faker.internet.password({ length: 12 }),
      name: faker.person.fullName(),
      role: faker.helpers.arrayElement(['user', 'admin', 'moderator']),
      avatar: faker.image.avatar(),
      bio: faker.lorem.paragraph(),
      createdAt: faker.date.past(),
      ...overrides,
    };
  }

  static async createInDb(overrides = {}) {
    const user = this.create(overrides);
    await db.users.insert(user);
    return user;
  }

  static createMany(count: number, overrides = {}) {
    return Array.from({ length: count }, () => this.create(overrides));
  }
}

class ProductFactory {
  static create(overrides = {}) {
    return {
      id: faker.string.uuid(),
      name: faker.commerce.productName(),
      description: faker.commerce.productDescription(),
      price: parseFloat(faker.commerce.price({ min: 10, max: 500 })),
      stock: faker.number.int({ min: 0, max: 100 }),
      category: faker.commerce.department(),
      images: [faker.image.url()],
      ...overrides,
    };
  }
}

class OrderFactory {
  static create(overrides = {}) {
    const items = faker.helpers.multiple(() => ({
      productId: faker.string.uuid(),
      quantity: faker.number.int({ min: 1, max: 5 }),
      price: parseFloat(faker.commerce.price({ min: 10, max: 200 })),
    }), { count: faker.number.int({ min: 1, max: 5 }) });

    return {
      id: faker.string.uuid(),
      userId: faker.string.uuid(),
      items,
      total: items.reduce((sum, item) => sum + item.price * item.quantity, 0),
      status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered']),
      shippingAddress: {
        street: faker.location.streetAddress(),
        city: faker.location.city(),
        zipCode: faker.location.zipCode(),
        country: faker.location.country(),
      },
      ...overrides,
    };
  }
}

export { UserFactory, ProductFactory, OrderFactory };
''',
        ),
        UsageExample(
            title="API Mocking (Jest)",
            description="Mock external API calls",
            code=r'''import { jest } from '@jest/globals';

// Mock entire module
jest.mock('../services/paymentService', () => ({
  chargeCard: jest.fn().mockResolvedValue({ success: true, transactionId: 'tx_123' }),
  refund: jest.fn().mockResolvedValue({ success: true }),
  getBalance: jest.fn().mockResolvedValue({ amount: 1000 }),
}));

// Mock fetch API
global.fetch = jest.fn();

// Mock implementation in test
beforeEach(() => {
  jest.clearAllMocks();

  fetch.mockImplementation((url) => {
    if (url.includes('/users')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve([{ id: 1, name: 'John' }]),
      });
    }
    return Promise.resolve({ ok: true, json: () => Promise.resolve([]) });
  });
});

// Mock timers
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-15T10:00:00Z'));

// Mock modules with dependencies
jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn(),
  create: jest.fn(() => ({
    interceptors: { request: { use: jest.fn() }, response: { use: jest.fn() } },
  })),
}));

// Spy on methods
const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
''',
        ),
        UsageExample(
            title="Database Fixtures (Python)",
            description="Pytest fixtures for database tests",
            code=r'''import pytest
from faker import Faker
from myapp.models import User, Product, Order
from myapp.db import SessionLocal, Base, engine

fake = Faker()

@pytest.fixture(scope='session')
def db_engine():
    """Create test database engine"""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(db_engine):
    """Create fresh database session per test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    # Rollback after test
    transaction.rollback()
    session.close()
    connection.close()

@pytest.fixture
def user(db_session):
    """Create a test user"""
    user = User(
        email=fake.email(),
        name=fake.name(),
        password_hash='hashed_password',
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def products(db_session):
    """Create test products"""
    products = [
        Product(name=fake.product_name(), price=fake.pyfloat(2, 2, 10, 500))
        for _ in range(5)
    ]
    db_session.add_all(products)
    db_session.commit()
    return products

@pytest.fixture
def order(db_session, user, products):
    """Create a test order"""
    order = Order(
        user_id=user.id,
        total=sum(p.price for p in products),
        status='pending',
    )
    db_session.add(order)
    db_session.commit()
    return order

# Usage
def test_order_creation(db_session, order):
    assert order.status == 'pending'
    assert len(order.items) > 0
''',
        ),
        UsageExample(
            title="Factory Boy (Python)",
            description="Advanced test factories",
            code=r'''import factory
from factory import Faker, Sequence, SubFactory, RelatedFactory
from myapp.models import User, Post, Category

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    email = Faker('email')
    name = Faker('name')
    password = factory.django.Password(password='password123')
    is_active = True
    is_staff = False

class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = Faker('word')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-'))

class PostFactory(factory.Factory):
    class Meta:
        model = Post

    title = Faker('sentence', nb_words=5)
    content = Faker('paragraph', nb_sentences=10)
    author = SubFactory(UserFactory)
    category = SubFactory(CategoryFactory)
    is_published = True

# Factory with traits
class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    status = 'pending'
    total = Faker('pyfloat', left_digits=3, right_digits=2)

    class Params:
        paid = factory.Trait(
            status='paid',
            paid_at=Faker('date_time_this_month'),
        )
        shipped = factory.Trait(
            status='shipped',
            shipped_at=Faker('date_time_this_month'),
        )
        cancelled = factory.Trait(
            status='cancelled',
            cancelled_at=Faker('date_time_this_month'),
        )

# Usage
# user = UserFactory.create()
# admin = UserFactory.create(is_staff=True, is_superuser=True)
# order = OrderFactory.create(paid=True)
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(title="Hardcoded Test Data", description="Fixed values in tests", solution="Use factories with Faker", impact="Brittle tests, data conflicts"),
        AntiPattern(title="Real API Calls", description="Calling external services", solution="Mock all external APIs", impact="Slow, flaky, costly tests"),
        AntiPattern(title="Shared Fixtures", description="Tests modifying shared data", solution="Fresh fixtures per test", impact="Test interdependence, flakiness"),
        AntiPattern(title="Over-Mocking", description="Mocking everything", solution="Mock only external dependencies", impact="False confidence, missing real issues"),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "tests/factories.ts": self.usage_examples[0].code,
                "tests/mocks/api.mock.ts": self.usage_examples[1].code,
                "tests/conftest.py": self.usage_examples[2].code,
                "tests/factories.py": self.usage_examples[3].code,
            },
            "metadata": {"language": options.get("language", "node")},
        }
