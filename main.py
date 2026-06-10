"""
ARIA CLI - Main entry point
"""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from config import settings, ensure_directories
from graph import ARIAWorkflow
from utils.logger import logger
from utils.formatter import formatter
from utils.metrics import metrics_collector
from memory import vector_store, metadata_db

# Initialize CLI
app = typer.Typer(help="🤖 ARIA - Advanced Reasoning & Intelligence Agent CLI")
console = Console()

# Initialize workflow
workflow = None

def initialize_app():
    """Initialize application"""
    global workflow
    
    # Ensure directories exist
    ensure_directories()
    
    # Initialize workflow
    workflow = ARIAWorkflow()
    
    logger.info("✅ ARIA system initialized")

@app.command()
def run(
    task: str = typer.Argument(..., help="Task description"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="Additional context"),
    show_metrics: bool = typer.Option(False, "--metrics", "-m", help="Show performance metrics")
):
    """
    Execute a task using ARIA
    
    Example: aria run "Research machine learning" --context "for beginners"
    """
    if not workflow:
        initialize_app()
    
    formatter.print_title("ARIA Task Execution", f"Task: {task}")
    
    # Execute workflow
    result = workflow.execute(task, context or "")
    
    # Display results
    if result["status"] == "success":
        formatter.print_success("Task completed successfully!")
        
        # Display results metadata
        if result.get("classification"):
            formatter.print_info(f"Classification: {result['classification'].get('primary_agent', 'N/A')}")
        
        if result.get("routing"):
            formatter.print_info(f"Agent sequence: {' → '.join(result['routing'])}")
        
        # Display final output with better formatting
        if result.get("final_output"):
            console.print(Panel(result["final_output"], title="[bold cyan]Solution[/bold cyan]", border_style="cyan", padding=(1, 2)))
        else:
            formatter.print_info("Task processed (no output generated)")
        
        # Show metrics if requested
        if show_metrics:
            metrics = metrics_collector.get_summary()
            formatter.print_metrics(metrics)
    
    else:
        formatter.print_error(f"Task failed: {result.get('error', 'Unknown error')}")

@app.command()
def chat():
    """Interactive chat mode"""
    if not workflow:
        initialize_app()
    
    formatter.print_title("ARIA Interactive Chat", "Type 'exit' to quit")
    
    while True:
        try:
            task = console.input("[cyan]You:[/cyan] ")
            
            if task.lower() in ["exit", "quit", "bye"]:
                formatter.print_info("Goodbye!")
                break
            
            if not task.strip():
                continue
            
            # Execute task
            result = workflow.execute(task)
            
            if result["status"] == "success":
                final_output = result.get('final_output', '')
                if final_output:
                    # Display formatted output
                    console.print(f"\n[bold green]🤖 ARIA:[/bold green]")
                    console.print(Panel(final_output, border_style="green", padding=(1, 2)))
                    console.print()
                else:
                    console.print(f"\n[green]ARIA:[/green] Task completed successfully.\n")
            else:
                error_msg = result.get('error', 'Unknown error')
                console.print(f"\n[bold red]❌ Error:[/bold red] {error_msg}\n")
        
        except KeyboardInterrupt:
            formatter.print_info("\nInterrupted by user")
            break
        except Exception as e:
            formatter.print_error(f"Error: {e}")

@app.command()
def status():
    """Show ARIA system status"""
    if not workflow:
        initialize_app()
    
    formatter.print_title("ARIA System Status")
    
    # Workflow info
    workflow_info = workflow.get_workflow_info()
    formatter.print_section("Workflow", f"Agents: {', '.join(workflow_info['available_agents'])}")
    
    # Memory stats
    memory_stats = vector_store.get_memory_stats()
    formatter.print_section("Memory", f"Total memories: {memory_stats['total_memories']}")
    
    # Database stats
    db_stats = metadata_db.get_stats()
    formatter.print_section("Database", f"Total tasks: {db_stats['total_tasks']}")
    
    # Metrics
    metrics = metrics_collector.get_summary()
    formatter.print_metrics(metrics)

@app.command()
def history(limit: int = typer.Option(10, "--limit", "-l", help="Number of recent tasks")):
    """Show task history"""
    if not workflow:
        initialize_app()
    
    formatter.print_title("Task History", f"Last {limit} tasks")
    
    tasks = metadata_db.get_task_history(limit)
    
    if tasks:
        task_data = [
            {
                "Task": task[1][:50] + "..." if len(task[1]) > 50 else task[1],
                "Status": task[4],
                "Time": f"{task[3]:.2f}s",
                "Date": str(task[5])[:10]
            }
            for task in tasks
        ]
        formatter.print_table(task_data, "Recent Tasks")
    else:
        formatter.print_info("No task history found")

@app.command()
def clear_memory():
    """Clear all stored memories"""
    if typer.confirm("⚠️  Are you sure? This will delete all memories."):
        vector_store.clear_memory()
        formatter.print_success("All memories cleared")
    else:
        formatter.print_info("Cancelled")

@app.command()
def research(
    query: str = typer.Argument(..., help="Research query"),
    deep: bool = typer.Option(False, "--deep", "-d", help="Conduct deep research")
):
    """Conduct research"""
    if not workflow:
        initialize_app()
    
    formatter.print_title("Research Mode", query)
    
    # Get research agent
    research_agent = workflow.research_agent
    
    if deep:
        aspects = [
            "Overview and Background",
            "Current State",
            "Future Trends",
            "Practical Applications",
            "Related Topics"
        ]
        result = research_agent.deep_research(query, aspects)
    else:
        result = research_agent.execute(query)
    
    if result.get("status") == "success":
        formatter.print_success("Research completed!")
        if "synthesis" in result:
            formatter.print_section("Synthesis", result["synthesis"])
    else:
        formatter.print_error(f"Research failed: {result.get('error')}")

@app.command()
def write(
    topic: str = typer.Argument(..., help="Writing topic"),
    style: str = typer.Option("blog", "--style", "-s", help="Writing style (blog, tutorial, etc)")
):
    """Generate written content"""
    if not workflow:
        initialize_app()
    
    formatter.print_title("Content Generation", f"{style}: {topic}")
    
    creative_agent = workflow.creative_agent
    
    if style == "blog":
        output = creative_agent.write_blog_post(topic)
    elif style == "tutorial":
        output = creative_agent.create_tutorial(topic)
    else:
        result = creative_agent.execute(f"Write about: {topic}")
        output = result.get("enhanced_output", "")
    
    if output:
        formatter.print_section("Generated Content", output)
    else:
        formatter.print_error("Content generation failed")

@app.command()
def analyze_code(
    code_snippet: Optional[str] = typer.Argument(None, help="Code to analyze")
):
    """Analyze code"""
    if not workflow:
        initialize_app()
    
    formatter.print_title("Code Analysis")
    
    if not code_snippet:
        console.print("Paste your code (enter 'END' on a new line when done):")
        lines = []
        while True:
            line = console.input()
            if line == "END":
                break
            lines.append(line)
        code_snippet = "\n".join(lines)
    
    technical_agent = workflow.technical_agent
    result = technical_agent.debug_code(code_snippet)
    
    if result:
        formatter.print_section("Analysis", result.get("debug_advice", ""))

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """ARIA - Advanced Reasoning & Intelligence Agent"""
    if ctx.invoked_subcommand is None:
        # Show welcome banner
        banner = """
╔═════════════════════════════════════════════╗
║     🤖 ARIA System                          ║
║     Advanced Reasoning & Intelligence       ║
║     Agent CLI                               ║
╚═════════════════════════════════════════════╝
        """
        console.print(banner)
        console.print("[cyan]Use 'aria --help' for commands[/cyan]")

if __name__ == "__main__":
    app()