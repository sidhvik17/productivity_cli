"""
Productivity CLI - Unified command-line tool for task management, 
expense tracking, reminders, and analytics.
"""
import typer
from typing import Optional
from rich.console import Console
from datetime import datetime

from src.core import TaskBoard, Ledger, Notifier, AnalyticsEngine
from src.utils.config import PRIORITIES, STATUSES, EXPENSE_CATEGORIES

# Initialize Typer app
app = typer.Typer(
    name="productivity-cli",
    help="Unified CLI for task management, expense tracking, and analytics",
    add_completion=False
)

# Initialize console
console = Console()

# Initialize components
taskboard = TaskBoard()
ledger = Ledger()
notifier = Notifier()
analytics = AnalyticsEngine()


# TASK COMMANDS

task_app = typer.Typer(help="Manage tasks")
app.add_typer(task_app, name="task")


@task_app.command("add")
def add_task(
    title: str = typer.Argument(..., help="Task title"),
    priority: str = typer.Option("Medium", "--priority", "-p", help="Task priority (High/Medium/Low)"),
    deadline: Optional[str] = typer.Option(None, "--deadline", "-d", help="Deadline (YYYY-MM-DD)"),
    description: Optional[str] = typer.Option("", "--description", "-desc", help="Task description"),
):
    """Add a new task"""
    try:
        task = taskboard.add_task(title, priority, deadline, description)
        console.print(f"[green]✓ Task created: {task['title']} (ID: {task['id'][-6:]})[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@task_app.command("list")
def list_tasks(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="Filter by priority"),
):
    """List all tasks"""
    tasks = taskboard.list_tasks(status, priority)
    taskboard.display_tasks(tasks)


@task_app.command("update")
def update_task_status(
    task_id: str = typer.Argument(..., help="Task ID (full or last 6 chars)"),
    status: str = typer.Option(..., "--status", "-s", help="New status (Todo/Doing/Done)"),
):
    """Update task status"""
    # Find task by partial ID
    tasks = taskboard.list_tasks()
    matching_task = None
    for task in tasks:
        if task['id'].endswith(task_id) or task['id'] == task_id:
            matching_task = task
            break
    
    if not matching_task:
        console.print(f"[red]Task with ID '{task_id}' not found[/red]")
        raise typer.Exit(1)
    
    try:
        if taskboard.update_task_status(matching_task['id'], status):
            console.print(f"[green]✓ Task status updated to {status}[/green]")
        else:
            console.print("[red]Failed to update task[/red]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@task_app.command("edit")
def edit_task(
    task_id: str = typer.Argument(..., help="Task ID (full or last 6 chars)"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New title"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="New priority"),
    deadline: Optional[str] = typer.Option(None, "--deadline", "-d", help="New deadline"),
    description: Optional[str] = typer.Option(None, "--description", "-desc", help="New description"),
):
    """Edit task details"""
    # Find task by partial ID
    tasks = taskboard.list_tasks()
    matching_task = None
    for task in tasks:
        if task['id'].endswith(task_id) or task['id'] == task_id:
            matching_task = task
            break
    
    if not matching_task:
        console.print(f"[red]Task with ID '{task_id}' not found[/red]")
        raise typer.Exit(1)
    
    try:
        if taskboard.update_task(matching_task['id'], title, description, priority, deadline):
            console.print(f"[green]✓ Task updated successfully[/green]")
        else:
            console.print("[red]Failed to update task[/red]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@task_app.command("delete")
def delete_task(
    task_id: str = typer.Argument(..., help="Task ID (full or last 6 chars)"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete a task"""
    # Find task by partial ID
    tasks = taskboard.list_tasks()
    matching_task = None
    for task in tasks:
        if task['id'].endswith(task_id) or task['id'] == task_id:
            matching_task = task
            break
    
    if not matching_task:
        console.print(f"[red]Task with ID '{task_id}' not found[/red]")
        raise typer.Exit(1)
    
    if not confirm:
        confirm = typer.confirm(f"Delete task '{matching_task['title']}'?")
        if not confirm:
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit()
    
    if taskboard.delete_task(matching_task['id']):
        console.print(f"[green]✓ Task deleted[/green]")
    else:
        console.print("[red]Failed to delete task[/red]")


# EXPENSE COMMANDS

expense_app = typer.Typer(help="Track expenses")
app.add_typer(expense_app, name="expense")


@expense_app.command("add")
def add_expense(
    amount: float = typer.Argument(..., help="Expense amount"),
    category: str = typer.Argument(..., help=f"Category: {', '.join(EXPENSE_CATEGORIES)}"),
    description: Optional[str] = typer.Option("", "--description", "-d", help="Expense description"),
    date: Optional[str] = typer.Option(None, "--date", help="Date (YYYY-MM-DD, defaults to today)"),
):
    """Add a new expense"""
    try:
        expense = ledger.add_expense(amount, category, description, date)
        console.print(f"[green]✓ Expense logged: ${expense['amount']:.2f} - {expense['category']} (ID: {expense['id'][-6:]})[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@expense_app.command("list")
def list_expenses(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    start_date: Optional[str] = typer.Option(None, "--start", "-s", help="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end", "-e", help="End date (YYYY-MM-DD)"),
):
    """List all expenses"""
    expenses = ledger.list_expenses(category, start_date, end_date)
    ledger.display_expenses(expenses)


@expense_app.command("total")
def expense_total(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    start_date: Optional[str] = typer.Option(None, "--start", "-s", help="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end", "-e", help="End date (YYYY-MM-DD)"),
):
    """Calculate total expenses"""
    total = ledger.get_total(category, start_date, end_date)
    
    if category:
        console.print(f"[bold]Total {category} expenses: [green]${total:.2f}[/green][/bold]")
    elif start_date or end_date:
        period = f"{start_date or 'beginning'} to {end_date or 'today'}"
        console.print(f"[bold]Total expenses ({period}): [green]${total:.2f}[/green][/bold]")
    else:
        console.print(f"[bold]Total expenses: [green]${total:.2f}[/green][/bold]")


@expense_app.command("breakdown")
def expense_breakdown(
    start_date: Optional[str] = typer.Option(None, "--start", "-s", help="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end", "-e", help="End date (YYYY-MM-DD)"),
):
    """Show spending breakdown by category"""
    breakdown = ledger.get_category_breakdown(start_date, end_date)
    
    if not breakdown:
        console.print("[yellow]No expenses found[/yellow]")
        return
    
    console.print("\n[bold cyan]Spending Breakdown by Category[/bold cyan]\n")
    total = sum(breakdown.values())
    
    for category, amount in breakdown.items():
        percentage = (amount / total * 100) if total > 0 else 0
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        console.print(f"{category:15} ${amount:8.2f} ({percentage:5.1f}%) {bar}")
    
    console.print(f"\n[bold]Total: [green]${total:.2f}[/green][/bold]")


@expense_app.command("delete")
def delete_expense(
    expense_id: str = typer.Argument(..., help="Expense ID (full or last 6 chars)"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete an expense"""
    # Find expense by partial ID
    expenses = ledger.list_expenses()
    matching_expense = None
    for expense in expenses:
        if expense['id'].endswith(expense_id) or expense['id'] == expense_id:
            matching_expense = expense
            break
    
    if not matching_expense:
        console.print(f"[red]Expense with ID '{expense_id}' not found[/red]")
        raise typer.Exit(1)
    
    if not confirm:
        confirm = typer.confirm(
            f"Delete expense: ${matching_expense['amount']:.2f} - {matching_expense['category']}?"
        )
        if not confirm:
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit()
    
    if ledger.delete_expense(matching_expense['id']):
        console.print(f"[green]✓ Expense deleted[/green]")
    else:
        console.print("[red]Failed to delete expense[/red]")


# REMINDER COMMANDS

reminder_app = typer.Typer(help="Manage reminders")
app.add_typer(reminder_app, name="reminder")


@reminder_app.command("check")
def check_reminders():
    """Check for upcoming deadlines"""
    upcoming = notifier.get_upcoming_deadlines(7)
    
    if not upcoming:
        console.print("[green]✓ No upcoming deadlines in the next 7 days![/green]")
        return
    
    console.print("\n[bold yellow]📅 Upcoming Deadlines (Next 7 Days)[/bold yellow]\n")
    
    for task in upcoming:
        days = task['days_until']
        priority_color = {
            "High": "red",
            "Medium": "yellow",
            "Low": "green"
        }.get(task["priority"], "white")
        
        if days == 0:
            day_text = "[bold red]TODAY[/bold red]"
        elif days == 1:
            day_text = "[bold yellow]TOMORROW[/bold yellow]"
        else:
            day_text = f"in {days} days"
        
        console.print(
            f"[{priority_color}]• {task['title']}[/{priority_color}] "
            f"- Due {day_text} ({task['deadline']})"
        )


@reminder_app.command("start")
def start_reminder_service():
    """Start background reminder service (runs until stopped)"""
    console.print("[cyan]Starting reminder service...[/cyan]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    notifier.start()
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping reminder service...[/yellow]")
        notifier.stop()


# ANALYTICS COMMANDS

analytics_app = typer.Typer(help="View analytics and insights")
app.add_typer(analytics_app, name="analytics")


@analytics_app.command("weekly")
def weekly_report():
    """Show weekly analytics report"""
    analytics.display_weekly_report()
    
    # Show insights
    insights = analytics.get_insights()
    if insights:
        console.print("\n[bold cyan]💡 Insights[/bold cyan]\n")
        for insight in insights:
            console.print(f"  {insight}")


@analytics_app.command("monthly")
def monthly_report():
    """Show monthly analytics report"""
    analytics.display_monthly_report()
    
    # Show insights
    insights = analytics.get_insights()
    if insights:
        console.print("\n[bold cyan]💡 Insights[/bold cyan]\n")
        for insight in insights:
            console.print(f"  {insight}")


@analytics_app.command("insights")
def show_insights():
    """Show actionable insights"""
    insights = analytics.get_insights()
    
    if not insights:
        console.print("[green]✓ Everything looks good! Keep up the great work.[/green]")
        return
    
    console.print("\n[bold cyan]💡 Insights & Recommendations[/bold cyan]\n")
    for insight in insights:
        console.print(f"  {insight}\n")


# DASHBOARD COMMAND

@app.command("dashboard")
def show_dashboard():
    """Show complete dashboard with all information"""
    console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]       PRODUCTIVITY DASHBOARD         [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
    
    # Quick stats
    task_summary = analytics.generate_task_summary(7)
    expense_summary = analytics.generate_expense_summary(7)
    upcoming = notifier.get_upcoming_deadlines(3)
    
    console.print(f"[bold]📊 Quick Stats (Last 7 Days)[/bold]")
    console.print(f"  Tasks: {task_summary['completed']}/{task_summary['total']} completed ({task_summary['completion_rate']}%)")
    console.print(f"  Expenses: ${expense_summary['total_amount']:.2f} across {expense_summary['total_transactions']} transactions")
    console.print(f"  Upcoming: {len(upcoming)} deadline(s) in next 3 days\n")
    
    # Recent tasks
    recent_tasks = taskboard.list_tasks()[:5]
    if recent_tasks:
        console.print("[bold]📝 Recent Tasks[/bold]")
        for task in recent_tasks[:5]:
            status_icon = {"Todo": "○", "Doing": "⟳", "Done": "✓"}.get(task['status'], "○")
            console.print(f"  {status_icon} {task['title'][:50]} [{task['priority']}]")
        console.print()
    
    # Insights
    insights = analytics.get_insights()
    if insights:
        console.print("[bold]💡 Today's Insights[/bold]")
        for insight in insights[:3]:
            console.print(f"  • {insight}")
        console.print()


# MAIN ENTRY POINT

if __name__ == "__main__":
    app()
