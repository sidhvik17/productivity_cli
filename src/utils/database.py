"""
SQLite Database Storage Module for Productivity CLI
Provides a SQL-based storage backend as an alternative to JSON storage
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import json

from .config import DATA_DIR


# Database file path
DATABASE_FILE = DATA_DIR / "productivity.db"


class SQLiteStore:
    """Handle reading and writing data using SQLite database"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.db_path = DATABASE_FILE
        self._ensure_database_exists()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory for dict-like access"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Todo',
                deadline TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Create expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id TEXT PRIMARY KEY,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT DEFAULT '',
                date TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Create reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id TEXT PRIMARY KEY,
                task_id TEXT,
                reminder_time TEXT NOT NULL,
                message TEXT DEFAULT '',
                is_active INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite Row to dictionary"""
        if row is None:
            return {}
        return dict(row)
    
    def load(self) -> List[Dict[str, Any]]:
        """Load all data from the table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name}')
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]
    
    def append(self, item: Dict[str, Any]):
        """Insert a new item into the table"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        columns = ', '.join(item.keys())
        placeholders = ', '.join(['?' for _ in item])
        values = tuple(item.values())
        
        cursor.execute(
            f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})',
            values
        )
        conn.commit()
        conn.close()
    
    def update(self, condition: Callable[[Dict], bool], updates: Dict[str, Any]) -> bool:
        """Update items matching a condition"""
        # Load all items and find matching ones
        items = self.load()
        updated = False
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        for item in items:
            if condition(item):
                set_clause = ', '.join([f'{key} = ?' for key in updates.keys()])
                values = tuple(updates.values()) + (item['id'],)
                cursor.execute(
                    f'UPDATE {self.table_name} SET {set_clause} WHERE id = ?',
                    values
                )
                updated = True
        
        conn.commit()
        conn.close()
        return updated
    
    def delete(self, condition: Callable[[Dict], bool]) -> bool:
        """Delete items matching a condition"""
        items = self.load()
        deleted = False
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        for item in items:
            if condition(item):
                cursor.execute(
                    f'DELETE FROM {self.table_name} WHERE id = ?',
                    (item['id'],)
                )
                deleted = True
        
        conn.commit()
        conn.close()
        return deleted
    
    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a single item by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_dict(row) if row else None
    
    def query(self, where_clause: str = "", params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a custom query with optional WHERE clause
        
        Args:
            where_clause: SQL WHERE clause (without the 'WHERE' keyword)
            params: Parameters for the query
        
        Returns:
            List of matching items
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        sql = f'SELECT * FROM {self.table_name}'
        if where_clause:
            sql += f' WHERE {where_clause}'
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]
    
    def execute_raw(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a raw SQL query
        
        Args:
            sql: Full SQL query
            params: Parameters for the query
        
        Returns:
            List of result rows as dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        
        # Check if this is a SELECT query
        if sql.strip().upper().startswith('SELECT'):
            rows = cursor.fetchall()
            conn.close()
            return [self._row_to_dict(row) for row in rows]
        else:
            conn.commit()
            conn.close()
            return []
    
    def count(self, where_clause: str = "", params: tuple = ()) -> int:
        """Count items, optionally with a WHERE clause"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        sql = f'SELECT COUNT(*) as count FROM {self.table_name}'
        if where_clause:
            sql += f' WHERE {where_clause}'
        
        cursor.execute(sql, params)
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0
    
    def aggregate(self, column: str, operation: str = "SUM", 
                  where_clause: str = "", params: tuple = ()) -> float:
        """
        Perform aggregation on a column
        
        Args:
            column: Column to aggregate
            operation: SQL aggregate function (SUM, AVG, MIN, MAX, COUNT)
            where_clause: Optional WHERE clause
            params: Parameters for the query
        
        Returns:
            Aggregated value
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        sql = f'SELECT {operation}({column}) as result FROM {self.table_name}'
        if where_clause:
            sql += f' WHERE {where_clause}'
        
        cursor.execute(sql, params)
        result = cursor.fetchone()
        conn.close()
        return result['result'] if result and result['result'] else 0.0


class TaskStore(SQLiteStore):
    """Specialized store for tasks with additional query methods"""
    
    def __init__(self):
        super().__init__('tasks')
    
    def get_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get tasks filtered by status"""
        return self.query('status = ?', (status,))
    
    def get_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Get tasks filtered by priority"""
        return self.query('priority = ?', (priority,))
    
    def get_overdue(self) -> List[Dict[str, Any]]:
        """Get all overdue tasks (deadline passed and not Done)"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.query(
            'deadline < ? AND status != ?',
            (today, 'Done')
        )
    
    def get_due_soon(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get tasks due within the next N days"""
        from datetime import timedelta
        today = datetime.now()
        future = (today + timedelta(days=days)).strftime('%Y-%m-%d')
        today_str = today.strftime('%Y-%m-%d')
        
        return self.query(
            'deadline >= ? AND deadline <= ? AND status != ?',
            (today_str, future, 'Done')
        )
    
    def get_completion_stats(self) -> Dict[str, int]:
        """Get task completion statistics"""
        return {
            'total': self.count(),
            'todo': self.count('status = ?', ('Todo',)),
            'doing': self.count('status = ?', ('Doing',)),
            'done': self.count('status = ?', ('Done',))
        }


class ExpenseStore(SQLiteStore):
    """Specialized store for expenses with additional query methods"""
    
    def __init__(self):
        super().__init__('expenses')
    
    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get expenses filtered by category"""
        return self.query('category = ?', (category,))
    
    def get_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get expenses within a date range"""
        return self.query('date >= ? AND date <= ?', (start_date, end_date))
    
    def get_total_by_category(self) -> Dict[str, float]:
        """Get total amount spent per category"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) as total 
            FROM expenses 
            GROUP BY category
        ''')
        rows = cursor.fetchall()
        conn.close()
        return {row['category']: row['total'] for row in rows}
    
    def get_monthly_totals(self) -> List[Dict[str, Any]]:
        """Get monthly spending totals"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
            FROM expenses
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]
    
    def get_total(self, category: Optional[str] = None, 
                  start_date: Optional[str] = None, end_date: Optional[str] = None) -> float:
        """Get total expenses with optional filters"""
        where_parts = []
        params = []
        
        if category:
            where_parts.append('category = ?')
            params.append(category)
        if start_date:
            where_parts.append('date >= ?')
            params.append(start_date)
        if end_date:
            where_parts.append('date <= ?')
            params.append(end_date)
        
        where_clause = ' AND '.join(where_parts) if where_parts else ""
        return self.aggregate('amount', 'SUM', where_clause, tuple(params))


def migrate_json_to_sqlite():
    """
    Migrate existing JSON data to SQLite database
    Useful for transitioning from JSON storage to SQLite
    """
    from .storage import DataStore
    from .config import TASKS_FILE, EXPENSES_FILE
    
    task_store = TaskStore()
    expense_store = ExpenseStore()
    
    # Migrate tasks
    if TASKS_FILE.exists():
        json_store = DataStore(TASKS_FILE)
        tasks = json_store.load()
        for task in tasks:
            try:
                task_store.append(task)
            except sqlite3.IntegrityError:
                # Task already exists, skip
                pass
    
    # Migrate expenses
    if EXPENSES_FILE.exists():
        json_store = DataStore(EXPENSES_FILE)
        expenses = json_store.load()
        for expense in expenses:
            try:
                expense_store.append(expense)
            except sqlite3.IntegrityError:
                # Expense already exists, skip
                pass
    
    print(f"Migration complete! Database created at: {DATABASE_FILE}")


# Utility function for generating IDs (same as in storage.py for consistency)
def generate_id() -> str:
    """Generate a unique ID based on timestamp"""
    return datetime.now().strftime("%Y%m%d%H%M%S%f")
