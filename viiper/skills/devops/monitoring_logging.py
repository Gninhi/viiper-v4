"""
Monitoring & Logging Skill.

Production monitoring with Prometheus, Grafana, and centralized logging.
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


class MonitoringLoggingSkill(Skill):
    """
    Monitoring and logging patterns.

    Features:
    - Prometheus metrics collection
    - Grafana dashboards
    - Centralized logging (ELK/Loki)
    - Alert rules
    - Distributed tracing
    - Log aggregation
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Monitoring & Logging",
        slug="monitoring-logging",
        category=SkillCategory.DEVOPS_MONITORING,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["monitoring", "logging", "prometheus", "grafana", "elk", "observability"],
        estimated_time_minutes=60,
        description="Complete monitoring and logging setup",
    )

    dependencies: list = [
        Dependency(
            name="prom-client",
            version="^15.1.0",
            package_manager="npm",
            reason="Prometheus metrics (Node.js)",
        ),
        Dependency(
            name="prometheus-client",
            version="^0.19.0",
            package_manager="pip",
            reason="Prometheus metrics (Python)",
        ),
        Dependency(
            name="winston",
            version="^3.11.0",
            package_manager="npm",
            reason="Structured logging (Node.js)",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use RED/USE Metrics",
            description="Rate, Errors, Duration / Utilization, Saturation, Errors",
            code_reference="http_requests_total, http_request_duration_seconds",
            benefit="Standard metrics framework",
        ),
        BestPractice(
            title="Structured Logging",
            description="JSON format with consistent fields",
            code_reference="{level, timestamp, service, trace_id, message}",
            benefit="Queryable logs, better analysis",
        ),
        BestPractice(
            title="Correlation IDs",
            description="Track requests across services",
            code_reference="X-Correlation-ID header",
            benefit="Distributed tracing, debugging",
        ),
        BestPractice(
            title="Log Levels",
            description="DEBUG, INFO, WARN, ERROR, FATAL",
            code_reference="logger.error('Database connection failed')",
            benefit="Proper alerting, noise reduction",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Prometheus Metrics (Node.js)",
            description="Express.js middleware for metrics",
            code=r'''import promClient from 'prom-client';

// Create Registry
const register = new promClient.Registry();
promClient.collectDefaultMetrics({ register });

// Custom metrics
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10],
  registers: [register],
});

const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register],
});

const activeConnections = new promClient.Gauge({
  name: 'http_active_connections',
  help: 'Number of active HTTP connections',
  registers: [register],
});

// Metrics middleware
export function metricsMiddleware(req, res, next) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route?.path || req.path;

    httpRequestDuration
      .labels(req.method, route, res.statusCode)
      .observe(duration);

    httpRequestsTotal
      .labels(req.method, route, res.statusCode)
      .inc();
  });

  next();
}

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
''',
        ),
        UsageExample(
            name="Structured Logging (Node.js)",
            description="Winston with JSON format",
            code=r'''import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'ISO8601' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'api-service',
    version: process.env.APP_VERSION || 'dev',
  },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      ),
    }),
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error',
      maxsize: 10485760, // 10MB
      maxFiles: 5,
    }),
    new winston.transports.File({
      filename: 'logs/combined.log',
      maxsize: 10485760,
      maxFiles: 5,
    }),
  ],
});

// Request logging middleware
export function requestLogger(req, res, next) {
  const startTime = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - startTime;
    logger.info({
      message: 'HTTP request',
      type: 'http',
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration_ms: duration,
      ip: req.ip,
      user_agent: req.get('user-agent'),
      trace_id: req.headers['x-correlation-id'],
    });
  });

  next();
}

// Usage
logger.info('Server started', { port: 3000, env: process.env.NODE_ENV });
logger.error('Database connection failed', { error, retryCount: 3 });
''',
        ),
        UsageExample(
            name="Prometheus Alert Rules",
            description="Alerting rules for common scenarios",
            code=r'''groups:
  - name: application_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} over 5 minutes"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m]))
            by (le, route)
          ) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s for route {{ $labels.route }}"

      - alert: ServiceDown
        expr: up{job="api-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"

      - alert: HighMemoryUsage
        expr: |
          (process_resident_memory_bytes / memory_total_bytes) > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value | humanizePercentage }}"
''',
        ),
        UsageExample(
            name="Grafana Dashboard JSON",
            description="Application metrics dashboard",
            code=r'''{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (route)",
            "legendFormat": "{{ route }}"
          }
        ]
      },
      {
        "id": 2,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
            "legendFormat": "Error Rate"
          }
        ]
      },
      {
        "id": 3,
        "title": "Latency (p50, p95, p99)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p99"
          }
        ]
      }
    ]
  }
}
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Logging Secrets - Sensitive data in logs",
            why="Security breach, compliance violation",
            good="Mask passwords, tokens, PII",
        ),
        AntiPattern(
            bad="No Log Rotation - Logs grow indefinitely",
            why="Disk full, performance issues",
            good="Implement log rotation, retention policy",
        ),
        AntiPattern(
            bad="Too Many Metrics - High cardinality labels",
            why="Prometheus memory explosion",
            good="Avoid user_id, request_id as labels",
        ),
        AntiPattern(
            bad="No Alert Fatigue Management - Too many alerts",
            why="Ignored alerts, burnout",
            good="Alert on symptoms, not causes",
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate monitoring configuration."""
        options = options or {}

        include_prometheus = options.get("include_prometheus", True)
        include_grafana = options.get("include_grafana", True)
        include_alerts = options.get("include_alerts", True)

        result = {
            "files": {},
            "metadata": {
                "includes_prometheus": include_prometheus,
                "includes_grafana": include_grafana,
                "includes_alerts": include_alerts,
            }
        }

        if include_prometheus:
            result["files"]["prometheus.yml"] = r'''global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'api-service'
    static_configs:
      - targets: ['api:3000']
    metrics_path: '/metrics'

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

rule_files:
  - 'alerts/*.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
'''
        if include_alerts:
            result["files"]["alerts/application_alerts.yml"] = self.usage_examples[2].code

        if include_grafana:
            result["files"]["grafana/dashboards/application.json"] = self.usage_examples[3].code

        return result
