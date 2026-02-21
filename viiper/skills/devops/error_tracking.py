"""
Error Tracking Skill.

Sentry integration for production error tracking and performance monitoring.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class ErrorTrackingSkill(Skill):
    """
    Error tracking with Sentry.

    Features:
    - Automatic error capture
    - Performance monitoring
    - User feedback
    - Release tracking
    - Source maps
    - Custom breadcrumbs
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Error Tracking",
        slug="error-tracking",
        category=SkillCategory.DEVOPS_MONITORING,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["sentry", "error-tracking", "monitoring", "debugging", "performance"],
        estimated_time_minutes=30,
        description="Sentry integration for error tracking and performance",
    )

    dependencies: list = [
        Dependency(name="@sentry/node", version="^7.91.0", package_manager="npm", reason="Sentry SDK (Node.js)"),
        Dependency(name="@sentry/react", version="^7.91.0", package_manager="npm", reason="Sentry React integration"),
        Dependency(name="sentry-sdk", version="^1.39.0", package_manager="pip", reason="Sentry SDK (Python)"),
    ]

    best_practices: list = [
        BestPractice(title="Use Release Tracking", description="Tag errors with release version", code_reference="Sentry.init({ release: '1.0.0' })", benefit="Track errors per release, see what fixed them"),
        BestPractice(title="Configure Sample Rates", description="Adjust sampling for high-traffic apps", code_reference="tracesSampleRate: 0.1", benefit="Cost control, performance"),
        BestPractice(title="Add User Context", description="Associate errors with users", code_reference="Sentry.setUser({ id, email })", benefit="Better debugging, user impact analysis"),
        BestPractice(title="Use Breadcrumbs", description="Track user actions before errors", code_reference="Sentry.addBreadcrumb({ message, category })", benefit="Context for debugging"),
    ]

    usage_examples: list = [
        UsageExample(
            name="Sentry Setup (Node.js)",
            description="Express.js integration",
            code=r'''import * as Sentry from "@sentry/node";
import { nodeProfilingIntegration } from "@sentry/profiling-node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
  integrations: [
    nodeProfilingIntegration(),
    Sentry.httpIntegration(),
    Sentry.expressIntegration(),
  ],
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
  profilesSampleRate: 0.1,
  beforeSend(event, hint) {
    // Filter out sensitive data
    if (event.request?.headers?.authorization) {
      delete event.request.headers.authorization;
    }
    return event;
  },
});

const app = express();
app.use(Sentry.requestHandler());
app.use(Sentry.tracingHandler());

// Error handler
app.use(Sentry.errorHandler());
''',
        ),
        UsageExample(
            name="Sentry Setup (Python)",
            description="FastAPI integration",
            code=r'''import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENVIRONMENT", "development"),
    release=os.getenv("APP_VERSION", "dev"),
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1 if os.getenv("ENVIRONMENT") == "production" else 1.0,
    profiles_sample_rate=0.1,
    before_send=lambda event, hint: event,
)
''',
        ),
        UsageExample(
            name="Custom Error Context",
            description="Add context to errors",
            code=r'''import Sentry from "@sentry/node";

// Set user context
Sentry.setUser({
  id: user.id,
  email: user.email,
  username: user.username,
});

// Add breadcrumb
Sentry.addBreadcrumb({
  category: 'auth',
  message: 'User logged in',
  level: 'info',
  data: { userId: user.id },
});

// Add tags
Sentry.setTag('feature', 'checkout');
Sentry.setTag('payment_method', 'stripe');

// Capture exception with context
try {
  await processPayment(order);
} catch (error) {
  Sentry.captureException(error, {
    extra: {
      orderId: order.id,
      amount: order.total,
      currency: order.currency,
    },
    level: 'error',
  });
}
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Logging PII - Personal data in error reports...",
            why="GDPR violation, privacy breach",
            good="Filter sensitive data in beforeSend"
        ),
        AntiPattern(
            bad="100% Sample Rate in Production - Capturing all transactions...",
            why="High costs, performance impact",
            good="Use 0.1 or lower for production"
        ),
        AntiPattern(
            bad="No Release Tracking - Errors not linked to versions...",
            why="Can't track which release caused error",
            good="Set release version on init"
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "sentry.node.ts": self.usage_examples[0].code,
                "sentry.python.py": self.usage_examples[1].code,
            },
            "metadata": {"framework": options.get("framework", "express")},
        }
