"""
Task Management Module
Handles CRUD operations for tasks with priorities and status tracking
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
import pandas as pd
from rich.console import Console
from rich.table import Table

from ..utils.storage import DataStore, generate_id
from ..utils.config import TASKS_FILE, PRIORITIES, STATUSES


class TaskBoard:
    """Manage tasks with CRUD operations"""
    
    def __init__(self):
        self.store = DataStore(TASKS_FILE)
        self.console = Console()
    
    def add_task(
        self, 
        title: str, 
        priority: str = "Medium", 
        deadline: Optional[str] = None,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Add a new task
        
        Args:
            title: Task title
            priority: Task priority (High, Medium, Low)
            deadline: Optional deadline in YYYY-MM-DD format
            description: Optional task description
        
        Returns:
            Created task dictionary
        """
        if priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(PRIORITIES)}")
        
        task = {
            "id": generate_id(),
            "title": title,
            "description": description,
            "priority": priority,
            "status": "Todo",
            "deadline": deadline,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.store.append(task)
        return task
    
    def list_tasks(
        self, 
        status: Optional[str] = None, 
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List tasks with optional filtering
        
        Args:
            status: Filter by status
            priority: Filter by priority
        
        Returns:
            List of tasks matching filters
        """
        tasks = self.store.load()
        
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]
        
        return tasks
    
    def update_task_status(self, task_id: str, new_status: str) -> bool:
        """
        Update task status
        
        Args:
            task_id: Task ID
            new_status: New status (Todo, Doing, Done)
        
        Returns:
            True if updated successfully
        """
        if new_status not in STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(STATUSES)}")
        
        return self.store.update(
            condition=lambda t: t["id"] == task_id,
            updates={"status": new_status, "updated_at": datetime.now().isoformat()}
        )
    
    def update_task(
        self, 
        task_id: str, 
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        deadline: Optional[str] = None
    ) -> bool:
        """Update task fields"""
        updates = {"updated_at": datetime.now().isoformat()}
        
        if title:
            updates["title"] = title
        if description is not None:
            updates["description"] = description
        if priority:
            if priority not in PRIORITIES:
                raise ValueError(f"Priority must be one of: {', '.join(PRIORITIES)}")
            updates["priority"] = priority
        if deadline is not None:
            updates["deadline"] = deadline
        
        return self.store.update(
            condition=lambda t: t["id"] == task_id,
            updates=updates
        )
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID"""
        return self.store.delete(condition=lambda t: t["id"] == task_id)
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID"""
        tasks = self.store.load()
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def display_tasks(self, tasks: Optional[List[Dict[str, Any]]] = None):
        """Display tasks in a formatted table"""
        if tasks is None:
            tasks = self.list_tasks()
        
        if not tasks:
            self.console.print("[yellow]No tasks found.[/yellow]")
            return
        
        table = Table(title="Task Board", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Title", style="cyan")
        table.add_column("Priority", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Deadline", justify="center")
        
        for task in tasks:
            # Color code priority
            priority_color = {
                "High": "[red]High[/red]",
                "Medium": "[yellow]Medium[/yellow]",
                "Low": "[green]Low[/green]"
            }.get(task["priority"], task["priority"])
            
            # Color code status
            status_color = {
                "Todo": "[red]Todo[/red]",
                "Doing": "[yellow]Doing[/yellow]",
                "Done": "[green]Done[/green]"
            }.get(task["status"], task["status"])
            
            table.add_row(
                task["id"][-6:],  # Show last 6 chars of ID
                task["title"][:50],  # Truncate long titles
                priority_color,
                status_color,
                task.get("deadline", "N/A")
            )
        
        self.console.print(table)
    
    def get_completion_rate(self) -> float:
        """Calculate task completion rate"""
        tasks = self.store.load()
        if not tasks:
            return 0.0
        
        completed = len([t for t in tasks if t["status"] == "Done"])
        return (completed / len(tasks)) * 100
