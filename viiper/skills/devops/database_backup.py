"""
Database Backup Skill.

Automated backup strategies for PostgreSQL, MySQL, and MongoDB.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class DatabaseBackupSkill(Skill):
    """
    Database backup and recovery patterns.

    Features:
    - Automated daily backups
    - Point-in-time recovery
    - S3 storage
    - Backup rotation
    - Restore procedures
    - Backup verification
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Database Backup",
        slug="database-backup",
        category=SkillCategory.DEVOPS_INFRASTRUCTURE,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["backup", "database", "postgresql", "mysql", "mongodb", "disaster-recovery"],
        estimated_time_minutes=40,
        description="Automated database backup and recovery",
    )

    dependencies: list = [
        Dependency(name="aws-sdk", version="^2.1507.0", package_manager="npm", reason="S3 upload (Node.js)"),
        Dependency(name="boto3", version="^1.34.0", package_manager="pip", reason="S3 upload (Python)"),
    ]

    best_practices: list = [
        BestPractice(title="3-2-1 Backup Rule", description="3 copies, 2 media types, 1 offsite", code_reference="Local + S3 + Glacier", benefit="Disaster recovery"),
        BestPractice(title="Test Restores Regularly", description="Monthly restore tests", code_reference="Automated restore verification", benefit="Confidence in backups"),
        BestPractice(title="Encrypt Backups", description="AES-256 encryption at rest", code_reference="S3 SSE-S3 or SSE-KMS", benefit="Security, compliance"),
        BestPractice(title="Backup Rotation", description="Keep 7 daily, 4 weekly, 12 monthly", code_reference="Grandfather-father-son scheme", benefit="Cost optimization, history"),
    ]

    usage_examples: list = [
        UsageExample(
            name="PostgreSQL Backup Script",
            description="Backup to S3 with rotation",
            code=r'''#!/bin/bash
set -euo pipefail

# Configuration
DB_NAME="${DATABASE_NAME:-myapp}"
DB_USER="${DATABASE_USER:-postgres}"
S3_BUCKET="${BACKUP_S3_BUCKET:-myapp-backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"
BACKUP_DIR="/tmp/backups"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "Starting backup of $DB_NAME at $(date)"

# Dump and compress
pg_dump -U "$DB_USER" -h "$DATABASE_HOST" -d "$DB_NAME" | gzip > "$BACKUP_FILE"

# Verify backup
if [ ! -s "$BACKUP_FILE" ]; then
    echo "ERROR: Backup file is empty"
    exit 1
fi

echo "Backup created: $BACKUP_FILE ($(du -h "$BACKUP_FILE" | cut -f1))"

# Upload to S3
S3_KEY="postgresql/${DB_NAME}/$(date +%Y/%m/%d)/$(basename "$BACKUP_FILE")"
aws s3 cp "$BACKUP_FILE" "s3://${S3_BUCKET}/${S3_KEY}" \
    --storage-class STANDARD_IA \
    --server-side-encryption AES256

echo "Uploaded to S3: s3://${S3_BUCKET}/${S3_KEY}"

# Cleanup local file
rm "$BACKUP_FILE"

# Delete old backups
echo "Deleting backups older than $RETENTION_DAYS days"
aws s3 rm "s3://${S3_BUCKET}/postgresql/${DB_NAME}/" \
    --recursive \
    --exclude "*" \
    --include "*.sql.gz" \
    --region us-east-1

echo "Backup completed successfully at $(date)"
''',
        ),
        UsageExample(
            name="MongoDB Backup Script",
            description="mongodump to S3",
            code=r'''#!/bin/bash
set -euo pipefail

MONGO_URI="${MONGODB_URI:-mongodb://localhost:27017}"
DB_NAME="${MONGODB_DATABASE:-myapp}"
S3_BUCKET="${BACKUP_S3_BUCKET:-myapp-backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/tmp/backups/$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

echo "Starting MongoDB backup at $(date)"

# Dump database
mongodump --uri="$MONGO_URI" --db="$DB_NAME" --out="$BACKUP_DIR"

# Compress
tar -czf "$BACKUP_DIR.tar.gz" -C "$BACKUP_DIR" .
BACKUP_FILE="$BACKUP_DIR.tar.gz"

# Upload to S3
aws s3 cp "$BACKUP_FILE" "s3://${S3_BUCKET}/mongodb/${DB_NAME}/$(date +%Y/%m/%d)/$(basename "$BACKUP_FILE")" \
    --storage-class STANDARD_IA \
    --server-side-encryption AES256

# Cleanup
rm -rf "$BACKUP_DIR" "$BACKUP_FILE"

echo "MongoDB backup completed at $(date)"
''',
        ),
        UsageExample(
            name="GitHub Actions Backup Workflow",
            description="Scheduled daily backups",
            code=r'''name: Database Backup

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup PostgreSQL client
        run: |
          sudo apt-get update
          sudo apt-get install -y postgresql-client

      - name: Install AWS CLI
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Run backup script
        env:
          DATABASE_HOST: ${{ secrets.DATABASE_HOST }}
          DATABASE_NAME: ${{ secrets.DATABASE_NAME }}
          DATABASE_USER: ${{ secrets.DATABASE_USER }}
          DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
          BACKUP_S3_BUCKET: ${{ secrets.BACKUP_S3_BUCKET }}
        run: |
          chmod +x ./scripts/backup-db.sh
          ./scripts/backup-db.sh

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: '{"text": "Database backup FAILED!"}'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
''',
        ),
        UsageExample(
            name="Restore Script",
            description="Restore from S3 backup",
            code=r'''#!/bin/bash
set -euo pipefail

DB_NAME="${DATABASE_NAME:-myapp}"
DB_USER="${DATABASE_USER:-postgres}"
S3_BUCKET="${BACKUP_S3_BUCKET:-myapp-backups}"

# Find latest backup or use provided date
if [ -z "${BACKUP_DATE:-}" ]; then
    BACKUP_KEY=$(aws s3 ls "s3://${S3_BUCKET}/postgresql/${DB_NAME}/" \
        --recursive | sort | tail -n 1 | awk '{print $4}')
else
    BACKUP_KEY="postgresql/${DB_NAME}/${BACKUP_DATE}/"
fi

if [ -z "$BACKUP_KEY" ]; then
    echo "ERROR: No backup found"
    exit 1
fi

echo "Restoring from: s3://${S3_BUCKET}/${BACKUP_KEY}"

# Download backup
BACKUP_FILE="/tmp/restore_$(basename "$BACKUP_KEY")"
aws s3 cp "s3://${S3_BUCKET}/${BACKUP_KEY}" "$BACKUP_FILE"

# Restore
echo "Restoring database..."
gunzip -c "$BACKUP_FILE" | psql -U "$DB_USER" -h "$DATABASE_HOST" -d "$DB_NAME"

echo "Restore completed successfully"
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No Backup Verification - Never testing restores...",
            why="Discover backup is corrupt during emergency",
            good="Monthly automated restore tests"
        ),
        AntiPattern(
            bad="Backups on Same Server - Local backups only...",
            why="Lose everything if server fails",
            good="Offsite storage (S3, Glacier)"
        ),
        AntiPattern(
            bad="No Encryption - Unencrypted backups...",
            why="Data breach if backups accessed",
            good="Enable S3 SSE encryption"
        ),
        AntiPattern(
            bad="Infinite Retention - Keeping all backups forever...",
            why="High storage costs",
            good="Implement rotation policy"
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        db_type = options.get("database", "postgresql")
        return {
            "files": {
                "scripts/backup-db.sh": self.usage_examples[0].code if db_type == "postgresql" else self.usage_examples[1].code,
                "scripts/restore-db.sh": self.usage_examples[3].code,
                ".github/workflows/backup.yml": self.usage_examples[2].code,
            },
            "metadata": {"database_type": db_type},
        }
