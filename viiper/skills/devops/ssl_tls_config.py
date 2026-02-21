"""
SSL/TLS Configuration Skill.

HTTPS setup, certificate management, and security headers.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class SSLTLSConfigSkill(Skill):
    """
    SSL/TLS configuration and certificate management.

    Features:
    - Let's Encrypt certificates
    - Auto-renewal
    - HTTPS redirection
    - Security headers
    - HSTS configuration
    - TLS best practices
    """

    metadata: SkillMetadata = SkillMetadata(
        name="SSL/TLS Configuration",
        slug="ssl-tls-config",
        category=SkillCategory.DEVOPS_SECURITY,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["ssl", "tls", "https", "letsencrypt", "certbot", "security"],
        estimated_time_minutes=35,
        description="SSL/TLS setup with automatic certificate renewal",
    )

    dependencies: list = [
        Dependency(name="certbot", version="latest", package_manager="system", reason="Let's Encrypt client"),
        Dependency(name="helmet", version="^7.1.0", package_manager="npm", reason="Security headers (Node.js)"),
        Dependency(name="fastapi-limiter", version="^0.1.6", package_manager="pip", reason="Security middleware (Python)"),
    ]

    best_practices: list = [
        BestPractice(title="Use HSTS", description="Strict-Transport-Security header", code_reference="max-age=31536000; includeSubDomains", benefit="Forces HTTPS, prevents downgrade attacks"),
        BestPractice(title="Auto-Renew Certificates", description="Certbot renewal cron job", code_reference="certbot renew --quiet", benefit="No downtime from expired certs"),
        BestPractice(title="HTTPS Everywhere", description="Redirect all HTTP to HTTPS", code_reference="app.use(httpsRedirect())", benefit="Encryption for all traffic"),
        BestPractice(title="Security Headers", description="CSP, X-Frame-Options, etc.", code_reference="helmet() middleware", benefit="XSS, clickjacking protection"),
    ]

    usage_examples: list = [
        UsageExample(
            name="Nginx SSL Configuration",
            description="Modern TLS config with Let's Encrypt",
            code=r'''server {
    listen 80;
    server_name example.com www.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Modern TLS configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.8 valid=300s;
    resolver_timeout 5s;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Other settings
    client_max_body_size 10M;
    keepalive_timeout 70;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
''',
        ),
        UsageExample(
            name="HTTPS Middleware (Express)",
            description="Force HTTPS in production",
            code=r'''import helmet from 'helmet';
import { Request, Response, NextFunction } from 'express';

// Security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.example.com"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://api.example.com"],
      frameAncestors: ["'self'"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}));

// HTTPS redirect
function httpsRedirect(req: Request, res: Response, next: NextFunction) {
  if (process.env.NODE_ENV === 'production' && !req.secure) {
    return res.redirect('https://' + req.headers.host + req.url);
  }
  next();
}

app.use(httpsRedirect);
''',
        ),
        UsageExample(
            name="Certbot Setup",
            description="Obtain and auto-renew certificates",
            code=r'''# Install certbot
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Test auto-renewal (dry run)
sudo certbot renew --dry-run

# Add to crontab (renew daily at 3 AM)
echo "0 3 * * * /usr/bin/certbot renew --quiet --deploy-hook \"systemctl reload nginx\"" | sudo tee -a /etc/crontab

# Verify renewal schedule
sudo certbot renew --cert-name example.com --dry-run
''',
        ),
        UsageExample(
            name="Docker Compose with Nginx Proxy",
            description="Reverse proxy with SSL",
            code=r'''version: '3.9'

services:
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/letsencrypt
      - ./html:/usr/share/nginx/html
    depends_on:
      - app
    networks:
      - web

  app:
    build: .
    expose:
      - "3000"
    environment:
      - NODE_ENV=production
    networks:
      - web

  certbot:
    image: certbot/certbot
    volumes:
      - ./certs:/etc/letsencrypt
      - ./html:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

networks:
  web:
    driver: bridge
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Expired Certificates - No auto-renewal configured...",
            why="Site downtime, browser warnings",
            good="Certbot cron job with --deploy-hook"
        ),
        AntiPattern(
            bad="HTTP Only - No HTTPS redirection...",
            why="Unencrypted traffic, MITM attacks",
            good="301 redirect to HTTPS"
        ),
        AntiPattern(
            bad="Weak TLS Ciphers - TLSv1.0, TLSv1.1 enabled...",
            why="Vulnerable to attacks",
            good="Only TLSv1.2 and TLSv1.3"
        ),
        AntiPattern(
            bad="No HSTS - Missing Strict-Transport-Security...",
            why="SSL stripping attacks possible",
            good="Add HSTS header with long max-age"
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "nginx.conf": self.usage_examples[0].code,
                "middleware/https.ts": self.usage_examples[1].code,
                "scripts/setup-ssl.sh": self.usage_examples[2].code,
                "docker-compose.ssl.yml": self.usage_examples[3].code,
            },
            "metadata": {"webserver": options.get("webserver", "nginx")},
        }
