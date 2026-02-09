"""
Data storage utilities for managing JSON files
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class DataStore:
    """Handle reading and writing JSON data files"""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create file with empty list if it doesn't exist"""
        if not self.filepath.exists():
            self.save([])
    
    def load(self) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    
    def save(self, data: List[Dict[str, Any]]):
        """Save data to JSON file"""
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def append(self, item: Dict[str, Any]):
        """Append a new item to the data file"""
        data = self.load()
        data.append(item)
        self.save(data)
    
    def update(self, condition: callable, updates: Dict[str, Any]) -> bool:
        """Update items matching a condition"""
        data = self.load()
        updated = False
        
        for item in data:
            if condition(item):
                item.update(updates)
                updated = True
        
        if updated:
            self.save(data)
        
        return updated
    
    def delete(self, condition: callable) -> bool:
        """Delete items matching a condition"""
        data = self.load()
        original_length = len(data)
        
        data = [item for item in data if not condition(item)]
        
        if len(data) < original_length:
            self.save(data)
            return True
        
        return False


def generate_id() -> str:
    """Generate a unique ID based on timestamp"""
    return datetime.now().strftime("%Y%m%d%H%M%S%f")
