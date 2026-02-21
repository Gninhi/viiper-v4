"""
Unit Testing Skill.

Jest, Vitest, and pytest patterns for unit testing.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class UnitTestingSkill(Skill):
    """
    Unit testing patterns and best practices.

    Features:
    - Test structure (AAA pattern)
    - Mocking and stubbing
    - Test coverage
    - Snapshot testing
    - Parameterized tests
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Unit Testing",
        slug="unit-testing",
        category=SkillCategory.TESTING_UNIT,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["testing", "jest", "vitest", "pytest", "unit-tests", "tdd"],
        estimated_time_minutes=40,
        description="Unit testing patterns with Jest, Vitest, and pytest",
    )

    dependencies: list = [
        Dependency(name="jest", version="^29.7.0", package_manager="npm", reason="Testing framework (Node.js)"),
        Dependency(name="vitest", version="^1.1.0", package_manager="npm", reason="Vite-native testing"),
        Dependency(name="@testing-library/react", version="^14.1.0", package_manager="npm", reason="React testing utilities"),
        Dependency(name="pytest", version="^7.4.0", package_manager="pip", reason="Testing framework (Python)"),
        Dependency(name="pytest-cov", version="^4.1.0", package_manager="pip", reason="Coverage plugin"),
        Dependency(name="pytest-mock", version="^3.12.0", package_manager="pip", reason="Mocking plugin"),
    ]

    best_practices: list = [
        BestPractice(title="AAA Pattern", description="Arrange, Act, Assert structure", code_reference="setup -> execute -> verify", benefit="Clear, consistent test structure"),
        BestPractice(title="One Assertion Per Test", description="Test one behavior per test", code_reference="it('should return true when valid')", benefit="Clear failures, easier debugging"),
        BestPractice(title="Descriptive Test Names", description="Test name describes expected behavior", code_reference="it('should throw error when email is invalid')", benefit="Living documentation"),
        BestPractice(title="Test Edge Cases", description="Null, empty, boundary values", code_reference="test.each([[0], [-1], [null]])", benefit="Catch edge case bugs"),
    ]

    usage_examples: list = [
        UsageExample(
            title="Jest Unit Tests",
            description="Testing utility functions",
            code=r'''import { describe, it, expect, jest } from '@jest/globals';
import { formatDate, calculateTotal, validateEmail } from './utils';

describe('Utils', () => {
  describe('formatDate', () => {
    it('should format date as YYYY-MM-DD', () => {
      const date = new Date('2024-01-15');
      expect(formatDate(date)).toBe('2024-01-15');
    });

    it('should handle invalid dates', () => {
      expect(() => formatDate('invalid')).toThrow('Invalid date');
    });
  });

  describe('calculateTotal', () => {
    it('should sum array of numbers', () => {
      expect(calculateTotal([1, 2, 3])).toBe(6);
    });

    it('should return 0 for empty array', () => {
      expect(calculateTotal([])).toBe(0);
    });

    it('should handle negative numbers', () => {
      expect(calculateTotal([-1, -2, 3])).toBe(0);
    });
  });

  describe('validateEmail', () => {
    const validEmails = ['test@example.com', 'user.name@domain.co.uk'];
    const invalidEmails = ['invalid', '@missing.com', 'no@domain'];

    it.each(validEmails)('should accept valid email: %s', (email) => {
      expect(validateEmail(email)).toBe(true);
    });

    it.each(invalidEmails)('should reject invalid email: %s', (email) => {
      expect(validateEmail(email)).toBe(false);
    });
  });
});
''',
        ),
        UsageExample(
            title="Vitest Tests",
            description="Vite-native testing with mocks",
            code=r'''import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchUser, processOrder } from './services';

// Mock modules
vi.mock('./api', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Services', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('fetchUser', () => {
    it('should fetch user data', async () => {
      const mockUser = { id: 1, name: 'John' };
      vi.mocked(apiClient.get).mockResolvedValue(mockUser);

      const result = await fetchUser(1);

      expect(apiClient.get).toHaveBeenCalledWith('/users/1');
      expect(result).toEqual(mockUser);
    });

    it('should handle errors', async () => {
      vi.mocked(apiClient.get).mockRejectedValue(new Error('Not found'));

      await expect(fetchUser(999)).rejects.toThrow('Not found');
    });
  });
});
''',
        ),
        UsageExample(
            title="Pytest Tests",
            description="Python unit testing",
            code=r'''import pytest
from unittest.mock import Mock, patch
from myapp.utils import calculate_discount, validate_input, process_data

class TestUtils:
    def test_calculate_discount_valid(self):
        """Should apply correct discount"""
        assert calculate_discount(100, 10) == 90
        assert calculate_discount(200, 20) == 160

    def test_calculate_discount_invalid(self):
        """Should raise error for invalid discount"""
        with pytest.raises(ValueError, match="Invalid discount"):
            calculate_discount(100, 110)

    @pytest.mark.parametrize("price,discount,expected", [
        (100, 0, 100),
        (100, 50, 50),
        (200, 25, 150),
    ])
    def test_calculate_discount_parametrized(self, price, discount, expected):
        """Test multiple scenarios"""
        assert calculate_discount(price, discount) == expected

    @patch('myapp.utils.api_client')
    def test_with_mock(self, mock_client):
        """Test with mocked dependency"""
        mock_client.get.return_value = {"id": 1, "name": "Test"}

        result = process_data(1)

        mock_client.get.assert_called_once_with("/data/1")
        assert result["name"] == "Test"
''',
        ),
        UsageExample(
            title="Snapshot Testing",
            description="Testing React components",
            code=r'''import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    const { container } = render(<Button>Click me</Button>);
    expect(container).toMatchSnapshot();
  });

  it('renders with different variants', () => {
    const { rerender } = render(<Button variant="primary">Primary</Button>);
    expect(screen.getByRole('button')).toHaveClass('btn-primary');

    rerender(<Button variant="secondary">Secondary</Button>);
    expect(screen.getByRole('button')).toHaveClass('btn-secondary');
  });

  it('calls onClick when clicked', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(title="Testing Implementation", description="Testing internal state instead of behavior", solution="Test public API and behavior", impact="Brittle tests, refactoring breaks tests"),
        AntiPattern(title="Interdependent Tests", description="Tests that rely on other tests", solution="Each test should be isolated", impact="Flaky tests, hard to debug"),
        AntiPattern(title="No Assertions", description="Tests without expect()", solution="Every test needs assertions", impact="False positives, tests pass without verifying"),
        AntiPattern(title="Magic Numbers", description="Unexplained values in tests", solution="Use descriptive constants", impact="Unclear test intent"),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        framework = options.get("framework", "jest")
        return {
            "files": {
                "tests/utils.test.ts": framework in ["jest", "vitest"] and self.usage_examples[0].code or "",
                "tests/services.test.ts": framework == "vitest" and self.usage_examples[1].code or "",
                "tests/test_utils.py": framework == "pytest" and self.usage_examples[2].code or "",
                "tests/Button.test.tsx": self.usage_examples[3].code,
            },
            "metadata": {"framework": framework},
        }
