"""Premium Email Service Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class EmailServiceSkill(Skill):
    """Email sending with templates and transactional patterns."""

    metadata: SkillMetadata = SkillMetadata(
        name="Email Service",
        slug="email-service",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["email", "nodemailer", "sendgrid", "smtp", "templates"],
        estimated_time_minutes=25,
        description="Transactional emails with templates, SMTP, and SendGrid support",
    )

    dependencies: list = [
        Dependency(name="nodemailer", version="^6.9.7", package_manager="npm", reason="Email sending (Node.js)"),
        Dependency(name="handlebars", version="^4.7.8", package_manager="npm", reason="Email templates"),
        Dependency(name="@sendgrid/mail", version="^8.1.0", package_manager="npm", reason="SendGrid integration"),
        Dependency(name="fastapi-mail", version="^1.4.1", package_manager="pip", reason="Email service (FastAPI)"),
        Dependency(name="jinja2", version="^3.1.2", package_manager="pip", reason="Email templates (Python)"),
    ]

    best_practices: list = [
        BestPractice(
            title="Use Email Templates",
            description="Separate design from code",
            code_reference="Handlebars/Jinja2 templates",
            benefit="Maintainable, reusable email designs",
        ),
        BestPractice(
            title="Queue Email Sending",
            description="Don't block API requests",
            code_reference="Use Bull/Celery for background jobs",
            benefit="Better performance, retry on failure",
        ),
        BestPractice(
            title="Handle Send Failures",
            description="Log errors, retry failed sends",
            code_reference="Try/catch with logging",
            benefit="Reliability, debugging",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Send Welcome Email",
            description="Transactional email on signup",
            code='''await emailService.sendWelcomeEmail({
  to: user.email,
  name: user.name,
  verificationUrl: `${baseUrl}/verify?token=${token}`
})''',
        ),
        UsageExample(
            name="Password Reset Email",
            description="Send reset link",
            code='''await send_password_reset_email(
    to=user.email,
    reset_url=f"{base_url}/reset?token={token}"
)''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Blocking requests while sending email",
            why="Slow API responses, poor UX",
            good="Queue emails in background",
        ),
        AntiPattern(
            bad="Hardcoded HTML in code",
            why="Hard to maintain, no designer input",
            good="Use template files",
        ),
    ]

    file_structure: dict = {
        "backend/lib/email.ts": "Email service (Node.js)",
        "backend/lib/email.py": "Email service (Python)",
        "backend/templates/welcome.html": "Welcome email template",
        "backend/templates/password-reset.html": "Password reset template",
    }

    email_service_ts: str = '''// backend/lib/email.ts
import nodemailer from 'nodemailer'
import handlebars from 'handlebars'
import fs from 'fs'
import path from 'path'

interface EmailOptions {
  to: string
  subject: string
  html: string
  text?: string
}

class EmailService {
  private transporter: nodemailer.Transporter

  constructor() {
    // SMTP configuration
    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASSWORD,
      },
    })
  }

  async sendEmail(options: EmailOptions): Promise<void> {
    try {
      await this.transporter.sendMail({
        from: process.env.EMAIL_FROM || 'noreply@example.com',
        to: options.to,
        subject: options.subject,
        html: options.html,
        text: options.text,
      })

      console.log(`Email sent to ${options.to}`)
    } catch (error) {
      console.error('Failed to send email:', error)
      throw new Error('Email sending failed')
    }
  }

  private loadTemplate(templateName: string): string {
    const templatePath = path.join(__dirname, '../templates', `${templateName}.html`)
    return fs.readFileSync(templatePath, 'utf-8')
  }

  private compileTemplate(templateName: string, data: any): string {
    const template = this.loadTemplate(templateName)
    const compiled = handlebars.compile(template)
    return compiled(data)
  }

  async sendWelcomeEmail(data: {
    to: string
    name: string
    verificationUrl: string
  }): Promise<void> {
    const html = this.compileTemplate('welcome', data)

    await this.sendEmail({
      to: data.to,
      subject: 'Welcome to Our Platform!',
      html,
      text: `Welcome ${data.name}! Please verify your email: ${data.verificationUrl}`,
    })
  }

  async sendPasswordResetEmail(data: {
    to: string
    name: string
    resetUrl: string
  }): Promise<void> {
    const html = this.compileTemplate('password-reset', data)

    await this.sendEmail({
      to: data.to,
      subject: 'Password Reset Request',
      html,
      text: `Hi ${data.name}, reset your password: ${data.resetUrl}`,
    })
  }

  async sendVerificationEmail(data: {
    to: string
    name: string
    code: string
  }): Promise<void> {
    const html = `
      <h1>Verify Your Email</h1>
      <p>Hi ${data.name},</p>
      <p>Your verification code is: <strong>${data.code}</strong></p>
      <p>This code expires in 15 minutes.</p>
    `

    await this.sendEmail({
      to: data.to,
      subject: 'Email Verification Code',
      html,
      text: `Your verification code: ${data.code}`,
    })
  }
}

export const emailService = new EmailService()
'''

    email_service_py: str = '''# backend/lib/email.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USER"),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_FROM", "noreply@example.com"),
    MAIL_PORT=int(os.getenv("SMTP_PORT", "587")),
    MAIL_SERVER=os.getenv("SMTP_HOST"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

# Template environment
template_dir = Path(__file__).parent.parent / "templates"
env = Environment(loader=FileSystemLoader(str(template_dir)))

class EmailService:
    """Email service for transactional emails."""

    def __init__(self):
        self.mail = FastMail(conf)

    async def send_email(
        self,
        to: str,
        subject: str,
        html: str,
        text: str = None
    ) -> None:
        """Send email."""
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[to],
                body=html,
                subtype="html",
            )

            await self.mail.send_message(message)
            logger.info(f"Email sent to {to}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise Exception("Email sending failed")

    def render_template(self, template_name: str, data: dict) -> str:
        """Render email template."""
        template = env.get_template(f"{template_name}.html")
        return template.render(**data)

    async def send_welcome_email(
        self,
        to: str,
        name: str,
        verification_url: str
    ) -> None:
        """Send welcome email."""
        html = self.render_template("welcome", {
            "name": name,
            "verification_url": verification_url,
        })

        await self.send_email(
            to=to,
            subject="Welcome to Our Platform!",
            html=html,
            text=f"Welcome {name}! Please verify your email: {verification_url}",
        )

    async def send_password_reset_email(
        self,
        to: str,
        name: str,
        reset_url: str
    ) -> None:
        """Send password reset email."""
        html = self.render_template("password-reset", {
            "name": name,
            "reset_url": reset_url,
        })

        await self.send_email(
            to=to,
            subject="Password Reset Request",
            html=html,
            text=f"Hi {name}, reset your password: {reset_url}",
        )

    async def send_verification_code(
        self,
        to: str,
        name: str,
        code: str
    ) -> None:
        """Send verification code email."""
        html = f"""
        <h1>Verify Your Email</h1>
        <p>Hi {name},</p>
        <p>Your verification code is: <strong>{code}</strong></p>
        <p>This code expires in 15 minutes.</p>
        """

        await self.send_email(
            to=to,
            subject="Email Verification Code",
            html=html,
            text=f"Your verification code: {code}",
        )

# Singleton instance
email_service = EmailService()
'''

    welcome_template: str = '''<!-- backend/templates/welcome.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #4f46e5; color: white; padding: 20px; text-align: center; }
        .content { padding: 30px; background: #f9fafb; }
        .button { display: inline-block; padding: 12px 24px; background: #4f46e5; color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Our Platform!</h1>
        </div>
        <div class="content">
            <p>Hi {{name}},</p>
            <p>Thank you for joining us! We're excited to have you on board.</p>
            <p>To get started, please verify your email address by clicking the button below:</p>
            <a href="{{verificationUrl}}" class="button">Verify Email</a>
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p><a href="{{verificationUrl}}">{{verificationUrl}}</a></p>
        </div>
        <div class="footer">
            <p>If you didn't create this account, please ignore this email.</p>
        </div>
    </div>
</body>
</html>
'''

    reset_template: str = '''<!-- backend/templates/password-reset.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #ef4444; color: white; padding: 20px; text-align: center; }
        .content { padding: 30px; background: #f9fafb; }
        .button { display: inline-block; padding: 12px 24px; background: #ef4444; color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Password Reset</h1>
        </div>
        <div class="content">
            <p>Hi {{name}},</p>
            <p>We received a request to reset your password. Click the button below to create a new password:</p>
            <a href="{{resetUrl}}" class="button">Reset Password</a>
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p><a href="{{resetUrl}}">{{resetUrl}}</a></p>
            <p><strong>This link expires in 1 hour.</strong></p>
        </div>
        <div class="footer">
            <p>If you didn't request a password reset, please ignore this email or contact support if you have concerns.</p>
        </div>
    </div>
</body>
</html>
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/email.ts": self.email_service_ts,
            "backend/lib/email.py": self.email_service_py,
            "backend/templates/welcome.html": self.welcome_template,
            "backend/templates/password-reset.html": self.reset_template,
        }
