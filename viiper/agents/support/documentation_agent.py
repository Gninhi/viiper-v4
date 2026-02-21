"""
Documentation Agent for VIIPER.

Generates comprehensive technical documentation, user guides, and API docs.
Ensures all projects have world-class documentation.
"""

from typing import ClassVar, Dict, Any, List, Optional
from datetime import datetime

from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask
from viiper.core.phase import Phase


class DocumentationAgent(Agent):
    """
    Agent specialized in creating technical documentation.

    Capabilities:
    - Technical documentation (README, API docs, Architecture)
    - User guides and tutorials
    - Code documentation and inline comments
    - Documentation quality checks
    - Multi-format output (Markdown, HTML, PDF)
    """

    name: str = "Documentation Agent"
    role: AgentRole = AgentRole.SUPPORT
    capabilities: list = [AgentCapability.DOCUMENTATION]

    # --- Class-level templates (ClassVar to avoid Pydantic field detection) ---

    README_TEMPLATE: ClassVar[str] = """# {project_name}

{description}

## 🚀 Quick Start

{quick_start}

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

{features}

## 📦 Installation

```bash
{installation}
```

## 🎯 Usage

{usage_examples}

## 📚 API Reference

{api_docs}

## 🤝 Contributing

{contributing}

## 📄 License

{license}

---

Generated with ❤️ by VIIPER Documentation Agent
"""

    USER_GUIDE_TEMPLATE: ClassVar[str] = """# {title} - User Guide

## Overview

{overview}

## Prerequisites

{prerequisites}

## Step-by-Step Instructions

{steps}

## Tips & Best Practices

{tips}

## Troubleshooting

{troubleshooting}

## Next Steps

{next_steps}
"""

    # -------------------------------------------------------------------------

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute documentation task.

        Task metadata keys:
            doc_type: str  - "readme" | "api" | "user_guide" | "architecture" | "inline_comments"
            project_name: str - Name of the project
            variant: str     - Project variant
            phase: str       - Current phase
            tech_stack: dict - Technology stack (for api / architecture docs)
            guide_title: str - Title for user guide
        """
        doc_type = task.metadata.get("doc_type", "readme")

        # Build a minimal context dict from task metadata
        ctx = {
            "project_name": task.metadata.get("project_name", "Unnamed Project"),
            "variant": task.metadata.get("variant", "saas"),
            "phase": task.metadata.get("phase", "production"),
            "tech_stack": task.metadata.get("tech_stack", {}),
        }

        dispatch = {
            "readme": self._generate_readme,
            "api": self._generate_api_docs,
            "user_guide": self._generate_user_guide,
            "architecture": self._generate_architecture_doc,
            "inline_comments": self._generate_code_comments,
        }

        handler = dispatch.get(doc_type)
        if handler is None:
            return {"success": False, "error": f"Unknown documentation type: {doc_type}"}

        return handler(ctx, task)

    # -------------------------------------------------------------------------
    # Handlers
    # -------------------------------------------------------------------------

    def _generate_readme(self, ctx: Dict[str, Any], task: AgentTask) -> Dict[str, Any]:
        """Generate project README."""
        project_name = ctx["project_name"]
        variant = ctx["variant"]
        phase = ctx["phase"]

        features = self._variant_features(variant)
        api_note = (
            "See API documentation below"
            if phase in {"production", "execution", "rentabilisation", "iteration"}
            else "API documentation coming soon"
        )

        readme = self.README_TEMPLATE.format(
            project_name=project_name,
            description=f"{variant.capitalize()} project built with VIIPER",
            quick_start=self._generate_quick_start(project_name),
            features=self._format_features(features),
            installation=f"npm install {project_name.lower().replace(' ', '-')}",
            usage_examples=self._generate_usage_examples(project_name),
            api_docs=api_note,
            contributing=self._generate_contributing_guide(),
            license="MIT License - see [LICENSE](LICENSE) file for details.",
        )

        return {
            "success": True,
            "output": {"file": "README.md", "content": readme, "type": "markdown"},
            "artifacts": {
                "readme_generated": True,
                "sections": ["quick_start", "features", "installation", "usage"],
            },
        }

    def _generate_api_docs(self, ctx: Dict[str, Any], task: AgentTask) -> Dict[str, Any]:
        """Generate API documentation."""
        tech_stack = ctx.get("tech_stack", {})
        backend = tech_stack.get("backend", "express").lower()
        project_name = ctx["project_name"]

        if "fastapi" in backend or "python" in backend:
            content = self._fastapi_docs()
        else:
            content = self._generic_api_docs(project_name)

        return {
            "success": True,
            "output": {"file": "docs/API.md", "content": content, "type": "markdown"},
            "artifacts": {"backend_framework": backend},
        }

    def _generate_user_guide(self, ctx: Dict[str, Any], task: AgentTask) -> Dict[str, Any]:
        """Generate user guide."""
        project_name = ctx["project_name"]
        guide_title = task.metadata.get("guide_title", f"{project_name} Guide")

        guide = self.USER_GUIDE_TEMPLATE.format(
            title=guide_title,
            overview=f"This guide helps you get started with {project_name} and make the most of its features.",
            prerequisites=self._prerequisites(),
            steps=self._guide_steps(),
            tips=self._best_practices(),
            troubleshooting=self._troubleshooting(),
            next_steps=self._next_steps(),
        )

        return {
            "success": True,
            "output": {
                "file": f"docs/guides/{guide_title.lower().replace(' ', '_')}.md",
                "content": guide,
                "type": "markdown",
            },
            "artifacts": {"sections": 6, "estimated_read_time": "10 min"},
        }

    def _generate_architecture_doc(self, ctx: Dict[str, Any], task: AgentTask) -> Dict[str, Any]:
        """Generate architecture documentation."""
        tech_stack = ctx.get("tech_stack", {})
        project_name = ctx["project_name"]
        variant = ctx["variant"]

        content = f"""# Architecture Documentation

## System Overview

{project_name} is built using a **{variant}** architecture.

## Technology Stack

{self._format_tech_stack(tech_stack)}

## Architecture Diagram

```
{self._architecture_diagram()}
```

## Component Breakdown

{self._component_breakdown()}

## Data Flow

{self._data_flow()}

## Security Considerations

{self._security_section()}

## Scalability Strategy

{self._scalability_section()}

## Deployment Architecture

{self._deployment_architecture()}

---

Last updated: {datetime.now().strftime("%Y-%m-%d")}
"""

        return {
            "success": True,
            "output": {"file": "docs/ARCHITECTURE.md", "content": content, "type": "markdown"},
            "artifacts": {"diagrams_generated": True, "components_documented": len(tech_stack)},
        }

    def _generate_code_comments(self, ctx: Dict[str, Any], task: AgentTask) -> Dict[str, Any]:
        """Generate inline code documentation guidelines."""
        return {
            "success": True,
            "output": {
                "message": "Code documentation guidelines generated",
                "guidelines": {
                    "functions": "Use JSDoc for JS/TS, Docstrings for Python",
                    "classes": "Document all public methods and attributes",
                    "complex_logic": "Add inline comments for business logic",
                    "types": "Use TypeScript or type hints everywhere",
                },
            },
            "artifacts": {
                "documentation_coverage_target": "90%",
                "style_guide": "JSDoc/Google Style",
            },
        }

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _variant_features(self, variant: str) -> List[str]:
        """Return feature list based on project variant."""
        feature_map: Dict[str, List[str]] = {
            "landing": ["Responsive design", "Lead capture", "Analytics tracking"],
            "saas": ["User authentication", "Dashboard", "Subscription management", "API access"],
            "web_app": ["Interactive UI", "Real-time updates", "User profiles", "Data visualization"],
            "mobile_app": ["Cross-platform", "Offline support", "Push notifications", "Mobile-optimized"],
            "ai_product": ["AI-powered features", "Machine learning models", "Natural language processing", "Predictive analytics"],
        }
        return feature_map.get(variant, ["Core functionality", "User management", "Data persistence"])

    def _format_features(self, features: List[str]) -> str:
        return "\n".join(f"- ✨ {f}" for f in features)

    def _generate_quick_start(self, project_name: str) -> str:
        slug = project_name.lower().replace(" ", "-")
        return (
            "```bash\n"
            f"git clone <repo-url>\n"
            f"cd {slug}\n"
            "npm install\n"
            "cp .env.example .env\n"
            "npm run dev\n"
            "```"
        )

    def _generate_usage_examples(self, project_name: str) -> str:
        class_name = project_name.replace(" ", "")
        pkg_name = project_name.lower().replace(" ", "-")
        return (
            "### Basic Usage\n\n"
            "```javascript\n"
            f"import {{ {class_name} }} from '{pkg_name}';\n\n"
            f"const app = new {class_name}();\n"
            "app.start();\n"
            "```"
        )

    def _generate_contributing_guide(self) -> str:
        return (
            "We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md).\n\n"
            "1. Fork the repository\n"
            "2. Create your feature branch (`git checkout -b feature/amazing-feature`)\n"
            "3. Commit your changes (`git commit -m 'Add amazing feature'`)\n"
            "4. Push to the branch (`git push origin feature/amazing-feature`)\n"
            "5. Open a Pull Request"
        )

    def _format_tech_stack(self, tech_stack: Dict[str, str]) -> str:
        if not tech_stack:
            return "- Frontend: React\n- Backend: Node.js/Express\n- Database: PostgreSQL"
        return "\n".join(f"- {k.capitalize()}: {v}" for k, v in tech_stack.items())

    def _architecture_diagram(self) -> str:
        return (
            "┌─────────────────┐\n"
            "│   Client App    │\n"
            "└────────┬────────┘\n"
            "         │\n"
            "         ▼\n"
            "┌─────────────────┐\n"
            "│   API Gateway   │\n"
            "└────────┬────────┘\n"
            "         │\n"
            "    ┌────┴────┐\n"
            "    ▼         ▼\n"
            "┌────────┐ ┌────────┐\n"
            "│Services│ │Database│\n"
            "└────────┘ └────────┘"
        )

    def _component_breakdown(self) -> str:
        return (
            "### Frontend\n"
            "- **Components**: Reusable UI components\n"
            "- **Pages**: Route-level page components\n"
            "- **Services**: API integration layer\n"
            "- **Store**: State management\n\n"
            "### Backend\n"
            "- **Controllers**: Request handlers\n"
            "- **Services**: Business logic\n"
            "- **Models**: Data layer\n"
            "- **Middleware**: Request processing"
        )

    def _data_flow(self) -> str:
        return (
            "1. User interacts with Frontend\n"
            "2. API calls go through Gateway\n"
            "3. Services process business logic\n"
            "4. Data persisted to Database\n"
            "5. Response returned to Client"
        )

    def _security_section(self) -> str:
        return (
            "- Authentication: JWT tokens with refresh\n"
            "- Authorization: Role-based access control\n"
            "- Data encryption: At rest and in transit\n"
            "- Input validation: Schema validation on all inputs\n"
            "- Rate limiting: Prevents abuse\n"
            "- Security headers: CSP, HSTS, etc."
        )

    def _scalability_section(self) -> str:
        return (
            "- Horizontal scaling: Stateless services\n"
            "- Caching: Redis for session and data\n"
            "- CDN: Static assets served via CDN\n"
            "- Database: Read replicas for scaling reads\n"
            "- Load balancing: Distribute traffic evenly"
        )

    def _deployment_architecture(self) -> str:
        return (
            "- CI/CD: GitHub Actions → Docker → Kubernetes\n"
            "- Hosting: Cloud provider (AWS/GCP/Azure)\n"
            "- Monitoring: Prometheus + Grafana\n"
            "- Logging: Centralized logging with ELK\n"
            "- Alerts: PagerDuty for critical issues"
        )

    def _generic_api_docs(self, project_name: str) -> str:
        return (
            "# API Documentation\n\n"
            "## Base URL\n"
            f"```\nhttps://api.{project_name.lower().replace(' ', '-')}.com/v1\n```\n\n"
            "## Authentication\n"
            "All API requests require a Bearer token in the Authorization header.\n\n"
            "## Endpoints\n\n"
            "### Health Check\n**GET** `/health`\n\n"
            "### Users\n"
            "**GET** `/users` - List users\n"
            "**POST** `/users` - Create user\n"
            "**GET** `/users/:id` - Get user\n"
            "**PUT** `/users/:id` - Update user\n"
            "**DELETE** `/users/:id` - Delete user\n\n"
            "## Response Format\n\n"
            "```json\n"
            '{\n  "success": true,\n  "data": {},\n  "message": "Operation completed"\n}\n'
            "```"
        )

    def _fastapi_docs(self) -> str:
        return (
            "# API Documentation\n\n"
            "FastAPI auto-generates interactive docs at:\n"
            "- Swagger UI: `/docs`\n"
            "- ReDoc: `/redoc`\n\n"
            "## Endpoints\n\n"
            "See interactive documentation at the URLs above."
        )

    def _prerequisites(self) -> str:
        return (
            "- Modern web browser (Chrome, Firefox, Safari, Edge)\n"
            "- Basic understanding of web applications\n"
            "- Account credentials (provided by your administrator)"
        )

    def _guide_steps(self) -> str:
        return (
            "### 1. Access the Application\n\n"
            "Navigate to the application URL and log in with your credentials.\n\n"
            "### 2. Complete Your Profile\n\n"
            "Fill in your profile information and preferences.\n\n"
            "### 3. Explore the Dashboard\n\n"
            "Familiarize yourself with the main dashboard and navigation.\n\n"
            "### 4. Start Using Core Features\n\n"
            "Begin with the basic features before exploring advanced options."
        )

    def _best_practices(self) -> str:
        return (
            "- Keep your browser updated for best performance\n"
            "- Use strong, unique passwords\n"
            "- Log out when finished, especially on shared computers\n"
            "- Regularly check for updates and new features"
        )

    def _troubleshooting(self) -> str:
        return (
            "### Can't Log In?\n\n"
            "- Verify your credentials are correct\n"
            "- Check if Caps Lock is enabled\n"
            "- Clear browser cache and cookies\n"
            "- Contact support if issues persist\n\n"
            "### Page Not Loading?\n\n"
            "- Check your internet connection\n"
            "- Try refreshing the page\n"
            "- Disable browser extensions temporarily\n"
            "- Try a different browser"
        )

    def _next_steps(self) -> str:
        return (
            "- Explore advanced features in the [Advanced Guide](advanced.md)\n"
            "- Join our community forum for tips and support\n"
            "- Check out video tutorials on our YouTube channel\n"
            "- Read the [API Documentation](API.md) for developers"
        )
