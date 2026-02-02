"""
Unit tests for TaskBoard
"""
import unittest
import os
import json
from pathlib import Path
from datetime import datetime

from src.core.taskboard import TaskBoard
from src.utils.config import TASKS_FILE


class TestTaskBoard(unittest.TestCase):
    """Test TaskBoard functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use a test file
        self.test_file = Path("/tmp/test_tasks.json")
        # Backup original file path
        self.original_file = TASKS_FILE
        # Replace with test file
        import src.utils.config as config
        config.TASKS_FILE = self.test_file
        
        # Create fresh taskboard
        self.taskboard = TaskBoard()
        
        # Clear test file
        if self.test_file.exists():
            self.test_file.unlink()
    
    def tearDown(self):
        """Clean up after tests"""
        # Restore original file path
        import src.utils.config as config
        config.TASKS_FILE = self.original_file
        
        # Remove test file
        if self.test_file.exists():
            self.test_file.unlink()
    
    def test_add_task(self):
        """Test adding a task"""
        task = self.taskboard.add_task(
            title="Test Task",
            priority="High",
            description="Test description"
        )
        
        self.assertEqual(task["title"], "Test Task")
        self.assertEqual(task["priority"], "High")
        self.assertEqual(task["status"], "Todo")
        self.assertIsNotNone(task["id"])
    
    def test_add_task_invalid_priority(self):
        """Test adding task with invalid priority"""
        with self.assertRaises(ValueError):
            self.taskboard.add_task("Test", priority="Invalid")
    
    def test_list_tasks(self):
        """Test listing tasks"""
        # Add some tasks
        self.taskboard.add_task("Task 1", priority="High")
        self.taskboard.add_task("Task 2", priority="Low")
        
        # List all tasks
        tasks = self.taskboard.list_tasks()
        self.assertEqual(len(tasks), 2)
        
        # Filter by priority
        high_tasks = self.taskboard.list_tasks(priority="High")
        self.assertEqual(len(high_tasks), 1)
        self.assertEqual(high_tasks[0]["title"], "Task 1")
    
    def test_update_task_status(self):
        """Test updating task status"""
        task = self.taskboard.add_task("Test Task")
        
        # Update to Doing
        result = self.taskboard.update_task_status(task["id"], "Doing")
        self.assertTrue(result)
        
        # Verify update
        updated_task = self.taskboard.get_task_by_id(task["id"])
        self.assertEqual(updated_task["status"], "Doing")
    
    def test_update_task_invalid_status(self):
        """Test updating with invalid status"""
        task = self.taskboard.add_task("Test Task")
        
        with self.assertRaises(ValueError):
            self.taskboard.update_task_status(task["id"], "Invalid")
    
    def test_delete_task(self):
        """Test deleting a task"""
        task = self.taskboard.add_task("Test Task")
        
        # Delete task
        result = self.taskboard.delete_task(task["id"])
        self.assertTrue(result)
        
        # Verify deletion
        tasks = self.taskboard.list_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_completion_rate(self):
        """Test completion rate calculation"""
        # Add tasks
        task1 = self.taskboard.add_task("Task 1")
        task2 = self.taskboard.add_task("Task 2")
        
        # Mark one as complete
        self.taskboard.update_task_status(task1["id"], "Done")
        
        # Check completion rate
        rate = self.taskboard.get_completion_rate()
        self.assertEqual(rate, 50.0)


if __name__ == '__main__':
    unittest.main()
