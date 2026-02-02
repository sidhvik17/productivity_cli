"""
Expense Tracking Module
Handles logging and tracking of expenses with categories
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
import pandas as pd
from rich.console import Console
from rich.table import Table

from ..utils.storage import DataStore, generate_id
from ..utils.config import EXPENSES_FILE, EXPENSE_CATEGORIES


class Ledger:
    """Manage financial expenses"""
    
    def __init__(self):
        self.store = DataStore(EXPENSES_FILE)
        self.console = Console()
    
    def add_expense(
        self,
        amount: float,
        category: str,
        description: str = "",
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a new expense
        
        Args:
            amount: Expense amount
            category: Expense category
            description: Optional description
            date: Optional date in YYYY-MM-DD format (defaults to today)
        
        Returns:
            Created expense dictionary
        """
        if category not in EXPENSE_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(EXPENSE_CATEGORIES)}")
        
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        expense = {
            "id": generate_id(),
            "amount": float(amount),
            "category": category,
            "description": description,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat()
        }
        
        self.store.append(expense)
        return expense
    
    def list_expenses(
        self,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List expenses with optional filtering
        
        Args:
            category: Filter by category
            start_date: Filter expenses after this date
            end_date: Filter expenses before this date
        
        Returns:
            List of expenses matching filters
        """
        expenses = self.store.load()
        
        if category:
            expenses = [e for e in expenses if e["category"] == category]
        
        if start_date:
            expenses = [e for e in expenses if e["date"] >= start_date]
        
        if end_date:
            expenses = [e for e in expenses if e["date"] <= end_date]
        
        return expenses
    
    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense by ID"""
        return self.store.delete(condition=lambda e: e["id"] == expense_id)
    
    def get_total(
        self,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> float:
        """
        Calculate total expenses
        
        Args:
            category: Filter by category
            start_date: Filter expenses after this date
            end_date: Filter expenses before this date
        
        Returns:
            Total amount
        """
        expenses = self.list_expenses(category, start_date, end_date)
        return sum(e["amount"] for e in expenses)
    
    def get_category_breakdown(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Get spending breakdown by category
        
        Returns:
            Dictionary mapping category to total amount
        """
        expenses = self.list_expenses(start_date=start_date, end_date=end_date)
        
        breakdown = {}
        for expense in expenses:
            category = expense["category"]
            breakdown[category] = breakdown.get(category, 0) + expense["amount"]
        
        return breakdown
    
    def display_expenses(self, expenses: Optional[List[Dict[str, Any]]] = None):
        """Display expenses in a formatted table"""
        if expenses is None:
            expenses = self.list_expenses()
        
        if not expenses:
            self.console.print("[yellow]No expenses found.[/yellow]")
            return
        
        # Sort by date, most recent first
        expenses = sorted(expenses, key=lambda x: x["date"], reverse=True)
        
        table = Table(title="Expense Ledger", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Date", style="cyan")
        table.add_column("Category", justify="center")
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Description")
        
        for expense in expenses[:50]:  # Show last 50 expenses
            table.add_row(
                expense["id"][-6:],
                expense["date"],
                expense["category"],
                f"${expense['amount']:.2f}",
                expense["description"][:40]  # Truncate long descriptions
            )
        
        self.console.print(table)
        
        # Show total
        total = sum(e["amount"] for e in expenses)
        self.console.print(f"\n[bold]Total: [green]${total:.2f}[/green][/bold]")
