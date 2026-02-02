"""
Analytics Engine Module
Generate insights and reports from task and expense data
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..utils.storage import DataStore
from ..utils.config import TASKS_FILE, EXPENSES_FILE, WEEKLY_DAYS, MONTHLY_DAYS


class AnalyticsEngine:
    """Generate analytics and insights"""
    
    def __init__(self):
        self.task_store = DataStore(TASKS_FILE)
        self.expense_store = DataStore(EXPENSES_FILE)
        self.console = Console()
    
    def generate_task_summary(self, period_days: int = WEEKLY_DAYS) -> Dict[str, Any]:
        """
        Generate task completion summary
        
        Args:
            period_days: Number of days to analyze
        
        Returns:
            Dictionary with task statistics
        """
        tasks = self.task_store.load()
        
        if not tasks:
            return {
                "total": 0,
                "completed": 0,
                "in_progress": 0,
                "todo": 0,
                "completion_rate": 0,
                "high_priority": 0,
                "overdue": 0
            }
        
        # Filter tasks within period
        cutoff_date = datetime.now() - timedelta(days=period_days)
        recent_tasks = [
            t for t in tasks
            if datetime.fromisoformat(t["created_at"]) >= cutoff_date
        ]
        
        # Calculate statistics
        total = len(tasks)
        completed = len([t for t in tasks if t["status"] == "Done"])
        in_progress = len([t for t in tasks if t["status"] == "Doing"])
        todo = len([t for t in tasks if t["status"] == "Todo"])
        high_priority = len([t for t in tasks if t["priority"] == "High"])
        
        # Calculate overdue tasks
        today = datetime.now().date()
        overdue = 0
        for task in tasks:
            if task["status"] != "Done" and task.get("deadline"):
                try:
                    deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                    if deadline < today:
                        overdue += 1
                except ValueError:
                    continue
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "todo": todo,
            "completion_rate": round(completion_rate, 1),
            "high_priority": high_priority,
            "overdue": overdue,
            "recent_tasks": len(recent_tasks)
        }
    
    def generate_expense_summary(self, period_days: int = WEEKLY_DAYS) -> Dict[str, Any]:
        """
        Generate expense summary
        
        Args:
            period_days: Number of days to analyze
        
        Returns:
            Dictionary with expense statistics
        """
        expenses = self.expense_store.load()
        
        if not expenses:
            return {
                "total_amount": 0,
                "total_transactions": 0,
                "by_category": {},
                "average_expense": 0,
                "largest_expense": 0
            }
        
        # Filter expenses within period
        cutoff_date = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
        recent_expenses = [
            e for e in expenses
            if e["date"] >= cutoff_date
        ]
        
        if not recent_expenses:
            return {
                "total_amount": 0,
                "total_transactions": 0,
                "by_category": {},
                "average_expense": 0,
                "largest_expense": 0
            }
        
        # Calculate statistics
        total_amount = sum(e["amount"] for e in recent_expenses)
        total_transactions = len(recent_expenses)
        
        # Category breakdown
        by_category = {}
        for expense in recent_expenses:
            category = expense["category"]
            by_category[category] = by_category.get(category, 0) + expense["amount"]
        
        # Sort categories by amount
        by_category = dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True))
        
        average_expense = total_amount / total_transactions if total_transactions > 0 else 0
        largest_expense = max((e["amount"] for e in recent_expenses), default=0)
        
        return {
            "total_amount": round(total_amount, 2),
            "total_transactions": total_transactions,
            "by_category": {k: round(v, 2) for k, v in by_category.items()},
            "average_expense": round(average_expense, 2),
            "largest_expense": round(largest_expense, 2)
        }
    
    def display_weekly_report(self):
        """Display a comprehensive weekly report"""
        self.console.print("\n[bold cyan]📊 WEEKLY REPORT[/bold cyan]\n")
        
        # Task summary
        task_summary = self.generate_task_summary(WEEKLY_DAYS)
        
        task_info = f"""
[bold]Tasks Overview (Last 7 Days)[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Tasks: {task_summary['total']}
New Tasks: {task_summary['recent_tasks']}
Completed: {task_summary['completed']} ✓
In Progress: {task_summary['in_progress']} ⟳
Todo: {task_summary['todo']} ○
Completion Rate: {task_summary['completion_rate']}%
High Priority: {task_summary['high_priority']}
Overdue: {task_summary['overdue']} {'⚠️' if task_summary['overdue'] > 0 else ''}
"""
        self.console.print(Panel(task_info.strip(), border_style="green"))
        
        # Expense summary
        expense_summary = self.generate_expense_summary(WEEKLY_DAYS)
        
        expense_info = f"""
[bold]Expense Overview (Last 7 Days)[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Spent: ${expense_summary['total_amount']:.2f}
Transactions: {expense_summary['total_transactions']}
Average: ${expense_summary['average_expense']:.2f}
Largest: ${expense_summary['largest_expense']:.2f}
"""
        
        if expense_summary['by_category']:
            expense_info += "\n[bold]By Category:[/bold]\n"
            for category, amount in expense_summary['by_category'].items():
                percentage = (amount / expense_summary['total_amount'] * 100) if expense_summary['total_amount'] > 0 else 0
                expense_info += f"  • {category}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        self.console.print(Panel(expense_info.strip(), border_style="yellow"))
    
    def display_monthly_report(self):
        """Display a comprehensive monthly report"""
        self.console.print("\n[bold magenta]📈 MONTHLY REPORT[/bold magenta]\n")
        
        # Task summary
        task_summary = self.generate_task_summary(MONTHLY_DAYS)
        
        task_info = f"""
[bold]Tasks Overview (Last 30 Days)[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Tasks: {task_summary['total']}
New Tasks: {task_summary['recent_tasks']}
Completed: {task_summary['completed']} ✓
In Progress: {task_summary['in_progress']} ⟳
Todo: {task_summary['todo']} ○
Completion Rate: {task_summary['completion_rate']}%
High Priority: {task_summary['high_priority']}
Overdue: {task_summary['overdue']} {'⚠️' if task_summary['overdue'] > 0 else ''}
"""
        self.console.print(Panel(task_info.strip(), border_style="green"))
        
        # Expense summary
        expense_summary = self.generate_expense_summary(MONTHLY_DAYS)
        
        expense_info = f"""
[bold]Expense Overview (Last 30 Days)[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Spent: ${expense_summary['total_amount']:.2f}
Transactions: {expense_summary['total_transactions']}
Average: ${expense_summary['average_expense']:.2f}
Largest: ${expense_summary['largest_expense']:.2f}
"""
        
        if expense_summary['by_category']:
            expense_info += "\n[bold]By Category:[/bold]\n"
            for category, amount in expense_summary['by_category'].items():
                percentage = (amount / expense_summary['total_amount'] * 100) if expense_summary['total_amount'] > 0 else 0
                expense_info += f"  • {category}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        self.console.print(Panel(expense_info.strip(), border_style="yellow"))
    
    def get_insights(self) -> List[str]:
        """Generate actionable insights based on data"""
        insights = []
        
        # Task insights
        task_summary = self.generate_task_summary(WEEKLY_DAYS)
        
        if task_summary['completion_rate'] >= 80:
            insights.append("🎉 Excellent work! Your task completion rate is over 80%!")
        elif task_summary['completion_rate'] < 50:
            insights.append("📌 Consider breaking down tasks into smaller chunks to improve completion rate.")
        
        if task_summary['overdue'] > 0:
            insights.append(f"⚠️  You have {task_summary['overdue']} overdue task(s). Prioritize these!")
        
        if task_summary['high_priority'] > 5:
            insights.append("🎯 You have many high-priority tasks. Focus on the most critical ones first.")
        
        # Expense insights
        expense_summary = self.generate_expense_summary(WEEKLY_DAYS)
        
        if expense_summary['total_amount'] > 0:
            # Find biggest spending category
            if expense_summary['by_category']:
                top_category = max(expense_summary['by_category'].items(), key=lambda x: x[1])
                percentage = (top_category[1] / expense_summary['total_amount']) * 100
                
                if percentage > 50:
                    insights.append(
                        f"💰 {percentage:.0f}% of your spending this week was on {top_category[0]}. "
                        f"Consider if this aligns with your budget goals."
                    )
        
        return insights
