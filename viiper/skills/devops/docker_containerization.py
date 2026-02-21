"""
Docker Containerization Skill.

Production-ready Docker patterns for Node.js and Python applications.
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


class DockerContainerizationSkill(Skill):
    """
    Docker containerization patterns.

    Features:
    - Multi-stage builds for optimization
    - Production-ready Dockerfiles
    - Docker Compose for local development
    - Health checks
    - Volume management
    - Network configuration
    - Environment variables
    - Security best practices
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Docker Containerization",
        slug="docker-containerization",
        category=SkillCategory.DEVOPS_DEPLOYMENT,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["docker", "containerization", "devops", "deployment", "compose"],
        estimated_time_minutes=45,
        description="Production-ready Docker setup with multi-stage builds",
    )

    dependencies: list = [
        Dependency(
            name="docker",
            version="latest",
            package_manager="system",
            reason="Container runtime",
        ),
        Dependency(
            name="docker-compose",
            version="latest",
            package_manager="system",
            reason="Multi-container orchestration",
        ),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Multi-Stage Builds",
            description="Separate build and runtime environments",
            code_reference="FROM node:20-alpine AS builder ... FROM node:20-alpine AS runtime",
            benefit="Smaller images, faster deployments, better security",
        ),
        BestPractice(
            title="Use .dockerignore",
            description="Exclude unnecessary files from build context",
            code_reference="node_modules, .git, .env, *.log",
            benefit="Faster builds, smaller images, security",
        ),
        BestPractice(
            title="Run as Non-Root User",
            description="Create dedicated user for running app",
            code_reference="USER node",
            benefit="Security isolation, privilege reduction",
        ),
        BestPractice(
            title="Use Health Checks",
            description="Define HEALTHCHECK in Dockerfile",
            code_reference="HEALTHCHECK --interval=30s CMD curl -f http://localhost:3000/health",
            benefit="Container orchestration, auto-recovery",
        ),
        BestPractice(
            title="Pin Base Image Versions",
            description="Use specific versions, not 'latest'",
            code_reference="FROM node:20.10-alpine3.18",
            benefit="Reproducible builds, predictable behavior",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Node.js Dockerfile (Express)",
            description="Production Dockerfile for Express.js app",
            code=r"""# syntax=docker/dockerfile:1

# Build stage
FROM node:20.10-alpine3.18 AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY pnpm-lock.yaml* ./

# Install dependencies
RUN npm ci --only=production

# Copy source and build
COPY . .

# Production stage
FROM node:20.10-alpine3.18 AS runtime

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy from builder
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app ./

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Use dumb-init as PID 1
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
""",
        ),
        UsageExample(
            name="Python Dockerfile (FastAPI)",
            description="Production Dockerfile for FastAPI app",
            code=r"""# syntax=docker/dockerfile:1

# Build stage
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
        ),
        UsageExample(
            name="Docker Compose for Development",
            description="Full development environment with services",
            code=r"""version: '3.9'

services:
  # API Service
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app_dev
      - REDIS_URL=redis://redis:6379
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network

  # Database
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app_dev
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Redis
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Worker (Background Jobs)
  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: ["node", "dist/worker.js"]
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
""",
        ),
        UsageExample(
            name=".dockerignore File",
            description="Exclude unnecessary files from Docker build",
            code=r"""# Dependencies
node_modules
npm-debug.log
yarn-error.log

# Build output
dist
build
.next

# Environment files
.env
.env.local
.env.*.local

# IDE
.idea
.vscode
*.swp
*.swo

# Git
.git
.gitignore

# Documentation
README.md
docs
*.md

# Tests
coverage
.nyc_output
*.test.ts
*.spec.ts
__tests__

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Misc
.DS_Store
Thumbs.db
*.log
logs
tmp
temp
""",
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Running as Root - Container runs as root user",
            why="Security vulnerability - container escape risk",
            good="Create and use non-root user (USER node)",
        ),
        AntiPattern(
            bad="Using Latest Tag - FROM node:latest or FROM python:latest",
            why="Unpredictable builds, breaking changes",
            good="Pin specific versions (FROM node:20.10-alpine3.18)",
        ),
        AntiPattern(
            bad="No .dockerignore - All files copied to build context",
            why="Slow builds, large images, secrets exposure",
            good="Create comprehensive .dockerignore file",
        ),
        AntiPattern(
            bad="Single Stage Build - Build and runtime in same image",
            why="Large images, slower deployments",
            good="Use multi-stage builds with separate builder and runtime stages",
        ),
        AntiPattern(
            bad="No Health Checks - Container status unknown",
            why="Orchestration issues, undetected failures",
            good="Add HEALTHCHECK instruction to Dockerfile",
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate Docker configuration files."""
        options = options or {}

        framework = options.get("framework", "express")
        include_compose = options.get("include_compose", True)
        include_worker = options.get("include_worker", True)

        result = {
            "files": {},
            "metadata": {
                "framework": framework,
                "includes_compose": include_compose,
                "includes_worker": include_worker,
            },
        }

        # Generate Dockerfile based on framework
        if framework in ["express", "node", "nestjs"]:
            result["files"]["Dockerfile"] = self.usage_examples[0].code
        elif framework in ["fastapi", "flask", "django", "python"]:
            result["files"]["Dockerfile"] = self.usage_examples[1].code

        # Generate docker-compose.yml
        if include_compose:
            result["files"]["docker-compose.yml"] = self.usage_examples[2].code

        # Generate .dockerignore
        result["files"][".dockerignore"] = self.usage_examples[3].code

        return result
