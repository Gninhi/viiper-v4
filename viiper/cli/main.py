"""
VIIPER V4 CLI Tool.

Command-line interface for managing VIIPER projects.
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from viiper.core.project import Project
from viiper.core.variant import Variant
from viiper.core.phase import Phase
from viiper.orchestrator import ProjectOrchestrator
from viiper.agents.research import MarketResearchAgent, UserInterviewAgent

app = typer.Typer(
    name="viiper",
    help="VIIPER V4: Revolutionary Multi-Agent Framework for Product Development",
    add_completion=False,
)
console = Console()


@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    variant: str = typer.Option(
        "saas", "--variant", "-v", help="Project variant (landing, web, saas, mobile, ai)"
    ),
    budget: float = typer.Option(10000, "--budget", "-b", help="Project budget in EUR"),
    timeline: int = typer.Option(12, "--timeline", "-t", help="Timeline in weeks"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save project to database"),
):
    """
    Initialize a new VIIPER project.

    Example:
        viiper init my-saas --variant=saas --budget=10000 --timeline=12
    """
    from viiper.persistence import get_session, ProjectRepository
    from datetime import datetime

    try:
        # Parse variant
        variant_enum = Variant(variant.lower())

        # Create project
        project = Project(
            name=name,
            variant=variant_enum,
            budget=budget,
            timeline_weeks=timeline,
            started_at=datetime.now(),
        )

        # Save to database if requested
        if save:
            session = get_session()
            repo = ProjectRepository(session)

            try:
                # Check if project with same name exists
                existing = repo.get_by_name(name)
                if existing:
                    rprint(f"\n[bold yellow]⚠[/bold yellow] Project '{name}' already exists!")
                    overwrite = typer.confirm("Overwrite existing project?")
                    if not overwrite:
                        rprint("\n[yellow]Cancelled[/yellow]\n")
                        raise typer.Exit(0)
                    # Delete existing and create new
                    repo.hard_delete(existing.id)

                # Save project
                project = repo.create(project)
                rprint(f"\n[bold green]✓[/bold green] Project '{name}' initialized and saved!")
                rprint(f"[dim]Project ID: {project.id}[/dim]")
            finally:
                session.close()
        else:
            rprint(f"\n[bold green]✓[/bold green] Project '{name}' initialized (not saved)!")

        rprint(f"\n{project}")

        rprint("\n[bold]Next steps:[/bold]")
        rprint("1. Review project configuration")
        rprint("2. Run: viiper execute --phase=validation")
        rprint("3. Check status: viiper status")
        if save:
            rprint(f"4. View anytime: viiper load {name}\n")
        else:
            rprint("4. Save project: viiper init <name> --save\n")

    except ValueError as e:
        rprint(f"\n[bold red]✗[/bold red] Invalid variant: {variant}")
        rprint(f"Valid variants: {', '.join([v.value for v in Variant])}\n")
        raise typer.Exit(1)


@app.command()
def status(detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed status")):
    """
    Show project status and health.

    Example:
        viiper status --detailed
    """
    # For demo purposes, create a sample project
    # In production, this would load from persistent storage
    project = Project(
        name="Demo Project",
        variant=Variant.SAAS,
        budget=10000,
        timeline_weeks=12,
        current_users=45,
        target_users=100,
        budget_spent=3500,
    )

    orchestrator = ProjectOrchestrator(project)

    # Register some sample agents
    orchestrator.register_agent(MarketResearchAgent())
    orchestrator.register_agent(UserInterviewAgent())

    # Get status
    orch_status = orchestrator.get_status()

    rprint("\n[bold]Project Status[/bold]")
    rprint(f"Project: {orch_status['project']}")
    rprint(f"Phase: {orch_status['current_phase']}")
    rprint(f"Health: {orch_status['project_health']:.1f}/10\n")

    if detailed:
        summary = project.get_summary()

        # Agents table
        table = Table(title="Agent Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Registered", str(orch_status["agents_registered"]))
        table.add_row("Active", str(orch_status["agents_active"]))
        table.add_row("Idle", str(orch_status["agents_idle"]))

        console.print(table)

        # Project metrics
        rprint(f"\n[bold]Timeline:[/bold] {summary['timeline']['progress']}")
        rprint(f"[bold]Budget:[/bold] {summary['budget']['usage']}")
        rprint(f"[bold]Users:[/bold] {summary['metrics']['users']}")
        rprint(f"[bold]Revenue:[/bold] {summary['metrics']['revenue']}")
        rprint(f"[bold]On Track:[/bold] {'✅ Yes' if summary['on_track'] else '⚠️ No'}\n")


@app.command()
def execute(
    phase: Optional[str] = typer.Option(
        None, "--phase", "-p", help="Phase to execute (validation, ideation, production, etc.)"
    ),
    auto: bool = typer.Option(False, "--auto", help="Auto-execute without confirmation"),
):
    """
    Execute project phase with agents.

    Example:
        viiper execute --phase=validation --auto
    """
    # Demo implementation
    project = Project(name="Demo Project", variant=Variant.SAAS, budget=10000, timeline_weeks=12)

    orchestrator = ProjectOrchestrator(project)
    orchestrator.register_agent(MarketResearchAgent())
    orchestrator.register_agent(UserInterviewAgent())

    # Parse phase
    target_phase = Phase(phase.lower()) if phase else project.phase

    if not auto:
        confirm = typer.confirm(f"Execute {target_phase.display_name} phase?")
        if not confirm:
            rprint("\n[yellow]Cancelled[/yellow]\n")
            raise typer.Exit(0)

    rprint(f"\n[bold]Executing {target_phase.display_name} Phase...[/bold]\n")

    # This would be async in production
    import asyncio

    result = asyncio.run(orchestrator.execute_phase(target_phase))

    if result.success:
        rprint(f"[bold green]✓[/bold green] Phase completed successfully!")
        rprint(f"Tasks completed: {result.tasks_completed}")
        rprint(f"Duration: {result.duration_seconds:.2f}s\n")
    else:
        rprint(f"[bold red]✗[/bold red] Phase execution failed")
        rprint(f"Tasks failed: {result.tasks_failed}")
        for error in result.errors:
            rprint(f"  - {error}")
        rprint()


@app.command()
def health():
    """
    Show detailed health score.

    Example:
        viiper health
    """
    # Demo project
    project = Project(
        name="Demo Project",
        variant=Variant.SAAS,
        budget=10000,
        timeline_weeks=12,
        current_users=45,
        target_users=100,
        current_revenue=2400,
        target_revenue=10000,
        budget_spent=3500,
    )

    health_score = project.calculate_health_score()

    rprint(str(health_score))


@app.command()
def phases():
    """
    List all VIIPER phases with descriptions.

    Example:
        viiper phases
    """
    rprint("\n[bold]VIIPER Phases[/bold]\n")

    for phase in Phase:
        min_weeks, max_weeks = phase.typical_duration_weeks
        duration = f"{min_weeks}-{max_weeks} weeks" if max_weeks > 0 else "Ongoing"

        rprint(f"[bold cyan]{phase.short_code}[/bold cyan] - {phase.display_name}")
        rprint(f"   Duration: {duration}")
        rprint(f"   {phase.description}\n")


@app.command()
def gates(
    project_name: str = typer.Argument(..., help="Project name"),
    to_phase: Optional[str] = typer.Option(
        None, "--to", "-t", help="Target phase to check transition"
    ),
):
    """
    Check quality gates for project transitions.

    Example:
        viiper gates my-project --to=ideation
        viiper gates my-project  # Check current phase gate
    """
    from viiper.persistence import get_session, ProjectRepository
    from viiper.core.quality_gates import validate_transition, gate_registry

    session = get_session()
    try:
        repo = ProjectRepository(session)
        project = repo.get_by_name(project_name)

        if not project:
            rprint(f"\n[bold red]✗[/bold red] Project '{project_name}' not found!\n")
            raise typer.Exit(1)

        if to_phase:
            # Validate specific transition
            try:
                target_phase = Phase(to_phase.lower())
            except ValueError:
                rprint(f"\n[bold red]✗[/bold red] Invalid phase: {to_phase}")
                valid_phases = ", ".join([p.value for p in Phase])
                rprint(f"Valid phases: {valid_phases}\n")
                raise typer.Exit(1)

            result = validate_transition(project, target_phase)

            rprint(f"\n[bold]Quality Gate: {result.gate_name}[/bold]")
            rprint(f"Transition: {result.from_phase.display_name} → {result.to_phase.display_name}")

            if result.status.value == "passed":
                rprint(f"Status: [bold green]✅ PASSED[/bold green] (Score: {result.score}/10)")
            elif result.status.value == "warning":
                rprint(f"Status: [bold yellow]⚠️  WARNING[/bold yellow] (Score: {result.score}/10)")
            else:
                rprint(f"Status: [bold red]❌ FAILED[/bold red] (Score: {result.score}/10)")

            rprint(f"\n[bold]Criteria:[/bold]")
            for criterion in result.criteria_results:
                status_icon = "✅" if criterion["status"] == "passed" else "❌"
                rprint(f"  {status_icon} {criterion['criterion']}: {criterion['message']}")

            if result.blocking_issues:
                rprint(f"\n[bold red]Blocking Issues:[/bold red]")
                for issue in result.blocking_issues:
                    rprint(f"  - {issue}")

            if result.recommendations:
                rprint(f"\n[bold yellow]Recommendations:[/bold yellow]")
                for rec in result.recommendations[:5]:  # Show first 5
                    rprint(f"  - {rec}")

            rprint()

            if result.can_transition:
                rprint("[bold green]✓ Transition allowed[/bold green]\n")
            else:
                rprint("[bold red]✗ Transition blocked[/bold red]")
                rprint("Use --force to bypass (not recommended)\n")
                raise typer.Exit(1)
        else:
            # List all gates
            rprint("\n[bold]Quality Gates[/bold]\n")

            for gate_info in gate_registry.list_gates():
                rprint(f"[bold]{gate_info['name']}[/bold]")
                rprint(f"  Transition: {gate_info['from_phase']} → {gate_info['to_phase']}")
                rprint(f"  Criteria: {gate_info['criteria_count']}")
                rprint(f"  Minimum Score: {gate_info['minimum_score']}/10\n")

    finally:
        session.close()


@app.command()
def ckb(
    action: str = typer.Argument(..., help="Action: add, search, stats, list"),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Entry title"),
    content: Optional[str] = typer.Option(None, "--content", "-c", help="Entry content"),
    entry_type: Optional[str] = typer.Option(
        None, "--type", help="Entry type (pattern, lesson, etc.)"
    ),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated tags"),
):
    """
    Collective Knowledge Base management.

    Examples:
        viiper ckb add --title="React Pattern" --content="Use hooks" --type=pattern --tags=react,frontend
        viiper ckb search --query="authentication"
        viiper ckb stats
        viiper ckb list
    """
    from viiper.ckb import (
        CollectiveKnowledgeBase,
        KnowledgeEntry,
        KnowledgeType,
        add_knowledge,
        search_knowledge,
        get_knowledge_stats,
        collective_kb,
    )

    if action == "add":
        if not title or not content:
            rprint("\n[bold red]✗[/bold red] --title and --content are required for 'add'\n")
            raise typer.Exit(1)

        # Parse type
        kb_type = KnowledgeType.PATTERN
        if entry_type:
            try:
                kb_type = KnowledgeType(entry_type.lower())
            except ValueError:
                valid_types = ", ".join([t.value for t in KnowledgeType])
                rprint(f"\n[bold red]✗[/bold red] Invalid type. Valid types: {valid_types}\n")
                raise typer.Exit(1)

        # Parse tags
        tag_list = tags.split(",") if tags else []

        entry = add_knowledge(
            title=title,
            content=content,
            entry_type=kb_type,
            tags=tag_list,
        )

        rprint(f"\n[bold green]✓[/bold green] Knowledge entry added!")
        rprint(f"ID: {entry.id}")
        rprint(f"Type: {entry.type.value}")
        rprint(f"Title: {entry.title}\n")

    elif action == "search":
        if not query:
            rprint("\n[bold red]✗[/bold red] --query is required for 'search'\n")
            raise typer.Exit(1)

        # Parse type filter
        type_filter = None
        if entry_type:
            try:
                type_filter = KnowledgeType(entry_type.lower())
            except ValueError:
                pass

        # Parse tags filter
        tag_list = tags.split(",") if tags else []

        results = search_knowledge(
            query=query,
            entry_type=type_filter,
            tags=tag_list if tag_list else None,
        )

        rprint(f"\n[bold]Search Results for:[/bold] {query}\n")

        if not results:
            rprint("[dim]No results found.[/dim]\n")
        else:
            for entry in results:
                rprint(f"[bold cyan]{entry.title}[/bold cyan] [{entry.type.value}]")
                rprint(
                    f"  {entry.content[:100]}..."
                    if len(entry.content) > 100
                    else f"  {entry.content}"
                )
                rprint(
                    f"  [dim]Tags: {', '.join(entry.tags)} | Used: {entry.usage_count} times[/dim]\n"
                )

    elif action == "stats":
        stats = get_knowledge_stats()

        rprint("\n[bold]Collective Knowledge Base Statistics[/bold]\n")
        rprint(f"Total Entries: {stats['total_entries']}")
        rprint(f"Total Usage: {stats['total_usage']}")
        rprint(f"Average Confidence: {stats['average_confidence']}\n")

        rprint("[bold]By Type:[/bold]")
        for type_name, count in stats["by_type"].items():
            if count > 0:
                rprint(f"  {type_name}: {count}")

        if stats.get("most_used"):
            rprint(f"\n[bold]Most Used:[/bold]")
            for entry_id in stats["most_used"][:5]:
                entry = collective_kb.get(entry_id)
                if entry:
                    rprint(f"  - {entry.title} ({entry.usage_count} uses)")

        rprint()

    elif action == "list":
        entries = collective_kb.get_recent(limit=20)

        rprint(f"\n[bold]Recent Knowledge Entries ({len(entries)} shown)[/bold]\n")

        for entry in entries:
            rprint(f"[bold cyan]{entry.title}[/bold cyan]")
            rprint(f"  Type: {entry.type.value}")
            rprint(f"  ID: {entry.id}")
            rprint(f"  Tags: {', '.join(entry.tags) if entry.tags else 'None'}")
            rprint(f"  Created: {entry.created_at.strftime('%Y-%m-%d')}\n")

    else:
        rprint(f"\n[bold red]✗[/bold red] Unknown action: {action}")
        rprint("Valid actions: add, search, stats, list\n")
        raise typer.Exit(1)


@app.command()
def variants():
    """
    List all project variants with characteristics.

    Example:
        viiper variants
    """
    table = Table(title="VIIPER Project Variants")
    table.add_column("Variant", style="cyan")
    table.add_column("Timeline", style="green")
    table.add_column("Budget", style="yellow")
    table.add_column("Primary Metrics", style="magenta")

    for variant in Variant:
        min_weeks, max_weeks = variant.typical_timeline_weeks
        min_budget, max_budget = variant.typical_budget_range
        metrics = ", ".join(variant.primary_metrics[:2])  # First 2 metrics

        table.add_row(
            variant.display_name,
            f"{min_weeks}-{max_weeks} weeks",
            f"€{min_budget:,}-{max_budget:,}",
            metrics,
        )

    console.print("\n")
    console.print(table)
    console.print("\n")


@app.command()
def version():
    """Show VIIPER version."""
    from viiper import __version__

    rprint(f"\nVIIPER V4 Framework v{__version__}\n")


@app.command()
def list_projects(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    variant: Optional[str] = typer.Option(None, "--variant", "-v", help="Filter by variant"),
    phase: Optional[str] = typer.Option(None, "--phase", "-p", help="Filter by phase"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of projects to show"),
):
    """
    List all projects.

    Example:
        viiper list-projects --status=active --limit=10
    """
    from viiper.persistence import get_session, ProjectRepository
    from viiper.core.variant import Variant
    from viiper.core.phase import Phase

    # Parse filters
    variant_filter = Variant(variant) if variant else None
    phase_filter = Phase(phase) if phase else None

    # Get projects from database
    session = get_session()
    repo = ProjectRepository(session)

    try:
        projects = repo.list(status=status, variant=variant_filter, phase=phase_filter, limit=limit)

        if not projects:
            rprint("\n[yellow]No projects found[/yellow]\n")
            return

        # Create table
        table = Table(title=f"Projects ({len(projects)})")
        table.add_column("Name", style="cyan")
        table.add_column("Variant", style="green")
        table.add_column("Phase", style="yellow")
        table.add_column("Status", style="magenta")
        table.add_column("Health", style="blue")
        table.add_column("Budget", style="red")

        for project in projects:
            health = project.health_score.overall if project.health_score else 0.0
            health_str = f"{health:.1f}/10"
            budget_pct = project.get_budget_usage() * 100

            table.add_row(
                project.name,
                project.variant.display_name,
                project.phase.short_code,
                project.status,
                health_str,
                f"{budget_pct:.0f}%",
            )

        console.print("\n")
        console.print(table)
        console.print("\n")

    finally:
        session.close()


@app.command()
def load(
    identifier: str = typer.Argument(..., help="Project ID or name to load"),
    show_details: bool = typer.Option(False, "--details", "-d", help="Show detailed information"),
):
    """
    Load and display a project.

    Example:
        viiper load my-saas --details
    """
    from viiper.persistence import get_session, ProjectRepository

    session = get_session()
    repo = ProjectRepository(session)

    try:
        # Try to load by ID first, then by name
        project = repo.get(identifier)
        if not project:
            project = repo.get_by_name(identifier)

        if not project:
            rprint(f"\n[bold red]✗[/bold red] Project '{identifier}' not found\n")
            raise typer.Exit(1)

        # Display project
        rprint(str(project))

        if show_details:
            # Show health score
            if project.health_score:
                rprint(str(project.health_score))

            # Show metadata
            if project.metadata.tags or project.metadata.industry:
                rprint("[bold]Metadata:[/bold]")
                if project.metadata.tags:
                    rprint(f"Tags: {', '.join(project.metadata.tags)}")
                if project.metadata.industry:
                    rprint(f"Industry: {project.metadata.industry}")
                if project.metadata.target_market:
                    rprint(f"Target Market: {project.metadata.target_market}")
                rprint()

    finally:
        session.close()


@app.command()
def archive(
    identifier: str = typer.Argument(..., help="Project ID or name to archive"),
    hard: bool = typer.Option(False, "--hard", help="Permanently delete (cannot be undone)"),
):
    """
    Archive or delete a project.

    Example:
        viiper archive my-old-project
        viiper archive my-old-project --hard  # Permanent deletion
    """
    from viiper.persistence import get_session, ProjectRepository

    session = get_session()
    repo = ProjectRepository(session)

    try:
        # Get project first
        project = repo.get(identifier)
        if not project:
            project = repo.get_by_name(identifier)

        if not project:
            rprint(f"\n[bold red]✗[/bold red] Project '{identifier}' not found\n")
            raise typer.Exit(1)

        # Confirm
        action = "permanently delete" if hard else "archive"
        confirm = typer.confirm(f"Are you sure you want to {action} project '{project.name}'?")

        if not confirm:
            rprint("\n[yellow]Cancelled[/yellow]\n")
            raise typer.Exit(0)

        # Delete
        if hard:
            success = repo.hard_delete(project.id)
            action_past = "deleted"
        else:
            success = repo.delete(project.id)
            action_past = "archived"

        if success:
            rprint(f"\n[bold green]✓[/bold green] Project '{project.name}' {action_past}\n")
        else:
            rprint(f"\n[bold red]✗[/bold red] Failed to {action} project\n")
            raise typer.Exit(1)

    finally:
        session.close()


@app.command()
def db_init():
    """
    Initialize the database and run migrations.

    Example:
        viiper db-init
    """
    from viiper.persistence import init_database
    import subprocess

    rprint("\n[bold]Initializing VIIPER database...[/bold]\n")

    # Initialize database
    try:
        db = init_database()
        rprint(f"[bold green]✓[/bold green] Database initialized at: {db.database_url}")
    except Exception as e:
        rprint(f"[bold red]✗[/bold red] Failed to initialize database: {e}\n")
        raise typer.Exit(1)

    # Run migrations
    rprint("\n[bold]Running migrations...[/bold]\n")
    try:
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)

        if result.returncode == 0:
            rprint("[bold green]✓[/bold green] Migrations completed successfully\n")
        else:
            rprint(f"[bold red]✗[/bold red] Migration failed:\n{result.stderr}\n")
            raise typer.Exit(1)
    except FileNotFoundError:
        rprint(
            "[bold yellow]⚠[/bold yellow] Alembic not found. Install with: pip install alembic\n"
        )
        raise typer.Exit(1)


@app.command()
def db_upgrade():
    """
    Run database migrations to latest version.

    Example:
        viiper db-upgrade
    """
    import subprocess

    rprint("\n[bold]Running database migrations...[/bold]\n")

    try:
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)

        if result.returncode == 0:
            rprint("[bold green]✓[/bold green] Database upgraded successfully\n")
            if result.stdout:
                rprint(result.stdout)
        else:
            rprint(f"[bold red]✗[/bold red] Migration failed:\n{result.stderr}\n")
            raise typer.Exit(1)
    except FileNotFoundError:
        rprint(
            "[bold yellow]⚠[/bold yellow] Alembic not found. Install with: pip install alembic\n"
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
