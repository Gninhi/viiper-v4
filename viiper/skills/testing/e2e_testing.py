"""
E2E Testing Skill.

Playwright and Cypress patterns for end-to-end testing.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class E2ETestingSkill(Skill):
    """
    End-to-end testing with Playwright and Cypress.

    Features:
    - Browser automation
    - Visual regression testing
    - Network mocking
    - Multi-browser testing
    - Mobile emulation
    - Screenshots and videos
    """

    metadata: SkillMetadata = SkillMetadata(
        name="E2E Testing",
        slug="e2e-testing",
        category=SkillCategory.TESTING_E2E,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["testing", "e2e", "playwright", "cypress", "browser-automation"],
        estimated_time_minutes=60,
        description="End-to-end browser testing with Playwright",
    )

    dependencies: list = [
        Dependency(name="@playwright/test", version="^1.40.0", package_manager="npm", reason="E2E testing framework"),
        Dependency(name="cypress", version="^13.6.0", package_manager="npm", reason="Alternative E2E framework"),
    ]

    best_practices: list = [
        BestPractice(title="Test User Journeys", description="Complete user flows", code_reference="login -> browse -> add to cart -> checkout", benefit="Real user scenario validation"),
        BestPractice(title="Data Attributes", description="Use data-testid for selectors", code_reference="data-testid='submit-button'", benefit="Stable selectors, refactoring safe"),
        BestPractice(title="Page Object Model", description="Encapsulate page interactions", code_reference="class LoginPage { ... }", benefit="DRY, maintainable tests"),
        BestPractice(title="Network Mocking", description="Mock API responses when needed", code_reference="page.route('**/api/**', route => ...)", benefit="Faster tests, test edge cases"),
    ]

    usage_examples: list = [
        UsageExample(
            title="Playwright E2E Tests",
            description="Complete user flow testing",
            code=r'''import { test, expect } from '@playwright/test';

test.describe('E-Commerce Flow', () => {
  test('complete purchase flow', async ({ page }) => {
    // Navigate to homepage
    await page.goto('/');

    // Search for product
    await page.fill('[data-testid="search-input"]', 'Laptop');
    await page.click('[data-testid="search-button"]');

    // Wait for results and click first product
    await page.waitForSelector('[data-testid="product-card"]');
    await page.click('[data-testid="product-card"] >> nth=0');

    // Add to cart
    await page.click('[data-testid="add-to-cart"]');

    // Verify cart badge
    await expect(page.locator('[data-testid="cart-badge"]')).toHaveText('1');

    // Go to cart
    await page.click('[data-testid="cart-button"]');
    await page.waitForURL('/cart');

    // Verify product in cart
    await expect(page.locator('[data-testid="cart-item"]')).toBeVisible();

    // Checkout
    await page.click('[data-testid="checkout-button"]');

    // Fill shipping info
    await page.fill('[data-testid="shipping-name"]', 'John Doe');
    await page.fill('[data-testid="shipping-address"]', '123 Main St');
    await page.fill('[data-testid="shipping-city"]', 'New York');

    // Place order
    await page.click('[data-testid="place-order"]');

    // Verify success
    await page.waitForURL('/order-success');
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="order-number"]')).toBeVisible();
  });

  test('login and access dashboard', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'user@example.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="login-button"]');

    await page.waitForURL('/dashboard');
    await expect(page.locator('[data-testid="welcome-message"]')).toContainText('Welcome');
  });

  test('responsive design - mobile', async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 375, height: 667 },
      deviceScaleFactor: 2,
    });
    const page = await context.newPage();

    await page.goto('/');
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();

    await context.close();
  });
});
''',
        ),
        UsageExample(
            title="Playwright Config",
            description="Configuration for E2E tests",
            code=r'''// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['json', { outputFile: 'results.json' }]],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
''',
        ),
        UsageExample(
            title="Page Object Model",
            description="Reusable page objects",
            code=r'''// tests/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email"]');
    this.passwordInput = page.locator('[data-testid="password"]');
    this.submitButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async loginWithInvalidCredentials(email: string, password: string) {
    await this.login(email, password);
    return this.errorMessage.textContent();
  }
}

// tests/pages/DashboardPage.ts
export class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly navigation: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.locator('[data-testid="welcome-message"]');
    this.navigation = page.locator('[data-testid="main-nav"]');
  }

  async waitForLoad() {
    await this.welcomeMessage.waitFor({ state: 'visible' });
  }

  async getWelcomeMessage() {
    return this.welcomeMessage.textContent();
  }
}

// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

test.describe('Login', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
  });

  test('successful login', async ({ page }) => {
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');
    await dashboardPage.waitForLoad();
    await expect(dashboardPage.welcomeMessage).toContainText('Welcome');
  });

  test('failed login', async () => {
    await loginPage.goto();
    const error = await loginPage.loginWithInvalidCredentials('bad@email.com', 'wrong');
    expect(error).toContain('Invalid credentials');
  });
});
''',
        ),
        UsageExample(
            title="Visual Regression Testing",
            description="Screenshot comparisons",
            code=r'''import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage should match snapshot', async ({ page }) => {
    await page.goto('/');

    // Full page screenshot
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test('component should match snapshot', async ({ page }) => {
    await page.goto('/components');

    const button = page.locator('[data-testid="primary-button"]');
    await expect(button).toHaveScreenshot('primary-button.png');
  });

  test('dark mode should match snapshot', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="theme-toggle"]');

    await expect(page).toHaveScreenshot('homepage-dark.png');
  });
});
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(title="Fragile Selectors", description="CSS selectors that break easily", solution="Use data-testid attributes", impact="Brittle tests, maintenance burden"),
        AntiPattern(title="Testing Everything", description="E2E tests for all scenarios", solution="Test pyramid: more unit, fewer E2E", impact="Slow CI, flaky tests"),
        AntiPattern(title="No Wait Strategy", description="Fixed delays everywhere", solution="Use proper wait conditions", impact="Slow or flaky tests"),
        AntiPattern(title("Ignoring Mobile", description="Only testing desktop", solution="Test on mobile viewports", impact="Missing mobile bugs"),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "tests/e2e/checkout.spec.ts": self.usage_examples[0].code,
                "playwright.config.ts": self.usage_examples[1].code,
                "tests/pages/LoginPage.ts": self.usage_examples[2].code,
                "tests/e2e/visual.spec.ts": self.usage_examples[3].code,
            },
            "metadata": {"framework": "playwright"},
        }
