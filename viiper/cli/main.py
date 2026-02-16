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
    add_completion=False
)
console = Console()


@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    variant: str = typer.Option("saas", "--variant", "-v", help="Project variant (landing, web, saas, mobile, ai)"),
    budget: float = typer.Option(10000, "--budget", "-b", help="Project budget in EUR"),
    timeline: int = typer.Option(12, "--timeline", "-t", help="Timeline in weeks")
):
    """
    Initialize a new VIIPER project.
    
    Example:
        viiper init my-saas --variant=saas --budget=10000 --timeline=12
    """
    try:
        # Parse variant
        variant_enum = Variant(variant.lower())
        
        # Create project
        project = Project(
            name=name,
            variant=variant_enum,
            budget=budget,
            timeline_weeks=timeline
        )
        
        rprint(f"\n[bold green]✓[/bold green] Project '{name}' initialized successfully!")
        rprint(f"\n{project}")
        
        rprint("\n[bold]Next steps:[/bold]")
        rprint("1. Review project configuration")
        rprint("2. Run: viiper execute --phase=validation")
        rprint("3. Check status: viiper status\n")
        
    except ValueError as e:
        rprint(f"\n[bold red]✗[/bold red] Invalid variant: {variant}")
        rprint(f"Valid variants: {', '.join([v.value for v in Variant])}\n")
        raise typer.Exit(1)


@app.command()
def status(
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed status")
):
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
        budget_spent=3500
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
        
        table.add_row("Registered", str(orch_status['agents_registered']))
        table.add_row("Active", str(orch_status['agents_active']))
        table.add_row("Idle", str(orch_status['agents_idle']))
        
        console.print(table)
        
        # Project metrics
        rprint(f"\n[bold]Timeline:[/bold] {summary['timeline']['progress']}")
        rprint(f"[bold]Budget:[/bold] {summary['budget']['usage']}")
        rprint(f"[bold]Users:[/bold] {summary['metrics']['users']}")
        rprint(f"[bold]Revenue:[/bold] {summary['metrics']['revenue']}")
        rprint(f"[bold]On Track:[/bold] {'✅ Yes' if summary['on_track'] else '⚠️ No'}\n")


@app.command()
def execute(
    phase: Optional[str] = typer.Option(None, "--phase", "-p", help="Phase to execute (validation, ideation, production, etc.)"),
    auto: bool = typer.Option(False, "--auto", help="Auto-execute without confirmation")
):
    """
    Execute project phase with agents.
    
    Example:
        viiper execute --phase=validation --auto
    """
    # Demo implementation
    project = Project(
        name="Demo Project",
        variant=Variant.SAAS,
        budget=10000,
        timeline_weeks=12
    )
    
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
        budget_spent=3500
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
            metrics
        )
    
    console.print("\n")
    console.print(table)
    console.print("\n")


@app.command()
def version():
    """Show VIIPER version."""
    from viiper import __version__
    rprint(f"\nVIIPER V4 Framework v{__version__}\n")


if __name__ == "__main__":
    app()
