"""
Output formatting utilities
"""
from typing import Any, Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.table import Table
import json

console = Console()

class ARIAFormatter:
    """Format output for ARIA system"""
    
    @staticmethod
    def print_title(text: str, subtitle: str = "") -> None:
        """Print formatted title"""
        console.print(f"\n[bold cyan]🤖 {text}[/bold cyan]")
        if subtitle:
            console.print(f"[dim]{subtitle}[/dim]")
    
    @staticmethod
    def print_section(title: str, content: str, style: str = "cyan") -> None:
        """Print formatted section"""
        panel = Panel(
            content,
            title=f"[bold {style}]{title}[/bold {style}]",
            expand=False,
            border_style=style
        )
        console.print(panel)
    
    @staticmethod
    def print_agent_thinking(agent_name: str, thoughts: str) -> None:
        """Print agent thinking process"""
        console.print(f"\n[yellow]🧠 {agent_name} Thinking:[/yellow]")
        console.print(f"[dim]{thoughts}[/dim]")
    
    @staticmethod
    def print_tool_call(tool_name: str, args: Dict[str, Any]) -> None:
        """Print tool call"""
        console.print(f"[blue]🛠️  Calling: {tool_name}[/blue]")
        console.print(f"[dim]Args: {json.dumps(args, indent=2)}[/dim]")
    
    @staticmethod
    def print_tool_result(result: str, success: bool = True) -> None:
        """Print tool result"""
        emoji = "✅" if success else "❌"
        color = "green" if success else "red"
        console.print(f"[{color}]{emoji} Result:[/{color}] {result}")
    
    @staticmethod
    def print_reasoning_chain(steps: List[str]) -> None:
        """Print reasoning chain"""
        console.print("\n[magenta]🔗 Reasoning Chain:[/magenta]")
        for i, step in enumerate(steps, 1):
            console.print(f"  [dim]{i}.[/dim] {step}")
    
    @staticmethod
    def print_code(code: str, language: str = "python") -> None:
        """Print formatted code"""
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        console.print(syntax)
    
    @staticmethod
    def print_table(data: List[Dict[str, str]], title: str = "") -> None:
        """Print formatted table"""
        if not data:
            return
        
        table = Table(title=title, show_header=True, header_style="bold cyan")
        
        # Add columns
        for key in data[0].keys():
            table.add_column(key)
        
        # Add rows
        for row in data:
            table.add_row(*[str(v) for v in row.values()])
        
        console.print(table)
    
    @staticmethod
    def print_metrics(metrics: Dict[str, Any]) -> None:
        """Print performance metrics"""
        table = Table(title="📊 Performance Metrics", show_header=True, header_style="bold green")
        table.add_column("Metric")
        table.add_column("Value")
        
        for key, value in metrics.items():
            table.add_row(key, str(value))
        
        console.print(table)
    
    @staticmethod
    def print_success(message: str) -> None:
        """Print success message"""
        console.print(f"[green]✅ {message}[/green]")
    
    @staticmethod
    def print_error(message: str) -> None:
        """Print error message"""
        console.print(f"[red]❌ {message}[/red]")
    
    @staticmethod
    def print_warning(message: str) -> None:
        """Print warning message"""
        console.print(f"[yellow]⚠️  {message}[/yellow]")
    
    @staticmethod
    def print_info(message: str) -> None:
        """Print info message"""
        console.print(f"[cyan]ℹ️  {message}[/cyan]")

# Global formatter instance
formatter = ARIAFormatter()