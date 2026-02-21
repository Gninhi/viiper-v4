"""
Environment Configuration Skill.

Environment variables, secrets management, and configuration patterns.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class EnvironmentConfigSkill(Skill):
    """
    Environment configuration patterns.

    Features:
    - Environment variables validation
    - Secrets management
    - Multi-environment setup
    - .env file patterns
    - Configuration hierarchy
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Environment Configuration",
        slug="environment-config",
        category=SkillCategory.DEVOPS_INFRASTRUCTURE,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["environment", "configuration", "secrets", "dotenv", "validation"],
        estimated_time_minutes=25,
        description="Environment variables and secrets management",
    )

    dependencies: list = [
        Dependency(name="dotenv", version="^16.3.1", package_manager="npm", reason="Environment variables (Node.js)"),
        Dependency(name="zod", version="^3.22.4", package_manager="npm", reason="Environment validation"),
        Dependency(name="pydantic", version="^2.5.0", package_manager="pip", reason="Settings management (Python)"),
        Dependency(name="python-dotenv", version="^1.0.0", package_manager="pip", reason="Environment variables (Python)"),
    ]

    best_practices: list = [
        BestPractice(title="Validate Environment Variables", description="Use schema validation at startup", code_reference="Zod schema for env vars", benefit="Fail fast, clear error messages"),
        BestPractice(title="Never Commit Secrets", description=".env files in .gitignore", code_reference=".env*.local in .gitignore", benefit="Security, prevent leaks"),
        BestPractice(title="Use Environment Prefixes", description="Group related variables", code_reference="DATABASE_URL, REDIS_URL, AWS_S3_BUCKET", benefit="Organization, clarity"),
        BestPractice(title="Provide Defaults", description="Default values for non-critical vars", code_reference="PORT: process.env.PORT || 3000", benefit="Local development ease"),
    ]

    usage_examples: list = [
        UsageExample(
            name="Environment Validation (Node.js)",
            description="Zod schema for env vars",
            code=r'''import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.string().transform(Number).default('3000'),

  // Database
  DATABASE_URL: z.string().url(),
  DATABASE_POOL_SIZE: z.string().transform(Number).default('10'),

  // Redis
  REDIS_URL: z.string().url(),

  // Auth
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default('15m'),
  REFRESH_TOKEN_EXPIRES_IN: z.string().default('7d'),

  // External Services
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  SENDGRID_API_KEY: z.string().startsWith('SG.'),

  // S3
  AWS_ACCESS_KEY_ID: z.string().min(1),
  AWS_SECRET_ACCESS_KEY: z.string().min(1),
  AWS_S3_BUCKET: z.string().min(1),
  AWS_REGION: z.string().default('us-east-1'),
});

export type Env = z.infer<typeof envSchema>;

function loadEnv(): Env {
  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    console.error('Invalid environment variables:');
    console.error(JSON.stringify(result.error.format(), null, 2));
    process.exit(1);
  }

  return result.data;
}

export const env = loadEnv();
''',
        ),
        UsageExample(
            name="Environment Validation (Python)",
            description="Pydantic Settings",
            code=r'''from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, HttpUrl, field_validator
from typing import Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )

    # App
    APP_NAME: str = "My App"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "production", "test"] = "development"
    PORT: int = 8000

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10

    # Redis
    REDIS_URL: str

    # Auth
    JWT_SECRET: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_IN: str = "15m"

    # External Services
    STRIPE_SECRET_KEY: str = Field(..., pattern=r"^sk_")
    SENDGRID_API_KEY: str = Field(..., pattern=r"^SG\.")

    # S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_REGION: str = "us-east-1"

    @field_validator('PORT', 'DATABASE_POOL_SIZE')
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('Must be positive')
        return v

# Load settings
settings = Settings()
''',
        ),
        UsageExample(
            name=".env.example Template",
            description="Template for developers",
            code=r'''# Application
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://localhost:5432/myapp_dev
DATABASE_POOL_SIZE=10

# Redis
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=your-super-secret-key-at-least-32-chars
JWT_EXPIRES_IN=15m
REFRESH_TOKEN_EXPIRES_IN=7d

# Stripe (Get keys from https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_ID=price_xxx

# SendGrid (Get API key from https://app.sendgrid.com/settings/api_keys)
SENDGRID_API_KEY=SG.xxx
SENDGRID_FROM_EMAIL=noreply@example.com

# AWS S3
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_BUCKET=my-bucket
AWS_REGION=us-east-1

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=xxx

# Feature Flags
FEATURE_NEW_DASHBOARD=true
FEATURE_BETA_API=false
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Committing .env Files - Secrets in git history...",
            why="Security breach",
            good="Add .env to .gitignore"
        ),
        AntiPattern(
            bad="No Validation - Undefined env vars cause runtime errors...",
            why="Hard to debug errors",
            good="Validate at startup with Zod/Pydantic"
        ),
        AntiPattern(
            bad="Hardcoded Values - Environment-specific values in code...",
            why="Deployment issues",
            good="Use environment variables"
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        lang = options.get("language", "node")
        return {
            "files": {
                ".env.example": self.usage_examples[2].code,
                "env.node.ts": self.usage_examples[0].code if lang == "node" else "",
                "env.python.py": self.usage_examples[1].code if lang != "node" else "",
            },
            "metadata": {"language": lang},
        }
