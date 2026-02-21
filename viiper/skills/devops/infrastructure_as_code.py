"""
Infrastructure as Code Skill.

Terraform patterns for cloud infrastructure provisioning.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class InfrastructureAsCodeSkill(Skill):
    """
    Infrastructure as Code with Terraform.

    Features:
    - Multi-environment setup
    - State management
    - Module patterns
    - CI/CD for infrastructure
    - Policy as code
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Infrastructure as Code",
        slug="infrastructure-as-code",
        category=SkillCategory.DEVOPS_INFRASTRUCTURE,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["terraform", "iac", "aws", "cloud", "provisioning"],
        estimated_time_minutes=60,
        description="Terraform infrastructure provisioning patterns",
    )

    dependencies: list = [
        Dependency(name="terraform", version="^1.6.0", package_manager="system", reason="Infrastructure as Code"),
        Dependency(name="aws", version="^5.0", package_manager="terraform", reason="AWS provider"),
    ]

    best_practices: list = [
        BestPractice(title="Remote State", description="Store state in S3 with DynamoDB locking", code_reference="backend \"s3\" {}", benefit="Team collaboration, state locking"),
        BestPractice(title="Module Structure", description="Reusable modules for resources", code_reference="modules/vpc, modules/eks", benefit="DRY, consistency across environments"),
        BestPractice(title="Environment Separation", description="Separate state per environment", code_reference="terraform/{dev,staging,prod}", benefit="Isolation, blast radius reduction"),
        BestPractice(title="Version Pinning", description="Pin provider and module versions", code_reference="version = \"~> 5.0\"", benefit="Reproducible deployments"),
    ]

    usage_examples: list = [
        UsageExample(
            name="Terraform Project Structure",
            description="Multi-environment layout",
            code=r'''infrastructure/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds/
│   ├── eks/
│   └── s3/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
└── scripts/
    └── terraform.sh
''',
        ),
        UsageExample(
            name="VPC Module",
            description="Reusable VPC configuration",
            code=r'''# modules/vpc/main.tf

resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = var.name
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.name}-private-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.name}-igw"
  }
}

resource "aws_nat_gateway" "main" {
  count         = length(var.public_subnet_cidrs)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
}

resource "aws_eip" "nat" {
  count = length(var.public_subnet_cidrs)
  domain = "vpc"
}
''',
        ),
        UsageExample(
            name="Main Configuration",
            description="Environment-specific setup",
            code=r'''# environments/production/main.tf

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "myapp-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "myapp"
      Environment = "production"
      ManagedBy   = "terraform"
    }
  }
}

module "vpc" {
  source = "../../modules/vpc"

  name                 = "myapp-prod"
  environment          = "production"
  cidr_block           = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.10.0/24", "10.0.20.0/24"]
  availability_zones   = ["us-east-1a", "us-east-1b"]
}

module "rds" {
  source = "../../modules/rds"

  name           = "myapp-prod-db"
  environment    = "production"
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
  instance_class = "db.r6g.large"
  multi_az       = true
}
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Local State - terraform.tfstate on local machine...",
            why="No team collaboration, state corruption risk",
            good="Remote state in S3 with locking"
        ),
        AntiPattern(
            bad="Hardcoded Values - Values in main.tf instead of variables...",
            why="No reusability, environment drift",
            good="Use variables and tfvars files"
        ),
        AntiPattern(
            bad="No State Locking - Concurrent modifications possible...",
            why="State corruption",
            good="DynamoDB state locking"
        ),
        AntiPattern(
            bad="Manual Changes - Console changes outside Terraform...",
            why="State drift, undocumented changes",
            good="Import resources, enforce IaC only"
        ),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "modules/vpc/main.tf": self.usage_examples[1].code,
                "environments/production/main.tf": self.usage_examples[2].code,
                "structure.txt": self.usage_examples[0].code,
            },
            "metadata": {"cloud": options.get("cloud", "aws")},
        }
