"""Premium Background Jobs Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class BackgroundJobsSkill(Skill):
    """Background job processing with Bull and task queues."""

    metadata: SkillMetadata = SkillMetadata(
        name="Background Jobs",
        slug="background-jobs",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["background-jobs", "bull", "queue", "async", "workers", "celery"],
        estimated_time_minutes=30,
        description="Async job processing with Bull (Node.js) and task queues (Python)",
    )

    dependencies: list = [
        Dependency(name="bull", version="^4.12.0", package_manager="npm", reason="Job queue (Node.js)"),
        Dependency(name="bullmq", version="^5.1.7", package_manager="npm", reason="Modern Bull (recommended)"),
        Dependency(name="ioredis", version="^5.3.2", package_manager="npm", reason="Redis client for Bull"),
        Dependency(name="arq", version="^0.25.0", package_manager="pip", reason="Async job queue (Python)"),
    ]

    best_practices: list = [
        BestPractice(
            title="Don't Block API Requests",
            description="Queue long-running tasks",
            code_reference="await queue.add('email', data)",
            benefit="Fast API responses, better UX",
        ),
        BestPractice(
            title="Implement Retry Logic",
            description="Retry failed jobs with backoff",
            code_reference="attempts: 3, backoff: exponential",
            benefit="Resilience to transient failures",
        ),
        BestPractice(
            title="Monitor Job Progress",
            description="Track job status, completion, failures",
            code_reference="job.progress(), job.getState()",
            benefit="Visibility, debugging, user feedback",
        ),
        BestPractice(
            title="Set Job Timeouts",
            description="Prevent jobs from hanging",
            code_reference="timeout: 60000 (60 seconds)",
            benefit="Resource management, prevent leaks",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Queue Email Job",
            description="Send email asynchronously",
            code='''await emailQueue.add('send-welcome', {
  to: user.email,
  name: user.name
})''',
        ),
        UsageExample(
            name="Process Job",
            description="Worker processes queued jobs",
            code='''emailQueue.process('send-welcome', async (job) => {
  await sendWelcomeEmail(job.data)
})''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Blocking requests while processing",
            why="Slow API, poor UX, timeout issues",
            good="Queue jobs, return immediately",
        ),
        AntiPattern(
            bad="No retry logic",
            why="Transient failures lose data",
            good="Retry with exponential backoff",
        ),
        AntiPattern(
            bad="No job timeout",
            why="Hanging jobs consume resources",
            good="Set reasonable timeouts",
        ),
    ]

    file_structure: dict = {
        "backend/queues/email.queue.ts": "Email job queue (Bull)",
        "backend/workers/email.worker.ts": "Email worker (Bull)",
        "backend/queues/tasks.py": "Task queue (Python ARQ)",
    }

    bull_queue_ts: str = r'''// backend/queues/email.queue.ts
import Bull, { Job, Queue } from 'bull'
import Redis from 'ioredis'

// Redis connection
const redisConnection = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
}

// Create email queue
export const emailQueue: Queue = new Bull('email', {
  redis: redisConnection,
  defaultJobOptions: {
    attempts: 3, // Retry failed jobs 3 times
    backoff: {
      type: 'exponential',
      delay: 2000, // Start with 2 seconds
    },
    removeOnComplete: true, // Clean up completed jobs
    removeOnFail: false, // Keep failed jobs for debugging
  },
})

// Job types
export interface WelcomeEmailJob {
  to: string
  name: string
  verificationUrl: string
}

export interface PasswordResetEmailJob {
  to: string
  name: string
  resetUrl: string
}

export interface NotificationEmailJob {
  to: string
  subject: string
  message: string
}

// Add jobs to queue
export async function queueWelcomeEmail(data: WelcomeEmailJob) {
  return emailQueue.add('welcome', data, {
    priority: 1, // High priority
  })
}

export async function queuePasswordResetEmail(data: PasswordResetEmailJob) {
  return emailQueue.add('password-reset', data, {
    priority: 1,
  })
}

export async function queueNotificationEmail(data: NotificationEmailJob) {
  return emailQueue.add('notification', data, {
    priority: 3, // Lower priority
    delay: 5000, // Wait 5 seconds before processing
  })
}

// Queue events
emailQueue.on('completed', (job: Job) => {
  console.log(`Job ${job.id} completed`)
})

emailQueue.on('failed', (job: Job, err: Error) => {
  console.error(`Job ${job.id} failed:`, err.message)
})

emailQueue.on('stalled', (job: Job) => {
  console.warn(`Job ${job.id} stalled`)
})

// Get queue stats
export async function getQueueStats() {
  const [waiting, active, completed, failed, delayed] = await Promise.all([
    emailQueue.getWaitingCount(),
    emailQueue.getActiveCount(),
    emailQueue.getCompletedCount(),
    emailQueue.getFailedCount(),
    emailQueue.getDelayedCount(),
  ])

  return { waiting, active, completed, failed, delayed }
}

// Clean up old jobs
export async function cleanOldJobs() {
  // Remove completed jobs older than 24 hours
  await emailQueue.clean(24 * 60 * 60 * 1000, 'completed')

  // Remove failed jobs older than 7 days
  await emailQueue.clean(7 * 24 * 60 * 60 * 1000, 'failed')
}
'''

    bull_worker_ts: str = r'''// backend/workers/email.worker.ts
import { emailQueue } from '../queues/email.queue'
import { Job } from 'bull'
import { emailService } from '../lib/email'

// Process welcome emails
emailQueue.process('welcome', async (job: Job) => {
  const { to, name, verificationUrl } = job.data

  console.log(`Processing welcome email for ${to}`)

  try {
    await emailService.sendWelcomeEmail({ to, name, verificationUrl })

    // Update job progress
    await job.progress(100)

    return { success: true, sentTo: to }
  } catch (error) {
    console.error('Failed to send welcome email:', error)
    throw error // Bull will retry
  }
})

// Process password reset emails
emailQueue.process('password-reset', async (job: Job) => {
  const { to, name, resetUrl } = job.data

  console.log(`Processing password reset email for ${to}`)

  try {
    await emailService.sendPasswordResetEmail({ to, name, resetUrl })
    await job.progress(100)
    return { success: true, sentTo: to }
  } catch (error) {
    console.error('Failed to send password reset email:', error)
    throw error
  }
})

// Process notification emails
emailQueue.process('notification', async (job: Job) => {
  const { to, subject, message } = job.data

  console.log(`Processing notification email for ${to}`)

  try {
    await emailService.sendEmail({
      to,
      subject,
      html: message,
    })

    await job.progress(100)
    return { success: true, sentTo: to }
  } catch (error) {
    console.error('Failed to send notification email:', error)
    throw error
  }
})

console.log('Email worker started')

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('Shutting down worker...')
  await emailQueue.close()
  process.exit(0)
})
'''

    arq_tasks_py: str = r'''# backend/queues/tasks.py
import asyncio
from arq import create_pool
from arq.connections import RedisSettings
from typing import Any
import os
import logging

logger = logging.getLogger(__name__)

# Redis settings
redis_settings = RedisSettings(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    password=os.getenv("REDIS_PASSWORD"),
)

# Task functions
async def send_welcome_email(ctx: dict, to: str, name: str, verification_url: str):
    """Send welcome email task."""
    from backend.lib.email import email_service

    logger.info(f"Sending welcome email to {to}")

    try:
        await email_service.send_welcome_email(
            to=to,
            name=name,
            verification_url=verification_url
        )
        return {"success": True, "sent_to": to}
    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")
        raise

async def send_password_reset_email(ctx: dict, to: str, name: str, reset_url: str):
    """Send password reset email task."""
    from backend.lib.email import email_service

    logger.info(f"Sending password reset email to {to}")

    try:
        await email_service.send_password_reset_email(
            to=to,
            name=name,
            reset_url=reset_url
        )
        return {"success": True, "sent_to": to}
    except Exception as e:
        logger.error(f"Failed to send password reset email: {e}")
        raise

async def process_uploaded_file(ctx: dict, file_id: str, file_path: str):
    """Process uploaded file (e.g., image resizing, virus scan)."""
    logger.info(f"Processing file {file_id}")

    # Simulate processing
    await asyncio.sleep(2)

    return {"success": True, "file_id": file_id}

async def generate_report(ctx: dict, user_id: str, report_type: str):
    """Generate report in background."""
    logger.info(f"Generating {report_type} report for user {user_id}")

    # Simulate report generation
    await asyncio.sleep(5)

    return {"success": True, "report_type": report_type}

# Worker class
class WorkerSettings:
    """ARQ worker settings."""

    functions = [
        send_welcome_email,
        send_password_reset_email,
        process_uploaded_file,
        generate_report,
    ]

    redis_settings = redis_settings

    # Job retry configuration
    max_tries = 3
    retry_jobs = True

    # Job timeout (seconds)
    job_timeout = 60

    # Worker configuration
    max_jobs = 10  # Max concurrent jobs
    poll_delay = 0.5  # Seconds to wait when queue is empty

    # On job start
    on_job_start = lambda ctx: logger.info(f"Job started: {ctx['job_id']}")

    # On job completion
    on_job_end = lambda ctx: logger.info(f"Job completed: {ctx['job_id']}")

# Queue client
class TaskQueue:
    """Task queue client."""

    def __init__(self):
        self.pool = None

    async def connect(self):
        """Connect to Redis."""
        self.pool = await create_pool(redis_settings)

    async def disconnect(self):
        """Disconnect from Redis."""
        if self.pool:
            await self.pool.close()

    async def enqueue(
        self,
        function: str,
        *args,
        _job_id: str = None,
        _queue_name: str = None,
        _defer_until: float = None,
        _defer_by: float = None,
        **kwargs
    ):
        """Enqueue a job."""
        job = await self.pool.enqueue_job(
            function,
            *args,
            _job_id=_job_id,
            _queue_name=_queue_name,
            _defer_until=_defer_until,
            _defer_by=_defer_by,
            **kwargs
        )
        return job

# Singleton instance
task_queue = TaskQueue()

# Example usage
"""
from backend.queues.tasks import task_queue

# In FastAPI startup
@app.on_event("startup")
async def startup():
    await task_queue.connect()

@app.on_event("shutdown")
async def shutdown():
    await task_queue.disconnect()

# Enqueue jobs
@app.post("/api/auth/register")
async def register(user: CreateUserRequest):
    # Create user...

    # Queue welcome email
    await task_queue.enqueue(
        "send_welcome_email",
        to=user.email,
        name=user.name,
        verification_url=f"https://example.com/verify?token={token}"
    )

    return {"message": "User created"}

# Run worker
# python -m arq backend.queues.tasks.WorkerSettings
"""
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/queues/email.queue.ts": self.bull_queue_ts,
            "backend/workers/email.worker.ts": self.bull_worker_ts,
            "backend/queues/tasks.py": self.arq_tasks_py,
        }
