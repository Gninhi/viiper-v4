"""
Base classes and enums for the Skills Library.

Defines the foundation for all skills in VIIPER.
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


class SkillCategory(str, Enum):
    """Categories for organizing skills."""

    # Frontend
    FRONTEND_COMPONENTS = "frontend_components"
    FRONTEND_FORMS = "frontend_forms"
    FRONTEND_ANIMATIONS = "frontend_animations"
    FRONTEND_LAYOUT = "frontend_layout"
    FRONTEND_STATE = "frontend_state"

    # Backend
    BACKEND_API = "backend_api"
    BACKEND_DATABASE = "backend_database"
    BACKEND_AUTH = "backend_auth"
    BACKEND_BUSINESS_LOGIC = "backend_business_logic"
    BACKEND_MIDDLEWARE = "backend_middleware"

    # DevOps
    DEVOPS_DEPLOYMENT = "devops_deployment"
    DEVOPS_MONITORING = "devops_monitoring"
    DEVOPS_INFRASTRUCTURE = "devops_infrastructure"
    DEVOPS_CI_CD = "devops_ci_cd"
    DEVOPS_SECURITY = "devops_security"

    # Testing
    TESTING_UNIT = "testing_unit"
    TESTING_INTEGRATION = "testing_integration"
    TESTING_E2E = "testing_e2e"
    TESTING_UTILITIES = "testing_utilities"

    # Data/ML
    DATA_PROCESSING = "data_processing"
    DATA_ANALYTICS = "data_analytics"
    DATA_ML_INTEGRATION = "data_ml_integration"


class SkillDifficulty(str, Enum):
    """Difficulty levels for skills."""

    BEGINNER = "beginner"  # Simple, straightforward implementations
    INTERMEDIATE = "intermediate"  # Requires some experience
    ADVANCED = "advanced"  # Complex patterns, security considerations
    EXPERT = "expert"  # Enterprise-grade, high-scale patterns


class SkillMetadata(BaseModel):
    """Metadata for a skill."""

    name: str = Field(..., description="Human-readable name")
    slug: str = Field(..., description="Unique identifier (kebab-case)")
    category: SkillCategory = Field(..., description="Skill category")
    version: str = Field(default="1.0.0", description="Semantic version")
    author: str = Field(default="VIIPER Agent", description="Author/agent name")
    tags: List[str] = Field(default_factory=list, description="Tags for search")
    difficulty: SkillDifficulty = Field(
        default=SkillDifficulty.INTERMEDIATE, description="Skill difficulty level"
    )
    estimated_time_minutes: int = Field(default=30, description="Estimated implementation time")
    description: str = Field(default="", description="Brief description of what this skill does")


class Dependency(BaseModel):
    """Dependency required by a skill."""

    name: str = Field(..., description="Package name")
    version: str = Field(..., description="Version requirement (e.g., ^1.0.0)")
    package_manager: str = Field(default="npm", description="Package manager (npm, pip, etc.)")
    reason: Optional[str] = Field(None, description="Why this dependency is needed")


class BestPractice(BaseModel):
    """Best practice embedded in skill."""

    title: str = Field(..., description="Practice title")
    description: str = Field(..., description="Practice description")
    code_reference: Optional[str] = Field(None, description="Code snippet showing the practice")
    benefit: Optional[str] = Field(None, description="Benefit of following this")


class UsageExample(BaseModel):
    """Usage example for a skill."""

    name: str = Field(..., description="Example name")
    description: str = Field(default="", description="What this example shows")
    code: str = Field(..., description="Example code")


class AntiPattern(BaseModel):
    """Anti-pattern to avoid."""

    bad: str = Field(..., description="What NOT to do")
    why: str = Field(..., description="Why it's bad")
    good: str = Field(..., description="What to do instead")


class Skill(ABC, BaseModel):
    """
    Base class for all skills.

    A skill is a reusable code template with best practices,
    dependencies, and usage examples.

    Subclasses must implement:
    - metadata: SkillMetadata
    - generate(context) -> Dict[str, str]: Generate code files
    """

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    # Metadata (must be overridden in subclass)
    metadata: SkillMetadata

    # Dependencies (optional, override in subclass)
    dependencies: List[Dependency] = Field(default_factory=list)

    # Best practices (optional, override in subclass)
    best_practices: List[BestPractice] = Field(default_factory=list)

    # Usage examples (optional, override in subclass)
    usage_examples: List[UsageExample] = Field(default_factory=list)

    # Anti-patterns (optional, override in subclass)
    anti_patterns: List[AntiPattern] = Field(default_factory=list)

    # File structure this skill generates
    file_structure: Dict[str, str] = Field(
        default_factory=dict, description="Map of file paths to descriptions"
    )

    @abstractmethod
    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Generate code files for this skill.

        Args:
            context: Optional context (e.g., variant names, configuration)

        Returns:
            Dictionary mapping file paths to file contents

        Example:
            {
                "components/ui/button.tsx": "...",
                "lib/utils.ts": "..."
            }
        """
        pass

    def get_installation_steps(self) -> List[str]:
        """
        Get step-by-step installation instructions.

        Returns:
            List of installation steps
        """
        steps = []

        # Add dependency installation
        if self.dependencies:
            # Group by package manager
            by_pm: Dict[str, List[str]] = {}
            for dep in self.dependencies:
                if dep.package_manager not in by_pm:
                    by_pm[dep.package_manager] = []
                by_pm[dep.package_manager].append(f"{dep.name}@{dep.version}")

            for pm, packages in by_pm.items():
                if pm == "npm":
                    steps.append(f"npm install {' '.join(packages)}")
                elif pm == "pip":
                    steps.append(f"pip install {' '.join(packages)}")
                elif pm == "yarn":
                    steps.append(f"yarn add {' '.join(packages)}")

        # Add file creation steps
        for file_path in self.file_structure.keys():
            steps.append(f"Create {file_path}")

        return steps

    def get_documentation(self) -> str:
        """
        Generate markdown documentation for this skill.

        Returns:
            Markdown documentation string
        """
        md = f"# {self.metadata.name}\n\n"
        md += f"{self.metadata.description}\n\n"

        # Metadata
        md += "## Metadata\n\n"
        md += f"- **Category**: {self.metadata.category.value}\n"
        md += f"- **Difficulty**: {self.metadata.difficulty.value}\n"
        md += f"- **Estimated Time**: {self.metadata.estimated_time_minutes} minutes\n"
        md += f"- **Version**: {self.metadata.version}\n"
        md += f"- **Tags**: {', '.join(self.metadata.tags)}\n\n"

        # Dependencies
        if self.dependencies:
            md += "## Dependencies\n\n"
            for dep in self.dependencies:
                md += f"- **{dep.name}** ({dep.version})"
                if dep.reason:
                    md += f" - {dep.reason}"
                md += "\n"
            md += "\n"

        # Installation
        steps = self.get_installation_steps()
        if steps:
            md += "## Installation\n\n"
            for i, step in enumerate(steps, 1):
                md += f"{i}. {step}\n"
            md += "\n"

        # Best Practices
        if self.best_practices:
            md += "## Best Practices\n\n"
            for bp in self.best_practices:
                md += f"### {bp.title}\n\n"
                md += f"{bp.description}\n\n"
                if bp.code_reference:
                    md += f"```\n{bp.code_reference}\n```\n\n"

        # Usage Examples
        if self.usage_examples:
            md += "## Usage Examples\n\n"
            for ex in self.usage_examples:
                md += f"### {ex.name}\n\n"
                if ex.description:
                    md += f"{ex.description}\n\n"
                md += f"```\n{ex.code}\n```\n\n"

        # Anti-Patterns
        if self.anti_patterns:
            md += "## Anti-Patterns to Avoid\n\n"
            for ap in self.anti_patterns:
                md += f"### ❌ Bad: {ap.bad}\n\n"
                md += f"**Why**: {ap.why}\n\n"
                md += f"**✅ Good**: {ap.good}\n\n"

        return md

    def __repr__(self) -> str:
        return f"<Skill: {self.metadata.name} ({self.metadata.slug})>"
