"""
Event Tracking Skill.

Analytics event tracking with Mixpanel, Amplitude, and custom solutions.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class EventTrackingSkill(Skill):
    """
    Event tracking for analytics.

    Features:
    - Client-side tracking
    - Server-side tracking
    - User identification
    - Event properties
    - Batch processing
    - Privacy compliance
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Event Tracking",
        slug="event-tracking",
        category=SkillCategory.DATA_ANALYTICS,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["analytics", "tracking", "mixpanel", "amplitude", "events", "telemetry"],
        estimated_time_minutes=35,
        description="Event tracking for user analytics",
    )

    dependencies: list = [
        Dependency(name="mixpanel", version="^2.45.0", package_manager="npm", reason="Mixpanel SDK"),
        Dependency(name="@amplitude/analytics-browser", version="^2.3.0", package_manager="npm", reason="Amplitude SDK"),
        Dependency(name="posthog-js", version="^1.96.0", package_manager="npm", reason="PostHog SDK"),
    ]

    best_practices: list = [
        BestPractice(title="Consistent Naming", description="Snake case for events", code_reference="user_signed_up, purchase_completed", benefit="Discoverability, consistency"),
        BestPractice(title="User Identification", description="Identify users early", code_reference="analytics.identify(userId)", benefit="Cross-device tracking"),
        BestPractice(title="Rich Properties", description="Include context with events", code_reference="{ plan: 'pro', source: 'homepage' }", benefit="Better analysis"),
        BestPractice(title="Privacy First", description="Don't track sensitive data", code_reference="No passwords, PII in events", benefit="GDPR compliance"),
    ]

    usage_examples: list = [
        UsageExample(
            name="Analytics Service (Node.js)",
            description="Unified tracking interface",
            code=r'''import Mixpanel from 'mixpanel';

const mixpanel = Mixpanel.init(process.env.MIXPANEL_TOKEN);

interface TrackOptions {
  userId?: string;
  properties?: Record<string, any>;
}

class AnalyticsService {
  identify(userId: string, traits?: Record<string, any>) {
    mixpanel.people.set(userId, {
      $name: traits?.name,
      $email: traits?.email,
      $created: new Date().toISOString(),
      ...traits,
    });
  }

  track(eventName: string, options: TrackOptions = {}) {
    const { userId, properties } = options;

    mixpanel.track(eventName, {
      distinct_id: userId,
      time: new Date(),
      ...properties,
    });
  }

  // E-commerce events
  trackPurchase(userId: string, order: { id: string; total: number; items: any[] }) {
    this.track('purchase_completed', {
      userId,
      properties: {
        order_id: order.id,
        revenue: order.total,
        items_count: order.items.length,
      },
    });

    for (const item of order.items) {
      this.track('item_purchased', {
        userId,
        properties: {
          product_id: item.id,
          product_name: item.name,
          price: item.price,
          quantity: item.quantity,
        },
      });
    }
  }

  // User events
  trackSignup(userId: string, source?: string) {
    this.track('user_signed_up', {
      userId,
      properties: { source },
    });
  }

  trackLogin(userId: string) {
    this.track('user_logged_in', { userId });
  }

  // Feature usage
  trackFeatureUsage(userId: string, feature: string, action: string) {
    this.track('feature_used', {
      userId,
      properties: { feature, action },
    });
  }
}

export const analytics = new AnalyticsService();
''',
        ),
        UsageExample(
            name="Client-side Tracking (React)",
            description="React hooks for tracking",
            code=r'''import { useEffect, useCallback } from 'react';
import { analytics } from '../services/analytics';

// Hook for tracking page views
export function usePageView(pageName: string) {
  useEffect(() => {
    analytics.track('page_view', {
      properties: { page: pageName, path: window.location.pathname },
    });
  }, [pageName]);
}

// Hook for tracking clicks
export function useTrackClick(eventName: string, properties?: Record<string, any>) {
  return useCallback(
    (event: React.MouseEvent) => {
      analytics.track(eventName, { properties });
    },
    [eventName, properties]
  );
}

// Component example
export function SignupButton() {
  const handleClick = useTrackClick('signup_button_clicked', {
    location: 'homepage',
  });

  return (
    <button onClick={handleClick} data-testid="signup-button">
      Sign Up Free
    </button>
  );
}

// Track form submission
export function LoginForm() {
  const handleSubmit = async (data) => {
    try {
      await login(data);
      analytics.track('login_completed');
    } catch (error) {
      analytics.track('login_failed', {
        properties: { error: error.message },
      });
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}

// Track funnel steps
export function CheckoutFlow() {
  usePageView('checkout');

  const trackStep = (step: number) => {
    analytics.track('checkout_step', {
      properties: { step_number: step },
    });
  };

  return (
    <div>
      <button onClick={() => trackStep(1)}>Shipping</button>
      <button onClick={() => trackStep(2)}>Payment</button>
      <button onClick={() => trackStep(3)}>Confirm</button>
    </div>
  );
}
''',
        ),
        UsageExample(
            name="Server-side Events (Python)",
            description="FastAPI analytics middleware",
            code=r'''from fastapi import Request, Response
from posthog import Posthog

posthog = Posthog(
    project_api_key=os.getenv('POSTHOG_API_KEY'),
    host=os.getenv('POSTHOG_HOST'),
)

def identify_user(request: Request, user_id: str):
    """Identify user for tracking"""
    posthog.identify(
        distinct_id=user_id,
        properties={
            'email': request.state.user.email,
            'plan': request.state.user.plan,
        },
    )

def track_event(user_id: str, event: str, properties: dict = None):
    """Track an event"""
    posthog.capture(
        distinct_id=user_id,
        event=event,
        properties=properties,
    )

# Middleware for automatic tracking
@app.middleware("http")
async def track_requests(request: Request, call_next):
    # Track page view
    if request.method == "GET":
        track_event(
            user_id=request.state.user_id if hasattr(request.state, 'user_id') else 'anonymous',
            event='page_view',
            properties={'path': request.url.path},
        )

    response = await call_next(request)

    # Track response
    track_event(
        user_id=request.state.user_id if hasattr(request.state, 'user_id') else 'anonymous',
        event='api_request',
        properties={
            'method': request.method,
            'path': request.url.path,
            'status': response.status_code,
        },
    )

    return response
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(bad="Tracking PII", why="Personal data in events", good="Hash or avoid PII"),
        AntiPattern(bad="Inconsistent Naming", why="Mixed naming conventions", good="Establish naming convention"),
        AntiPattern(bad="No Event Schema", why="Unstructured event properties", good="Define event schemas"),
        AntiPattern(bad="Tracking Everything", why="No filtering of events", good="Track only meaningful events"),
    ]

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        return {
            "files": {
                "services/analytics.ts": self.usage_examples[0].code,
                "hooks/useAnalytics.ts": self.usage_examples[1].code,
                "middleware/analytics.py": self.usage_examples[2].code,
            },
            "metadata": {},
        }
