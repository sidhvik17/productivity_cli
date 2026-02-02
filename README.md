# 🚀 Productivity CLI

A unified command-line interface for managing daily tasks, tracking expenses, and receiving automated reminders with powerful analytics.

## ✨ Features

- **Task Management**: Create, update, and track tasks with priorities and deadlines
- **Expense Tracker**: Log and categorize expenses with detailed breakdowns
- **Smart Reminders**: Background alerts for upcoming deadlines
- **Analytics Dashboard**: Weekly/monthly reports with actionable insights
- **Beautiful UI**: Rich terminal formatting with colors, tables, and progress indicators

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. Clone or download the project:
```bash
cd productivity-cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the main script executable (optional):
```bash
chmod +x main.py
```

## 🎯 Quick Start

### Running the CLI

```bash
python main.py --help
```

Or if you made it executable:
```bash
./main.py --help
```

### Your First Commands

```bash
# Add a task
python main.py task add "Complete project proposal" -p High -d 2026-02-15

# List all tasks
python main.py task list

# Add an expense
python main.py expense add 50.00 Food -d "Dinner at restaurant"

# View dashboard
python main.py dashboard

# Check weekly analytics
python main.py analytics weekly
```

## 📚 Complete Command Reference

### Task Management

#### Add a task
```bash
python main.py task add "Task title" [OPTIONS]

Options:
  -p, --priority TEXT      Task priority (High/Medium/Low) [default: Medium]
  -d, --deadline TEXT      Deadline (YYYY-MM-DD)
  -desc, --description TEXT Task description
```

**Examples:**
```bash
# Simple task
python main.py task add "Review pull requests"

# Task with priority and deadline
python main.py task add "Launch marketing campaign" -p High -d 2026-02-10

# Task with full details
python main.py task add "Write documentation" -p Medium -d 2026-02-20 -desc "API docs for v2.0"
```

#### List tasks
```bash
python main.py task list [OPTIONS]

Options:
  -s, --status TEXT    Filter by status (Todo/Doing/Done)
  -p, --priority TEXT  Filter by priority (High/Medium/Low)
```

**Examples:**
```bash
# All tasks
python main.py task list

# Only high-priority tasks
python main.py task list -p High

# Only completed tasks
python main.py task list -s Done
```

#### Update task status
```bash
python main.py task update TASK_ID -s STATUS

Arguments:
  TASK_ID  Task ID (can use last 6 characters)
  
Options:
  -s, --status TEXT  New status (Todo/Doing/Done) [required]
```

**Examples:**
```bash
# Start working on a task
python main.py task update abc123 -s Doing

# Mark task as complete
python main.py task update abc123 -s Done
```

#### Edit task details
```bash
python main.py task edit TASK_ID [OPTIONS]

Options:
  -t, --title TEXT         New title
  -p, --priority TEXT      New priority
  -d, --deadline TEXT      New deadline
  -desc, --description TEXT New description
```

**Examples:**
```bash
# Change priority
python main.py task edit abc123 -p High

# Update deadline
python main.py task edit abc123 -d 2026-03-01

# Change multiple fields
python main.py task edit abc123 -t "Updated title" -p Medium
```

#### Delete a task
```bash
python main.py task delete TASK_ID [OPTIONS]

Options:
  -y, --yes  Skip confirmation
```

**Examples:**
```bash
# Delete with confirmation
python main.py task delete abc123

# Delete without confirmation
python main.py task delete abc123 -y
```

### Expense Tracking

#### Add an expense
```bash
python main.py expense add AMOUNT CATEGORY [OPTIONS]

Arguments:
  AMOUNT    Expense amount (e.g., 50.00)
  CATEGORY  Category (Food/Rent/Tech/Transport/Entertainment/Healthcare/Other)

Options:
  -d, --description TEXT  Expense description
  --date TEXT            Date (YYYY-MM-DD, defaults to today)
```

**Examples:**
```bash
# Simple expense
python main.py expense add 25.50 Food

# Expense with description
python main.py expense add 1200.00 Rent -d "Monthly rent payment"

# Expense with custom date
python main.py expense add 89.99 Tech --date 2026-01-28 -d "Wireless mouse"
```

#### List expenses
```bash
python main.py expense list [OPTIONS]

Options:
  -c, --category TEXT  Filter by category
  -s, --start TEXT     Start date (YYYY-MM-DD)
  -e, --end TEXT       End date (YYYY-MM-DD)
```

**Examples:**
```bash
# All expenses
python main.py expense list

# Food expenses only
python main.py expense list -c Food

# Expenses in January 2026
python main.py expense list -s 2026-01-01 -e 2026-01-31
```

#### Calculate total expenses
```bash
python main.py expense total [OPTIONS]

Options:
  -c, --category TEXT  Filter by category
  -s, --start TEXT     Start date (YYYY-MM-DD)
  -e, --end TEXT       End date (YYYY-MM-DD)
```

**Examples:**
```bash
# Total all expenses
python main.py expense total

# Total food expenses
python main.py expense total -c Food

# Total for date range
python main.py expense total -s 2026-01-01 -e 2026-01-31
```

#### Show spending breakdown
```bash
python main.py expense breakdown [OPTIONS]

Options:
  -s, --start TEXT  Start date (YYYY-MM-DD)
  -e, --end TEXT    End date (YYYY-MM-DD)
```

**Examples:**
```bash
# All-time breakdown
python main.py expense breakdown

# This month's breakdown
python main.py expense breakdown -s 2026-02-01
```

#### Delete an expense
```bash
python main.py expense delete EXPENSE_ID [OPTIONS]

Options:
  -y, --yes  Skip confirmation
```

### Reminders

#### Check upcoming deadlines
```bash
python main.py reminder check
```

Shows all tasks with deadlines in the next 7 days.

#### Start reminder service
```bash
python main.py reminder start
```

Starts a background service that monitors deadlines and sends alerts. Press Ctrl+C to stop.

### Analytics

#### Weekly report
```bash
python main.py analytics weekly
```

Shows comprehensive analytics for the last 7 days including:
- Task completion rates
- Expense totals and breakdowns
- Actionable insights

#### Monthly report
```bash
python main.py analytics monthly
```

Shows comprehensive analytics for the last 30 days.

#### Get insights
```bash
python main.py analytics insights
```

Displays actionable recommendations based on your data.

### Dashboard

#### Show complete dashboard
```bash
python main.py dashboard
```

Displays a unified view with:
- Quick stats (7-day summary)
- Recent tasks
- Today's insights

## 🗂️ Project Structure

```
productivity-cli/
├── main.py                 # Main CLI application
├── requirements.txt        # Python dependencies
├── data/                   # Data storage (JSON files)
│   ├── tasks.json
│   ├── expenses.json
│   └── reminders.json
├── src/
│   ├── core/              # Core business logic
│   │   ├── taskboard.py   # Task management
│   │   ├── ledger.py      # Expense tracking
│   │   ├── notifier.py    # Reminder system
│   │   └── analytics.py   # Analytics engine
│   └── utils/             # Utilities
│       ├── config.py      # Configuration
│       └── storage.py     # Data storage helpers
└── tests/                 # Unit tests
```

## 🎨 Design Principles

### Modular Architecture
Each feature is implemented as a separate class:
- `TaskBoard`: Task CRUD operations
- `Ledger`: Expense management
- `Notifier`: Background reminder service
- `AnalyticsEngine`: Data analysis and reporting

### Data Storage
- JSON files for human-readable, version-control-friendly storage
- Pandas DataFrames for efficient analytics
- Simple file-based approach (no database required)

### User Experience
- Rich terminal formatting with colors and tables
- Intuitive command structure
- Helpful error messages
- Confirmation prompts for destructive actions

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.8+ | Core implementation |
| CLI Framework | Typer | Command-line interface |
| Data Processing | Pandas | Analytics and reporting |
| Storage | JSON | Lightweight data persistence |
| UI/Styling | Rich | Terminal formatting |
| Threading | Python stdlib | Background reminders |

## 📊 Data Format

### Tasks (tasks.json)
```json
{
  "id": "20260201123456789012",
  "title": "Complete project proposal",
  "description": "Write Q1 proposal",
  "priority": "High",
  "status": "Todo",
  "deadline": "2026-02-15",
  "created_at": "2026-02-01T12:34:56.789012",
  "updated_at": "2026-02-01T12:34:56.789012"
}
```

### Expenses (expenses.json)
```json
{
  "id": "20260201123456789012",
  "amount": 50.00,
  "category": "Food",
  "description": "Dinner at restaurant",
  "date": "2026-02-01",
  "created_at": "2026-02-01T12:34:56.789012"
}
```

## 🔧 Customization

### Modifying Categories
Edit `src/utils/config.py`:
```python
EXPENSE_CATEGORIES = ["Food", "Rent", "Tech", "YourCategory"]
```

### Changing Check Intervals
Edit `src/core/notifier.py`:
```python
self.check_interval = 60  # Check every 60 seconds
```

### Adjusting Report Periods
Edit `src/utils/config.py`:
```python
WEEKLY_DAYS = 7
MONTHLY_DAYS = 30
```

## 💡 Usage Tips

1. **Short Task IDs**: You can use the last 6 characters of any ID for quicker typing
2. **Date Formats**: Always use YYYY-MM-DD format for dates
3. **Background Service**: Run reminder service in a separate terminal or use tmux/screen
4. **Data Backup**: The `data/` folder contains all your information - back it up regularly!
5. **Git Integration**: JSON files work great with version control

## 🚀 Advanced Workflows

### Morning Routine
```bash
# Check your dashboard
python main.py dashboard

# Review upcoming deadlines
python main.py reminder check

# Check insights
python main.py analytics insights
```

### Weekly Review
```bash
# Generate weekly report
python main.py analytics weekly

# Review all high-priority tasks
python main.py task list -p High

# Check spending breakdown
python main.py expense breakdown -s 2026-01-25
```

### End of Month
```bash
# Monthly analytics
python main.py analytics monthly

# Archive completed tasks (manual JSON edit)
# Review expense totals
python main.py expense total -s 2026-01-01 -e 2026-01-31
```

## 🐛 Troubleshooting

### Commands not found
Make sure you're in the project directory and Python is in your PATH.

### Permission denied
Make the script executable: `chmod +x main.py`

### Dependencies missing
Install requirements: `pip install -r requirements.txt`

### Data not persisting
Check that the `data/` directory exists and is writable.

## 🤝 Contributing

This is a personal productivity tool, but feel free to fork and customize for your needs!

## 📝 License

This project is open source and available for personal use.

## 🎯 Future Enhancements

Potential features for future development:
- [ ] Export reports to PDF/CSV
- [ ] Recurring tasks and expenses
- [ ] Budget tracking and alerts
- [ ] Data visualization charts
- [ ] Cloud sync capability
- [ ] Mobile companion app
- [ ] Natural language input
- [ ] Time tracking integration

---

**Built with ❤️ for terminal enthusiasts and productivity nerds**
