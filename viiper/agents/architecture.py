"""
Architecture agents for VIIPER framework.

Specialized agents for Phase I (Ideation): System design, tech stack selection,
and security planning.
"""

from typing import Dict, Any, List
from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from viiper.core.variant import Variant


class SystemDesignAgent(Agent):
    """
    Agent specialized in system architecture design.

    Capabilities:
    - System architecture design and documentation
    - Component breakdown and responsibilities
    - Scalability planning and patterns
    - Design pattern recommendations
    - Data flow architecture
    """

    name: str = "System Design Agent"
    role: AgentRole = AgentRole.ARCHITECTURE
    capabilities: list = [
        AgentCapability.SYSTEM_DESIGN,
        AgentCapability.SCALABILITY_PLANNING,
    ]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute system design task.

        Generates:
        - System architecture overview
        - Component breakdown
        - Scalability recommendations
        - Design patterns to use
        """
        # Extract project context from task description
        context = self._parse_context(task.description)

        # Generate architecture based on variant
        architecture = self._design_architecture(context)

        result = {
            "task_id": task.id,
            "task_name": task.name,
            "architecture": architecture,
            "components": self._identify_components(context),
            "scalability": self._scalability_recommendations(context),
            "design_patterns": self._recommend_patterns(context),
            "data_flow": self._design_data_flow(context),
            "recommendations": self._generate_recommendations(architecture),
            "confidence": 0.85,
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse task description for context."""
        # Simplified - in production would use NLP or structured input
        return {
            "variant": "saas",  # Would be extracted
            "scale": "medium",
            "users_expected": 1000,
        }

    def _design_architecture(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design system architecture based on context."""
        variant = context.get("variant", "saas")

        # Architecture patterns by variant
        if variant == "saas":
            return {
                "pattern": "Three-tier architecture",
                "tiers": ["Presentation (Frontend)", "Application (Backend API)", "Data (Database)"],
                "style": "Microservices-ready monolith",
                "description": "Start with a well-structured monolith that can be split into microservices later",
            }
        elif variant == "mobile":
            return {
                "pattern": "Client-Server with BaaS",
                "tiers": ["Mobile App", "Backend-as-a-Service", "Database"],
                "style": "Serverless backend",
                "description": "Mobile client with serverless backend for rapid development",
            }
        else:
            return {
                "pattern": "JAMstack",
                "tiers": ["Static Frontend", "API Services", "CDN"],
                "style": "Static-first with dynamic APIs",
                "description": "Pre-rendered pages with API-driven dynamic content",
            }

    def _identify_components(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify main system components."""
        return [
            {
                "name": "Frontend Application",
                "responsibility": "User interface and client-side logic",
                "technology": "Next.js / React",
            },
            {
                "name": "API Gateway",
                "responsibility": "Request routing, authentication, rate limiting",
                "technology": "Next.js API routes or dedicated API server",
            },
            {
                "name": "Business Logic Layer",
                "responsibility": "Core application logic and workflows",
                "technology": "Node.js / TypeScript services",
            },
            {
                "name": "Database Layer",
                "responsibility": "Data persistence and retrieval",
                "technology": "PostgreSQL with Prisma ORM",
            },
            {
                "name": "Authentication Service",
                "responsibility": "User auth, sessions, permissions",
                "technology": "NextAuth.js or Supabase Auth",
            },
            {
                "name": "File Storage",
                "responsibility": "User uploads, media files",
                "technology": "S3-compatible storage (AWS S3 or Supabase Storage)",
            },
        ]

    def _scalability_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide scalability recommendations."""
        scale = context.get("scale", "medium")
        users = context.get("users_expected", 1000)

        if users < 1000:
            tier = "small"
            strategy = "vertical_scaling"
        elif users < 10000:
            tier = "medium"
            strategy = "horizontal_scaling_ready"
        else:
            tier = "large"
            strategy = "distributed_architecture"

        return {
            "tier": tier,
            "strategy": strategy,
            "recommendations": [
                "Use database connection pooling (max 10-20 connections)",
                "Implement caching layer (Redis) for frequent queries",
                "Use CDN for static assets (Vercel Edge, Cloudflare)",
                "Optimize images (WebP, lazy loading)",
                "Implement API rate limiting per user",
                "Use database indexes on frequently queried fields",
                "Consider read replicas if read-heavy (>70% reads)",
            ],
            "bottlenecks_to_watch": [
                "Database connections under high load",
                "API response times (target: <200ms p95)",
                "Frontend bundle size (target: <500KB gzipped)",
            ],
            "monitoring_needed": [
                "Request latency (p50, p95, p99)",
                "Database query performance",
                "Error rates by endpoint",
                "User session duration",
            ],
        }

    def _recommend_patterns(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommend design patterns to use."""
        return [
            {
                "pattern": "Repository Pattern",
                "use_case": "Data access layer",
                "benefit": "Abstracts database operations, easier testing and switching DBs",
            },
            {
                "pattern": "Service Layer",
                "use_case": "Business logic",
                "benefit": "Separates business logic from controllers, reusable across endpoints",
            },
            {
                "pattern": "Factory Pattern",
                "use_case": "Creating complex objects (emails, notifications)",
                "benefit": "Centralizes object creation logic",
            },
            {
                "pattern": "Observer Pattern",
                "use_case": "Event-driven workflows (user signup → send email)",
                "benefit": "Decouples event producers from consumers",
            },
            {
                "pattern": "Singleton",
                "use_case": "Database connection, configuration",
                "benefit": "Single shared instance across application",
            },
        ]

    def _design_data_flow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Design data flow through the system."""
        return {
            "user_request_flow": [
                "User → Frontend (React)",
                "Frontend → API Gateway",
                "API Gateway → Auth Middleware",
                "Auth Middleware → Business Logic Service",
                "Business Logic → Database (via Repository)",
                "Database → Response back through chain",
            ],
            "authentication_flow": [
                "User submits credentials",
                "Frontend → Auth API",
                "Validate credentials against DB",
                "Generate JWT token",
                "Store session (Redis or DB)",
                "Return token to client",
                "Client includes token in subsequent requests",
            ],
            "data_persistence_flow": [
                "User action → API request",
                "Validate input (Zod/Joi)",
                "Transform to domain model",
                "Business logic validation",
                "Repository.save() → Database",
                "Emit event (if needed)",
                "Return success response",
            ],
        }

    def _generate_recommendations(self, architecture: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations."""
        return [
            "Start with monolith, plan for microservices split later",
            "Use TypeScript for type safety across frontend and backend",
            "Implement API versioning from day 1 (/api/v1/...)",
            "Use environment variables for all configuration",
            "Implement proper error handling and logging from start",
            "Set up monitoring and alerting early (Sentry, DataDog)",
            "Use feature flags for gradual rollouts",
            "Document API with OpenAPI/Swagger",
        ]


class TechStackAgent(Agent):
    """
    Agent specialized in technology stack selection.

    Capabilities:
    - Technology recommendation based on requirements
    - Dependency analysis and compatibility
    - Trade-off analysis (cost, performance, team expertise)
    - Tech stack validation against project variant
    """

    name: str = "Tech Stack Agent"
    role: AgentRole = AgentRole.ARCHITECTURE
    capabilities: list = [AgentCapability.TECH_STACK_SELECTION]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute tech stack selection task.

        Generates:
        - Recommended technology stack
        - Alternatives with trade-offs
        - Justification for each choice
        - Dependencies and compatibility matrix
        """
        # Get project context
        context = self._parse_context(task.description)
        variant = context.get("variant", Variant.SAAS)

        # Get recommended stack
        stack = self._get_recommended_stack(variant)

        # Analyze alternatives
        alternatives = self._analyze_alternatives(variant, stack)

        result = {
            "task_id": task.id,
            "task_name": task.name,
            "recommended_stack": stack,
            "alternatives": alternatives,
            "dependencies": self._analyze_dependencies(stack),
            "total_cost_estimate": self._estimate_costs(stack),
            "learning_curve": self._assess_learning_curve(stack),
            "justification": self._justify_choices(variant, stack),
            "confidence": 0.90,
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse context from task description."""
        # Simplified - would extract from structured input
        return {"variant": Variant.SAAS, "budget": 10000, "timeline_weeks": 12}

    def _get_recommended_stack(self, variant: Variant) -> Dict[str, str]:
        """Get recommended tech stack for variant."""
        # Use variant's recommended_tech_stack property
        return variant.recommended_tech_stack

    def _analyze_alternatives(
        self, variant: Variant, current_stack: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Analyze alternative technology choices."""
        alternatives = []

        if variant == Variant.SAAS:
            # Frontend alternatives
            alternatives.append(
                {
                    "category": "frontend",
                    "current": "Next.js",
                    "alternatives": [
                        {
                            "name": "Remix",
                            "pros": ["Better data loading", "Simpler mental model"],
                            "cons": ["Smaller ecosystem", "Less mature"],
                            "when_to_choose": "If you prefer web standards and simpler routing",
                        },
                        {
                            "name": "SvelteKit",
                            "pros": ["Smaller bundle size", "Less boilerplate"],
                            "cons": ["Smaller community", "Fewer libraries"],
                            "when_to_choose": "If bundle size is critical constraint",
                        },
                    ],
                }
            )

            # Backend alternatives
            alternatives.append(
                {
                    "category": "backend",
                    "current": "Node.js",
                    "alternatives": [
                        {
                            "name": "Python (FastAPI)",
                            "pros": ["Better for data/ML", "Clean async syntax"],
                            "cons": ["Slower than Node", "Different ecosystem"],
                            "when_to_choose": "If heavy data processing or ML integration",
                        },
                        {
                            "name": "Go",
                            "pros": ["Very fast", "Great concurrency"],
                            "cons": ["Steeper learning curve", "More verbose"],
                            "when_to_choose": "If performance is top priority",
                        },
                    ],
                }
            )

            # Database alternatives
            alternatives.append(
                {
                    "category": "database",
                    "current": "PostgreSQL",
                    "alternatives": [
                        {
                            "name": "MongoDB",
                            "pros": ["Flexible schema", "Easy horizontal scaling"],
                            "cons": ["No ACID by default", "Query complexity"],
                            "when_to_choose": "If schema changes frequently",
                        },
                        {
                            "name": "MySQL",
                            "pros": ["Well-known", "Good performance"],
                            "cons": ["Less features than Postgres", "JSON support weaker"],
                            "when_to_choose": "If team very familiar with MySQL",
                        },
                    ],
                }
            )

        return alternatives

    def _analyze_dependencies(self, stack: Dict[str, str]) -> Dict[str, List[str]]:
        """Analyze dependencies and compatibility."""
        return {
            "core_dependencies": [
                "next@14.x",
                "react@18.x",
                "typescript@5.x",
                "prisma@5.x",
                "next-auth@4.x",
            ],
            "dev_dependencies": [
                "eslint@8.x",
                "prettier@3.x",
                "vitest@1.x",
                "playwright@1.x",
            ],
            "infrastructure": ["postgresql@15.x", "redis@7.x", "nginx@1.x"],
            "compatibility_notes": [
                "Next.js 14 requires Node.js 18.17+",
                "Prisma works with PostgreSQL 12+",
                "NextAuth v4 compatible with Next.js 13+",
            ],
        }

    def _estimate_costs(self, stack: Dict[str, str]) -> Dict[str, Any]:
        """Estimate costs for the tech stack."""
        return {
            "development": {
                "monthly": 0,  # Open source
                "notes": "All development tools are free/open source",
            },
            "hosting": {
                "monthly_estimate": 50,
                "breakdown": {
                    "Vercel (frontend)": 0,  # Free tier
                    "Database (Supabase/Neon)": 0,  # Free tier initially
                    "File storage": 0,  # Free tier initially
                },
                "at_scale": {
                    "Vercel Pro": 20,
                    "Database": 25,
                    "Storage": 5,
                },
            },
            "third_party_services": {
                "monthly_estimate": 30,
                "breakdown": {
                    "Email (Resend)": 0,  # Free tier
                    "Monitoring (Sentry)": 0,  # Free tier
                    "Analytics": 0,  # Free tier
                    "Stripe (payments)": "2.9% + 30¢ per transaction",
                },
            },
            "total_monthly_mvp": 0,
            "total_monthly_at_scale": 80,
        }

    def _assess_learning_curve(self, stack: Dict[str, str]) -> Dict[str, str]:
        """Assess learning curve for the stack."""
        return {
            "overall": "Medium",
            "frontend": "Medium (React/Next.js well documented)",
            "backend": "Easy (Node.js familiar to most developers)",
            "database": "Easy (SQL is widely known)",
            "estimated_ramp_up": "1-2 weeks for experienced developer",
            "resources": [
                "Next.js documentation (excellent)",
                "React documentation",
                "Prisma documentation (great)",
                "Numerous YouTube tutorials and courses",
            ],
        }

    def _justify_choices(self, variant: Variant, stack: Dict[str, str]) -> List[str]:
        """Justify technology choices."""
        return [
            "Next.js: Industry standard for React apps, excellent DX, great performance",
            "TypeScript: Type safety prevents bugs, better IDE support, scales well",
            "PostgreSQL: Reliable, feature-rich, great for structured data",
            "Prisma: Modern ORM, type-safe, great migrations",
            "Supabase/NextAuth: Reduces auth complexity, focus on business logic",
            "Tailwind CSS: Rapid UI development, consistent design system",
            "Vercel: Zero-config deployment, great Next.js integration",
        ]


class SecurityPlanningAgent(Agent):
    """
    Agent specialized in security planning and compliance.

    Capabilities:
    - Security requirements analysis
    - Threat modeling
    - Compliance recommendations (GDPR, SOC2, etc.)
    - Security checklist generation
    - Vulnerability assessment planning
    """

    name: str = "Security Planning Agent"
    role: AgentRole = AgentRole.ARCHITECTURE
    capabilities: list = [AgentCapability.SECURITY_PLANNING]

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute security planning task.

        Generates:
        - Security checklist
        - Threat model
        - Compliance requirements
        - Implementation recommendations
        """
        context = self._parse_context(task.description)

        result = {
            "task_id": task.id,
            "task_name": task.name,
            "security_checklist": self._generate_security_checklist(),
            "threat_model": self._create_threat_model(context),
            "compliance": self._assess_compliance_needs(context),
            "authentication_plan": self._plan_authentication(),
            "data_protection": self._plan_data_protection(),
            "api_security": self._plan_api_security(),
            "infrastructure_security": self._plan_infrastructure_security(),
            "recommendations": self._generate_security_recommendations(),
            "priority_actions": self._identify_priority_actions(),
            "confidence": 0.88,
        }

        return result

    def _parse_context(self, description: str) -> Dict[str, Any]:
        """Parse context from task description."""
        return {"variant": "saas", "handles_pii": True, "target_market": "EU"}

    def _generate_security_checklist(self) -> Dict[str, List[Dict[str, str]]]:
        """Generate comprehensive security checklist."""
        return {
            "authentication": [
                {"item": "Implement secure password hashing (bcrypt/Argon2)", "priority": "CRITICAL"},
                {"item": "Add multi-factor authentication (MFA)", "priority": "HIGH"},
                {"item": "Implement session management with secure tokens", "priority": "CRITICAL"},
                {"item": "Add rate limiting on auth endpoints", "priority": "HIGH"},
                {"item": "Implement account lockout after failed attempts", "priority": "MEDIUM"},
            ],
            "authorization": [
                {"item": "Implement role-based access control (RBAC)", "priority": "CRITICAL"},
                {"item": "Add permission checks on all sensitive operations", "priority": "CRITICAL"},
                {"item": "Implement API key rotation", "priority": "MEDIUM"},
                {"item": "Use principle of least privilege", "priority": "HIGH"},
            ],
            "data_protection": [
                {"item": "Encrypt data at rest (database encryption)", "priority": "CRITICAL"},
                {"item": "Encrypt data in transit (HTTPS/TLS 1.3)", "priority": "CRITICAL"},
                {"item": "Implement field-level encryption for sensitive data", "priority": "HIGH"},
                {"item": "Secure backup strategy with encryption", "priority": "HIGH"},
                {"item": "Implement data retention policies", "priority": "MEDIUM"},
            ],
            "input_validation": [
                {"item": "Validate all user inputs", "priority": "CRITICAL"},
                {"item": "Sanitize inputs to prevent XSS", "priority": "CRITICAL"},
                {"item": "Use parameterized queries (prevent SQL injection)", "priority": "CRITICAL"},
                {"item": "Implement CSRF protection", "priority": "HIGH"},
                {"item": "Validate file uploads (type, size, content)", "priority": "HIGH"},
            ],
            "api_security": [
                {"item": "Implement rate limiting per user/IP", "priority": "HIGH"},
                {"item": "Use API versioning", "priority": "MEDIUM"},
                {"item": "Implement request signing for critical APIs", "priority": "MEDIUM"},
                {"item": "Add CORS configuration", "priority": "HIGH"},
                {"item": "Implement API authentication (OAuth 2.0/JWT)", "priority": "CRITICAL"},
            ],
            "monitoring": [
                {"item": "Set up security event logging", "priority": "HIGH"},
                {"item": "Implement intrusion detection", "priority": "MEDIUM"},
                {"item": "Monitor for suspicious activities", "priority": "HIGH"},
                {"item": "Set up alerting for security events", "priority": "HIGH"},
                {"item": "Regular security audits", "priority": "MEDIUM"},
            ],
        }

    def _create_threat_model(self, context: Dict[str, Any]) -> Dict[str, List[str]]:
        """Create threat model (STRIDE)."""
        return {
            "spoofing": [
                "Attacker impersonates legitimate user",
                "Mitigation: Strong authentication, MFA, session management",
            ],
            "tampering": [
                "Attacker modifies data in transit or at rest",
                "Mitigation: HTTPS, data integrity checks, audit logs",
            ],
            "repudiation": [
                "User denies performing an action",
                "Mitigation: Comprehensive audit logging, digital signatures",
            ],
            "information_disclosure": [
                "Sensitive data exposed to unauthorized parties",
                "Mitigation: Encryption, access controls, data classification",
            ],
            "denial_of_service": [
                "Attacker makes system unavailable",
                "Mitigation: Rate limiting, DDoS protection, auto-scaling",
            ],
            "elevation_of_privilege": [
                "Attacker gains unauthorized permissions",
                "Mitigation: RBAC, least privilege, input validation",
            ],
        }

    def _assess_compliance_needs(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance requirements."""
        target_market = context.get("target_market", "US")
        handles_pii = context.get("handles_pii", True)

        requirements = []

        if target_market in ["EU", "Global"] or handles_pii:
            requirements.append(
                {
                    "regulation": "GDPR",
                    "applies": True,
                    "key_requirements": [
                        "Data minimization",
                        "Right to be forgotten",
                        "Data portability",
                        "Consent management",
                        "Privacy by design",
                        "Data breach notification (72h)",
                    ],
                    "implementation": [
                        "Add privacy policy",
                        "Implement consent banners",
                        "Add data export functionality",
                        "Add account deletion",
                        "Implement data retention policies",
                    ],
                }
            )

        requirements.append(
            {
                "regulation": "SOC 2",
                "applies": target_market == "Enterprise",
                "key_requirements": [
                    "Access controls",
                    "Encryption",
                    "Monitoring and logging",
                    "Incident response",
                    "Change management",
                ],
                "implementation": [
                    "Document security policies",
                    "Implement access reviews",
                    "Set up monitoring",
                    "Create incident response plan",
                ],
            }
        )

        return {"requirements": requirements, "estimated_effort_weeks": 2}

    def _plan_authentication(self) -> Dict[str, Any]:
        """Plan authentication implementation."""
        return {
            "strategy": "OAuth 2.0 + JWT",
            "providers": ["Email/Password", "Google OAuth", "GitHub OAuth"],
            "session_management": {
                "type": "JWT with refresh tokens",
                "token_expiry": "15 minutes (access), 7 days (refresh)",
                "storage": "httpOnly cookies",
            },
            "password_requirements": {
                "min_length": 12,
                "complexity": "At least 1 uppercase, lowercase, number, special char",
                "hashing": "bcrypt with salt (cost factor 12)",
            },
            "mfa": {"required_for": "Admin users", "optional_for": "Regular users", "method": "TOTP (Google Authenticator)"},
            "implementation_libraries": ["NextAuth.js", "Passport.js", "Supabase Auth"],
        }

    def _plan_data_protection(self) -> Dict[str, Any]:
        """Plan data protection measures."""
        return {
            "encryption_at_rest": {
                "method": "AES-256",
                "scope": "Database, file storage, backups",
                "key_management": "AWS KMS or similar",
            },
            "encryption_in_transit": {"method": "TLS 1.3", "scope": "All communications", "cert_provider": "Let's Encrypt"},
            "sensitive_data_handling": {
                "pii_fields": ["email", "name", "phone", "address"],
                "encryption": "Field-level encryption for highly sensitive data",
                "access_logging": "Log all access to PII",
            },
            "data_retention": {
                "user_data": "Retain until account deletion + 30 days",
                "logs": "90 days",
                "backups": "30 days",
            },
        }

    def _plan_api_security(self) -> Dict[str, Any]:
        """Plan API security measures."""
        return {
            "authentication": "JWT Bearer tokens",
            "rate_limiting": {"authenticated": "100 req/min", "unauthenticated": "10 req/min", "ip_based": "1000 req/hour"},
            "cors": {"allowed_origins": ["https://app.example.com"], "allowed_methods": ["GET", "POST", "PUT", "DELETE"], "credentials": True},
            "input_validation": {
                "library": "Zod or Joi",
                "validate": "All request bodies, query params, path params",
            },
            "api_versioning": {"strategy": "URL-based (/api/v1/, /api/v2/)", "deprecation_policy": "6 months notice"},
        }

    def _plan_infrastructure_security(self) -> Dict[str, Any]:
        """Plan infrastructure security."""
        return {
            "network": {
                "firewall": "Cloud provider firewall + WAF",
                "ddos_protection": "Cloudflare or AWS Shield",
                "private_subnets": "Database in private subnet",
            },
            "secrets_management": {
                "tool": "Environment variables + secrets manager",
                "never_commit": "API keys, passwords, private keys",
                "rotation": "90 days for critical secrets",
            },
            "monitoring": {
                "security_events": "Failed logins, permission changes, data access",
                "alerting": "Slack/email for critical events",
                "siem": "Consider DataDog or Sentry for scale",
            },
        }

    def _generate_security_recommendations(self) -> List[str]:
        """Generate security recommendations."""
        return [
            "Implement security headers (HSTS, CSP, X-Frame-Options)",
            "Regular dependency updates (Dependabot)",
            "Security scanning in CI/CD (Snyk, npm audit)",
            "Penetration testing before launch",
            "Security training for team",
            "Incident response plan documented",
            "Regular security audits (quarterly)",
            "Bug bounty program (when scaled)",
        ]

    def _identify_priority_actions(self) -> List[Dict[str, str]]:
        """Identify priority security actions for MVP."""
        return [
            {
                "action": "Implement HTTPS everywhere",
                "timeline": "Week 1",
                "effort": "Low",
                "impact": "CRITICAL",
            },
            {
                "action": "Set up authentication with secure password hashing",
                "timeline": "Week 1-2",
                "effort": "Medium",
                "impact": "CRITICAL",
            },
            {
                "action": "Add input validation on all endpoints",
                "timeline": "Week 2-3",
                "effort": "Medium",
                "impact": "CRITICAL",
            },
            {
                "action": "Implement rate limiting",
                "timeline": "Week 3",
                "effort": "Low",
                "impact": "HIGH",
            },
            {
                "action": "Set up security monitoring and logging",
                "timeline": "Week 4",
                "effort": "Medium",
                "impact": "HIGH",
            },
            {
                "action": "Add GDPR compliance features (if applicable)",
                "timeline": "Week 5-6",
                "effort": "High",
                "impact": "HIGH",
            },
        ]
