"""
Reminder System Module
Background alerts for upcoming deadlines
"""
import threading
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from rich.console import Console

from ..utils.storage import DataStore
from ..utils.config import TASKS_FILE


class Notifier:
    """Background reminder system for task deadlines"""
    
    def __init__(self):
        self.store = DataStore(TASKS_FILE)
        self.console = Console()
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.check_interval = 60  # Check every 60 seconds
    
    def start(self):
        """Start the background reminder service"""
        if self.running:
            self.console.print("[yellow]Notifier is already running.[/yellow]")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        self.console.print("[green]Reminder service started.[/green]")
    
    def stop(self):
        """Stop the background reminder service"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        self.console.print("[yellow]Reminder service stopped.[/yellow]")
    
    def _run(self):
        """Main loop for checking deadlines"""
        while self.running:
            self._check_deadlines()
            time.sleep(self.check_interval)
    
    def _check_deadlines(self):
        """Check for upcoming deadlines and send notifications"""
        tasks = self.store.load()
        today = datetime.now().date()
        
        for task in tasks:
            # Skip completed tasks
            if task["status"] == "Done":
                continue
            
            # Check if task has a deadline
            if not task.get("deadline"):
                continue
            
            try:
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                days_until = (deadline - today).days
                
                # Notify for tasks due today or overdue
                if days_until == 0:
                    self._send_notification(
                        task,
                        f"⚠️  Task '{task['title']}' is due TODAY!"
                    )
                elif days_until < 0:
                    self._send_notification(
                        task,
                        f"🚨 Task '{task['title']}' is OVERDUE by {abs(days_until)} day(s)!"
                    )
                elif days_until == 1:
                    self._send_notification(
                        task,
                        f"📅 Task '{task['title']}' is due TOMORROW!"
                    )
                elif days_until <= 3:
                    self._send_notification(
                        task,
                        f"📌 Task '{task['title']}' is due in {days_until} days."
                    )
                    
            except ValueError:
                # Invalid date format
                continue
    
    def _send_notification(self, task: Dict[str, Any], message: str):
        """
        Send a notification to the console
        
        Args:
            task: Task dictionary
            message: Notification message
        """
        priority_color = {
            "High": "red",
            "Medium": "yellow",
            "Low": "green"
        }.get(task["priority"], "white")
        
        self.console.print(f"[{priority_color}]{message}[/{priority_color}]")
    
    def get_upcoming_deadlines(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get tasks with deadlines in the next N days
        
        Args:
            days: Number of days to look ahead
        
        Returns:
            List of tasks with upcoming deadlines
        """
        tasks = self.store.load()
        today = datetime.now().date()
        upcoming = []
        
        for task in tasks:
            if task["status"] == "Done":
                continue
            
            if not task.get("deadline"):
                continue
            
            try:
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                days_until = (deadline - today).days
                
                if 0 <= days_until <= days:
                    task_copy = task.copy()
                    task_copy["days_until"] = days_until
                    upcoming.append(task_copy)
                    
            except ValueError:
                continue
        
        # Sort by deadline (soonest first)
        upcoming.sort(key=lambda x: x["days_until"])
        return upcoming
    
    def check_now(self):
        """Manually trigger a deadline check"""
        self._check_deadlines()
