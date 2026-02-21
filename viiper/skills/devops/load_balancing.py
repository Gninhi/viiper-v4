"""
Load Balancing Skill.

High availability with load balancers, health checks, and auto-scaling.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class LoadBalancingSkill(Skill):
    """
    Load balancing patterns for high availability.

    Features:
    - Round-robin, least-connections algorithms
    - Health checks
    - Sticky sessions
    - Rate limiting
    - Auto-scaling triggers
    - Blue-green deployments
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Load Balancing",
        slug="load-balancing",
        category=SkillCategory.DEVOPS_INFRASTRUCTURE,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["load-balancing", "nginx", "haproxy", "high-availability", "scaling"],
        estimated_time_minutes=45,
        description="Load balancer configuration for high availability",
    )

    dependencies: list = [
        Dependency(name="nginx", version="latest", package_manager="system", reason="Load balancer"),
        Dependency(name="haproxy", version="latest", package_manager="system", reason="Alternative load balancer"),
    ]

    best_practices: list = [
        BestPractice(title="Health Checks", description="Active health monitoring", code_reference="health_check interval=5s;", benefit="Automatic failover, no traffic to unhealthy instances"),
        BestPractice(title="Connection Draining", description="Graceful shutdown", code_reference="shutdown_timeout 30s;", benefit="No dropped connections during deploys"),
        BestPractice(title="Sticky Sessions When Needed", description="Session affinity for stateful apps", code_reference="ip_hash;", benefit="User session persistence"),
        BestPractice(title="Rate Limiting", description="Protect against abuse", code_reference="limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;", benefit="DDoS protection, fair usage"),
    ]

    usage_examples: list = [
        UsageExample(
            name="Nginx Load Balancer",
            description="Round-robin with health checks",
            code=r'''upstream backend {
    least_conn;  # Least connections algorithm

    server app1:3000 weight=3 max_fails=3 fail_timeout=30s;
    server app2:3000 weight=3 max_fails=3 fail_timeout=30s;
    server app3:3000 weight=2 max_fails=3 fail_timeout=30s backup;

    keepalive 32;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\\n";
        add_header Content-Type text/plain;
    }
}
''',
        ),
        UsageExample(
            name="HAProxy Configuration",
            description="Advanced load balancing",
            code=r'''global
    log /dev/log local0
    maxconn 4096
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5s
    timeout client  30s
    timeout server  30s
    retries 3

frontend http_front
    bind *:80
    default_backend app_servers

    # Rate limiting
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny if { sc_http_req_rate(0) gt 100 }

backend app_servers
    balance leastconn
    option httpchk GET /health
    http-check expect status 200

    server app1 app1:3000 check inter 5s fall 3 rise 2
    server app2 app2:3000 check inter 5s fall 3 rise 2
    server app3 app3:3000 check inter 5s fall 3 rise 2

# Stats page
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats admin if LOCALHOST
''',
        ),
        UsageExample(
            name="Docker Swarm Load Balancing",
            description="Built-in service discovery",
            code=r'''# Initialize swarm
docker swarm init

# Deploy service with replicas
docker service create \
  --name api \
  --replicas 5 \
  --publish published=80,target=3000 \
  --update-parallelism 1 \
  --update-delay 10s \
  --health-cmd "curl -f http://localhost:3000/health || exit 1" \
  --health-interval 10s \
  --health-timeout 5s \
  --health-retries 3 \
  myapp:latest

# Scale service
docker service scale api=10

# Rolling update
docker service update --image myapp:latest api

# Rollback if needed
docker service rollback api
''',
        ),
        UsageExample(
            name="AWS ALB with Auto Scaling",
            description="Cloud load balancing",
            code=r'''# Terraform configuration

resource "aws_lb" "main" {
  name               = "main-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = true
}

resource "aws_lb_target_group" "app" {
  name     = "app-tg"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "app-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  target_group_arns   = [aws_lb_target_group.app.arn]
  min_size            = 2
  max_size            = 10
  desired_capacity    = 3

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  # Auto-scaling policies
  dynamic "tag" {
    for_each = {
      "Name" = "app-server"
      "Environment" = var.environment
    }
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.app.name
}
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No Health Checks - Traffic sent to dead instances...",
            why="Downtime, failed requests",
            good="Configure active health checks"
        ),
        AntiPattern(
            bad="Single Point of Failure - One load balancer instance...",
            why="Complete outage if LB fails",
            good="Multiple AZs, failover"
        ),
        AntiPattern(
            bad="Session Affinity Without Need - Sticky sessions by default...",
            why="Uneven load distribution",
            good="Use stateless apps when possible"
        ),
        AntiPattern(
            bad="No Rate Limiting - Unlimited requests per IP...",
            why="DDoS vulnerability, abuse",
            good="Configure rate limiting"
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        lb_type = options.get("load_balancer", "nginx")
        return {
            "files": {
                "nginx-lb.conf": lb_type == "nginx" and self.usage_examples[0].code or "",
                "haproxy.cfg": lb_type == "haproxy" and self.usage_examples[1].code or "",
                "docker-swarm.sh": self.usage_examples[2].code,
                "terraform/alb.tf": self.usage_examples[3].code,
            },
            "metadata": {"load_balancer_type": lb_type},
        }
