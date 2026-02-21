"""Premium Database Migrations Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class MigrationsSkill(Skill):
    """Database migration patterns for persistent data management."""

    metadata: SkillMetadata = SkillMetadata(
        name="Database Migrations",
        slug="migrations",
        category=SkillCategory.BACKEND_DATABASE,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["migrations", "database", "alembic", "prisma", "evolution"],
        estimated_time_minutes=30,
        description="Robust patterns for database schema evolution, seeding, and migration safety.",
    )

    dependencies: list = [
        Dependency(name="alembic", version="^1.13.0", package_manager="pip", reason="Schema migrations for SQLAlchemy"),
        Dependency(name="prisma", version="^5.7.0", package_manager="npm", reason="Type-safe schema migrations"),
    ]

    best_practices: list = [
        BestPractice(
            title="Always Test Down Migrations",
            description="Ensure that your downgrade scripts work as expected to allow safe rollbacks.",
            code_reference="alembic downgrade -1",
            benefit="Prevents permanent data loss during failed deployments.",
        ),
        BestPractice(
            title="Separation of Seeding",
            description="Keep migrations for schema changes only; use separate seed scripts for initial data.",
            code_reference="npx prisma db seed",
            benefit="Cleaner migration history and easier environment resets.",
        ),
        BestPractice(
            title="Descriptive Migration Names",
            description="Use clear intent-based names for migration files.",
            code_reference="20240216_add_user_bio_table",
            benefit="Easier for teams to understand the evolution of the schema.",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Alembic Revision",
            description="Creating a new auto-generated revision in Python.",
            code='''alembic revision --autogenerate -m "add index to users email"''',
        ),
        UsageExample(
            name="Prisma Migration",
            description="Applying a schema change in Node.js.",
            code='''npx prisma migrate dev --name init_auth_tables''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Manually editing database schema",
            why="Leads to schema drift where code and DB are out of sync.",
            good="Always use migration scripts checked into version control.",
        ),
        AntiPattern(
            bad="Deletions without backups",
            why="Dropping columns in a migration can be irreversible if not careful.",
            good="Consider soft deletes or explicitly backup data before destructive migrations.",
        ),
    ]

    file_structure: dict = {
        "infra/migrations/env.py": "Alembic configuration (Python)",
        "prisma/schema.prisma": "Prisma schema example (Node.js)",
    }

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        # Implementation details for standard migration files
        return {
            "prisma/schema.prisma": "// Prisma schema definition...\n",
            "infra/migrations/readme.md": "# Migration Instructions\nUse `alembic upgrade head` to apply changes.\n",
        }
