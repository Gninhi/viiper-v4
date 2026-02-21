"""
Performance Monitoring Skill.

APM tools, profiling, and performance optimization.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class PerformanceMonitoringSkill(Skill):
    """
    Application Performance Monitoring.

    Features:
    - APM integration (DataDog, New Relic)
    - Custom metrics
    - Distributed tracing
    - Profiling
    - Performance budgets
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Performance Monitoring",
        slug="performance-monitoring",
        category=SkillCategory.DEVOPS_MONITORING,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["apm", "performance", "datadog", "profiling", "tracing"],
        estimated_time_minutes=45,
        description="APM and performance monitoring setup",
    )

    dependencies: list = [
        Dependency(name="dd-trace", version="^4.0.0", package_manager="npm", reason="DataDog APM (Node.js)"),
        Dependency(name="ddtrace", version="^2.4.0", package_manager="pip", reason="DataDog APM (Python)"),
    ]

    best_practices: list = [
        BestPractice(title="Trace Key Operations", description="Instrument critical paths", code_reference="tracer.trace('db.query')", benefit="Visibility into performance bottlenecks"),
        BestPractice(title="Set Performance Budgets", description="Define SLOs for latency", code_reference="p95 < 200ms for API calls", benefit="Clear performance targets"),
        BestPractice(title="Profile in Production", description="Continuous profiling", code_reference="py-spy, clinic.js", benefit="Real-world performance data"),
        BestPractice(title="Monitor Business Metrics", description="Track conversions, not just tech metrics", code_reference="tracer.trace('checkout.completed')", benefit="Business impact visibility"),
    ]

    usage_examples: list = [
        UsageExample(
            name="DataDog APM (Node.js)",
            description="Express.js tracing",
            code=r'''import tracer from 'dd-trace';

tracer.init({
  service: 'myapp-api',
  env: process.env.NODE_ENV,
  version: process.env.APP_VERSION,
  logInjection: true,
  runtimeMetrics: true,
  profiling: true,
});

// Custom instrumentation
import { tracer } from 'dd-trace';

async function processOrder(order) {
  return tracer.trace('order.process', async (span) => {
    span.setTag('order.id', order.id);
    span.setTag('order.total', order.total);

    try {
      await validateOrder(order);
      await chargePayment(order);
      await shipOrder(order);

      span.setTag('order.status', 'completed');
      return { success: true };
    } catch (error) {
      span.setTag('error', error);
      span.setTag('order.status', 'failed');
      throw error;
    }
  });
}

// Database query tracing
tracer.use('pg', {
  service: 'myapp-db',
  queryTextMasking: true,
});
''',
        ),
        UsageExample(
            name="Performance Dashboard",
            description="Key metrics to monitor",
            code=r'''# Grafana dashboard panels

# API Latency (p50, p95, p99)
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))

# Error Rate by Endpoint
sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (endpoint)
/
sum(rate(http_requests_total[5m])) by (endpoint)

# Throughput (requests/second)
sum(rate(http_requests_total[5m])) by (endpoint)

# Database Query Performance
histogram_quantile(0.95, sum(rate(db_query_duration_seconds_bucket[5m])) by (le, query_type))

# Cache Hit Rate
sum(rate(cache_hits_total[5m]))
/
(sum(rate(cache_hits_total[5m])) + sum(rate(cache_misses_total[5m])))

# Memory Usage by Service
process_resident_memory_bytes / 1024 / 1024

# Active Connections
sum(http_active_connections) by (service)
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No Distributed Tracing - Can't trace requests across services...",
            why="Hard to debug performance issues",
            good="Implement tracing with correlation IDs"
        ),
        AntiPattern(
            bad="Only Monitoring Uptime - No business metrics tracked...",
            why="Missing business impact",
            good="Track conversions, user actions"
        ),
        AntiPattern(
            bad="Sampling Too Aggressive - Missing important traces...",
            why="Blind spots in monitoring",
            good="Adjust sample rate based on traffic"
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "datadog.node.ts": self.usage_examples[0].code,
                "grafana/performance-dashboard.json": self.usage_examples[1].code,
            },
            "metadata": {"apm_provider": options.get("provider", "datadog")},
        }
