"""
Elite Architecture Agents - World-Class System Design.

Produces enterprise-grade, scalable, and innovative architectures.
"""

from typing import Dict, Any, List
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from viiper.agents.design_excellence import DesignPhilosophy


class EliteSystemDesignAgent(Agent):
    """
    Elite agent for world-class system architecture.

    Capabilities:
    - Enterprise-grade system design
    - Scalability planning (Netflix, Uber scale)
    - Microservices/Event-driven architectures
    - Cloud-native patterns
    - Performance optimization strategies

    Philosophy: Design for scale, design for failure, design for evolution.
    """

    name: str = "Elite System Design Agent"
    role: AgentRole = AgentRole.ARCHITECTURE
    capabilities: list = [
        AgentCapability.SYSTEM_DESIGN,
        AgentCapability.SCALABILITY_PLANNING
    ]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute elite system design task.

        Produces enterprise-grade architecture specifications.
        """
        context = self._parse_context(task.description)

        result = {
            "task_id": task.id,
            "task_name": task.name,

            # Architecture Design
            "architecture_style": self._select_architecture_style(context),
            "system_components": self._design_system_components(context),
            "data_architecture": self._design_data_architecture(context),
            "communication_patterns": self._design_communication_patterns(context),

            # Scalability & Performance
            "scalability_strategy": self._design_scalability_strategy(context),
            "performance_targets": self._set_performance_targets(context),
            "caching_strategy": self._design_caching_strategy(context),

            # Reliability & Resilience
            "fault_tolerance": self._design_fault_tolerance(context),
            "disaster_recovery": self._design_disaster_recovery(),
            "monitoring_strategy": self._design_monitoring_strategy(),

            # Security Architecture
            "security_architecture": self._design_security_architecture(context),
            "compliance_requirements": self._identify_compliance_requirements(context),

            # Cloud & Infrastructure
            "cloud_strategy": self._design_cloud_strategy(context),
            "infrastructure_as_code": self._recommend_iac_tools(),

            # Documentation
            "architecture_diagrams": self._specify_diagrams(),
            "design_decisions": self._document_design_decisions(context),
            "trade_offs": self._analyze_trade_offs(context),

            # Best Practices
            "industry_references": self._provide_industry_references(context),
            "anti_patterns_to_avoid": self._identify_anti_patterns(),

            "confidence": 0.96,
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse context and extract system requirements."""
        description_lower = description.lower()

        # Determine scale
        scale = "medium"
        if any(word in description_lower for word in ["million", "large", "enterprise", "global"]):
            scale = "large"
        elif any(word in description_lower for word in ["startup", "small", "mvp"]):
            scale = "small"

        # Determine domain
        domain = "general"
        if "saas" in description_lower:
            domain = "saas"
        elif "ecommerce" in description_lower or "marketplace" in description_lower:
            domain = "ecommerce"
        elif "fintech" in description_lower or "payment" in description_lower:
            domain = "fintech"
        elif "social" in description_lower:
            domain = "social"
        elif "iot" in description_lower:
            domain = "iot"

        return {
            "description": description,
            "scale": scale,
            "domain": domain,
            "target_users": self._estimate_user_scale(scale),
            "availability_requirement": "99.99%" if scale == "large" else "99.9%"
        }

    def _estimate_user_scale(self, scale: str) -> str:
        """Estimate user scale."""
        scales = {
            "small": "1K - 100K users",
            "medium": "100K - 10M users",
            "large": "10M+ users (Netflix/Uber scale)"
        }
        return scales.get(scale, "100K - 10M users")

    def _select_architecture_style(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select optimal architecture style.

        Returns world-class architecture pattern.
        """
        scale = context.get("scale", "medium")
        domain = context.get("domain", "general")

        # Architecture styles for different scales
        if scale == "small":
            style = "modular_monolith"
            rationale = "Start simple, evolve to microservices when needed"
            examples = ["Linear (early days)", "GitHub (early days)"]
        elif scale == "medium":
            style = "service_oriented"
            rationale = "Balance complexity and scalability"
            examples = ["Shopify", "Stripe"]
        else:  # large
            style = "microservices_event_driven"
            rationale = "Ultimate scalability and team autonomy"
            examples = ["Netflix", "Uber", "Amazon"]

        return {
            "style": style,
            "rationale": rationale,
            "characteristics": self._get_architecture_characteristics(style),
            "when_to_use": f"{scale.capitalize()} scale projects",
            "examples": examples,
            "evolution_path": self._describe_evolution_path(style)
        }

    def _get_architecture_characteristics(self, style: str) -> List[str]:
        """Get characteristics of architecture style."""
        characteristics = {
            "modular_monolith": [
                "Single deployable unit with clear module boundaries",
                "Shared database with logical separation",
                "Internal APIs between modules",
                "Easy to start, can evolve to microservices",
                "Lower operational complexity"
            ],
            "service_oriented": [
                "3-7 core services with clear responsibilities",
                "Each service has own database (database per service)",
                "API gateway for external traffic",
                "Service mesh for internal communication",
                "Moderate operational complexity"
            ],
            "microservices_event_driven": [
                "10+ small, focused services",
                "Event-driven communication via message broker",
                "Complete service autonomy",
                "Polyglot persistence (different DBs per service)",
                "High operational complexity, requires DevOps maturity"
            ]
        }
        return characteristics.get(style, [])

    def _describe_evolution_path(self, current_style: str) -> str:
        """Describe how architecture can evolve."""
        paths = {
            "modular_monolith": "Modular Monolith → Extract services gradually → Microservices",
            "service_oriented": "Service-Oriented → Add more services → Event-driven microservices",
            "microservices_event_driven": "Already at peak, focus on optimization"
        }
        return paths.get(current_style, "Evolve based on needs")

    def _design_system_components(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design core system components."""
        scale = context.get("scale", "medium")
        domain = context.get("domain", "general")

        components = {
            "api_layer": {
                "type": "API Gateway + BFF (Backend for Frontend)",
                "tech": "GraphQL Federation or REST with Kong/Nginx",
                "responsibilities": [
                    "Request routing and load balancing",
                    "Authentication and authorization",
                    "Rate limiting and throttling",
                    "Request/response transformation",
                    "API versioning"
                ],
                "pattern": "Gateway Aggregation Pattern"
            },
            "core_services": self._design_core_services(domain),
            "data_layer": {
                "primary_database": "PostgreSQL (ACID guarantees)",
                "caching": "Redis + CDN",
                "search": "Elasticsearch or Algolia",
                "analytics": "ClickHouse or BigQuery",
                "pattern": "Database Per Service + CQRS"
            },
            "messaging": {
                "async_communication": "Apache Kafka or RabbitMQ",
                "real_time": "WebSockets via Socket.io or Centrifugo",
                "pattern": "Event-Driven Architecture"
            },
            "storage": {
                "object_storage": "S3 or CloudFlare R2",
                "cdn": "CloudFlare or Fastly",
                "pattern": "Content Delivery Network"
            }
        }

        if scale == "large":
            components["orchestration"] = {
                "container_orchestration": "Kubernetes (EKS/GKE)",
                "service_mesh": "Istio or Linkerd",
                "pattern": "Sidecar Pattern for cross-cutting concerns"
            }

        return components

    def _design_core_services(self, domain: str) -> List[Dict[str, Any]]:
        """Design domain-specific core services."""
        service_patterns = {
            "saas": [
                {"name": "Auth Service", "responsibility": "User authentication, sessions, SSO"},
                {"name": "User Service", "responsibility": "User profiles, preferences, teams"},
                {"name": "Billing Service", "responsibility": "Subscriptions, payments, invoices"},
                {"name": "Notification Service", "responsibility": "Email, SMS, push notifications"},
                {"name": "Analytics Service", "responsibility": "Events, metrics, dashboards"}
            ],
            "ecommerce": [
                {"name": "Product Catalog", "responsibility": "Products, inventory, search"},
                {"name": "Order Service", "responsibility": "Cart, checkout, order management"},
                {"name": "Payment Service", "responsibility": "Payment processing, refunds"},
                {"name": "Shipping Service", "responsibility": "Shipping, tracking, logistics"},
                {"name": "Recommendation Service", "responsibility": "Personalization, ML-based recommendations"}
            ],
            "fintech": [
                {"name": "Account Service", "responsibility": "Account management, KYC"},
                {"name": "Transaction Service", "responsibility": "Payment processing, ledger"},
                {"name": "Compliance Service", "responsibility": "AML, fraud detection"},
                {"name": "Reporting Service", "responsibility": "Statements, tax documents"},
                {"name": "Integration Service", "responsibility": "External bank/payment integrations"}
            ]
        }

        return service_patterns.get(domain, service_patterns["saas"])

    def _design_data_architecture(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design world-class data architecture."""
        return {
            "data_strategy": "Polyglot Persistence - Right tool for the right job",
            "databases": {
                "transactional": {
                    "tech": "PostgreSQL with read replicas",
                    "use_case": "Core business data (users, orders, etc.)",
                    "pattern": "Primary-Replica replication"
                },
                "caching": {
                    "tech": "Redis Cluster",
                    "use_case": "Session data, frequently accessed data",
                    "ttl_strategy": "Short TTL (5-60min) for hot data"
                },
                "search": {
                    "tech": "Elasticsearch",
                    "use_case": "Full-text search, faceted search",
                    "indexing": "Near real-time via Change Data Capture"
                },
                "analytics": {
                    "tech": "ClickHouse or BigQuery",
                    "use_case": "OLAP queries, dashboards, reports",
                    "data_pipeline": "ETL via Apache Airflow"
                },
                "time_series": {
                    "tech": "TimescaleDB or InfluxDB",
                    "use_case": "Metrics, logs, events",
                    "retention": "Hot: 30 days, Warm: 90 days, Cold: 1 year"
                }
            },
            "data_consistency": {
                "pattern": "Eventual Consistency with Saga Pattern",
                "compensation": "Compensating transactions for failures",
                "example": "Order placed → Inventory reserved → Payment processed → Notification sent"
            },
            "data_migration": {
                "strategy": "Blue-Green deployments with dual writes",
                "tools": "Liquibase or Flyway for schema migrations"
            },
            "backup_strategy": {
                "frequency": "Continuous (PITR - Point in Time Recovery)",
                "retention": "30 days hot, 1 year cold",
                "testing": "Monthly restore drills"
            }
        }

    def _design_communication_patterns(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design service communication patterns."""
        return {
            "synchronous": {
                "pattern": "REST API or gRPC",
                "when": "Real-time response needed (user-facing requests)",
                "timeout": "3-5 seconds with circuit breaker",
                "retry": "Exponential backoff (3 retries max)"
            },
            "asynchronous": {
                "pattern": "Event-Driven via Message Broker (Kafka)",
                "when": "Non-critical, long-running, or fan-out operations",
                "benefits": [
                    "Decoupling of services",
                    "Better fault tolerance",
                    "Natural audit log",
                    "Replay capability"
                ],
                "example": "User signed up → Email service + Analytics service + CRM service"
            },
            "api_design": {
                "rest": {
                    "versioning": "URL versioning (/v1/users)",
                    "pagination": "Cursor-based for large datasets",
                    "filtering": "Query params with JSON:API spec",
                    "standards": "RESTful maturity level 2-3"
                },
                "graphql": {
                    "when": "Complex data fetching requirements",
                    "tools": "Apollo Federation for distributed schemas",
                    "benefits": "Frontend controls data shape, reduces over-fetching"
                }
            },
            "service_mesh": {
                "tech": "Istio or Linkerd",
                "features": [
                    "Automatic retry and circuit breaking",
                    "Mutual TLS between services",
                    "Distributed tracing",
                    "Traffic management (canary deployments)"
                ]
            }
        }

    def _design_scalability_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design comprehensive scalability strategy."""
        return {
            "horizontal_scaling": {
                "approach": "Stateless services with auto-scaling",
                "metrics": "CPU > 70% or custom metrics (queue depth)",
                "scaling_rules": [
                    "Scale out: Add instances when load increases",
                    "Scale in: Remove instances during low traffic (save cost)",
                    "Min replicas: 2 (HA), Max: Dynamic based on traffic"
                ]
            },
            "vertical_scaling": {
                "when": "Database, cache, specific bottlenecks",
                "approach": "Upgrade instance types during low-traffic windows",
                "limits": "Know limits - plan horizontal split before maxing out"
            },
            "database_scaling": {
                "read_replicas": "2-5 replicas for read-heavy workloads",
                "sharding": "Shard by user_id or tenant_id when > 10M records",
                "partitioning": "Time-based partitioning for analytics tables",
                "connection_pooling": "PgBouncer to reduce connection overhead"
            },
            "caching_layers": {
                "cdn": "Static assets (images, CSS, JS) - 90%+ cache hit rate",
                "application_cache": "Redis for session, API responses - 70%+ hit rate",
                "database_cache": "PostgreSQL query cache + shared buffers",
                "strategy": "Cache invalidation via TTL + Event-driven purge"
            },
            "queue_management": {
                "pattern": "Background jobs via queue (Sidekiq, Bull)",
                "priority_queues": "Critical, High, Normal, Low",
                "dead_letter_queue": "Failed jobs for manual review",
                "monitoring": "Queue depth alerts (> 1000 = scale workers)"
            },
            "load_balancing": {
                "layer_7": "Application load balancer (ALB) - HTTP/HTTPS",
                "layer_4": "Network load balancer (NLB) - TCP/UDP",
                "algorithm": "Least connections or round-robin",
                "health_checks": "HTTP 200 on /health endpoint"
            }
        }

    def _set_performance_targets(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Set world-class performance targets."""
        return {
            "api_response_time": "p50: <100ms, p95: <300ms, p99: <500ms",
            "page_load_time": "FCP < 1.5s, LCP < 2.5s, TTI < 3.8s",
            "throughput": "10,000+ requests/second per service",
            "database_query": "p95: <50ms, p99: <100ms",
            "cache_hit_rate": "> 80% for hot data",
            "uptime": context.get("availability_requirement", "99.9%"),
            "error_rate": "< 0.1% (1 error per 1000 requests)",
            "concurrent_users": f"{context.get('target_users', '100K users')}"
        }

    def _design_caching_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design multi-layer caching strategy."""
        return {
            "layers": {
                "L1_CDN": {
                    "scope": "Static assets (images, CSS, JS, fonts)",
                    "ttl": "1 year with cache busting",
                    "hit_rate_target": "> 95%"
                },
                "L2_API_Gateway": {
                    "scope": "Public API responses",
                    "ttl": "5-60 minutes",
                    "invalidation": "Purge on data update events"
                },
                "L3_Application_Cache": {
                    "scope": "User sessions, computed data",
                    "tech": "Redis",
                    "ttl": "15 minutes - 24 hours",
                    "pattern": "Cache-Aside (Lazy Loading)"
                },
                "L4_Database_Query_Cache": {
                    "scope": "Frequently executed queries",
                    "tech": "PostgreSQL query cache",
                    "ttl": "1-5 minutes"
                }
            },
            "cache_warming": "Pre-populate cache with popular data during deployment",
            "cache_stampede_prevention": "Use locking or probabilistic early expiration",
            "monitoring": "Track hit rate, evictions, memory usage"
        }

    def _design_fault_tolerance(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design fault-tolerant system."""
        return {
            "redundancy": {
                "multi_az": "Deploy across 2-3 availability zones",
                "multi_region": "Critical services in 2+ regions (disaster recovery)",
                "redundant_components": "No single point of failure"
            },
            "circuit_breaker": {
                "pattern": "Circuit Breaker Pattern (Hystrix/Resilience4j)",
                "states": "Closed → Open (failures) → Half-Open (test) → Closed",
                "threshold": "Open after 50% failure rate in 10s window",
                "timeout": "Try again after 30s"
            },
            "retry_logic": {
                "pattern": "Exponential backoff with jitter",
                "attempts": "3 retries max",
                "backoff": "100ms, 200ms, 400ms",
                "idempotency": "Ensure requests are idempotent (use request IDs)"
            },
            "timeout_strategy": {
                "connection_timeout": "3 seconds",
                "read_timeout": "5 seconds",
                "total_request_timeout": "10 seconds"
            },
            "graceful_degradation": {
                "approach": "Fail partially, not completely",
                "examples": [
                    "Recommendations fail → Show default content",
                    "Search slow → Show cached results",
                    "Payment fails → Queue for retry, notify user"
                ]
            },
            "bulkhead_pattern": {
                "isolation": "Isolate critical resources (thread pools, connections)",
                "benefit": "One slow service doesn't bring down entire system"
            }
        }

    def _design_disaster_recovery(self) -> Dict[str, Any]:
        """Design disaster recovery strategy."""
        return {
            "rpo": "Recovery Point Objective: < 1 hour (max data loss)",
            "rto": "Recovery Time Objective: < 4 hours (max downtime)",
            "backup_strategy": {
                "frequency": "Continuous backups with 5-minute snapshots",
                "storage": "Cross-region replication (S3)",
                "retention": "30 days incremental, 1 year annual",
                "encryption": "AES-256 at rest, TLS in transit"
            },
            "failover_strategy": {
                "active_active": "Multi-region active-active for critical services",
                "active_passive": "Standby region for non-critical services",
                "dns_failover": "Route53 health checks with automatic failover"
            },
            "runbooks": [
                "Database failure → Promote read replica",
                "Region outage → Failover to backup region",
                "Data corruption → Restore from point-in-time backup",
                "Security breach → Isolate affected services, rotate credentials"
            ],
            "testing": "Quarterly disaster recovery drills (GameDays)"
        }

    def _design_monitoring_strategy(self) -> Dict[str, Any]:
        """Design comprehensive monitoring."""
        return {
            "observability_pillars": {
                "metrics": {
                    "tool": "Prometheus + Grafana or Datadog",
                    "what": "CPU, memory, requests/sec, latency, error rate",
                    "alerts": "PagerDuty for critical, Slack for warnings"
                },
                "logs": {
                    "tool": "ELK Stack or Loki",
                    "structure": "Structured JSON logs with trace IDs",
                    "retention": "30 days hot, 90 days warm"
                },
                "traces": {
                    "tool": "Jaeger or Zipkin",
                    "sampling": "100% for errors, 1% for success",
                    "benefit": "End-to-end request visibility"
                }
            },
            "golden_signals": {
                "latency": "How long requests take",
                "traffic": "How many requests",
                "errors": "Rate of failed requests",
                "saturation": "How full the service is (CPU, memory)"
            },
            "slo_sli": {
                "sli": "Service Level Indicator - What you measure",
                "slo": "Service Level Objective - Target for SLI",
                "example": "SLI: API latency p99, SLO: < 500ms 99.9% of time"
            },
            "alerting_philosophy": {
                "actionable": "Only alert if action required",
                "grouped": "Group related alerts to reduce noise",
                "escalation": "Page if not acknowledged in 15 minutes"
            }
        }

    def _design_security_architecture(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design security-first architecture."""
        return {
            "defense_in_depth": "Multiple layers of security",
            "layers": {
                "network": {
                    "vpc": "Private subnets for services, public for load balancers",
                    "security_groups": "Least privilege - only required ports",
                    "ddos_protection": "CloudFlare or AWS Shield"
                },
                "application": {
                    "authentication": "JWT + Refresh tokens, OAuth 2.0/OIDC",
                    "authorization": "RBAC (Role-Based Access Control)",
                    "input_validation": "Validate all inputs, sanitize outputs",
                    "rate_limiting": "Per-user and per-IP limits"
                },
                "data": {
                    "encryption_at_rest": "AES-256 for databases and S3",
                    "encryption_in_transit": "TLS 1.3 for all connections",
                    "secret_management": "HashiCorp Vault or AWS Secrets Manager",
                    "pii_handling": "Tokenization or encryption for PII"
                },
                "api": {
                    "api_keys": "Per-client API keys with rotation",
                    "cors": "Restrictive CORS policy",
                    "csrf": "CSRF tokens for state-changing operations",
                    "input_validation": "JSON schema validation"
                }
            },
            "security_scanning": {
                "sast": "Static Analysis Security Testing in CI",
                "dast": "Dynamic Analysis in staging",
                "dependency_scanning": "Snyk or Dependabot for vulnerabilities",
                "container_scanning": "Trivy for Docker images"
            },
            "incident_response": {
                "plan": "Documented incident response plan",
                "team": "On-call rotation with escalation",
                "communication": "Status page for customer communication",
                "post_mortem": "Blameless post-mortems after incidents"
            }
        }

    def _identify_compliance_requirements(self, context: Dict[str, Any]) -> List[str]:
        """Identify compliance requirements."""
        domain = context.get("domain", "general")

        base_compliance = ["GDPR (EU users)", "CCPA (California users)"]

        domain_compliance = {
            "fintech": ["PCI DSS", "SOC 2", "ISO 27001", "AML/KYC"],
            "healthcare": ["HIPAA", "HITRUST"],
            "ecommerce": ["PCI DSS", "SOC 2"],
            "saas": ["SOC 2", "ISO 27001"]
        }

        return base_compliance + domain_compliance.get(domain, ["SOC 2"])

    def _design_cloud_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design cloud strategy."""
        return {
            "provider": "AWS (recommended) or GCP",
            "multi_cloud": "Single cloud initially, multi-cloud for disaster recovery",
            "compute": {
                "containers": "Docker + Kubernetes (EKS/GKE)",
                "serverless": "AWS Lambda for event-driven tasks",
                "vms": "EC2 for legacy/special requirements"
            },
            "managed_services": {
                "database": "RDS PostgreSQL with Multi-AZ",
                "cache": "ElastiCache Redis",
                "storage": "S3 for objects, EFS for shared files",
                "message_queue": "SQS/SNS or Kafka MSK"
            },
            "cost_optimization": {
                "reserved_instances": "For predictable workloads (30-40% savings)",
                "spot_instances": "For batch jobs (70-90% savings)",
                "auto_scaling": "Scale down during off-peak hours",
                "rightsizing": "Monthly review of instance utilization"
            }
        }

    def _recommend_iac_tools(self) -> Dict[str, str]:
        """Recommend Infrastructure as Code tools."""
        return {
            "terraform": "Multi-cloud infrastructure provisioning",
            "kubernetes_manifests": "Kubernetes resources (Helm charts)",
            "docker_compose": "Local development environment",
            "github_actions": "CI/CD pipelines",
            "git_repository": "Infrastructure code versioned with application code"
        }

    def _specify_diagrams(self) -> List[str]:
        """Specify required architecture diagrams."""
        return [
            "C4 Model - Context Diagram (system in environment)",
            "C4 Model - Container Diagram (services and databases)",
            "C4 Model - Component Diagram (internal structure)",
            "Deployment Diagram (infrastructure and regions)",
            "Data Flow Diagram (how data moves)",
            "Sequence Diagrams (key user journeys)",
            "Entity Relationship Diagram (data model)"
        ]

    def _document_design_decisions(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """Document key architectural decisions (ADRs)."""
        return [
            {
                "decision": "Use PostgreSQL as primary database",
                "rationale": "ACID compliance, mature ecosystem, excellent performance",
                "alternatives": "MySQL (less features), MongoDB (no transactions)"
            },
            {
                "decision": "Event-driven architecture with Kafka",
                "rationale": "Decoupling, replay capability, audit log",
                "alternatives": "Direct service calls (coupling), RabbitMQ (no replay)"
            },
            {
                "decision": "Kubernetes for container orchestration",
                "rationale": "Industry standard, cloud-agnostic, rich ecosystem",
                "alternatives": "ECS (AWS lock-in), Docker Swarm (less mature)"
            },
            {
                "decision": f"Target availability: {context.get('availability_requirement')}",
                "rationale": "Balance cost and reliability based on business needs",
                "alternatives": "99.999% (very expensive), 99% (too many outages)"
            }
        ]

    def _analyze_trade_offs(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze architecture trade-offs."""
        return {
            "consistency_vs_availability": {
                "choice": "Eventual consistency (AP in CAP theorem)",
                "benefit": "Better availability and partition tolerance",
                "cost": "Temporary inconsistency between services",
                "mitigation": "Saga pattern for critical workflows"
            },
            "complexity_vs_scalability": {
                "choice": "Microservices for large scale",
                "benefit": "Independent scaling and deployment",
                "cost": "Operational complexity, distributed transactions",
                "mitigation": "Start simple, extract services gradually"
            },
            "cost_vs_performance": {
                "choice": "Auto-scaling with spot instances",
                "benefit": "Cost savings during low traffic",
                "cost": "Slight latency during scale-up",
                "mitigation": "Keep min replicas for baseline performance"
            },
            "flexibility_vs_standardization": {
                "choice": "Polyglot persistence (multiple databases)",
                "benefit": "Right tool for each job (PostgreSQL + Redis + Elasticsearch)",
                "cost": "More operational overhead",
                "mitigation": "Limit to 3-4 data stores, use managed services"
            }
        }

    def _provide_industry_references(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """Provide world-class architecture references."""
        scale = context.get("scale", "medium")

        references = {
            "small": [
                {"company": "Linear", "learnings": "Start with modular monolith, excellent DX"},
                {"company": "Notion", "learnings": "Performance obsession, clever caching"},
                {"company": "Vercel", "learnings": "Edge computing, global distribution"}
            ],
            "medium": [
                {"company": "Stripe", "learnings": "API design excellence, reliability"},
                {"company": "Shopify", "learnings": "Multi-tenancy, resilience patterns"},
                {"company": "GitHub", "learnings": "Scaling PostgreSQL, performance"}
            ],
            "large": [
                {"company": "Netflix", "learnings": "Chaos engineering, microservices at scale"},
                {"company": "Uber", "learnings": "Real-time data, distributed systems"},
                {"company": "Amazon", "learnings": "Service-oriented architecture pioneering"},
                {"company": "Airbnb", "learnings": "Service mesh, observability"}
            ]
        }

        return references.get(scale, references["medium"])

    def _identify_anti_patterns(self) -> List[Dict[str, str]]:
        """Identify anti-patterns to avoid."""
        return [
            {
                "anti_pattern": "Distributed Monolith",
                "description": "Microservices that are tightly coupled",
                "avoid": "Ensure services can deploy independently"
            },
            {
                "anti_pattern": "Premature Microservices",
                "description": "Starting with microservices before understanding domain",
                "avoid": "Start with modular monolith, extract services later"
            },
            {
                "anti_pattern": "Single Database for Multiple Services",
                "description": "Services sharing database (violates microservice principles)",
                "avoid": "Database per service pattern"
            },
            {
                "anti_pattern": "Synchronous Cascade",
                "description": "Service A calls B calls C calls D (latency adds up)",
                "avoid": "Use async events, limit call depth to 2-3"
            },
            {
                "anti_pattern": "Mega Service",
                "description": "One service does too much",
                "avoid": "Keep services focused (single responsibility)"
            },
            {
                "anti_pattern": "No Monitoring",
                "description": "Flying blind without metrics and logs",
                "avoid": "Observability from day one"
            }
        ]


# Export
__all__ = ["EliteSystemDesignAgent"]
