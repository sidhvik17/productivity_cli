# Productivity CLI - Complete Project Overview

## 📋 Table of Contents
1. [Project Summary](#project-summary)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Core Components](#core-components)
5. [Installation & Usage](#installation--usage)
6. [Development Guide](#development-guide)
7. [Testing](#testing)
8. [Future Enhancements](#future-enhancements)

---

## Project Summary

**Productivity CLI** is a unified command-line interface that helps users manage their daily tasks, track financial spending, and receive automated reminders while providing insights through data visualization.

### Key Features
✅ **Task Management** - Full CRUD with priorities and status tracking  
✅ **Expense Tracker** - Categorized spending with analytics  
✅ **Smart Reminders** - Background deadline monitoring  
✅ **Analytics Engine** - Weekly/monthly reports with insights  
✅ **Beautiful Terminal UI** - Rich formatting with colors and tables  

### Target Users
- **Power Users**: Developers who live in the terminal
- **Minimalists**: Users wanting distraction-free productivity
- **Data Enthusiasts**: People who love insights and metrics

---

## Architecture

### Design Philosophy
The project follows **Object-Oriented Programming** principles with a modular architecture. Each feature is encapsulated in its own class, managed by a central CLI interface.

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Typer CLI + Rich Terminal)                 │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼──────┐           ┌────────▼────────┐
│  Core Logic  │           │  Data Storage   │
│              │           │                 │
│ • TaskBoard  │◄─────────►│  JSON Files     │
│ • Ledger     │           │                 │
│ • Notifier   │           │ • tasks.json    │
│ • Analytics  │           │ • expenses.json │
└──────────────┘           └─────────────────┘
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Interface** | Typer 0.9.0 | CLI framework with auto-completion |
| **Display** | Rich 13.7.0 | Terminal styling, tables, colors |
| **Data Analysis** | Pandas 2.1.4 | DataFrame operations, analytics |
| **Scheduling** | Schedule 1.2.1 | Background task scheduling |
| **Storage** | JSON | Lightweight, human-readable persistence |
| **Language** | Python 3.8+ | Core implementation |

---

## File Structure

```
productivity-cli/
├── main.py                      # CLI entry point (Typer app)
├── setup.py                     # Installation and demo script
├── requirements.txt             # Python dependencies
├── README.md                    # Full documentation
├── QUICKSTART.md               # Quick reference guide
├── DEMO.py                     # Interactive demonstration
├── .gitignore                  # Git ignore rules
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── core/                   # Core business logic
│   │   ├── __init__.py
│   │   ├── taskboard.py       # Task management (TaskBoard class)
│   │   ├── ledger.py          # Expense tracking (Ledger class)
│   │   ├── notifier.py        # Reminders (Notifier class)
│   │   └── analytics.py       # Analytics (AnalyticsEngine class)
│   │
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       ├── config.py          # Configuration constants
│       └── storage.py         # Data storage helpers (DataStore class)
│
├── data/                       # Data files (created at runtime)
│   ├── tasks.json             # Task data
│   ├── expenses.json          # Expense data
│   └── reminders.json         # Reminder data
│
└── tests/                     # Unit tests
    └── test_taskboard.py      # TaskBoard tests
```

---

## Core Components

### 1. TaskBoard (`src/core/taskboard.py`)

**Purpose**: Manage tasks with CRUD operations

**Key Methods**:
- `add_task()` - Create new task with priority/deadline
- `list_tasks()` - List/filter tasks by status/priority
- `update_task_status()` - Change task status (Todo/Doing/Done)
- `update_task()` - Modify task details
- `delete_task()` - Remove task
- `display_tasks()` - Rich table visualization
- `get_completion_rate()` - Calculate completion percentage

**Data Model**:
```python
{
    "id": "unique_timestamp_id",
    "title": "Task title",
    "description": "Optional description",
    "priority": "High|Medium|Low",
    "status": "Todo|Doing|Done",
    "deadline": "YYYY-MM-DD or null",
    "created_at": "ISO timestamp",
    "updated_at": "ISO timestamp"
}
```

### 2. Ledger (`src/core/ledger.py`)

**Purpose**: Track and analyze expenses

**Key Methods**:
- `add_expense()` - Log new expense
- `list_expenses()` - List/filter expenses by category/date
- `delete_expense()` - Remove expense
- `get_total()` - Calculate totals with filters
- `get_category_breakdown()` - Spending by category
- `display_expenses()` - Rich table visualization

**Data Model**:
```python
{
    "id": "unique_timestamp_id",
    "amount": 123.45,
    "category": "Food|Rent|Tech|Transport|Entertainment|Healthcare|Other",
    "description": "Optional description",
    "date": "YYYY-MM-DD",
    "created_at": "ISO timestamp"
}
```

### 3. Notifier (`src/core/notifier.py`)

**Purpose**: Background deadline monitoring

**Key Methods**:
- `start()` - Start background service (threaded)
- `stop()` - Stop background service
- `get_upcoming_deadlines()` - Get tasks due soon
- `check_now()` - Manual deadline check

**Features**:
- Runs in separate thread (non-blocking)
- Checks every 60 seconds
- Alerts for: today, tomorrow, 3-day window, overdue

### 4. AnalyticsEngine (`src/core/analytics.py`)

**Purpose**: Generate insights and reports

**Key Methods**:
- `generate_task_summary()` - Task statistics for period
- `generate_expense_summary()` - Expense stats for period
- `display_weekly_report()` - 7-day comprehensive report
- `display_monthly_report()` - 30-day comprehensive report
- `get_insights()` - Actionable recommendations

**Insights Generated**:
- Task completion trends
- Spending patterns
- Priority distribution
- Overdue task alerts
- Budget recommendations

### 5. DataStore (`src/utils/storage.py`)

**Purpose**: Abstract JSON file operations

**Key Methods**:
- `load()` - Read JSON file
- `save()` - Write JSON file
- `append()` - Add new item
- `update()` - Modify items by condition
- `delete()` - Remove items by condition

**Features**:
- Automatic file creation
- Error handling
- Atomic operations

---

## Installation & Usage

### Quick Start (3 steps)

```bash
# 1. Navigate to project
cd productivity-cli

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start using!
python main.py dashboard
```

### Essential Commands

```bash
# Task Management
python main.py task add "Task title" -p High -d 2026-02-15
python main.py task list
python main.py task update <id> -s Done

# Expense Tracking
python main.py expense add 50.00 Food -d "Description"
python main.py expense list
python main.py expense breakdown

# Analytics
python main.py dashboard
python main.py analytics weekly
python main.py reminder check
```

### Get Help
```bash
python main.py --help                 # Main help
python main.py task --help            # Task commands
python main.py expense --help         # Expense commands
python main.py analytics --help       # Analytics commands
python main.py reminder --help        # Reminder commands
```

---

## Development Guide

### Adding a New Feature

1. **Create Core Module** (`src/core/newfeature.py`)
```python
from ..utils.storage import DataStore, generate_id
from ..utils.config import NEW_FEATURE_FILE

class NewFeature:
    def __init__(self):
        self.store = DataStore(NEW_FEATURE_FILE)
    
    def add_item(self, data):
        item = {"id": generate_id(), **data}
        self.store.append(item)
        return item
```

2. **Update Config** (`src/utils/config.py`)
```python
NEW_FEATURE_FILE = DATA_DIR / "newfeature.json"
```

3. **Add CLI Commands** (`main.py`)
```python
feature_app = typer.Typer(help="New feature")
app.add_typer(feature_app, name="feature")

@feature_app.command("add")
def add_feature_item(...):
    # Implementation
```

4. **Write Tests** (`tests/test_newfeature.py`)
```python
import unittest
from src.core.newfeature import NewFeature

class TestNewFeature(unittest.TestCase):
    def test_add_item(self):
        # Test implementation
```

### Code Style Guidelines

- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Documentation**: Docstrings for all public methods
- **Type Hints**: Use where beneficial for clarity
- **Error Handling**: Validate inputs, raise ValueError for bad data
- **Console Output**: Use Rich library for formatting

---

## Testing

### Run Unit Tests
```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_taskboard

# Run with verbose output
python -m unittest discover tests -v
```

### Test Coverage
Current test coverage includes:
- ✅ TaskBoard CRUD operations
- ✅ Status validation
- ✅ Priority validation
- ✅ Completion rate calculation
- ⏳ Ledger operations (to be added)
- ⏳ Analytics calculations (to be added)

### Manual Testing Checklist
- [ ] Add task with all fields
- [ ] List tasks with filters
- [ ] Update task status
- [ ] Delete task
- [ ] Add expense with category
- [ ] View expense breakdown
- [ ] Check reminders
- [ ] Generate weekly report
- [ ] View dashboard

---

## Future Enhancements

### Phase 1 - Core Improvements
- [ ] Recurring tasks and expenses
- [ ] Task dependencies
- [ ] Subtasks support
- [ ] Search functionality
- [ ] Undo/redo operations

### Phase 2 - Data & Analytics
- [ ] Export to CSV/PDF
- [ ] Data visualization charts (matplotlib)
- [ ] Budget tracking and alerts
- [ ] Trends and predictions
- [ ] Custom report templates

### Phase 3 - Integration
- [ ] Calendar integration (Google Calendar)
- [ ] Cloud sync (Dropbox, Drive)
- [ ] API for external tools
- [ ] Webhook notifications
- [ ] Email reports

### Phase 4 - UX Enhancements
- [ ] Interactive TUI mode (textual)
- [ ] Natural language input
- [ ] Voice commands
- [ ] Mobile companion app
- [ ] Desktop notifications

### Phase 5 - Advanced Features
- [ ] Multi-user support
- [ ] Team collaboration
- [ ] Time tracking
- [ ] Pomodoro timer
- [ ] Habit tracker
- [ ] Goal setting & tracking

---

## Contributing

This project follows standard Python development practices:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

---

## License

This project is open source and available for personal use.

---

## Support

For issues or questions:
1. Check the README.md and QUICKSTART.md
2. Review the DEMO.py for examples
3. Use `--help` on any command
4. Check test files for usage examples

---

**Built with ❤️ for productivity enthusiasts**

*Last Updated: February 1, 2026*
