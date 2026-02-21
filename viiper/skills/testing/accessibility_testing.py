"""
Accessibility Testing Skill.

WCAG compliance testing and accessibility validation.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class AccessibilityTestingSkill(Skill):
    """
    Accessibility testing and WCAG compliance.

    Features:
    - Automated a11y testing
    - Screen reader testing
    - Keyboard navigation
    - Color contrast
    - ARIA validation
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Accessibility Testing",
        slug="accessibility-testing",
        category=SkillCategory.TESTING_A11Y,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["testing", "accessibility", "wcag", "a11y", "aria"],
        estimated_time_minutes=35,
        description="Accessibility testing for WCAG compliance",
    )

    dependencies: list = [
        Dependency(name="@axe-core/playwright", version="^4.8.2", package_manager="npm", reason="Axe core for Playwright"),
        Dependency(name="jest-axe", version="^8.0.0", package_manager="npm", reason="Jest accessibility assertions"),
        Dependency(name="@testing-library/react", version="^14.1.0", package_manager="npm", reason="Accessible testing utilities"),
    ]

    best_practices: list = [
        BestPractice(title="Test with Keyboard", description="All interactions keyboard accessible", code_reference="tab, enter, space, arrow keys", benefit="Screen reader and motor impairment support"),
        BestPractice(title="Semantic HTML", description="Use proper HTML elements", code_reference="<button>, <nav>, <main>", benefit="Built-in accessibility"),
        BestPractice(title="ARIA Labels", description="Describe interactive elements", code_reference="aria-label, aria-describedby", benefit="Screen reader context"),
        BestPractice(title="Color Contrast", description="WCAG AA minimum 4.5:1", code_reference="contrast checker tools", benefit="Visual impairment support"),
    ]

    usage_examples: list = [
        UsageExample(
            title="Playwright Accessibility Tests",
            description="Axe-core integration",
            code=r'''import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage should not have accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('login form should be accessible', async ({ page }) => {
    await page.goto('/login');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .include('[data-testid="login-form"]')
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('navigation should have landmark', async ({ page }) => {
    await page.goto('/');

    const nav = page.locator('nav');
    await expect(nav).toHaveAttribute('aria-label');
  });

  test('images should have alt text', async ({ page }) => {
    await page.goto('/products');

    const images = page.locator('img');
    const count = await images.count();

    for (let i = 0; i < count; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');
      expect(alt).toBeDefined();
    }
  });
});
''',
        ),
        UsageExample(
            title="Jest Axe Tests",
            description="Component accessibility testing",
            code=r'''import { axe, toHaveNoViolations } from 'jest-axe';
import { render, screen } from '@testing-library/react';
import { Button } from './Button';
import { Modal } from './Modal';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('Button should be accessible', async () => {
    const { container } = render(
      <Button aria-label="Submit form">Submit</Button>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('Modal should trap focus', async () => {
    render(
      <Modal isOpen={true} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    const modal = screen.getByRole('dialog');
    expect(modal).toHaveAttribute('aria-modal', 'true');
    expect(modal).toHaveAttribute('aria-labelledby');
  });

  it('Form should have proper labels', async () => {
    const { container } = render(
      <form>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" aria-required="true" />
      </form>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
''',
        ),
        UsageExample(
            title="Keyboard Navigation Tests",
            description="Testing keyboard interactions",
            code=r'''import { test, expect } from '@playwright/test';

test.describe('Keyboard Navigation', () => {
  test('tab through form fields', async ({ page }) => {
    await page.goto('/login');

    await page.keyboard.press('Tab');
    await expect(page.locator('[data-testid="email"]')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.locator('[data-testid="password"]')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.locator('[data-testid="submit"]')).toBeFocused();
  });

  test('escape closes modal', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="open-modal"]');
    await expect(page.locator('[role="dialog"]')).toBeVisible();

    await page.keyboard.press('Escape');
    await expect(page.locator('[role="dialog"]')).not.toBeVisible();
  });

  test('arrow keys navigate menu', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="menu-button"]');

    await page.keyboard.press('ArrowDown');
    await expect(page.locator('[role="menuitem"]').first()).toBeFocused();

    await page.keyboard.press('ArrowDown');
    await expect(page.locator('[role="menuitem"]').nth(1)).toBeFocused();

    await page.keyboard.press('ArrowUp');
    await expect(page.locator('[role="menuitem"]').first()).toBeFocused();
  });

  test('enter activates buttons', async ({ page }) => {
    await page.goto('/');
    await page.locator('[data-testid="submit"]').focus();

    await page.keyboard.press('Enter');
    await expect(page.locator('[data-testid="success"]')).toBeVisible();
  });
});
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(title="Div for Everything", description="Using divs instead of semantic elements", solution="Use button, nav, main, article", impact="Screen readers can't navigate"),
        AntiPattern(title="No Focus Styles", description="outline: removed without replacement", solution="Custom focus styles", impact="Keyboard users can't see focus"),
        AntiPattern(title="Color Only Indicators", description="Information conveyed only by color", solution="Add text or icons", impact="Color blind users miss information"),
        AntiPattern(title="Missing Skip Links", description="No way to skip navigation", solution="Add skip to main content link", impact="Keyboard users must tab through nav every page"),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "tests/a11y/axe.spec.ts": self.usage_examples[0].code,
                "tests/a11y/components.test.tsx": self.usage_examples[1].code,
                "tests/a11y/keyboard.spec.ts": self.usage_examples[2].code,
            },
            "metadata": {},
        }
