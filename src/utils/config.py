"""
Configuration module for Productivity CLI
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Data file paths
TASKS_FILE = DATA_DIR / "tasks.json"
EXPENSES_FILE = DATA_DIR / "expenses.json"
REMINDERS_FILE = DATA_DIR / "reminders.json"

# Task priorities
PRIORITIES = ["High", "Medium", "Low"]

# Task statuses
STATUSES = ["Todo", "Doing", "Done"]

# Expense categories
EXPENSE_CATEGORIES = ["Food", "Rent", "Tech", "Transport", "Entertainment", "Healthcare", "Other"]

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Analytics settings
WEEKLY_DAYS = 7
MONTHLY_DAYS = 30
